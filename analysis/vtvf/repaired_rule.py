"""
repaired_rule.py -- per-patient statistics and the repaired decision rule
(docs/VT_VF_PROTOCOL_REPAIR_PLAN.md). SYNTHETIC calibration use only.

Design change that removes the LOPO dependence at its source
-------------------------------------------------------------
The primary per-patient statistic uses NO cross-patient training:

  c      = fixed, unfitted TD composite = mean of baseline-standardised
           (TD-1 S, TD-2 dG, TD-3 Qint)
  r      = residual of c after a within-patient linear regression on the five
           M1 conventional features, fitted on that patient's REMOTE windows
           only (outcome-free); remote residuals are blocked cross-fitted
  s_i,b  = AUROC(r over bin-b windows, r over remote windows) - 0.5

Because s_i,b depends only on patient i's data, the s_i,b are independent
across patients, and patient-level tests are valid without refitting
bootstraps. "Beyond conventional features" is operationalised as the
residual after the M1 regression; the cross-patient M1-vs-M4 LOPO model is
kept only as a secondary, descriptive analysis.
"""
from __future__ import annotations

import math

import numpy as np

BINS = {"B5": (2.0, 5.0), "B10": (5.0, 10.0), "B15": (10.0, 15.0), "B30": (15.0, 30.0)}
REMOTE_LEAD = 60.0
REMOTE_START = 50.0          # settle 15 + baseline 30 + window 5
MASK_ACQ = 0.20              # absolute: window masked if >20% of beats flagged
ALPHA_BIN = 0.05 / 8         # one-sided 0.00625 per bin (v2 effective level)
ALPHA_CTRL = 0.05            # control tests (affirmative-evidence tests)
ALPHA_PIPE = 0.001 / 4       # label-permutation pipeline control, per bin, two-sided


# --------------------------------------------------------------------------
# small stats helpers
# --------------------------------------------------------------------------
def auroc(pos, neg) -> float:
    pos, neg = np.asarray(pos), np.asarray(neg)
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    s = np.sort(neg)
    lo = np.searchsorted(s, pos, "left"); hi = np.searchsorted(s, pos, "right")
    return float(np.mean(lo + 0.5 * (hi - lo)) / len(neg))


def t_sf(t: float, df: int) -> float:
    from scipy.stats import t as T
    return float(T.sf(t, df))


def t_ppf(p: float, df: int) -> float:
    from scipy.stats import t as T
    return float(T.ppf(p, df))


def one_sided_t(x, alpha: float) -> dict:
    x = np.asarray([v for v in x if np.isfinite(v)])
    n = len(x)
    if n < 3:
        return {"n": n, "mean": float("nan"), "p": 1.0, "pass": False, "lo": float("nan"),
                "ub95": float("nan")}
    m, se = x.mean(), x.std(ddof=1) / math.sqrt(n)
    tt = m / se if se > 0 else (math.inf if m > 0 else -math.inf)
    p = t_sf(tt, n - 1)
    return {"n": n, "mean": float(m), "se": float(se), "p": p, "pass": bool(p < alpha),
            "lo": float(m - t_ppf(1 - alpha, n - 1) * se),
            "ub95": float(m + t_ppf(0.95, n - 1) * se)}


def sign_p(x) -> float:
    from scipy.stats import binom
    x = np.asarray([v for v in x if np.isfinite(v) and v != 0])
    if len(x) == 0:
        return 1.0
    return float(binom.sf(int((x > 0).sum()) - 1, len(x), 0.5))


# --------------------------------------------------------------------------
# per-patient statistics
# --------------------------------------------------------------------------
def _fit_predict(Xtr, ytr, Xte, lam=1e-3):
    A = np.column_stack([np.ones(len(Xtr)), Xtr])
    B = np.column_stack([np.ones(len(Xte)), Xte])
    R = lam * np.eye(A.shape[1]); R[0, 0] = 0
    beta = np.linalg.solve(A.T @ A + R, A.T @ ytr)
    return B @ beta


def residualise(c, X, remote, k_blocks: int = 5):
    """Residual of c on X. Coefficients from remote windows only; remote
    residuals blocked-cross-fitted in time; other windows use the full fit."""
    r = np.full(len(c), np.nan)
    ridx = np.flatnonzero(remote)
    if len(ridx) < 2 * X.shape[1] + 5:
        return r
    r_all = c - _fit_predict(X[ridx], c[ridx], X)
    r[:] = r_all
    blocks = np.array_split(ridx, k_blocks)
    for b in blocks:
        tr = np.setdiff1d(ridx, b)
        r[b] = c[b] - _fit_predict(X[tr], c[tr], X[b])
    return r


COMPOSITES = {"td3": [0, 1, 2],          # protocol TD-1, TD-2, TD-3
              "shape": [3, 4]}           # correlation-only deformation + its persistence


def basis(M1: np.ndarray, kind: str) -> np.ndarray:
    if kind == "linear":
        return M1
    return np.column_stack([M1, M1 ** 2, np.abs(np.diff(M1, axis=0, prepend=M1[:1]))])


def patient_stats(feat: dict, T_eff: float, guard: float = 2.0, leak: float = 0.0,
                  rng=None, permute: bool = False, remote_start: float = REMOTE_START,
                  composite: str = "td3", basis_kind: str = "linear") -> dict:
    """Statistics for one patient at a (possibly pseudo) event time T_eff."""
    end = feat["end"]
    use = end < T_eff
    lead = T_eff - end
    masked = feat["acq"] > MASK_ACQ
    remote = use & (end >= remote_start) & (lead >= REMOTE_LEAD) & ~masked
    c = feat["TD"][:, COMPOSITES[composite]].mean(axis=1).copy()
    rz = use & (end >= remote_start) & (lead >= REMOTE_LEAD)
    out = {"masked_frac_remote": float(masked[rz].mean()) if rz.any() else float("nan")}
    binmask = {}
    for b, (lo, hi) in BINS.items():
        lo_eff = max(lo, guard) if b == "B5" else lo
        binmask[b] = use & (lead > lo_eff) & (lead <= hi) & ~masked
        out[f"masked_frac_{b}"] = float(masked[use & (lead > lo_eff) & (lead <= hi)].mean()) \
            if (use & (lead > lo_eff) & (lead <= hi)).any() else float("nan")
    if leak:                                   # deliberately broken pipeline (label leakage)
        for b in BINS:
            c[binmask[b]] += leak
    Xb = basis(feat["M1"], basis_kind)
    r = residualise(c, Xb, remote)
    Xc = np.column_stack([Xb, feat["acq"]])
    rc = residualise(c, Xc, remote)
    for b in BINS:
        pm = binmask[b]
        rm = remote.copy()
        if permute and rng is not None:          # label permutation: null by construction
            pool = np.flatnonzero(pm | rm)
            k = int(pm.sum())
            pick = rng.choice(pool, size=k, replace=False) if k and len(pool) > k else np.array([], int)
            pm = np.zeros_like(pm); pm[pick] = True
            rm = np.zeros_like(rm); rm[np.setdiff1d(pool, pick)] = True
        ok = pm.sum() > 0 and rm.sum() >= 20
        out[b] = {
            "s": auroc(r[pm], r[rm]) - 0.5 if ok else float("nan"),
            "s_cond": auroc(rc[pm], rc[rm]) - 0.5 if ok else float("nan"),
            "a": auroc(feat["acq"][pm], feat["acq"][rm]) - 0.5 if ok else float("nan"),
            "hr": auroc(-feat["M1"][pm, 0], -feat["M1"][rm, 0]) - 0.5 if ok else float("nan"),
            "n_pos": int(pm.sum()), "n_neg": int(rm.sum())}
    return out


def pseudo_offsets(T: float, step: float = 180.0, t_min: float = 140.0) -> list[float]:
    """Pseudo-onsets every `step` min before T, keeping the full zone geometry."""
    return [T - step * k for k in range(1, 30) if T - step * k >= t_min]


# --------------------------------------------------------------------------
# study-level repaired decision rule
# --------------------------------------------------------------------------
ORDER = ["PIPELINE_INVALID", "UNRESOLVED", "ACQUISITION_EXPLAINED", "DRIFT_EXPLAINED",
         "NOT_SUPPORTED", "TRIGGER_PROXIMAL", "SINGLE_BIN_LONG_LEAD", "EXPLORATORY_ASSOCIATION"]


def decide(true_stats: list, pseudo_stats: list, perm_stats: list, pipe_pc_ok: bool,
           delta_ex: float, min_pseudo: int = 8) -> dict:
    """true_stats: per-patient dicts at the true event; pseudo_stats: per-patient
    list of dicts at pseudo-onsets; perm_stats: per-patient label-permutation dicts."""
    res = {"bins": {}}
    # 1. pipeline validity -- only actual failures
    perm_fail = False
    for b in BINS:
        x = np.array([p[b]["s"] for p in perm_stats])
        t = one_sided_t(x, 1.0)
        if t["n"] >= 3 and np.isfinite(t["mean"]):
            p2 = 2 * min(t["p"], 1 - t["p"])
            perm_fail |= p2 < ALPHA_PIPE
    res["perm_control_fail"] = bool(perm_fail)
    res["positive_control_fail"] = not pipe_pc_ok
    if perm_fail or not pipe_pc_ok:
        res["verdict"] = "PIPELINE_INVALID"
        return res
    passing = []
    harm = 0
    for b in BINS:
        s = np.array([p[b]["s"] for p in true_stats])
        tt = one_sided_t(s, ALPHA_BIN)
        sp = sign_p(s)
        prim = tt["pass"] and sp < ALPHA_BIN
        neg = one_sided_t(-s, ALPHA_BIN)
        harm += bool(neg["pass"] and sign_p(-s) < ALPHA_BIN)
        info = {"mean": tt["mean"], "p": tt["p"], "sign_p": sp, "n": tt["n"],
                "ub95": tt["ub95"], "primary": bool(prim)}
        if prim:
            # 2. temporal control: paired true-minus-pseudo, plus affirmative drift test
            d, pz = [], []
            for p_true, plist in zip(true_stats, pseudo_stats):
                vals = [q[b]["s"] for q in plist if np.isfinite(q[b]["s"])]
                if vals and np.isfinite(p_true[b]["s"]):
                    d.append(p_true[b]["s"] - np.mean(vals)); pz.append(np.mean(vals))
            info["n_pseudo"] = len(d)
            if len(d) < min_pseudo:
                info["temporal"] = "NON_EVALUABLE"
            else:
                td = one_sided_t(d, ALPHA_CTRL)
                tz = one_sided_t(pz, ALPHA_CTRL)
                if td["pass"]:
                    info["temporal"] = "PASS"
                elif tz["pass"]:
                    info["temporal"] = "DRIFT_AFFIRMED"      # pseudo-onsets show the effect too
                else:
                    info["temporal"] = "INCONCLUSIVE"
            # 3. acquisition: affirmative evidence required
            a = np.array([p[b]["a"] for p in true_stats])
            sc = np.array([p[b]["s_cond"] for p in true_stats])
            ta = one_sided_t(a, ALPHA_CTRL)
            tc = one_sided_t(sc, ALPHA_BIN)
            if ta["pass"] and not tc["pass"]:
                info["acquisition"] = "ACQ_AFFIRMED"
            else:
                info["acquisition"] = "PASS"
            info["survives"] = info["temporal"] == "PASS" and info["acquisition"] == "PASS"
            passing.append(b)
        res["bins"][b] = info
    res["harm"] = harm >= 2
    res["large_excluded"] = all(res["bins"][b]["ub95"] < delta_ex for b in BINS
                                if np.isfinite(res["bins"][b]["ub95"]))
    if not passing:
        res["verdict"] = "NOT_SUPPORTED"
        return res
    surv = [b for b in passing if res["bins"][b]["survives"]]
    if not surv:
        tags = [res["bins"][b] for b in passing]
        if any(t["acquisition"] == "ACQ_AFFIRMED" for t in tags):
            res["verdict"] = "ACQUISITION_EXPLAINED"
        elif any(t.get("temporal") == "DRIFT_AFFIRMED" for t in tags):
            res["verdict"] = "DRIFT_EXPLAINED"
        else:
            res["verdict"] = "UNRESOLVED"
        return res
    if res["harm"]:
        res["verdict"] = "NOT_SUPPORTED"
        return res
    long_ = [b for b in surv if b in ("B15", "B30")]
    if len(surv) >= 2 and long_:
        res["verdict"] = "EXPLORATORY_ASSOCIATION"
    elif long_:
        res["verdict"] = "SINGLE_BIN_LONG_LEAD"
    else:
        res["verdict"] = "TRIGGER_PROXIMAL"
    return res
