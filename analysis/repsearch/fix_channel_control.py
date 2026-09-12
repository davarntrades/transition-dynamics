"""
Harness bug 12 fix. The channel-shuffle control in attack_v2.py permuted
feature COLUMNS globally, which is a no-op for a ridge model: reordering
columns leaves the fit identical. It returned numbers bit-identical to the
uncontrolled arm, which is how it was caught.

The meaningful control permutes channel assignment INDEPENDENTLY PER ROW, so
the correspondence between a channel's autocorrelation and that channel's
identity is destroyed while the multiset of AC values in each row is preserved
exactly. It asks: does it matter WHICH channel is autocorrelated, or only how
autocorrelated the signals are in general?
"""
from __future__ import annotations
import json, os, sys, warnings
import numpy as np

_H = os.path.dirname(__file__)
_S = os.path.join(_H, "..", "structural")
sys.path.insert(0, _H); sys.path.insert(0, _S)
warnings.filterwarnings("ignore")
import windows as W, features as F, models as M
from cohort import RESULTS
from run_confirmatory import load_all, cv_scores
import variability as V
from repsearch_dev import build, BSTAR

SEED = 20260911


def main():
    cases, _ = load_all("confirmatory")
    rows, groups, labels, keeps = [], [], [], []
    for c in cases:
        for b, row in zip(build(c, False), c["rows"]):
            b["ac_only"] = b["autocorr"][:V.P]
            b["tau_only"] = b["autocorr"][V.P:]
            rows.append(b); groups.append(c["caseid"])
            labels.append(row["labels"]); keeps.append(row["keep"])
    groups = np.array(groups)
    rng = np.random.default_rng(SEED)
    out = {}
    for Hh in W.HORIZONS:
        hk = f"{Hh//60}min"
        keep = np.array([k[Hh] for k in keeps])
        y = np.array([l[Hh] for l in labels], float)[keep]
        g = groups[keep]
        bl = [b for b, kp in zip(rows, keep) if kp]
        sB, _, _ = cv_scores(F.design(bl, BSTAR), y, g)
        sR, _, _ = cv_scores(F.design(bl, BSTAR + ["autocorr"]), y, g)
        blc = []
        for b in bl:
            d = dict(b)
            p = rng.permutation(V.P)                # a fresh permutation PER ROW
            d["autocorr"] = np.concatenate([b["ac_only"][p], b["tau_only"][p]])
            blc.append(d)
        sC, _, _ = cv_scores(F.design(blc, BSTAR + ["autocorr"]), y, g)
        sc = {"B_star": sB, "V2_real": sR, "V2_rowwise_channel_shuffle": sC}
        _, dp = M.patient_bootstrap(y, g, sc, M.auprc, 2000, SEED)
        _, dr = M.patient_bootstrap(y, g, sc, M.auroc, 2000, SEED)
        rec = {}
        for k in ("V2_real", "V2_rowwise_channel_shuffle"):
            rec[k] = {"dAUPRC": M.paired_delta_ci(dp, k, "B_star"),
                      "dAUROC": M.paired_delta_ci(dr, k, "B_star")}
            a = rec[k]
            print(f"{hk}  {k:<30} dAUPRC {a['dAUPRC'][0]:+.5f} "
                  f"[{a['dAUPRC'][1]:+.5f},{a['dAUPRC'][2]:+.5f}]  "
                  f"dAUROC {a['dAUROC'][0]:+.4f}", flush=True)
        out[hk] = rec
    json.dump(out, open(os.path.join(RESULTS, "rs_channel_control.json"), "w"),
              indent=1, default=float)
    print("-> analysis/results/rs_channel_control.json")


if __name__ == "__main__":
    main()
