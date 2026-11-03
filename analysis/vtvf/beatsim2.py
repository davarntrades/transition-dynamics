"""
beatsim2.py -- extended beat-level SYNTHETIC generator and statistic panel
for the Phase-1 falsification suite (docs/VT_VF_FALSIFICATION_SUITE.md).

Extends beatsim.py (left unchanged so that run-2 results stay reproducible)
with:
  * heterogeneous patients (base heart rate, beat-level AR, baseline correlations)
  * several precursor TYPES -- correlation, variance, mean, intermittent
    correlation -- so that estimator comparisons are not rigged in favour of
    a correlation-sensitive statistic
  * conventional-only precursors: HR rise, HRV reduction, with physiological
    RT-RR coupling
  * realistic artefacts: morphology noise bursts (partially detected), beat
    detection errors in NN (missed/extra beats, partially flagged), baseline
    wander; elapsed-time gain drift; signal-dropout missingness (random and
    near-onset)
  * VT/VF subgroup labels with class-specific precursor presence
  * the full statistic panel, each on the last 256 clean beats, raw and
    locally detrended ("hp": centred 21-beat moving average removed inside
    the window -- uses only beats inside the window, so causal):
      S, dG (cov AIRM), Q (TD-3), shape (corr AIRM), Qshape, dG_hp, shape_hp,
      Qshape_hp, corrFrob_hp, meanabsr_hp, logdet_hp, diagAIRM_hp, covFrob_hp
    and conventional M1 features plus the TD-window duration (an HR proxy).

SYNTHETIC ONLY. Estimator code is shared with beatsim.py (identical to
analysis/estimators.py to ~1e-15).
"""
from __future__ import annotations

import math

import numpy as np
from scipy.signal import lfilter

from beatsim import (MEAN, NB, P, SCALE, SETTLE, BASE, W_MIN, _chol,
                     airm_batch, lw_shrunk_batch, spd_guard)

HP_W = 21                     # local-detrending moving-average width (beats)
MAX_SPAN_MIN = 10.0           # TD window invalid if its 256 clean beats span longer


def generate(rng, T_min: float, sc: dict) -> dict:
    het_pat = sc.get("het_patients", True)
    hr = float(np.clip(rng.normal(70, 8), 50, 100)) if het_pat else 70.0
    nn0 = 60.0 / hr
    phi_b = float(rng.uniform(0.65, 0.9)) if het_pat else 0.8
    jit = (lambda: rng.uniform(-0.1, 0.1)) if het_pat else (lambda: 0.0)
    c01, c12, c23 = 0.2 + jit(), 0.3 + jit(), 0.3 + jit()
    # subgroup class and precursor multiplier
    cls = "VF" if rng.random() < sc.get("p_vf", 0.3) else "VT"
    h = 1.0 + sc.get("het", 0.5) * rng.standard_normal()
    h = max(0.0, h)
    if rng.random() > sc.get("responders", 1.0):
        h = 0.0
    if sc.get("effect_class") and cls != sc["effect_class"]:
        h = 0.0
    n_est = int(T_min * hr * 1.2) + NB + 10
    phi_m, slow_sd = sc.get("phi_min", 0.95), sc.get("slow_sd", 0.5)
    n_min = int(T_min) + 3
    slow = lfilter([1.0], [1.0, -phi_m], rng.standard_normal((n_min, P)) * math.sqrt(1 - phi_m ** 2),
                   axis=0) * slow_sd
    t_nom = np.arange(n_est) * nn0 / 60.0
    lead = T_min - t_nom
    zone = (lead <= sc.get("pre_len", 30.0)) & (lead >= 0)
    ptype, g = sc.get("ptype", "corr"), sc.get("gamma", 0.0) * h
    u = rng.standard_normal((n_est, P))
    L0 = _chol(c01, c12, c23)
    frac = zone.astype(float)
    if g and ptype == "intermittent_corr":            # 2-min episodes covering ~50% of the zone
        ep = (np.floor(t_nom / 2.0).astype(int) % 2 == 0) if rng.random() < 0.5 else \
             (np.floor(t_nom / 2.0).astype(int) % 2 == 1)
        frac = (zone & ep).astype(float)
    if g and ptype == "nncorr":                       # precursor in NN-RTa coupling only
        L1 = _chol(min(0.95, c01 + g), c12, c23)
        innov = (u @ L0.T) * (1 - frac)[:, None] + (u @ L1.T) * frac[:, None]
    elif g and ptype in ("corr", "intermittent_corr"):
        L1 = _chol(c01, min(0.95, c12 + g), min(0.95, c23 + g))
        innov = (u @ L0.T) * (1 - frac)[:, None] + (u @ L1.T) * frac[:, None]
    else:
        innov = u @ L0.T
    if g and ptype == "var":
        innov[:, 1:] *= (1 + g * frac)[:, None]
    # conventional HRV reduction: NN fast innovations scaled down in the zone
    hrv = sc.get("conv_hrv", 0.0) * h
    if hrv:
        innov[:, 0] *= (1 - hrv * frac)
    fast = lfilter([math.sqrt(1 - phi_b ** 2)], [1.0, -phi_b], innov, axis=0)
    z = fast + slow[np.minimum(t_nom.astype(int), n_min - 1)]
    if g and ptype == "mean":
        z[:, 1:] += g * frac[:, None]
    kap = sc.get("conv_kappa", 0.0) * h
    if kap:
        z[:, 0] -= kap * frac
    x = np.array(MEAN, float) + z * SCALE
    x[:, 0] = x[:, 0] - MEAN[0] + nn0
    # physiological RT-RR coupling (restitution): RTa follows NN
    crt = sc.get("rt_coupling", 0.3)
    if crt:
        x[:, 1] += crt * (x[:, 0] - nn0) * (SCALE[1] / SCALE[0])
    x[:, 0] = np.clip(x[:, 0], 0.3, 2.0)
    # beat-detection errors in NN (missed beat: NN doubled; extra beat: NN halved)
    nn_rate = sc.get("nn_art_rate", 0.0) / 60.0
    nn_flag = np.zeros(len(x), bool)
    if nn_rate:
        hit = np.flatnonzero(rng.random(len(x)) < nn_rate / hr)
        for k in hit:
            x[k, 0] *= 2.0 if rng.random() < 0.5 else 0.5
            nn_flag[k] = rng.random() < sc.get("nn_detect", 0.9)
    t_min = np.cumsum(x[:, 0]) / 60.0
    keep = t_min < T_min
    x, t_min, nn_flag = x[keep], t_min[keep], nn_flag[keep]
    lead = T_min - t_min
    # morphology noise bursts, partially detected; rate rises near onset if requested
    rate = sc.get("art_base", 1.0) / 60.0 + sc.get("art_rate", 0.0) / 60.0 * np.clip(1 - lead / 60.0, 0, 1)
    starts = np.flatnonzero(rng.random(len(x)) < rate / hr)
    q_true = np.zeros(len(x), bool); q_obs = nn_flag.copy()
    det = sc.get("art_detect", 1.0)
    for s in starts:
        q_true[s:s + 20] = True
        if rng.random() < det:
            q_obs[s:s + 20] = True
    if q_true.any():
        x[q_true, 1:] += rng.standard_normal((int(q_true.sum()), 3)) * sc.get("art_amp", 2.0) * SCALE[1:]
    # baseline wander (slow random walk) on Tamp and ST
    wv = sc.get("wander", 0.0)
    if wv:
        w = np.cumsum(rng.standard_normal(len(x))) * wv / math.sqrt(hr * 10)
        x[:, 2] += w * SCALE[2]; x[:, 3] += w * SCALE[3]
    # elapsed-time gain drift on Tamp and ST
    gd = sc.get("gain_drift", 0.0)
    if gd:
        slope = rng.normal(gd, 0.25 * abs(gd))
        gain = 1.0 + slope * t_min / 600.0
        for ch in (2, 3):
            x[:, ch] = MEAN[ch] + (x[:, ch] - MEAN[ch]) * gain + 0.5 * SCALE[ch] * slope * t_min / 600.0
    # signal dropout missingness: remove beats inside gaps
    gaps = []
    gr = sc.get("gap_rate", 0.0)
    if gr:
        for _ in range(rng.poisson(gr * T_min / 60.0)):
            a = rng.uniform(0, T_min); gaps.append((a, a + rng.uniform(1, 10)))
    gn = sc.get("gap_near_onset", 0.0)
    if gn:
        for _ in range(rng.poisson(gn)):
            a = T_min - rng.uniform(2, 60); gaps.append((a, a + rng.uniform(1, 5)))
    if gaps:
        drop = np.zeros(len(x), bool)
        for a, b in gaps:
            drop |= (t_min >= a) & (t_min < b)
        x, t_min, q_obs = x[~drop], t_min[~drop], q_obs[~drop]
    return {"x": x, "t": t_min, "q": q_obs, "T": T_min, "cls": cls, "h": h}


def _hp(Y: np.ndarray, w: int = HP_W) -> np.ndarray:
    """Remove a centred moving average (width w, truncated at the window
    edges) inside each window. Y: (B, n, p)."""
    B, n, p = Y.shape
    c = np.concatenate([np.zeros((B, 1, p)), np.cumsum(Y, axis=1)], axis=1)
    i = np.arange(n); lo = np.clip(i - w // 2, 0, n); hi = np.clip(i + w // 2 + 1, 0, n)
    ma = (c[:, hi] - c[:, lo]) / (hi - lo)[None, :, None]
    return Y - ma


def _corr(S):
    d = np.sqrt(np.einsum("...ii->...i", S))
    return S / (d[..., :, None] * d[..., None, :])


def window_features(pt: dict) -> dict:
    x, t, q, T = pt["x"], pt["t"], pt["q"], pt["T"]
    bmask = (t >= SETTLE) & (t < SETTLE + BASE) & ~q
    med = np.median(x[bmask], axis=0)
    mad = np.median(np.abs(x[bmask] - med), axis=0) * 1.4826 + 1e-12
    xs = (x - med) / mad
    base = xs[bmask][None]
    S0 = lw_shrunk_batch(base)[0]; mu0 = base[0].mean(axis=0)
    P0 = np.linalg.pinv(spd_guard(S0))
    S0h = lw_shrunk_batch(_hp(base))[0]
    R0, R0h = _corr(S0), _corr(S0h)
    ends = np.arange(SETTLE + 5, int(np.floor(T)) + 1, 1.0)
    kend = np.searchsorted(t, ends, side="right")
    clean = np.flatnonzero(~q)
    cend = np.searchsorted(clean, kend, side="left")
    ok = (kend >= NB) & (cend >= NB)
    ends, kend, cend = ends[ok], kend[ok], cend[ok]
    idx = clean[cend[:, None] - NB + np.arange(NB)[None, :]]
    span = t[idx[:, -1]] - t[idx[:, 0]]
    valid = span <= MAX_SPAN_MIN
    Y = xs[idx]
    SW = lw_shrunk_batch(Y)
    Yh = _hp(Y)
    SWh = lw_shrunk_batch(Yh)
    RW, RWh = _corr(SW), _corr(SWh)
    # NN-conditional morphology structure: within each (detrended) window,
    # regress RTa, Tamp, ST on NN and keep the residuals (removes HR/HRV
    # effects transmitted through RT-RR coupling and NN-morphology covariance)
    def nn_cond(Z):
        nn = Z[:, :, :1]
        beta = (nn * Z[:, :, 1:]).sum(axis=1, keepdims=True) / ((nn ** 2).sum(axis=1, keepdims=True) + 1e-12)
        return Z[:, :, 1:] - nn * beta
    bh = _hp(base)
    S0p = lw_shrunk_batch(nn_cond(bh))[0]
    SWp = lw_shrunk_batch(nn_cond(Yh))
    R0p, RWp = _corr(S0p), _corr(SWp)
    st = {}
    st["pshape_hp"] = airm_batch(R0p, RWp)
    d = Y.mean(axis=1) - mu0
    st["S"] = np.sqrt(np.maximum(0, np.einsum("bi,ij,bj->b", d, P0, d)))
    st["dG"] = airm_batch(S0, SW)
    st["shape"] = airm_batch(R0, RW)
    st["dG_hp"] = airm_batch(S0h, SWh)
    st["shape_hp"] = airm_batch(R0h, RWh)
    iu = np.triu_indices(P, 1)
    st["corrFrob_hp"] = np.sqrt(((RWh - R0h) ** 2).sum(axis=(1, 2)))
    st["meanabsr_hp"] = np.abs(RWh[:, iu[0], iu[1]]).mean(axis=1)
    st["logdet_hp"] = np.abs(np.linalg.slogdet(spd_guard(SWh))[1] - np.linalg.slogdet(spd_guard(S0h))[1])
    vr = np.einsum("bii->bi", SWh) / np.diag(S0h)
    st["diagAIRM_hp"] = np.sqrt((np.log(vr) ** 2).sum(axis=1))
    st["covFrob_hp"] = np.sqrt(((SWh - S0h) ** 2).sum(axis=(1, 2)))
    base_w = (ends >= SETTLE + 5) & (ends <= SETTLE + BASE)

    def persist(v):
        thr = np.percentile(v[base_w], 95) if base_w.sum() >= 5 else np.percentile(v, 95)
        ce = np.concatenate([[0.0], np.cumsum(np.maximum(0.0, v - thr))])
        j = np.arange(len(ends)); j0 = np.searchsorted(ends, ends - 29.5)
        return ce[j + 1] - ce[j0]
    st["Q"] = persist(st["dG"])
    st["Qshape"] = persist(st["shape"])
    st["Qshape_hp"] = persist(st["shape_hp"])
    st["Qpshape_hp"] = persist(st["pshape_hp"])
    # conventional first-order features on 5-min time windows
    kstart = np.searchsorted(t, ends - W_MIN, side="right")
    cs = lambda v: np.concatenate([[0.0], np.cumsum(v)])
    nn, rt = x[:, 0], x[:, 1]
    c_nn, c_nn2, c_rt, c_rt2 = cs(nn), cs(nn ** 2), cs(rt), cs(rt ** 2)
    c_d2 = cs(np.concatenate([[0.0], np.diff(nn) ** 2])); c_q = cs(q.astype(float))
    cnt = np.maximum(kend - kstart, 2)
    mnn = (c_nn[kend] - c_nn[kstart]) / cnt
    sdnn = np.sqrt(np.maximum((c_nn2[kend] - c_nn2[kstart]) / cnt - mnn ** 2, 0))
    rmssd = np.sqrt((c_d2[kend] - c_d2[np.minimum(kstart + 1, kend)]) / np.maximum(cnt - 1, 1))
    mrt = (c_rt[kend] - c_rt[kstart]) / cnt
    sdrt = np.sqrt(np.maximum((c_rt2[kend] - c_rt2[kstart]) / cnt - mrt ** 2, 0))
    acq = (c_q[kend] - c_q[kstart]) / cnt
    M1 = np.column_stack([mnn, sdnn, rmssd, mrt, sdrt, span])

    def bstd(v):
        m = np.median(v[base_w], axis=0)
        s = np.median(np.abs(v[base_w] - m), axis=0) * 1.4826
        s = np.where(s > 1e-9, s, np.std(v[base_w], axis=0) + 1e-9)
        return (v - m) / s
    for k in list(st):
        st[k] = bstd(st[k])
        st[k][~valid] = np.nan
    M1 = bstd(M1); M1[~valid] = np.nan
    return {"end": ends, "M1": M1, "stats": st, "acq": acq, "valid": valid, "T": T,
            "cls": pt["cls"]}


COMPOSITES = {
    "td3": ["S", "dG", "Q"],                       # protocol v2 TD block (combined estimator)
    "shape_raw": ["shape", "Qshape"],              # run-2 recommended statistic
    "shape_hp": ["shape_hp", "Qshape_hp"],         # detrended correlation structure
    "pshape_hp": ["pshape_hp", "Qpshape_hp"],      # + NN-conditional (leakage-repaired candidate)
    "dG_hp": ["dG_hp"],                            # full covariance AIRM, detrended
    "corrFrob_hp": ["corrFrob_hp"],                # ordinary correlation statistic
    "meanabsr_hp": ["meanabsr_hp"],                # DNB-style mean |r|
    "logdet_hp": ["logdet_hp"],                    # covariance competitor
    "diagAIRM_hp": ["diagAIRM_hp"],                # variance-only competitor
    "covFrob_hp": ["covFrob_hp"],                  # covariance competitor
}
