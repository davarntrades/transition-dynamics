"""
repaired_rule2.py -- per-patient statistics over the beatsim2 statistic panel,
plus VT/VF subgroup reporting. The study-level decision rule is reused
unchanged from repaired_rule.decide (no alpha, gate or threshold changed).

Leakage repair (docs/VT_VF_FALSIFICATION_SUITE.md section 2):
  * covariance statistics on locally detrended beats ("_hp" statistics);
  * the conventional residualisation basis gains the TD-window duration
    (an HR proxy that is a deterministic function of beat timing);
  * an HR-stratified sensitivity statistic (s_hrmatch) compares bin windows
    only with remote windows of similar mean NN.
"""
from __future__ import annotations

import numpy as np

from repaired_rule import (ALPHA_BIN, ALPHA_CTRL, BINS, MASK_ACQ, REMOTE_LEAD, REMOTE_START,
                           auroc, decide, one_sided_t, pseudo_offsets, residualise, sign_p)

__all__ = ["patient_stats2", "decide", "subgroup_report", "pseudo_offsets", "BINS"]


def basis(M1: np.ndarray, kind: str, remote=None) -> np.ndarray:
    if kind == "none":
        return np.zeros((len(M1), 0))
    M1 = M1.copy()
    if kind.endswith("_clip") and remote is not None and remote.sum() > 5:
        # no extrapolation of the conventional adjustment beyond remote support
        lo = M1[remote].min(axis=0); hi = M1[remote].max(axis=0)
        M1 = np.clip(M1, lo, hi)
        kind = kind[:-5]
    core = M1[:, :5]
    if kind == "lin_dur":
        return np.column_stack([core, M1[:, 5:6]])
    if kind == "poly":                       # run-2 basis (no duration)
        return np.column_stack([core, core ** 2, np.abs(np.diff(core, axis=0, prepend=core[:1]))])
    if kind == "poly_dur":                   # + TD-window duration (HR proxy)
        d = M1[:, 5:6]
        return np.column_stack([core, core ** 2, np.abs(np.diff(core, axis=0, prepend=core[:1])),
                                d, d ** 2])
    raise ValueError(kind)


def _hr_matched_auroc(r, hr, pm, rm, tol=0.5):
    """Mean over bin windows of P(r_bin > r_remote | |hr_bin - hr_remote| < tol)."""
    vals = []
    rr, hh = r[rm], hr[rm]
    for i in np.flatnonzero(pm):
        sel = np.abs(hh - hr[i]) < tol
        if sel.sum() >= 5:
            v = rr[sel]
            vals.append(np.mean(r[i] > v) + 0.5 * np.mean(r[i] == v))
    return float(np.mean(vals)) - 0.5 if vals else float("nan")


# Phase-1 composites: (instantaneous statistics, persistence on the residual?)
# Persistence is computed on the conventional-adjusted residual series, never
# regressed itself: regressing the zero-inflated 30-min integral produced a
# +0.026 null bias (docs/VT_VF_FALSIFICATION_SUITE.md section 2.3).
COMPOSITES2 = {
    "td3": (["S", "dG"], True),             # combined estimator (S, dG, persistence)
    "shape_raw": (["shape"], True),          # run-2 statistic
    "shape_hp": (["shape_hp"], True),        # detrended correlation structure
    "pshape_hp": (["pshape_hp"], True),      # + NN-conditional (leakage-repaired candidate)
    "dG_hp": (["dG_hp"], False),             # full covariance AIRM
    "corrFrob_hp": (["corrFrob_hp"], False), # ordinary correlation statistic
    "meanabsr_hp": (["meanabsr_hp"], False), # DNB-style mean |r|
    "logdet_hp": (["logdet_hp"], False),     # generalised-variance competitor
    "diagAIRM_hp": (["diagAIRM_hp"], False), # variance-only competitor
    "covFrob_hp": (["covFrob_hp"], False),   # covariance competitor
}


def _persist_on_residual(r, end, base_w):
    thr = np.nanpercentile(r[base_w], 95) if base_w.sum() >= 5 else np.nanpercentile(r, 95)
    ce = np.concatenate([[0.0], np.cumsum(np.nan_to_num(np.maximum(0.0, r - thr)))])
    j = np.arange(len(end)); j0 = np.searchsorted(end, end - 29.5)
    return ce[j + 1] - ce[j0]


def _bstd(v, base_w):
    m = np.nanmedian(v[base_w]); s = np.nanmedian(np.abs(v[base_w] - m)) * 1.4826
    if not np.isfinite(s) or s < 1e-9:
        s = np.nanstd(v[base_w]) + 1e-9
    return (v - m) / s


def _score(feat, stat, X, remote, base_w, extra=None):
    inst, pers = COMPOSITES2[stat]
    c = np.nanmean(np.column_stack([feat["stats"][k] for k in inst]), axis=1)
    Xu = X if extra is None else np.column_stack([X, extra])
    if Xu.shape[1] == 0:
        r = np.nan_to_num(c) - np.nanmedian(c[remote]) if remote.any() else np.full(len(c), np.nan)
    else:
        r = residualise(np.nan_to_num(c), Xu, remote)
    if not pers:
        return r
    q = _persist_on_residual(r, feat["end"], base_w)
    return 0.5 * (_bstd(r, base_w) + _bstd(q, base_w))


def patient_stats2(feat: dict, T_eff: float, stat: str, basis_kind: str = "poly_dur",
                   guard: float = 2.0, rng=None, permute: bool = False) -> dict:
    end = feat["end"]
    use = (end < T_eff) & feat["valid"]
    lead = T_eff - end
    masked = feat["acq"] > MASK_ACQ
    remote = use & (end >= REMOTE_START) & (lead >= REMOTE_LEAD) & ~masked
    base_w = (end >= 20) & (end <= 45) & feat["valid"]
    X = basis(np.nan_to_num(feat["M1"]), basis_kind, remote)
    r = _score(feat, stat, X, remote, base_w)
    rc = _score(feat, stat, X, remote, base_w, extra=feat["acq"])
    hr = -np.nan_to_num(feat["M1"][:, 0])
    out = {"cls": feat["cls"],
           "frac_valid": float(feat["valid"][end < T_eff].mean()) if (end < T_eff).any() else float("nan")}
    for b, (lo, hi) in BINS.items():
        lo_eff = max(lo, guard) if b == "B5" else lo
        pm = use & (lead > lo_eff) & (lead <= hi) & ~masked
        rm = remote.copy()
        if permute and rng is not None:
            pool = np.flatnonzero(pm | rm); k = int(pm.sum())
            pick = rng.choice(pool, size=k, replace=False) if k and len(pool) > k else np.array([], int)
            pm = np.zeros_like(pm); pm[pick] = True
            rm = np.zeros_like(rm); rm[np.setdiff1d(pool, pick)] = True
        ok = pm.sum() > 0 and rm.sum() >= 20
        out[b] = {"s": auroc(r[pm], r[rm]) - 0.5 if ok else float("nan"),
                  "s_cond": auroc(rc[pm], rc[rm]) - 0.5 if ok else float("nan"),
                  "a": auroc(feat["acq"][pm], feat["acq"][rm]) - 0.5 if ok else float("nan"),
                  "s_hrmatch": _hr_matched_auroc(r, hr, pm, rm) if ok else float("nan"),
                  "conv_hr": auroc(hr[pm], hr[rm]) - 0.5 if ok else float("nan"),
                  "n_pos": int(pm.sum()), "n_neg": int(rm.sum())}
    return out


def subgroup_report(true_stats: list, alpha: float = ALPHA_BIN) -> dict:
    """Separate VT and VF estimates, a heterogeneity test, and the
    'driven by one class' rule (docs/VT_VF_ENDPOINT_ASSESSMENT.md C3-C4)."""
    from scipy.stats import t as T
    rep = {}
    for b in BINS:
        g = {}
        for cls in ("VT", "VF"):
            x = np.array([p[b]["s"] for p in true_stats if p["cls"] == cls])
            x = x[np.isfinite(x)]
            if len(x) >= 3:
                m, se = x.mean(), x.std(ddof=1) / np.sqrt(len(x))
                q = T.ppf(1 - alpha, len(x) - 1)
                g[cls] = {"n": len(x), "mean": float(m), "se": float(se),
                          "lo": float(m - q * se), "hi": float(m + q * se)}
            else:
                g[cls] = {"n": int(len(x))}
        het_p = float("nan")
        if all("se" in g[c] for c in ("VT", "VF")):
            z = (g["VT"]["mean"] - g["VF"]["mean"]) / np.hypot(g["VT"]["se"], g["VF"]["se"])
            from scipy.stats import norm
            het_p = float(2 * norm.sf(abs(z)))
        pooled = np.array([p[b]["s"] for p in true_stats]); pooled = pooled[np.isfinite(pooled)]
        pm = float(pooled.mean()) if len(pooled) else float("nan")
        one_class = False
        if all("se" in g[c] for c in ("VT", "VF")):
            a, v = g["VT"], g["VF"]
            one_class = (np.sign(a["mean"]) != np.sign(v["mean"])) or \
                        (a["lo"] > 0 and v["hi"] < 0.5 * pm) or (v["lo"] > 0 and a["hi"] < 0.5 * pm) or \
                        (het_p < 0.05)
        rep[b] = {"VT": g["VT"], "VF": g["VF"], "heterogeneity_p": het_p,
                  "pooled_mean": pm, "driven_by_one_class": bool(one_class)}
    return rep
