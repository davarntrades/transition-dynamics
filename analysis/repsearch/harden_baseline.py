"""
harden_baseline.py -- one more strengthening pass before freezing B*.

Mean |z| over the same 30 min lookback that persistence uses is a purely
MARGINAL quantity: per channel, no run structure, no cross-channel term. It is
also the most obvious alternative explanation for any persistence effect
("this channel has been displaced a lot lately"). It therefore belongs in the
COMPARATOR, not in a separate control arm. Putting it there is the conservative
choice and makes the persistence test strictly harder.
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
import blocks as B, persistence as PR

LOOKBACK_MIN = 30


def main():
    cases, _ = load_all("confirmatory")
    rows, groups, labels, keeps = [], [], [], []
    for r in cases:
        pf = PR.persistence_features(r["prep"], r["i0"], r["i1"], 1.0, LOOKBACK_MIN)
        steps = pf["max_steps"]
        for row in r["rows"]:
            k = PR.lookup(pf, row["t_idx"])
            b = B.base_blocks(row, r["prep"])
            if k is None:
                b["meanabsz"] = np.zeros(PR.P)
            else:
                lo = max(0, k - steps + 1)
                wnd = np.abs(pf["Z"][lo:k + 1])
                with np.errstate(invalid="ignore"):
                    b["meanabsz"] = np.nan_to_num(np.nanmean(wnd, axis=0), nan=0.0)
            rows.append(b); groups.append(r["caseid"])
            labels.append(row["labels"]); keeps.append(row["keep"])
    groups = np.array(groups)
    BSTAR = ["signed", "slope", "disp", "maxz", "aggz", "elapsed"]
    out = {}
    for H in W.HORIZONS:
        hk = f"{H//60}min"
        keep = np.array([k[H] for k in keeps])
        y = np.array([l[H] for l in labels], float)[keep]
        g = groups[keep]
        bl = [b for b, kp in zip(rows, keep) if kp]
        row = {}
        for name, ks in (("B8_compact_elapsed", BSTAR),
                         ("B11_plus_meanabsz", BSTAR + ["meanabsz"])):
            X = F.design(bl, ks)
            s, lam, praw = cv_scores(X, y, g)
            sl, _ = M.calibration_slope(y, praw)
            row[name] = {"auroc": M.auroc(y, s), "auprc": M.auprc(y, s),
                         "brier": M.brier(y, praw), "cal_slope": sl,
                         "p": X.shape[1]}
            c = row[name]
            print(f"{hk}  {name:<22} p={c['p']:>3} AUROC {c['auroc']:.4f} "
                  f"AUPRC {c['auprc']:.4f} Brier {c['brier']:.4f} "
                  f"calsl {c['cal_slope']:.2f}", flush=True)
        out[hk] = row
    json.dump(out, open(os.path.join(RESULTS, "rs_harden_baseline.json"), "w"),
              indent=1, default=float)
    print("-> analysis/results/rs_harden_baseline.json")


if __name__ == "__main__":
    main()
