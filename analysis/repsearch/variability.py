"""
variability.py -- mathematically distinct ways of extracting TEMPORAL
information from marginal variability.

The empirical survivor on development data is that marginal dispersion carries
substantially more signal than displacement. This module asks whether the
temporal ORGANISATION of fluctuations adds anything beyond the static
dispersion already inside B*.

Nothing here uses cross-channel covariance. Every quantity is per channel.

Note on autocorrelation (V2): the short-timescale experiment falsified a
TRANSFER claim -- that baseline relaxation predicts response relaxation. Using
autocorrelation as a predictive FEATURE is a different question and is tested
here on its own merits, with no relaxation, stiffness or recovery-time
interpretation attached.

All series are built on a continuous 60 s grid spanning the analysable
interval, independent of the label-exclusion rules, and read only samples at or
before their own timestamp.
"""
from __future__ import annotations
import os, sys
import numpy as np

_S = os.path.join(os.path.dirname(__file__), "..", "structural")
sys.path.insert(0, _S)
import windows as W  # noqa
from cohort import SHORT  # noqa

P = len(SHORT)
STRIDE_S = 60
VAR_WIN_S = 300          # rolling window for variance / AC / spectral / entropy
LOOKBACK_MIN = 30
THETA_V = np.log(1.5)    # "abnormal variability": 1.5x baseline SD, log scale


# ------------------------------------------------------------------ primitives
def _lag1(x):
    x = x[np.isfinite(x)]
    if len(x) < 20:
        return np.nan
    x = x - x.mean()
    d = np.dot(x, x)
    return np.dot(x[:-1], x[1:]) / d if d > 0 else np.nan


def _spectral(x):
    """Spectral edge (95% power) and high/low band power ratio."""
    x = x[np.isfinite(x)]
    if len(x) < 32:
        return np.nan, np.nan
    x = x - x.mean()
    f = np.fft.rfftfreq(len(x), d=W.DT)
    p = np.abs(np.fft.rfft(x)) ** 2
    if p[1:].sum() <= 0:
        return np.nan, np.nan
    p = p[1:]; f = f[1:]
    c = np.cumsum(p) / p.sum()
    sef = float(f[np.searchsorted(c, 0.95)])
    half = len(f) // 2
    lo, hi = p[:half].sum(), p[half:].sum()
    return sef, float(np.log((hi + 1e-12) / (lo + 1e-12)))


def _perm_entropy(x, order=3):
    """Bandt-Pompe permutation entropy, normalised to [0, 1]."""
    x = x[np.isfinite(x)]
    n = len(x) - order + 1
    if n < 20:
        return np.nan
    idx = np.argsort(np.lib.stride_tricks.sliding_window_view(x, order), axis=1)
    codes = np.dot(idx, order ** np.arange(order))
    _, cnt = np.unique(codes, return_counts=True)
    p = cnt / cnt.sum()
    import math
    return float(-np.sum(p * np.log(p)) / math.log(math.factorial(order)))


# ------------------------------------------------------- per-case grid series
def grids(prep, i0, i1, shuffle_within_window=False, seed=0):
    """Continuous 60 s-stride series of every primitive.

    shuffle_within_window: DESTRUCTIVE CONTROL. Permutes the raw samples inside
    each feature window before computing AC / spectral / entropy. The marginal
    distribution of the window is preserved exactly; only temporal order dies.
    """
    rng = np.random.default_rng(seed)
    Xi = prep["Xi"]; sig = prep["sigma"]; mu0 = prep["mu0"]
    step = int(STRIDE_S / W.DT)
    vw = int(VAR_WIN_S / W.DT)
    start = prep["b1"] + vw
    ts = np.arange(start, min(i1, Xi.shape[0]) + 1, step, dtype=int)
    n = len(ts)
    v = np.full((n, P), np.nan)      # log rolling SD relative to baseline SD
    ac = np.full((n, P), np.nan)     # lag-1 autocorrelation
    sef = np.full((n, P), np.nan)    # spectral edge
    bpr = np.full((n, P), np.nan)    # high/low band power ratio
    pe = np.full((n, P), np.nan)     # permutation entropy
    zc = np.full((n, P), np.nan)     # mean |z| over the window (level reference)
    for k, t in enumerate(ts):
        Wn = Xi[t - vw:t]
        for i in range(P):
            col = Wn[:, i]
            f = col[np.isfinite(col)]
            if len(f) < 30:
                continue
            zc[k, i] = np.mean(np.abs((f - mu0[i]) / sig[i]))
            s = f.std()
            v[k, i] = np.log(max(s, 1e-9) / max(sig[i], 1e-9))
            work = rng.permutation(f) if shuffle_within_window else f
            ac[k, i] = _lag1(work)
            sef[k, i], bpr[k, i] = _spectral(work)
            pe[k, i] = _perm_entropy(work)
    return {"t_idx": ts, "v": v, "ac": ac, "sef": sef, "bpr": bpr,
            "pe": pe, "zc": zc}


# --------------------------------------------- temporal operators on v-series
def _runlen(A, cap):
    n, p = A.shape
    R = np.zeros((n, p))
    for i in range(p):
        r = 0
        for k in range(n):
            r = min(r + 1, cap) if A[k, i] else 0
            R[k, i] = r
    return R


def temporal_blocks(G, steps, shuffle_series=False, rank_only=False, seed=0):
    """Operators applied to the v-series over a bounded lookback.

    shuffle_series: DESTRUCTIVE CONTROL -- permute v inside the lookback.
      Preserves the marginal distribution of variability exactly; destroys its
      temporal organisation. This is the direct test of H0 vs H1.
    rank_only: preserves ORDER, removes magnitude (v -> within-lookback rank).
    """
    rng = np.random.default_rng(seed)
    v = G["v"]
    n, p = v.shape
    run = np.zeros((n, p)); dv = np.zeros((n, p)); acc = np.zeros((n, p))
    cp = np.zeros((n, p)); cross = np.zeros((n, p)); since = np.zeros((n, p))
    for k in range(n):
        lo = max(0, k - steps + 1)
        wnd = v[lo:k + 1].copy()
        m = np.isfinite(wnd)
        if shuffle_series:
            for i in range(p):
                col = wnd[:, i]
                ok = np.isfinite(col)
                if ok.sum() > 1:
                    col[ok] = rng.permutation(col[ok])
                wnd[:, i] = col
        if rank_only:
            for i in range(p):
                col = wnd[:, i]; ok = np.isfinite(col)
                if ok.sum() > 1:
                    r = np.argsort(np.argsort(col[ok])) / max(ok.sum() - 1, 1)
                    col[ok] = r
                wnd[:, i] = col
        A = np.isfinite(wnd) & (wnd > (0.5 if rank_only else THETA_V))
        R = _runlen(A, steps)
        run[k] = R[-1]
        L = wnd.shape[0]
        tt = np.arange(L, dtype=float)
        for i in range(p):
            col = wnd[:, i]; ok = np.isfinite(col)
            if ok.sum() >= 3:
                x = tt[ok] - tt[ok].mean(); yv = col[ok] - col[ok].mean()
                d = np.dot(x, x)
                dv[k, i] = np.dot(x, yv) / d if d > 0 else 0.0
                acc[k, i] = np.sum(np.clip(col[ok], 0, None)) * (STRIDE_S / 60.0)
                a = A[:, i][ok].astype(int)
                cross[k, i] = float(np.sum(np.diff(a) > 0))
                up = np.flatnonzero(np.diff(a) > 0)
                since[k, i] = (len(a) - 1 - up[-1]) * (STRIDE_S / 60.0) \
                    if len(up) else steps * (STRIDE_S / 60.0)
                cp[k, i] = _maxsplit(col[ok])
    return {"run": run, "dv": dv, "acc": acc, "cp": cp,
            "cross": cross, "since": since}


def _maxsplit(x):
    """Max standardised two-sample split statistic -- a change-point score."""
    n = len(x)
    if n < 8:
        return 0.0
    best = 0.0
    c1 = np.cumsum(x); c2 = np.cumsum(x * x)
    for s in range(3, n - 3):
        m1 = c1[s - 1] / s
        m2 = (c1[-1] - c1[s - 1]) / (n - s)
        vv = (c2[-1] / n - (c1[-1] / n) ** 2)
        if vv <= 1e-12:
            continue
        best = max(best, abs(m1 - m2) / np.sqrt(vv))
    return float(best)
