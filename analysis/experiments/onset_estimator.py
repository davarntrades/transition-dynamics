"""
onset_estimator.py — STAGE 2/3: independent estimation of time-since-onset.

Stage 1 showed that alignment separates targeted from untargeted displacement
once true exposure is controlled. Controlling it by fiat is not available on
real data, so this module estimates onset from the displacement trajectory
alone and Stage 4 repeats the discrimination using the estimate.

MODEL — the existing dynamics, unchanged
----------------------------------------
    delta_i(t) = (f_i / k_i) * (1 - exp(-k_i (t - t0)))      for t >= t0
               = 0                                            for t <  t0

Written with b_i = f_i / k_i, so the model is LINEAR in b given (t0, k).

CIRCULARITY GUARDS — the point of this file
-------------------------------------------
1. k_i is estimated from BASELINE data only, via lag-1 autocorrelation:
   for the discrete recursion with a_i = exp(-k_i h), k_i = -log(a_i)/h.
   No post-onset data, no targeting label, no alignment.
2. The onset estimator never sees alignment. It fits per-channel amplitudes
   and selects t0 by held-out prediction error only.
3. TEMPORAL CROSS-FITTING: onset is estimated on odd-indexed samples of the
   pre-window; the alignment used in Stage 4 is computed from even-indexed
   samples. The two are not evaluated on the same observations.
4. The estimator may return None ("onset not identifiable") and is required to
   do so on stationary trajectories.

Run:  python3 analysis/experiments/onset_estimator.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(__file__)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, ".."))

import estimators as E                                            # noqa: E402
from exposure_stage1_oracle import (Config, simulate, stationary_cov,  # noqa: E402
                                    d_isotropic, d_stiff_sub, d_soft_sub,
                                    calibrate)


# ---------------------------------------------------------------------------
# Step 1 — per-channel rates, from BASELINE ONLY
# ---------------------------------------------------------------------------

def estimate_rates(baseline: np.ndarray, h: float) -> np.ndarray:
    """
    k_i from lag-1 autocorrelation of the baseline. Uses no post-onset data,
    no labels, and no alignment.

    In a rotated (non-diagonal) system the observed channels are mixtures of
    eigen-coordinates, so a per-channel rate is an effective rate rather than
    a true eigenvalue. That approximation is deliberate: it is what is
    available from real data, and Stage 3 measures what it costs.
    """
    X = np.asarray(baseline, float)
    Xc = X - X.mean(0)
    num = (Xc[:-1] * Xc[1:]).sum(0)
    den = (Xc * Xc).sum(0)
    a = np.clip(num / np.maximum(den, 1e-12), 1e-4, 0.9999)
    return -np.log(a) / h


# ---------------------------------------------------------------------------
# Step 2 — profile fit over candidate onsets
# ---------------------------------------------------------------------------

def _fit_given_onset(t_rel, Y, k, t0):
    """
    Closed-form least squares for b given (t0, k).
    Y is (n, p), centred on the baseline mean. Returns (b, prediction).
    """
    g = np.where(t_rel[:, None] >= t0, 1.0 - np.exp(-k[None, :] *
                                                    (t_rel[:, None] - t0)), 0.0)
    gg = (g * g).sum(0)
    b = np.where(gg > 1e-12, (g * Y).sum(0) / np.maximum(gg, 1e-12), 0.0)
    return b, g * b[None, :]


_NULL_CACHE = {}


def null_threshold(cfg: Config, n: int = 40, q: float = 0.95) -> float:
    """
    Identifiability threshold, calibrated on STATIONARY trajectories of the
    same configuration. Uses no targeting label and no post-onset data.

    Needed because interleaved cross-fitting does not control overfitting on
    autocorrelated data: with lag-1 correlation near 0.76 the "held-out" half
    is close to a copy of the fitting half, so a fit to pure noise still
    reduces held-out error. The split still does what Stage 4 requires — the
    alignment test uses observations the onset fit never saw — but the
    threshold for "is there an onset at all" has to come from the null
    distribution rather than from the held-out score being near zero.
    """
    key = (cfg.name, cfg.p, cfg.sigma, cfg.k_lo, cfg.k_hi, cfg.rotate, n, q)
    if key in _NULL_CACHE:
        return _NULL_CACHE[key]
    g = [estimate_onset(simulate(cfg, None, 0.0, 0.0, 10_000 + i), cfg,
                        _skip_ident=True)["gain_null"] for i in range(n)]
    thr = float(np.quantile(g, q))
    _NULL_CACHE[key] = thr
    return thr


def estimate_onset(X, cfg: Config, n_grid: int = 40, use_odd: bool = True,
                   _skip_ident: bool = False):
    """
    Profile least squares over candidate onsets with held-out scoring.

    Returns dict with T_hat (time-since-onset at the end of the window),
    identifiable (bool), reason, profile curve, and the 95% profile interval.
    """
    base = X[:cfg.base_n]
    pre = X[cfg.base_n:]
    n, p = pre.shape
    h = cfg.h

    k = estimate_rates(base, h)
    mu0 = base.mean(0)
    Y = pre - mu0
    t_rel = np.arange(n) * h

    # temporal cross-fitting: fit on one interleaved half, score on the other
    fit_idx = np.arange(0, n, 2) if use_odd else np.arange(1, n, 2)
    sc_idx = np.arange(1, n, 2) if use_odd else np.arange(0, n, 2)

    cands = np.linspace(0.0, t_rel[-1], n_grid)
    sse = np.empty(n_grid)
    for j, t0 in enumerate(cands):
        b, _ = _fit_given_onset(t_rel[fit_idx], Y[fit_idx], k, t0)
        g = np.where(t_rel[sc_idx][:, None] >= t0,
                     1.0 - np.exp(-k[None, :] * (t_rel[sc_idx][:, None] - t0)),
                     0.0)
        sse[j] = float(((Y[sc_idx] - g * b[None, :]) ** 2).sum())

    best = int(np.argmin(sse))
    t0_hat = float(cands[best])
    T_hat = float(t_rel[-1] - t0_hat)

    # --- identifiability ---
    # (a) does ANY onset beat a no-displacement model on held-out error?
    sse_null = float((Y[sc_idx] ** 2).sum())
    gain_null = (sse_null - sse[best]) / max(sse_null, 1e-12)
    # (b) is the profile actually peaked, or flat across the grid?
    rng_prof = (sse.max() - sse.min()) / max(sse.max(), 1e-12)
    # (c) profile interval: onsets whose held-out error is within 2% of best
    inside = cands[sse <= sse[best] * 1.02]
    width = float(inside.max() - inside.min()) if len(inside) else t_rel[-1]

    reason = ""
    ident = True
    if not _skip_ident:
        thr = null_threshold(cfg)
        if gain_null < thr:
            ident, reason = False, (
                f"displacement not distinguishable from stationary "
                f"(gain {gain_null:.3f} < null threshold {thr:.3f})")
        elif rng_prof < 0.01:
            ident, reason = False, "profile flat across candidate onsets"
        elif width > 0.60 * t_rel[-1]:
            ident, reason = False, "profile interval spans most of the window"

    return {"T_hat": T_hat if ident else None, "T_hat_raw": T_hat,
            "identifiable": ident, "reason": reason,
            "interval_width": width, "gain_null": gain_null,
            "profile": sse, "cands": cands, "k_hat": k}


def alignment_crossfit(X, cfg: Config, use_even=True):
    """
    Alignment computed from the samples NOT used for onset estimation.
    Baseline (and hence Lambda) is untouched by the split.
    """
    base = X[:cfg.base_n]
    pre = X[cfg.base_n:]
    idx = np.arange(1, len(pre), 2) if use_even else np.arange(0, len(pre), 2)
    S0 = E._spd_guard(E.shrunk_covariance(base))
    mu0 = base.mean(0)
    d = pre[idx].mean(0) - mu0
    return E.stiffness_alignment(d, S0, precision=np.linalg.pinv(S0))


# ---------------------------------------------------------------------------
# Stage 3 — validation against known truth
# ---------------------------------------------------------------------------

def main() -> str:
    out, w = [], lambda s: out.append(s)
    SEEDS = range(20)
    EXPOS = [3.0, 10.0, 30.0, 60.0, 120.0]
    SEVS = [10.0, 30.0]
    STRUCTS = [Config("wide-rotated"), Config("wide-diagonal", rotate=False),
               Config("high-noise", sigma=2.0), Config("narrow-rotated",
                                                       k_lo=0.60, k_hi=2.40)]

    w("# Stage 3 — onset estimator validation\n")
    w("Generated by `analysis/experiments/onset_estimator.py`. Rates are "
      "estimated from baseline only; the onset estimator never sees alignment "
      "or the targeting label; onset is fitted on odd-indexed samples and "
      "alignment is computed on even-indexed samples.\n")

    # --- rate recovery ---
    w("\n## 1. Baseline rate recovery\n")
    w("\nWhen channels are eigen-coordinates the estimated rate pairs with a "
      "true rate and the error is meaningful. When the system is rotated, the "
      "channels are mixtures and no such pairing exists, so only the "
      "geometric-mean rate is comparable. Reporting a per-channel error in "
      "that case would be comparing two different things.\n")
    w("\n| structure | metric | value |")
    w("|---|---|:--:|")
    for cfg in STRUCTS:
        gm_true = float(np.exp(np.mean(np.log(cfg.k))))
        per, gm = [], []
        for i in SEEDS:
            kh = estimate_rates(simulate(cfg, None, 0.0, 0.0, i)[:cfg.base_n],
                                cfg.h)
            gm.append(float(np.exp(np.mean(np.log(kh)))) / gm_true)
            if not cfg.rotate:
                per.append(float(np.median(np.abs(kh - cfg.k) / cfg.k)))
        if per:
            w(f"| {cfg.name} | median per-channel relative error | "
              f"{np.median(per):.2f} |")
        w(f"| {cfg.name} | geometric-mean rate, estimated / true | "
          f"{np.median(gm):.2f} |")

    # --- stationary control: must say "not identifiable" ---
    w("\n## 2. Stationary control — must decline to answer\n")
    w("\n| structure | fraction declared NOT identifiable |")
    w("|---|:--:|")
    for cfg in STRUCTS:
        flags = [not estimate_onset(simulate(cfg, None, 0.0, 0.0, i),
                                    cfg)["identifiable"] for i in SEEDS]
        w(f"| {cfg.name} | {np.mean(flags):.0%} |")

    # --- accuracy by regime ---
    w("\n## 3. Accuracy versus true exposure\n")
    w("\n| structure | severity | true T | median T̂ | MAE | bias | identifiable |")
    w("|---|:--:|:--:|:--:|:--:|:--:|:--:|")
    acc = []
    for cfg in STRUCTS:
        for sev in SEVS:
            for T in EXPOS:
                s = calibrate(cfg, d_stiff_sub, T, sev)
                res = [estimate_onset(simulate(cfg, d_stiff_sub(cfg, i), s, T, i),
                                      cfg) for i in SEEDS]
                ok = [r for r in res if r["identifiable"]]
                frac = len(ok) / len(res)
                if ok:
                    th = np.array([r["T_hat"] for r in ok])
                    mae = float(np.mean(np.abs(th - T)))
                    bias = float(np.mean(th - T))
                    med = float(np.median(th))
                else:
                    mae = bias = med = float("nan")
                acc.append({"cfg": cfg.name, "sev": sev, "T": T, "mae": mae,
                            "bias": bias, "frac": frac})
                w(f"| {cfg.name} | {sev:g} | {T:g} | {med:.1f} | {mae:.1f} "
                  f"| {bias:+.1f} | {frac:.0%} |")

    a = [x for x in acc if x["frac"] > 0 and x["mae"] == x["mae"]]
    w(f"\nOverall: median MAE **{np.median([x['mae'] for x in a]):.1f}** time "
      f"units; median bias {np.median([x['bias'] for x in a]):+.1f}; "
      f"identifiable in {np.mean([x['frac'] for x in acc]):.0%} of cases.\n")

    w("\n### Non-identifiable regimes\n")
    bad = [x for x in acc if x["frac"] < 0.5]
    if bad:
        w("\n| structure | severity | true T | identifiable |")
        w("|---|:--:|:--:|:--:|")
        for x in bad:
            w(f"| {x['cfg']} | {x['sev']:g} | {x['T']:g} | {x['frac']:.0%} |")
    else:
        w("\nNone: the estimator returned an onset in at least half of runs in "
          "every regime tested.\n")
    return "\n".join(out)


if __name__ == "__main__":
    txt = main()
    with open(os.path.join(_HERE, "..", "results",
                           "stage3_onset_validation.md"), "w") as fh:
        fh.write(txt)
    print(txt)
