"""
repsearch_dev.py -- representation search over temporal-variability
representations, on DEVELOPMENT patients only (the 166 burned cases).

B* is frozen. Endpoints, horizons, windows, exclusions, splits and metrics are
unchanged from the structural protocol.

Every candidate is paired with a DESTRUCTIVE CONTROL that preserves the
marginal distribution and destroys temporal ordering. The comparison
candidate-vs-control IS the test of

    H0: predictive information is primarily marginal dispersion
    H1: temporal organisation of fluctuations adds information

A candidate earns a temporal interpretation only if destroying the ordering
destroys its incremental information.
"""
from __future__ import annotations
import json, os, sys, time, warnings
import numpy as np

_H = os.path.dirname(__file__)
_S = os.path.join(_H, "..", "structural")
sys.path.insert(0, _H); sys.path.insert(0, _S)
warnings.filterwarnings("ignore")
import windows as W, features as F, models as M
from cohort import RESULTS
from run_confirmatory import load_all, cv_scores
import blocks as B, variability as V, persistence as PR

LOOKBACK_MIN = 30
STEPS = int(LOOKBACK_MIN * 60 / V.STRIDE_S)
BSTAR = ["signed", "slope", "disp", "maxz", "aggz", "elapsed", "meanabsz"]


def _tau_ac(ac):
    a = np.clip(ac, 1e-3, 0.999)
    return np.where(np.isfinite(ac) & (ac > 0), -W.DT / np.log(a), 0.0)


def build(case, shuffled):
    """All candidate blocks for one case, at every retained evaluation point."""
    prep, i0, i1 = case["prep"], case["i0"], case["i1"]
    G = V.grids(prep, i0, i1, shuffle_within_window=shuffled,
                seed=hash(case["caseid"]) % 2**31)
    T = V.temporal_blocks(G, STEPS, shuffle_series=shuffled,
                          seed=hash(case["caseid"]) % 2**31)
    pf = PR.persistence_features(prep, i0, i1, 1.0, LOOKBACK_MIN)
    out = []
    for row in case["rows"]:
        k = np.searchsorted(G["t_idx"], row["t_idx"], side="right") - 1
        b = B.base_blocks(row, prep)
        kp = PR.lookup(pf, row["t_idx"])
        if kp is None:
            b["meanabsz"] = np.zeros(V.P)
        else:
            lo = max(0, kp - pf["max_steps"] + 1)
            b["meanabsz"] = np.nan_to_num(
                np.nanmean(np.abs(pf["Z"][lo:kp + 1]), axis=0), nan=0.0)
        if k < 0:
            z = np.zeros(V.P)
            for key in ("vmarg", "runlen", "autocorr", "dvdt", "accum",
                        "changepoint", "hazard", "spectral"):
                b[key] = np.zeros({"vmarg": 2 * V.P, "spectral": 3 * V.P,
                                   "autocorr": 2 * V.P, "hazard": 2 * V.P,
                                   "runlen": V.P, "dvdt": V.P,
                                   "accum": V.P, "changepoint": V.P}[key])
        else:
            lo = max(0, k - STEPS + 1)
            vw = G["v"][lo:k + 1]
            with np.errstate(invalid="ignore"):
                vmean = np.nan_to_num(np.nanmean(vw, axis=0), nan=0.0)
                vmax = np.nan_to_num(np.nanmax(vw, axis=0), nan=0.0)
            nz = lambda a: np.nan_to_num(a, nan=0.0, posinf=0.0, neginf=0.0)
            b["vmarg"] = np.concatenate([vmean, vmax])
            b["runlen"] = np.log1p(T["run"][k] * (V.STRIDE_S / 60.0))
            b["autocorr"] = np.concatenate([nz(G["ac"][k]),
                                            np.log1p(_tau_ac(G["ac"][k]))])
            b["dvdt"] = nz(T["dv"][k])
            b["accum"] = np.log1p(np.clip(nz(T["acc"][k]), 0, None))
            b["changepoint"] = nz(T["cp"][k])
            b["hazard"] = np.concatenate([nz(T["cross"][k]),
                                          np.log1p(nz(T["since"][k]))])
            b["spectral"] = np.concatenate([nz(G["sef"][k]), nz(G["bpr"][k]),
                                            nz(G["pe"][k])])
        out.append(b)
    return out


CANDIDATES = {
    "V0_vmarg_static":  ["vmarg"],
    "V1_runlength":     ["runlen"],
    "V2_autocorr":      ["autocorr"],
    "V3_dvdt":          ["dvdt"],
    "V4_accum_excess":  ["accum"],
    "V5_changepoint":   ["changepoint"],
    "V6_hazard":        ["hazard"],
    "V7_spectral_entropy": ["spectral"],
    "V8_all_temporal":  ["runlen", "autocorr", "dvdt", "accum",
                         "changepoint", "hazard", "spectral"],
}
SHUFFLE_CONTROLLED = [k for k in CANDIDATES if k != "V0_vmarg_static"]


def main():
    t0 = time.time()
    cases, _ = load_all("confirmatory")
    print(f"development patients {len(cases)}", flush=True)
    real, ctrl, groups, labels, keeps = [], [], [], [], []
    for n, c in enumerate(cases):
        real += build(c, False)
        ctrl += build(c, True)
        for row in c["rows"]:
            groups.append(c["caseid"]); labels.append(row["labels"])
            keeps.append(row["keep"])
        if (n + 1) % 25 == 0:
            print(f"  built {n+1}/{len(cases)}  ({time.time()-t0:.0f}s)",
                  flush=True)
    groups = np.array(groups)
    print(f"feature build done in {(time.time()-t0)/60:.1f} min\n", flush=True)

    out = {}
    for Hh in W.HORIZONS:
        hk = f"{Hh//60}min"
        keep = np.array([k[Hh] for k in keeps])
        y = np.array([l[Hh] for l in labels], float)[keep]
        g = groups[keep]
        br = [b for b, kp in zip(real, keep) if kp]
        bc = [b for b, kp in zip(ctrl, keep) if kp]
        print(f"=== {hk}  n={len(y)} pos={int(y.sum())} prev={y.mean():.4f} ===",
              flush=True)

        sB, _, pB = cv_scores(F.design(br, BSTAR), y, g)
        base = {"auroc": M.auroc(y, sB), "auprc": M.auprc(y, sB),
                "brier": M.brier(y, pB),
                "cal_slope": M.calibration_slope(y, pB)[0],
                "sens@far10": M.sens_at_far(y, sB, 0.10)[0]}
        print(f"  B*{'':<22} AUROC {base['auroc']:.4f}  AUPRC {base['auprc']:.4f}"
              f"  Brier {base['brier']:.4f}  calsl {base['cal_slope']:.2f}",
              flush=True)
        res = {"B_star": base, "candidates": {}}
        for name, ks in CANDIDATES.items():
            Xr = F.design(br, BSTAR + ks)
            sr, _, pr = cv_scores(Xr, y, g)
            rec = {"p_added": Xr.shape[1] - len(F.design(br, BSTAR)[0]),
                   "auroc": M.auroc(y, sr), "auprc": M.auprc(y, sr),
                   "brier": M.brier(y, pr),
                   "cal_slope": M.calibration_slope(y, pr)[0],
                   "sens@far10": M.sens_at_far(y, sr, 0.10)[0]}
            rec["dAUROC"] = rec["auroc"] - base["auroc"]
            rec["dAUPRC"] = rec["auprc"] - base["auprc"]
            if name in SHUFFLE_CONTROLLED:
                Xc = F.design(bc, BSTAR + ks)
                sc, _, _ = cv_scores(Xc, y, g)
                rec["ctrl_auroc"] = M.auroc(y, sc)
                rec["ctrl_auprc"] = M.auprc(y, sc)
                rec["ctrl_dAUROC"] = rec["ctrl_auroc"] - base["auroc"]
                rec["ctrl_dAUPRC"] = rec["ctrl_auprc"] - base["auprc"]
                rec["temporal_gain_AUROC"] = rec["dAUROC"] - rec["ctrl_dAUROC"]
                rec["temporal_gain_AUPRC"] = rec["dAUPRC"] - rec["ctrl_dAUPRC"]
            res["candidates"][name] = rec
            c = rec
            extra = (f"  | ctrl dAUROC {c['ctrl_dAUROC']:+.4f}"
                     f"  temporal gain {c['temporal_gain_AUROC']:+.4f}"
                     if "ctrl_dAUROC" in c else "")
            print(f"  {name:<24} +{c['p_added']:>2}f  dAUROC {c['dAUROC']:+.4f}"
                  f"  dAUPRC {c['dAUPRC']:+.5f}  calsl {c['cal_slope']:.2f}"
                  f"{extra}", flush=True)
        out[hk] = res
        print(flush=True)
    out["elapsed_min"] = (time.time() - t0) / 60
    json.dump(out, open(os.path.join(RESULTS, "rs_repsearch_dev.json"), "w"),
              indent=1, default=float)
    print(f"-> analysis/results/rs_repsearch_dev.json  "
          f"({out['elapsed_min']:.1f} min)")


if __name__ == "__main__":
    main()
