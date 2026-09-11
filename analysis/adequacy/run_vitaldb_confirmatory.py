"""
run_vitaldb_confirmatory.py — the confirmatory model-adequacy test on VitalDB.

Runs the frozen protocol plus the 2026-09-11 amendment. Nothing here is tuned.

PIPELINE PER CASE
  baseline   first 120 min (amended rule 2); yields mu_0, Sigma_0, k_i
  admissible n_eff >= 10p in baseline AND block-bootstrap stationarity screen
  later      the segment AFTER the baseline, never used to estimate k_i
  Stage B    held-out block CV over 7 models on the later segment
  Stage C    baseline-derived k vs curvature-derived k, temporally separated
  surrogate  phase-randomised controls of the same later segment

OUT-OF-SAMPLE DISCIPLINE
  k_i comes only from the baseline window.
  Onset and amplitudes are fitted on training blocks of the later segment.
  Prediction is scored on held-out contiguous blocks of the later segment.
  No case contributes to both calibration and confirmatory sets.

Run:  python3 analysis/adequacy/run_vitaldb_confirmatory.py
"""
from __future__ import annotations
import json, os, sys
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
sys.path.insert(0, os.path.join(_H, ".."))

from vitaldb_fetch import load_case                                  # noqa
from vitaldb_cohort import split, BASELINE_MINUTES, INTERVAL_S       # noqa
from adequacy import (n_eff, baseline_rates, stage_b, stage_c,       # noqa
                      MODELS, phase_surrogate, MIN_NEFF_FACTOR,
                      MIN_RECORDINGS, ADEQUATE_FRAC, NARROW_FRAC,
                      MAX_DECLINE, MIN_RATE_RANKCORR)
from stationarity_calibration import stationarity_reject             # noqa

NB = int(BASELINE_MINUTES * 60 / INTERVAL_S)
H_HOURS = INTERVAL_S / 3600.0
# Analysis resolution for the later segment, chosen by an identifiability
# criterion rather than by convenience. A relaxation rate is recoverable at
# resolution h only if the lag-1 autocorrelation there exceeds exp(-0.5) =
# 0.607; above that the rate exceeds 1/(2h) and has decayed between samples.
# Measured on the calibration set, the fraction of identifiable channels is
# 96% at 2 s, 86% at 10 s, and only 43% at 60 s. The segment is therefore
# analysed at native 2 s resolution.
DECIM = 1


def prepare(caseid):
    d = load_case(caseid)
    X = d["X"]
    if X.size == 0 or len(d["channels"]) < 4:
        return None, "fewer than 4 channels"
    Xc = X[np.isfinite(X).all(axis=1)]
    if len(Xc) < NB + 600:
        return None, "too short after removing incomplete rows"
    B = Xc[:NB]
    p = B.shape[1]
    ne = n_eff(B)
    if ne < MIN_NEFF_FACTOR * p:
        return None, f"baseline n_eff {ne:.0f} < {MIN_NEFF_FACTOR*p}"
    rej, obs, thr, _ = stationarity_reject(B, n_boot=200, seed=caseid)
    if rej:
        return None, f"baseline non-stationary (shift {obs:.2f} > {thr:.2f})"
    later = Xc[NB:][::DECIM]
    if len(later) < 60:
        return None, "later segment too short"
    return {"caseid": caseid, "B": B, "later": later, "n_eff": ne,
            "channels": d["channels"], "sha256": d["sha256"]}, None


def run_case(rec):
    h = INTERVAL_S * DECIM / 3600.0          # hours per later-segment sample
    # Baseline rates are estimated at the SAME resolution as the later segment.
    # An autocorrelation rate is resolution dependent: rates derived at 2 s
    # reach ~1000/hour, whose relaxation time is seconds and is not
    # identifiable from curvature sampled once a minute. Decimating the
    # baseline first makes the two quantities refer to the same timescale band.
    k_base = baseline_rates(rec["B"][::DECIM], h)
    L = rec["later"] - rec["B"].mean(0)      # displacement from baseline mean
    res = stage_b(L, h, k_base)
    best = min(MODELS, key=lambda m: res[m])
    sur = []
    for s in range(8):
        rs = stage_b(phase_surrogate(L, 1000 + s), h, k_base)
        sur.append(min(MODELS, key=lambda m: rs[m]) == "M-exp")
    # IDENTIFIABILITY BAND. A relaxation rate can only be recovered from a
    # trajectory if its relaxation time lies between the sampling interval and
    # the segment length. Faster rates have decayed between samples; slower
    # ones have not begun to bend within the segment. Channels whose baseline
    # rate falls outside that band are excluded from the rate-consistency
    # comparison -- they are unidentifiable in principle, not badly fitted --
    # and the count is reported. They remain in Stage B.
    T_seg = len(rec["later"]) * h
    k_lo, k_hi = 1.0 / T_seg, 1.0 / (2.0 * h)
    band = (k_base >= k_lo) & (k_base <= k_hi)
    if band.sum() >= 3:
        c = stage_c(rec["later"][:, band], h, k_base[band])
    else:
        c = {"k_curv": np.full(int(band.sum()), np.nan),
             "rank_corr": float("nan"), "log_bias": float("nan")}
    return {"caseid": rec["caseid"], "mse": {m: res[m] for m in MODELS},
            "best": best, "exp_beats_free": res["M-exp"] <= res["M-exp-free"],
            "surrogate_sel": float(np.mean(sur)),
            "k_base": k_base.tolist(), "k_curv": c["k_curv"].tolist(),
            "rank_corr": c["rank_corr"], "log_bias": c["log_bias"],
            "n_identifiable": int(band.sum()), "k_band": [k_lo, k_hi],
            "n_eff": rec["n_eff"], "sha256": rec["sha256"]}


def main() -> str:
    ids = split()["confirmatory"]
    kept, excl = [], {}
    for c in ids:
        try:
            rec, why = prepare(c)
        except Exception as e:
            rec, why = None, f"error: {str(e)[:70]}"
        if rec is None:
            excl[c] = why
        else:
            kept.append(rec)
    results = []
    for rec in kept:
        try:
            results.append(run_case(rec))
        except Exception as e:
            excl[rec["caseid"]] = f"analysis error: {str(e)[:70]}"
    json.dump({"results": results, "excluded": excl},
              open(os.path.join(_H, "..", "results",
                                "vitaldb_confirmatory.json"), "w"), indent=1)
    return report(results, excl, len(ids))


def report(R, excl, n_screened) -> str:
    o, w = [], lambda s: o.append(s)
    w("# VitalDB confirmatory model-adequacy result\n")
    w("Frozen protocol plus the 2026-09-11 amendment. Nothing tuned.\n")
    w(f"\n| | |\n|---|:--:|")
    w(f"| cases screened | {n_screened} |")
    w(f"| admissible | **{len(R)}** |")
    w(f"| required | {MIN_RECORDINGS} |")
    if not R:
        w("\n**No admissible recordings. Stage B and C not evaluated.**\n")
        return "\n".join(o)

    from collections import Counter
    w(f"\n## Exclusions\n\n| reason | n |\n|---|:--:|")
    for r, n in Counter(v.split("(")[0].strip() for v in excl.values()).most_common():
        w(f"| {r} | {n} |")

    sel = np.array([r["best"] == "M-exp" for r in R], float)
    sur = np.array([r["surrogate_sel"] for r in R], float)
    beats_free = np.array([r["exp_beats_free"] for r in R], float)
    rc = np.array([r["rank_corr"] for r in R], float)
    rc = rc[np.isfinite(rc)]

    def ci(v, n=4000, seed=0):
        rng = np.random.default_rng(seed)
        m = [rng.choice(v, len(v), True).mean() for _ in range(n)]
        return float(np.quantile(m, .025)), float(np.quantile(m, .975))

    w("\n## Stage B — model selection\n")
    lo, hi = ci(sel)
    w(f"\n| quantity | value | 95% CI |\n|---|:--:|:--:|")
    w(f"| **M-exp selection rate** | **{sel.mean():.0%}** | [{lo:.0%}, {hi:.0%}] |")
    slo, shi = ci(sur)
    w(f"| surrogate selection rate | {sur.mean():.0%} | [{slo:.0%}, {shi:.0%}] |")
    d = sel - sur
    dlo, dhi = ci(d)
    w(f"| **difference** | **{d.mean():+.0%}** | [{dlo:+.0%}, {dhi:+.0%}] |")
    w(f"| M-exp beats free-rate variant | {beats_free.mean():.0%} | – |")

    w("\n### Held-out error by model (lower is better)\n")
    w("\n| model | median MSE | mean rank | won in |")
    w("|---|:--:|:--:|:--:|")
    M = np.array([[r["mse"][m] for m in MODELS] for r in R])
    ranks = M.argsort(1).argsort(1) + 1
    for j, m in enumerate(MODELS):
        w(f"| {m} | {np.median(M[:,j]):.4g} | {ranks[:,j].mean():.2f} "
          f"| {(M.argmin(1)==j).mean():.0%} |")

    w("\n## Stage C — baseline rates vs trajectory curvature\n")
    if len(rc):
        rlo, rhi = ci(rc)
        w(f"\n| quantity | value | 95% CI |\n|---|:--:|:--:|")
        w(f"| median rank correlation | **{np.median(rc):.2f}** | [{rlo:.2f}, {rhi:.2f}] |")
        w(f"| fraction with corr >= {MIN_RATE_RANKCORR} | {(rc>=MIN_RATE_RANKCORR).mean():.0%} | – |")

    w("\n## Per-subject distribution\n")
    w(f"\n- cases where M-exp won: {int(sel.sum())} of {len(R)}")
    w(f"\n- n_eff across cases: median {np.median([r['n_eff'] for r in R]):.0f}, "
      f"range {min(r['n_eff'] for r in R):.0f}–{max(r['n_eff'] for r in R):.0f}")
    top = np.argsort(-M[:, MODELS.index('M-exp')])[:3]
    w(f"\n- worst 3 cases for M-exp: "
      + ", ".join(f"{R[i]['caseid']} (MSE {M[i,MODELS.index('M-exp')]:.3g})" for i in top))

    w("\n## Verdict\n")
    frac = sel.mean()
    passes = (len(R) >= MIN_RECORDINGS and frac >= ADEQUATE_FRAC
              and dlo > 0 and beats_free.mean() > 0.5
              and len(rc) and np.median(rc) >= MIN_RATE_RANKCORR)
    if len(R) < MIN_RECORDINGS:
        v = "UNRESOLVED — fewer than the required admissible recordings"
    elif frac < NARROW_FRAC or dlo <= 0:
        v = "NOT SUPPORTED — exponential form not preferred, or no advantage over surrogates"
    elif passes:
        v = "SUPPORTED FOR MODEL ADEQUACY"
    else:
        v = "NOT SUPPORTED — one or more frozen gates failed"
    w(f"\n### **{v}**\n")
    return "\n".join(o)


if __name__ == "__main__":
    txt = main()
    with open(os.path.join(_H, "..", "results",
                           "vitaldb_confirmatory.md"), "w") as fh:
        fh.write(txt)
    print(txt)
