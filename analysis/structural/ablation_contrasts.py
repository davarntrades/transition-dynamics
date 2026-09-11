"""
ablation_contrasts.py -- companion to run_confirmatory.py.

Frozen decision criterion 3 requires patient-specific Sigma_0 to beat BOTH
diagonal and population. The main runner bootstraps every arm against M9 only,
so the two pairwise contrasts it needs are computed here.

Every score is recomputed with the same SEED and the same folds, so the numbers
are identical to the main run by construction -- this adds contrasts, it does
not re-fit anything differently. No threshold is touched.
"""
from __future__ import annotations
import json, os, sys, warnings
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
warnings.filterwarnings("ignore")
import windows as W, features as F, models as M
from cohort import RESULTS
from run_confirmatory import (load_all, assemble, s_columns, cv_scores,
                              fold_dependent_inv, SEED, N_BOOT)


def main(which="confirmatory"):
    rng = np.random.default_rng(SEED)
    cases, _ = load_all(which)
    D = assemble(cases)
    Scols, _ = s_columns(D, rng)
    out = {}
    for H in W.HORIZONS:
        hk = f"{H//60}min"
        keep = np.array([k[H] for k in D["keeps"]])
        y = np.array([lab[H] for lab in D["labels"]], float)[keep]
        g = D["groups"][keep]
        blocks = [b for b, kp in zip(D["blocks"], keep) if kp]
        X9 = F.design(blocks, F.M9)
        sc = {}
        for kind in ("patient", "diagonal"):
            col = np.log1p(Scols[kind]["lit"][keep])
            sc[kind], _, _ = cv_scores(np.hstack([X9, col.reshape(-1, 1)]), y, g)

        def mk(train_ids):
            inv = fold_dependent_inv("population", train_ids, D["Sigma"],
                                     np.random.default_rng(SEED))
            return np.log1p(np.array([F.S_literal(inv[gg], d) for gg, d in
                                      zip(D["groups"][keep], D["delta"][keep])]))
        sc["population"], _, _ = cv_scores(X9, y, g, extra_fn=mk)

        res = {}
        for stat, nm in ((M.auroc, "dAUROC"), (M.auprc, "dAUPRC")):
            _, draws = M.patient_bootstrap(y, g, sc, stat, N_BOOT, SEED)
            for other in ("diagonal", "population"):
                res[f"{nm}_patient_minus_{other}"] = \
                    M.paired_delta_ci(draws, "patient", other)
                res[f"{nm}_patient_minus_{other}_bonf"] = \
                    M.paired_delta_ci(draws, "patient", other, 0.05 / 3)
        out[hk] = res
        print(f"{hk}:")
        for k, v in res.items():
            if "bonf" not in k:
                print(f"  {k:<34} {v[0]:+.5f} [{v[1]:+.5f}, {v[2]:+.5f}]")
    p = os.path.join(RESULTS, f"sd_ablation_contrasts_{which}.json")
    json.dump(out, open(p, "w"), indent=1, default=float)
    print(f"-> {p}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "confirmatory")
