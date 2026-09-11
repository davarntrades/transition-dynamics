"""
windows.py -- feature extraction and labelling, exactly as frozen in
docs/PROTOCOL_STRUCTURAL_PREDICTION.md. No tunable knobs.
"""
from __future__ import annotations
import os, sys
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
from cohort import SHORT, MAP_IDX, INTERVAL_S, MIN_COVERAGE, PANEL_IDX  # noqa

DT = INTERVAL_S
P = len(SHORT)

BASE_T0, BASE_T1 = 30 * 60, 50 * 60   # baseline window (amendment A3)
FIRST_EVAL = 55 * 60
STRIDE = 60
FEAT_W = 5 * 60
GAP = 60
HORIZONS = (5 * 60, 10 * 60, 15 * 60)
REFRACTORY = 10 * 60
MAP_THRESH = 65.0
MAP_SEVERE = 55.0
EVENT_MIN_S = 60
MAX_GAP_S = 30
MAX_MISSING_FRAC = 0.20
MIN_EFF_BASELINE = 10 * P
MIN_ANALYSABLE_S = 60 * 60


def case_interval(n_samples, anestart, aneend, caseend):
    """Analysable index range on the RECORDING axis.

    VitalDB clinical times are seconds from casestart = 0, and `anestart` is
    routinely NEGATIVE: anaesthesia began before the recorder was started.
    So the analysable span is the intersection of the anaesthesia interval with
    the recording, not the metadata interval, which over-counts by the
    pre-recording induction time.
    """
    i0 = max(0, int(np.ceil(anestart / DT)))
    i1 = min(n_samples, int(np.floor(min(aneend, caseend) / DT)))
    return i0, i1


def interpolate_short_gaps(X, max_gap_s=MAX_GAP_S):
    """Linear interpolation across runs of NaN no longer than max_gap_s.
    Longer runs are left missing. Never uses a sample outside the array."""
    X = X.copy()
    max_n = int(round(max_gap_s / DT))
    n = X.shape[0]
    for j in range(X.shape[1]):
        col = X[:, j]
        bad = ~np.isfinite(col)
        if not bad.any():
            continue
        idx = np.flatnonzero(bad)
        # split into consecutive runs
        breaks = np.flatnonzero(np.diff(idx) > 1)
        starts = np.r_[0, breaks + 1]
        ends = np.r_[breaks, len(idx) - 1]
        for s, e in zip(starts, ends):
            a, b = idx[s], idx[e]
            if (b - a + 1) > max_n or a == 0 or b == n - 1:
                continue        # unbounded or too long -> stays missing
            lo, hi = col[a - 1], col[b + 1]
            if np.isfinite(lo) and np.isfinite(hi):
                col[a:b + 1] = np.linspace(lo, hi, b - a + 3)[1:-1]
    return X


def find_events(map_series, thresh=MAP_THRESH):
    """Onset indices of runs of MAP < thresh lasting >= EVENT_MIN_S.
    Missing samples break a run (they are not evidence of hypotension)."""
    below = np.isfinite(map_series) & (map_series < thresh)
    need = int(round(EVENT_MIN_S / DT))
    onsets, run = [], 0
    for i, b in enumerate(below):
        if b:
            run += 1
            if run == need:
                onsets.append(i - need + 1)
        else:
            run = 0
    return np.array(onsets, dtype=int)


def ledoit_wolf(Z):
    """Ledoit-Wolf shrinkage towards a scaled identity. Z is n x p, centred."""
    n, p = Z.shape
    S = Z.T @ Z / n
    mu = np.trace(S) / p
    target = mu * np.eye(p)
    d2 = np.sum((S - target) ** 2)
    b2 = sum(np.sum((np.outer(Z[i], Z[i]) - S) ** 2) for i in range(n)) / n**2
    b2 = min(b2, d2)
    shrink = 0.0 if d2 <= 0 else b2 / d2
    return (1 - shrink) * S + shrink * target, shrink


def _slopes(W):
    """OLS slope per channel over the feature window, in units per minute."""
    n = W.shape[0]
    t = (np.arange(n) * DT - (n - 1) * DT / 2) / 60.0
    den = np.sum(t * t)
    out = np.full(W.shape[1], np.nan)
    for j in range(W.shape[1]):
        col = W[:, j]
        m = np.isfinite(col)
        if m.sum() < 3:
            continue
        tt = t[m] - t[m].mean()
        d = np.sum(tt * tt)
        if d > 0:
            out[j] = np.sum(tt * (col[m] - col[m].mean())) / d
    return out


def prepare_case(X, ane_start_idx, ane_end_idx):
    """Baseline statistics. Returns None with a reason if the case is excluded."""
    Xi = interpolate_short_gaps(X[:, PANEL_IDX])
    b0 = ane_start_idx + int(BASE_T0 / DT)
    b1 = ane_start_idx + int(BASE_T1 / DT)
    if b1 > Xi.shape[0] or b1 > ane_end_idx:
        return None, "baseline beyond record"
    B = Xi[b0:b1]
    cov = np.isfinite(B).mean(axis=0)
    if (cov < MIN_COVERAGE).any():
        return None, f"coverage {cov.min():.2f} < {MIN_COVERAGE}"
    if len(find_events(B[:, MAP_IDX])) > 0:
        return None, "hypotension inside baseline window"
    rows = np.isfinite(B).all(axis=1)
    Bc = B[rows]
    if Bc.shape[0] < MIN_EFF_BASELINE:
        return None, f"only {Bc.shape[0]} complete baseline rows"
    mu0 = Bc.mean(axis=0)
    Sigma0, shrink = ledoit_wolf(Bc - mu0)
    return {"Xi": Xi, "mu0": mu0, "Sigma0": Sigma0, "shrink": shrink,
            "b1": b1, "sigma": np.sqrt(np.diag(Sigma0))}, None


def build_windows(prep, ane_start_idx, ane_end_idx, thresh=MAP_THRESH):
    """Evaluation points with features and per-horizon labels.
    Features NEVER read a sample later than t. Labels are the only thing that
    looks forward, and a point is dropped when its horizon is unobserved."""
    Xi, mu0, Sigma0 = prep["Xi"], prep["mu0"], prep["Sigma0"]
    sigma = prep["sigma"]
    end = min(ane_end_idx, Xi.shape[0])
    onsets = find_events(Xi[:, MAP_IDX], thresh)
    w = int(FEAT_W / DT)
    med_n = int(60 / DT)
    rows = []
    t = ane_start_idx + int(FIRST_EVAL / DT)
    while t < end:
        lo = t - w
        if lo < prep["b1"]:
            t += int(STRIDE / DT); continue
        W = Xi[lo:t]
        miss = (~np.isfinite(W)).mean(axis=0)
        if (miss > MAX_MISSING_FRAC).any():
            t += int(STRIDE / DT); continue
        mp = W[:, MAP_IDX]
        if np.nanmin(mp) < thresh:              # currently/recently hypotensive
            t += int(STRIDE / DT); continue
        prior = onsets[(onsets < t) & (onsets >= t - int(REFRACTORY / DT))]
        if len(prior):
            t += int(STRIDE / DT); continue
        tail = W[-med_n:]
        if not np.isfinite(tail).any(axis=0).all():
            t += int(STRIDE / DT); continue
        x = np.nanmedian(tail, axis=0)
        if not np.isfinite(x).all():
            t += int(STRIDE / DT); continue
        delta = x - mu0
        fut = onsets[onsets > t + int(GAP / DT)]
        nxt = fut[0] if len(fut) else None
        labels, keep = {}, {}
        for H in HORIZONS:
            hi = t + int((GAP + H) / DT)
            pos = nxt is not None and nxt <= hi
            if pos:
                labels[H] = 1; keep[H] = True
            elif hi <= end:
                labels[H] = 0; keep[H] = True
            else:
                labels[H] = 0; keep[H] = False   # censored -> dropped
        rows.append({
            "t_idx": t,
            "t_min": (t - ane_start_idx) * DT / 60.0,
            "x": x, "delta": delta, "z": delta / sigma,
            "sd_w": np.nanstd(W, axis=0),
            "slope": _slopes(W),
            "cov_w": _win_cov(W),
            "labels": labels, "keep": keep,
            "next_onset_min": ((nxt - t) * DT / 60.0) if nxt is not None else np.nan,
        })
        t += int(STRIDE / DT)
    return rows, onsets


def _win_cov(W):
    rows = np.isfinite(W).all(axis=1)
    Wc = W[rows]
    if Wc.shape[0] < W.shape[1] + 2:
        return None
    return np.cov(Wc.T)
