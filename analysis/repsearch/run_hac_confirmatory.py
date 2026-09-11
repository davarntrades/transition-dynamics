"""
run_hac_confirmatory.py -- the ONE-SHOT confirmatory run for H-AC.

Implements docs/PROTOCOL_AUTOCORR.md exactly as frozen at commit 9efe10c.
Written and committed BEFORE any confirmatory patient was accessed.

Binding rule is STRICT. The AUPRC-led reading is computed and reported under
its frozen secondary/provisional label only; it has no advancement authority.

Surrogate lambda convention: the 200-permutation controls reuse the median
lambda chosen by the real run's inner CV, exactly as the structural protocol's
surrogate did. This is the established convention in this programme and changes
no threshold.
"""
from __future__ import annotations
import json, os, sys, time, warnings
import numpy as np

_H = os.path.dirname(__file__)
_S = os.path.join(_H, "..", "structural")
sys.path.insert(0, _H); sys.path.insert(0, _S)
warnings.filterwarnings("ignore")
import windows as W, features as F, models as M
from cohort import RESULTS, SHORT
import run_confirmatory as RC
from run_confirmatory import cv_scores
from run_calibration import case_rows
import blocks as B, variability as V, persistence as PR, fast_ac
from cohort_rs import split as rs_split
from attack_v2 import repeated_frac

N_BOOT = 2000
N_PERM = 200
SEED = 20260911
BSTAR = ["signed", "slope", "disp", "maxz", "aggz", "elapsed", "meanabsz"]
ALPHA_BONF = 0.05 / 3
HK = ("5min", "10min", "15min")
PREDICTED_PASS = ("10min", "15min")
MIN_EVENT_PATIENTS, MIN_PREV = 30, 0.01


def _tau_ac(ac):
    a = np.clip(ac, 1e-3, 0.999)
    return np.where(np.isfinite(ac) & (ac > 0), -W.DT / np.log(a), 0.0)


def load(ids, thresh):
    cases, excl = [], {}
    for c in ids:
        try:
            r, why = case_rows(c, thresh)
        except Exception as e:
            excl[c] = f"error: {type(e).__name__}"; continue
        if r is None:
            excl[c] = why
        elif r["rows"]:
            cases.append(r)
        else:
            excl[c] = "no evaluation points"
    return cases, excl


def assemble(cases):
    rows, groups, labels, keeps, preps = [], [], [], [], []
    for c in cases:
        pf = PR.persistence_features(c["prep"], c["i0"], c["i1"], 1.0, 30)
        ts, ac = fast_ac.ac_grid(c["prep"], c["i0"], c["i1"], False,
                                 hash(c["caseid"]) % 2**31)
        tsr, RF = repeated_frac(c["prep"], c["i0"], c["i1"])
        for row in c["rows"]:
            b = B.base_blocks(row, c["prep"])
            kp = PR.lookup(pf, row["t_idx"])
            if kp is None:
                b["meanabsz"] = np.zeros(V.P)
            else:
                lo = max(0, kp - pf["max_steps"] + 1)
                b["meanabsz"] = np.nan_to_num(
                    np.nanmean(np.abs(pf["Z"][lo:kp + 1]), axis=0), nan=0.0)
            k = np.searchsorted(ts, row["t_idx"], side="right") - 1
            if k < 0:
                b["autocorr"] = np.zeros(2 * V.P)
                b["repfrac"] = np.zeros(V.P)
            else:
                a = np.nan_to_num(ac[k], nan=0.0)
                b["autocorr"] = np.concatenate([a, np.log1p(_tau_ac(ac[k]))])
                b["repfrac"] = np.nan_to_num(RF[k], nan=0.0)
            rows.append(b); groups.append(c["caseid"])
            labels.append(row["labels"]); keeps.append(row["keep"])
        preps.append(c)
    return rows, np.array(groups), labels, keeps


def horizon_slice(rows, groups, labels, keeps, H):
    keep = np.array([k[H] for k in keeps])
    return ([b for b, kp in zip(rows, keep) if kp],
            np.array([l[H] for l in labels], float)[keep], groups[keep])


def main():
    t0 = time.time()
    sp = rs_split()
    ids = sp["confirmatory"]
    report = {"frozen_commit": "9efe10c3c8cc31fd25c871c9ed80b2af89c89b15",
              "n_requested": len(ids), "primary": {}, "secondary_endpoint": {}}

    # ------------------------------------------------- PRIMARY ENDPOINT
    cases, excl = load(ids, W.MAP_THRESH)
    rows, groups, labels, keeps = assemble(cases)
    print(f"usable {len(cases)}/{len(ids)}  windows {len(groups)}", flush=True)
    report["n_usable"] = len(cases)
    report["n_windows"] = int(len(groups))
    report["exclusions"] = RC._tally(excl)

    perm_rng = np.random.default_rng(SEED + 101)
    for H in W.HORIZONS:
        hk = f"{H//60}min"
        bl, y, g = horizon_slice(rows, groups, labels, keeps, H)
        ev = int(len(np.unique(g[y == 1])))
        print(f"\n=== {hk}  n={len(y)} pos={int(y.sum())} prev={y.mean():.4f} "
              f"patients={len(np.unique(g))} event-patients={ev} ===", flush=True)

        XB = F.design(bl, BSTAR)
        XA = F.design(bl, BSTAR + ["autocorr"])
        sB, lamB, pB = cv_scores(XB, y, g)
        sA, lamA, pA = cv_scores(XA, y, g)
        sR, _, pR = cv_scores(F.design(bl, BSTAR + ["repfrac"]), y, g)
        sAR, _, pAR = cv_scores(F.design(bl, BSTAR + ["autocorr", "repfrac"]), y, g)
        lam_fix = float(np.median(lamA))

        sc = {"B_star": sB, "A": sA, "A_plus_repfrac": sAR, "repfrac_only": sR}
        _, dr = M.patient_bootstrap(y, g, sc, M.auroc, N_BOOT, SEED)
        _, dp = M.patient_bootstrap(y, g, sc, M.auprc, N_BOOT, SEED)
        dAUROC = M.paired_delta_ci(dr, "A", "B_star", ALPHA_BONF)
        dAUPRC = M.paired_delta_ci(dp, "A", "B_star", ALPHA_BONF)
        real_dprc = M.auprc(y, sA) - M.auprc(y, sB)
        print(f"  dAUROC {dAUROC[0]:+.4f} [{dAUROC[1]:+.4f},{dAUROC[2]:+.4f}]"
              f"   dAUPRC {dAUPRC[0]:+.5f} [{dAUPRC[1]:+.5f},{dAUPRC[2]:+.5f}]",
              flush=True)

        # ---- control 1: within-window shuffle, 200 permutations
        c1 = []
        for pi in range(N_PERM):
            cols = []
            for c in cases:
                ts, acs = fast_ac.ac_grid(c["prep"], c["i0"], c["i1"], True,
                                          SEED + 1000 * pi + c["caseid"])
                cols.append((c["caseid"], ts, acs))
            book = {cid: (ts, acs) for cid, ts, acs in cols}
            blc = []
            idx = 0
            for c in cases:
                ts, acs = book[c["caseid"]]
                for row in c["rows"]:
                    k = np.searchsorted(ts, row["t_idx"], side="right") - 1
                    blc.append(np.zeros(2 * V.P) if k < 0 else
                               np.concatenate([np.nan_to_num(acs[k], nan=0.0),
                                               np.log1p(_tau_ac(acs[k]))]))
            keep = np.array([k[H] for k in keeps])
            blk = [a for a, kp in zip(blc, keep) if kp]
            Xc = np.hstack([XB, np.array(blk)])
            s, _, _ = cv_scores(Xc, y, g, fixed_lam=lam_fix)
            c1.append(M.auprc(y, s) - M.auprc(y, sB))
            if (pi + 1) % 50 == 0:
                print(f"    control1 {pi+1}/{N_PERM}", flush=True)
        c1 = np.array(c1)

        # ---- control 2: row-wise channel shuffle, 200 permutations
        A_ac = np.array([b["autocorr"] for b in bl])
        c2 = []
        for pi in range(N_PERM):
            out = np.empty_like(A_ac)
            for r in range(A_ac.shape[0]):
                p = perm_rng.permutation(V.P)
                out[r] = np.concatenate([A_ac[r, :V.P][p], A_ac[r, V.P:][p]])
            s, _, _ = cv_scores(np.hstack([XB, out]), y, g, fixed_lam=lam_fix)
            c2.append(M.auprc(y, s) - M.auprc(y, sB))
        c2 = np.array(c2)

        # ---- control 3: repfrac
        d_rep = M.auprc(y, sR) - M.auprc(y, sB)
        d_AR = M.paired_delta_ci(dp, "A_plus_repfrac", "A", ALPHA_BONF) \
            if False else None
        ci_w = dAUPRC[2] - dAUPRC[1]
        d_AR_minus_A = (M.auprc(y, sAR) - M.auprc(y, sA))

        slB, _ = M.calibration_slope(y, pB)
        slA, _ = M.calibration_slope(y, pA)
        rec = {
            "n_rows": int(len(y)), "n_pos": int(y.sum()),
            "prevalence": float(y.mean()),
            "n_patients": int(len(np.unique(g))), "n_event_patients": ev,
            "auroc_B": M.auroc(y, sB), "auroc_A": M.auroc(y, sA),
            "auprc_B": M.auprc(y, sB), "auprc_A": M.auprc(y, sA),
            "dAUROC": dAUROC, "dAUPRC": dAUPRC,
            "brier_B": M.brier(y, pB), "brier_A": M.brier(y, pA),
            "cal_slope_B": slB, "cal_slope_A": slA,
            "sens_far10_B": M.sens_at_far(y, sB, 0.10)[0],
            "sens_far10_A": M.sens_at_far(y, sA, 0.10)[0],
            "lambda_A": [float(x) for x in lamA], "lambda_fixed": lam_fix,
            "control1_within_window": {
                "real": real_dprc, "p95": float(np.percentile(c1, 95)),
                "mean": float(c1.mean()), "n": N_PERM,
                "pass": bool(real_dprc > np.percentile(c1, 95))},
            "control2_channel_rowwise": {
                "real": real_dprc, "p95": float(np.percentile(c2, 95)),
                "mean": float(c2.mean()), "n": N_PERM,
                "pass": bool(real_dprc > np.percentile(c2, 95))},
            "control3_repfrac": {
                "repfrac_only_dAUPRC": d_rep,
                "half_real": 0.5 * real_dprc,
                "A_plus_repfrac_minus_A": d_AR_minus_A,
                "ci_width": ci_w,
                "pass": bool(d_rep < 0.5 * real_dprc and d_AR_minus_A <= ci_w)},
        }
        report["primary"][hk] = rec
        for c in ("control1_within_window", "control2_channel_rowwise",
                  "control3_repfrac"):
            print(f"  {c}: {'PASS' if rec[c]['pass'] else 'FAIL'}", flush=True)

    # ------------------------------------------------- SECONDARY ENDPOINT
    print("\n--- secondary endpoint MAP < 55 ---", flush=True)
    cases2, excl2 = load(ids, W.MAP_SEVERE)
    rows2, groups2, labels2, keeps2 = assemble(cases2)
    for H in W.HORIZONS:
        hk = f"{H//60}min"
        bl, y, g = horizon_slice(rows2, groups2, labels2, keeps2, H)
        ev = int(len(np.unique(g[y == 1])))
        XB = F.design(bl, BSTAR); XA = F.design(bl, BSTAR + ["autocorr"])
        sB, _, _ = cv_scores(XB, y, g); sA, _, _ = cv_scores(XA, y, g)
        sc = {"B_star": sB, "A": sA}
        _, dp = M.patient_bootstrap(y, g, sc, M.auprc, N_BOOT, SEED)
        _, dr = M.patient_bootstrap(y, g, sc, M.auroc, N_BOOT, SEED)
        report["secondary_endpoint"][hk] = {
            "n_pos": int(y.sum()), "prevalence": float(y.mean()),
            "n_event_patients": ev,
            "auprc_B": M.auprc(y, sB), "auprc_A": M.auprc(y, sA),
            "dAUPRC": M.paired_delta_ci(dp, "A", "B_star", ALPHA_BONF),
            "dAUROC": M.paired_delta_ci(dr, "A", "B_star", ALPHA_BONF)}
        r = report["secondary_endpoint"][hk]
        print(f"  {hk} dAUPRC {r['dAUPRC'][0]:+.5f} "
              f"[{r['dAUPRC'][1]:+.5f},{r['dAUPRC'][2]:+.5f}]", flush=True)

    report["elapsed_min"] = (time.time() - t0) / 60
    json.dump(report, open(os.path.join(RESULTS, "hac_confirmatory.json"), "w"),
              indent=1, default=float)
    print(f"\n-> analysis/results/hac_confirmatory.json "
          f"({report['elapsed_min']:.1f} min)")


if __name__ == "__main__":
    main()
