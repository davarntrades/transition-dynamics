"""
beatsim.py -- beat-level SYNTHETIC ECG-panel generator and the protocol's
actual Transition Dynamics estimators.

Addresses review finding F7 (the v2 simulation used linear 5-min mean shifts,
not the protocol's estimators). Here each synthetic patient emits a per-beat
4-channel panel (NN, RTa, Tamp, ST) and the windowed features are computed
exactly as the protocol specifies:

  * M1 (conventional, 5-min time windows): mean NN, SDNN, RMSSD, mean RTa, SD RTa
  * ACQ (pure-acquisition): fraction of beats flagged by a burst-artefact
    indicator in the 5-min window (an absolute, physically defined criterion)
  * TD-1  S(t)   = sqrt(d' Sigma0^-1 d), d = mean of last 256 beats - baseline mean
  * TD-2  dG(t)  = AIRM(Sigma0, Sigma_W) with Ledoit-Wolf shrinkage (identical
                  formula to analysis/estimators.py: shrunk_covariance +
                  _spd_guard + delta_G_structure), on the last 256 beats
  * TD-3  Qint(t)= sum over the trailing 30 min of max(0, dG - theta),
                  theta = baseline 95th percentile of dG

SYNTHETIC ONLY. Nothing here reads real data.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.signal import lfilter

P = 4                       # NN, RTa, Tamp, ST
NB = 256                    # beats per covariance window
W_MIN = 5                   # first-order window (min)
SETTLE, BASE = 15, 30       # min
BEATS_PER_MIN = 70.0
SCALE = np.array([0.04, 0.008, 0.05, 0.02])     # per-channel SD (s, s, mV, mV)
MEAN = np.array([0.86, 0.28, 0.30, 0.00])


def _chol(c01: float, c12: float, c23: float) -> np.ndarray:
    C = np.eye(P)
    C[0, 1] = C[1, 0] = c01
    C[1, 2] = C[2, 1] = c12
    C[2, 3] = C[3, 2] = c23
    w, v = np.linalg.eigh(C)
    C = v @ np.diag(np.maximum(w, 1e-3)) @ v.T
    d = np.sqrt(np.diag(C))
    return np.linalg.cholesky(C / np.outer(d, d))


def generate_patient(rng, T_min: float, sc: dict) -> dict:
    """Beat-level panel up to the (pseudo-)event at T_min minutes.

    sc keys (all optional):
      td_gamma   : TD-specific precursor, change in the RTa-Tamp and Tamp-ST
                   correlations during the last td_len minutes (marginals unchanged)
      td_len     : minutes (default 30); td_shape 'step' | 'ramp'
      conv_kappa : conventional precursor, NN mean shortening in SD units (HR rise)
      art_rate   : burst-artefact rate (bursts/hour) in the final 60 min
      art_base   : background burst rate (bursts/hour), default 1
      art_amp    : burst noise amplitude in channel-SD units (default 2)
      gain_drift : per-10-h multiplicative gain drift on Tamp and ST (mean slope)
      het        : SD of per-patient multiplier on precursor amplitudes
      phi_beat, phi_min, slow_sd : dynamics
    """
    het = sc.get("het", 0.5)
    h = max(0.0, 1.0 + het * rng.standard_normal()) if het > 0 else 1.0
    if rng.random() > sc.get("responders", 1.0):
        h = 0.0
    n_est = int(T_min * BEATS_PER_MIN * 1.15) + NB + 10
    phi_b, phi_m, slow_sd = sc.get("phi_beat", 0.8), sc.get("phi_min", 0.95), sc.get("slow_sd", 0.5)
    # slow minute-level component per channel
    n_min = int(T_min) + 3
    e = rng.standard_normal((n_min, P)) * math.sqrt(1 - phi_m ** 2)
    slow = lfilter([1.0], [1.0, -phi_m], e, axis=0) * slow_sd
    # fast beat-level component with time-varying correlation
    u = rng.standard_normal((n_est, P))
    L0 = _chol(0.2, 0.3, 0.3)
    g = sc.get("td_gamma", 0.0) * h
    L1 = _chol(0.2, min(0.95, 0.3 + g), min(0.95, 0.3 + g)) if g else L0
    # first pass with nominal timing to locate beats in the precursor zone
    nn0 = MEAN[0]
    t_nom = np.arange(n_est) * nn0 / 60.0                  # minutes
    lead_nom = T_min - t_nom
    td_len = sc.get("td_len", 30.0)
    in_td = (lead_nom <= td_len) & (lead_nom >= 0) & (g != 0)
    if sc.get("td_shape", "step") == "ramp" and g:
        frac = np.clip(1 - lead_nom / td_len, 0, 1)
    else:
        frac = in_td.astype(float)
    innov0 = u @ L0.T
    innov1 = u @ L1.T
    innov = innov0 * (1 - frac)[:, None] + innov1 * frac[:, None]
    fast = lfilter([math.sqrt(1 - phi_b ** 2)], [1.0, -phi_b], innov, axis=0)
    z = fast + slow[np.minimum(t_nom.astype(int), n_min - 1)]
    # conventional precursor: NN shortening in last 30 min (HR rise)
    kap = sc.get("conv_kappa", 0.0) * h
    if kap:
        z[:, 0] -= kap * ((lead_nom <= 30) & (lead_nom >= 0))
    x = MEAN + z * SCALE
    x[:, 0] = np.clip(x[:, 0], 0.3, 2.0)
    t_sec = np.cumsum(x[:, 0])
    t_min = t_sec / 60.0
    keep = t_min < T_min
    x, t_min = x[keep], t_min[keep]
    lead = T_min - t_min
    # recording artefacts: burst indicator q and added noise on morphology channels
    q = np.zeros(len(x), bool)
    base_rate = sc.get("art_base", 1.0) / 60.0           # per minute
    late_rate = sc.get("art_rate", 0.0) / 60.0
    rate = base_rate + late_rate * np.clip(1 - lead / 60.0, 0, 1)
    p_start = rate / BEATS_PER_MIN
    starts = np.flatnonzero(rng.random(len(x)) < p_start)
    for s in starts:
        q[s:s + 20] = True
    amp = sc.get("art_amp", 2.0)
    q_obs = q.copy()
    if q.any():
        noise = rng.standard_normal((int(q.sum()), 3)) * amp * SCALE[1:]
        x[q, 1:] += noise
        det = sc.get("art_detect", 1.0)               # per-burst detection probability
        if det < 1.0:
            for s in starts:
                if rng.random() > det:
                    q_obs[s:s + 20] = False
    # gain drift on Tamp, ST (multiplicative, elapsed-time locked)
    gd = sc.get("gain_drift", 0.0)
    if gd:
        slope = rng.normal(gd, 0.25 * abs(gd))
        gain = 1.0 + slope * t_min / 600.0
        x[:, 2] = MEAN[2] + (x[:, 2] - MEAN[2]) * gain + 0.5 * SCALE[2] * slope * t_min / 600.0
        x[:, 3] = MEAN[3] + (x[:, 3] - MEAN[3]) * gain + 0.5 * SCALE[3] * slope * t_min / 600.0
    return {"x": x, "t": t_min, "q": q_obs, "q_true": q, "T": T_min}


# ---------------------------------------------------------------------------
# Estimators (vectorised; identical formulas to analysis/estimators.py)
# ---------------------------------------------------------------------------
def lw_shrunk_batch(Y: np.ndarray) -> np.ndarray:
    """Ledoit-Wolf toward mu*I for a batch of windows Y (B, n, p), same formula
    as estimators.shrunk_covariance (S with n-1; b2 summed over rows / n^2)."""
    B, n, p = Y.shape
    Yc = Y - Y.mean(axis=1, keepdims=True)
    S = np.einsum("bni,bnj->bij", Yc, Yc) / max(1, n - 1)
    mu = np.trace(S, axis1=1, axis2=2) / p
    target = mu[:, None, None] * np.eye(p)
    d2 = ((S - target) ** 2).sum(axis=(1, 2))
    sq = (Yc ** 2).sum(axis=2)                                     # ||y_k||^2
    term1 = (sq ** 2).sum(axis=1)                                  # sum ||y||^4
    term2 = np.einsum("bni,bij,bnj->b", Yc, S, Yc)                 # sum y'Sy
    term3 = n * (S ** 2).sum(axis=(1, 2))                          # n ||S||^2
    b2 = (term1 - 2 * term2 + term3) / n ** 2
    alpha = np.where(d2 <= 0, 0.0, np.clip(b2 / np.where(d2 > 0, d2, 1), 0.0, 1.0))
    return (1 - alpha)[:, None, None] * S + alpha[:, None, None] * target


def spd_guard(S: np.ndarray, floor_ratio: float = 1e-6) -> np.ndarray:
    w, v = np.linalg.eigh((S + np.swapaxes(S, -1, -2)) / 2)
    floor = np.maximum(w.max(axis=-1, keepdims=True), 1e-12) * floor_ratio
    w = np.maximum(w, floor)
    return np.einsum("...ij,...j,...kj->...ik", v, w, v)


def airm_batch(S0: np.ndarray, SW: np.ndarray) -> np.ndarray:
    S0 = spd_guard(S0)
    SW = spd_guard(SW)
    w, v = np.linalg.eigh(S0)
    inv_sqrt = v @ np.diag(w ** -0.5) @ v.T
    M = np.einsum("ij,bjk,kl->bil", inv_sqrt, SW, inv_sqrt)
    ev = np.linalg.eigvalsh((M + np.swapaxes(M, 1, 2)) / 2)
    ev = np.maximum(ev, 1e-12)
    return np.sqrt((np.log(ev) ** 2).sum(axis=1))


def window_features(pt: dict, lead_onset: float | None = None) -> dict:
    """Features at window ends on a 1-min grid NOT aligned to the event
    (window end m in whole minutes of elapsed time; lead = T - m is fractional)."""
    x, t, q, T = pt["x"], pt["t"], pt["q"], pt["T"]
    # robust baseline standardisation of the panel
    bmask = (t >= SETTLE) & (t < SETTLE + BASE)
    med = np.median(x[bmask], axis=0)
    mad = np.median(np.abs(x[bmask] - med), axis=0) * 1.4826 + 1e-12
    xs = (x - med) / mad
    Sigma0 = lw_shrunk_batch(xs[bmask][None])[0]
    mu0 = xs[bmask].mean(axis=0)
    P0 = np.linalg.pinv(spd_guard(Sigma0))
    ends = np.arange(SETTLE + 5, int(np.floor(T)) + 1, 1.0)         # window end minutes
    kend = np.searchsorted(t, ends, side="right")                  # beats with t <= end
    # TD windows use the last NB beats NOT flagged as artefact (beat-level exclusion)
    clean = np.flatnonzero(~q)
    cend = np.searchsorted(clean, kend, side="left")               # clean beats before kend
    ok = (kend >= NB) & (cend >= NB)
    ends, kend, cend = ends[ok], kend[ok], cend[ok]
    idx = clean[cend[:, None] - NB + np.arange(NB)[None, :]]
    Y = xs[idx]                                                    # (B, NB, P)
    SW = lw_shrunk_batch(Y)
    dG = airm_batch(Sigma0, SW)
    d0 = np.sqrt(np.diag(Sigma0)); R0 = Sigma0 / np.outer(d0, d0)
    dW = np.sqrt(np.einsum("bii->bi", SW)); RW = SW / (dW[:, :, None] * dW[:, None, :])
    dGc = airm_batch(R0, RW)                                       # correlation-only (shape)
    d = Y.mean(axis=1) - mu0
    S = np.sqrt(np.maximum(0.0, np.einsum("bi,ij,bj->b", d, P0, d)))
    # first-order 5-min time windows via cumulative sums
    kstart = np.searchsorted(t, ends - W_MIN, side="right")
    cs = lambda v: np.concatenate([[0.0], np.cumsum(v)])
    nn, rt = x[:, 0], x[:, 1]
    c_nn, c_nn2, c_rt, c_rt2 = cs(nn), cs(nn ** 2), cs(rt), cs(rt ** 2)
    dnn2 = np.concatenate([[0.0], np.diff(nn) ** 2])
    c_d2, c_q = cs(dnn2), cs(q.astype(float))
    cnt = np.maximum(kend - kstart, 2)
    mean_nn = (c_nn[kend] - c_nn[kstart]) / cnt
    sd_nn = np.sqrt(np.maximum((c_nn2[kend] - c_nn2[kstart]) / cnt - mean_nn ** 2, 0))
    rmssd = np.sqrt((c_d2[kend] - c_d2[kstart + 1]) / np.maximum(cnt - 1, 1))
    mean_rt = (c_rt[kend] - c_rt[kstart]) / cnt
    sd_rt = np.sqrt(np.maximum((c_rt2[kend] - c_rt2[kstart]) / cnt - mean_rt ** 2, 0))
    acq = (c_q[kend] - c_q[kstart]) / cnt
    # TD-3 persistence integral over trailing 30 min of dG above baseline 95th pct
    base_w = (ends >= SETTLE + 5) & (ends <= SETTLE + BASE)
    theta = np.percentile(dG[base_w], 95) if base_w.sum() >= 5 else np.percentile(dG, 95)
    exc = np.maximum(0.0, dG - theta)
    ce = cs(exc)
    j = np.arange(len(ends))
    j0 = np.searchsorted(ends, ends - 29.5)
    Q = ce[j + 1] - ce[j0]
    excc = np.maximum(0.0, dGc - (np.percentile(dGc[base_w], 95) if base_w.sum() >= 5
                                  else np.percentile(dGc, 95)))
    cec = cs(excc)
    Qc = cec[j + 1] - cec[j0]
    M1 = np.column_stack([mean_nn, sd_nn, rmssd, mean_rt, sd_rt])
    TD = np.column_stack([S, dG, Q, dGc, Qc])        # TD-1, TD-2, TD-3, shape, shape-persistence
    # standardise every feature by its baseline windows (median / MAD)
    def bstd(F):
        m = np.median(F[base_w], axis=0)
        s = np.median(np.abs(F[base_w] - m), axis=0) * 1.4826
        s = np.where(s > 1e-9, s, np.std(F[base_w], axis=0) + 1e-9)
        return (F - m) / s
    return {"end": ends, "M1": bstd(M1), "TD": bstd(TD), "acq": acq,
            "td_raw": TD, "T": T}
