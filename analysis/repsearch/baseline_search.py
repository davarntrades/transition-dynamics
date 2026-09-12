"""
baseline_search.py -- establish the strongest MARGINALS-ONLY baseline on
DEVELOPMENT patients only, and record which features carry the signal.

Development pool = the 166 usable cases of the completed structural experiment.
Those patients are already burned; representation search is exactly what they
are for. The confirmatory set for the new experiment is fresh and untouched.

No new representation is tested here. This only picks the comparator.
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
import blocks as B


def assemble_dev():
    cases, _ = load_all("confirmatory")
    rows, groups, labels, keeps = [], [], [], []
    for r in cases:
        for row in r["rows"]:
            rows.append(B.base_blocks(row, r["prep"]))
            groups.append(r["caseid"]); labels.append(row["labels"])
            keeps.append(row["keep"])
    return rows, np.array(groups), labels, keeps, cases


def main():
    rows, groups, labels, keeps, cases = assemble_dev()
    print(f"development patients {len(set(groups))} · windows {len(groups)}\n")
    out = {}
    for H in W.HORIZONS:
        hk = f"{H//60}min"
        keep = np.array([k[H] for k in keeps])
        y = np.array([l[H] for l in labels], float)[keep]
        g = groups[keep]
        bl = [b for b, kp in zip(rows, keep) if kp]
        print(f"=== {hk}  n={len(y)} pos={int(y.sum())} "
              f"prev={y.mean():.4f} ===", flush=True)

        res = {"single_block": {}, "leave_one_out": {}, "candidates": {}}

        # 1 -- each M9 block alone
        for blk in sorted(set(B.M9)):
            s, _, _ = cv_scores(F.design(bl, [blk]), y, g)
            res["single_block"][blk] = {"auroc": M.auroc(y, s),
                                        "auprc": M.auprc(y, s),
                                        "p": B.BLOCK_WIDTH[blk]}
        # 2 -- leave one block out of M9
        s_full, _, _ = cv_scores(F.design(bl, B.M9), y, g)
        full = M.auroc(y, s_full)
        res["M9_auroc"] = full
        for blk in sorted(set(B.M9)):
            ks = [k for k in B.M9 if k != blk]
            s, _, _ = cv_scores(F.design(bl, ks), y, g)
            res["leave_one_out"][blk] = {"auroc": M.auroc(y, s),
                                         "drop": full - M.auroc(y, s)}
        # 3 -- candidate baselines
        for name, ks in B.CANDIDATE_BASELINES.items():
            X = F.design(bl, ks)
            s, lam, praw = cv_scores(X, y, g)
            sl, ic = M.calibration_slope(y, praw)
            res["candidates"][name] = {
                "auroc": M.auroc(y, s), "auprc": M.auprc(y, s),
                "brier": M.brier(y, praw), "cal_slope": sl,
                "sens@far10": M.sens_at_far(y, s, 0.10)[0],
                "p": X.shape[1], "lambda": [float(x) for x in lam]}
            c = res["candidates"][name]
            print(f"  {name:<24} p={c['p']:>3}  AUROC {c['auroc']:.4f}  "
                  f"AUPRC {c['auprc']:.4f}  Brier {c['brier']:.4f}  "
                  f"calslope {c['cal_slope']:.2f}", flush=True)
        out[hk] = res
        print()
    json.dump(out, open(os.path.join(RESULTS, "rs_baseline_search.json"), "w"),
              indent=1, default=float)
    print("-> analysis/results/rs_baseline_search.json")


if __name__ == "__main__":
    main()
