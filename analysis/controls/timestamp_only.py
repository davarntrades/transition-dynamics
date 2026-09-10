"""
timestamp_only.py — M0, the acquisition-process control.

This control runs BEFORE any physiological model is interpreted. It is not a
robustness check bolted on afterwards; it is the gate.

The reasoning
-------------
Clinical measurements are not sampled on a fixed schedule. A worried nurse
measures more often, orders more labs, and re-checks sooner. That concern
precedes the event. So measurement TIMING carries outcome information that has
nothing to do with physiology — and, worse, it contaminates the covariance
estimate itself, because a window sampled twice as densely has different
empirical second-order structure for purely procedural reasons.

M0 uses ONLY acquisition metadata. No physiological value ever enters it.

Preregistered leakage verdicts (fixed before running):

    AUPRC(M0) >= 0.90 * AUPRC(M3)   CRITICAL  — primary mechanistic claim fails
    AUPRC(M0) >= 0.70 * AUPRC(M3)   SEVERE    — claim downgraded to Level 1
    AUPRC(M0) >= 0.50 * AUPRC(M3)   MATERIAL  — must report jointly, always
    otherwise                       ACCEPTABLE

These are not thresholds to be renegotiated after seeing the numbers.
"""

from __future__ import annotations

import numpy as np


def acquisition_features(timestamps: np.ndarray, observed_mask: np.ndarray,
                         window: tuple[float, float]) -> dict:
    """
    Build M0's feature vector from acquisition metadata alone.

    timestamps    (T,)     time of each potential observation slot
    observed_mask (T, p)   True where a value actually exists
    window        (t0, t1) analysis window

    Deliberately contains NO physiological values. If you find yourself wanting
    to add one "just for context", that is the leakage this control exists to
    detect.
    """
    t = np.asarray(timestamps, float)
    M = np.asarray(observed_mask, bool)
    sel = (t >= window[0]) & (t < window[1])
    tw, Mw = t[sel], M[sel]
    if len(tw) < 2:
        return {}

    any_obs = Mw.any(axis=1)
    obs_times = tw[any_obs]
    gaps = np.diff(obs_times) if len(obs_times) > 1 else np.array([np.nan])
    span = max(1e-9, tw[-1] - tw[0])

    feats = {
        "n_observations": float(Mw.sum()),
        "observation_rate": float(Mw.sum() / span),
        "n_distinct_times": float(len(obs_times)),
        "mean_gap": float(np.nanmean(gaps)),
        "sd_gap": float(np.nanstd(gaps)),
        "min_gap": float(np.nanmin(gaps)),
        "gap_trend": float(np.polyfit(np.arange(len(gaps)), gaps, 1)[0])
                     if len(gaps) > 2 and not np.isnan(gaps).any() else 0.0,
        "missing_fraction": float(1.0 - Mw.mean()),
        "n_channels_ever": float((Mw.any(axis=0)).sum()),
        "channel_count_trend": float(
            np.polyfit(np.arange(len(Mw)), Mw.sum(axis=1), 1)[0]),
        "burstiness": float(np.nanstd(gaps) / np.nanmean(gaps))
                      if np.nanmean(gaps) > 0 else 0.0,
    }
    for j in range(Mw.shape[1]):
        feats[f"rate_ch{j}"] = float(Mw[:, j].sum() / span)
    return feats


LEAKAGE_LEVELS = (
    (0.90, "CRITICAL",   "Primary mechanistic claim FAILS. Result is acquisition behaviour."),
    (0.70, "SEVERE",     "Claim downgraded to Level 1 (retrospective association) at most."),
    (0.50, "MATERIAL",   "M0 and M3 must be reported jointly in every table and abstract."),
)


def leakage_verdict(auprc_m0: float, auprc_m3: float) -> dict:
    """Apply the preregistered verdicts. No discretion at analysis time."""
    if auprc_m3 <= 0:
        return {"ratio": float("nan"), "verdict": "UNDEFINED",
                "action": "M3 has no signal to compare against."}
    ratio = auprc_m0 / auprc_m3
    for thr, verdict, action in LEAKAGE_LEVELS:
        if ratio >= thr:
            return {"ratio": ratio, "verdict": verdict, "action": action}
    return {"ratio": ratio, "verdict": "ACCEPTABLE",
            "action": "Acquisition behaviour does not account for the signal."}


if __name__ == "__main__":
    print("M0 leakage verdict table (preregistered)\n" + "=" * 60)
    for m0, m3 in ((0.40, 0.42), (0.32, 0.42), (0.23, 0.42), (0.10, 0.42)):
        v = leakage_verdict(m0, m3)
        print(f"  AUPRC M0={m0:.2f}  M3={m3:.2f}  ratio={v['ratio']:.2f}  "
              f"-> {v['verdict']}")
        print(f"      {v['action']}")
