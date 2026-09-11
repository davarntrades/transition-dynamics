"""
attack_v2.py -- adversarial examination of the one candidate with the H1
signature: window autocorrelation.

Questions, in order of how badly they could kill it:
  1. Is the gain distinguishable from zero at all? (patient bootstrap)
  2. Is it a MONITOR ARTEFACT? High lag-1 AC is what a frozen or held signal
     looks like. If AC tracks the fraction of repeated consecutive samples,
     the "temporal organisation" is an instrumentation artefact.
  3. Which half carries it -- raw AC, or the derived tau_AC1?
  4. Does it survive CHANNEL SHUFFLE (channel i's AC attached to channel j)?
  5. Which channels carry it?
  6. Does it survive removing magnitude (rank-transform within patient)?
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
from run_confirmatory import load_all, cv_scores
import blocks as B, variability as V
from repsearch_dev import build, BSTAR, STEPS, _tau_ac

N_BOOT = 2000
SEED = 20260911


def repeated_frac(prep, i0, i1):
    """Per grid point, the fraction of consecutive samples that are identical
    inside the feature window -- a direct monitor-hold / freeze detector."""
    Xi = prep["Xi"]
    step = int(V.STRIDE_S / W.DT); vw = int(V.VAR_WIN_S / W.DT)
    ts = np.arange(prep["b1"] + vw, min(i1, Xi.shape[0]) + 1, step, dtype=int)
    R = np.full((len(ts), V.P), np.nan)
    for k, t in enumerate(ts):
        Wn = Xi[t - vw:t]
        for i in range(V.P):
            c = Wn[:, i]; c = c[np.isfinite(c)]
            if len(c) > 2:
                R[k, i] = float(np.mean(np.diff(c) == 0))
    return ts, R


def main():
    t0 = time.time()
    cases, _ = load_all("confirmatory")
    rows, groups, labels, keeps = [], [], [], []
    acs, reps = [], []
    for c in cases:
        rs = build(c, False)
        G = V.grids(c["prep"], c["i0"], c["i1"], seed=hash(c["caseid"]) % 2**31)
        tsr, RF = repeated_frac(c["prep"], c["i0"], c["i1"])
        for b, row in zip(rs, c["rows"]):
            k = np.searchsorted(G["t_idx"], row["t_idx"], side="right") - 1
            b["ac_only"] = b["autocorr"][:V.P]
            b["tau_only"] = b["autocorr"][V.P:]
            b["repfrac"] = np.nan_to_num(RF[k], nan=0.0) if k >= 0 else np.zeros(V.P)
            acs.append(b["ac_only"]); reps.append(b["repfrac"])
            rows.append(b); groups.append(c["caseid"])
            labels.append(row["labels"]); keeps.append(row["keep"])
    groups = np.array(groups)
    acs = np.array(acs); reps = np.array(reps)
    print(f"built {len(rows)} rows in {(time.time()-t0)/60:.1f} min\n", flush=True)

    # --- 2. monitor-artefact check, before any modelling
    print("MONITOR-ARTEFACT CHECK: corr(lag-1 AC, fraction of repeated samples)")
    art = {}
    for i, ch in enumerate(SHORT):
        a, r = acs[:, i], reps[:, i]
        m = np.isfinite(a) & np.isfinite(r)
        rho = float(np.corrcoef(M._rankdata(a[m]), M._rankdata(r[m]))[0, 1]) \
            if m.sum() > 10 else np.nan
        art[ch] = {"spearman": rho, "mean_repfrac": float(np.nanmean(r))}
        print(f"  {ch:<14} rho={rho:+.3f}   mean repeated-sample fraction="
              f"{np.nanmean(r):.3f}", flush=True)
    print()

    ARMS = {
        "V2_full":        ["autocorr"],
        "V2a_ac_only":    ["ac_only"],
        "V2b_tau_only":   ["tau_only"],
        "V2_plus_repfrac": ["autocorr", "repfrac"],
        "REPFRAC_only":   ["repfrac"],
    }
    out = {"artefact": art, "horizons": {}}
    rng = np.random.default_rng(SEED)
    for Hh in W.HORIZONS:
        hk = f"{Hh//60}min"
        keep = np.array([k[Hh] for k in keeps])
        y = np.array([l[Hh] for l in labels], float)[keep]
        g = groups[keep]
        bl = [b for b, kp in zip(rows, keep) if kp]
        print(f"=== {hk}  n={len(y)} pos={int(y.sum())} ===", flush=True)
        scores = {}
        sB, _, pB = cv_scores(F.design(bl, BSTAR), y, g)
        scores["B_star"] = sB
        for name, ks in ARMS.items():
            s, _, p = cv_scores(F.design(bl, BSTAR + ks), y, g)
            scores[name] = s
        # 4. channel shuffle -- channel i's AC attached to channel j
        perm = rng.permutation(V.P)
        blc = [dict(b) for b in bl]
        for b in blc:
            b["autocorr"] = np.concatenate([b["ac_only"][perm],
                                            b["tau_only"][perm]])
        s, _, _ = cv_scores(F.design(blc, BSTAR + ["autocorr"]), y, g)
        scores["V2_channel_shuffled"] = s
        # 5. per channel
        per_ch = {}
        for i, ch in enumerate(SHORT):
            bi = [dict(b) for b in bl]
            for b in bi:
                b["one"] = np.array([b["ac_only"][i], b["tau_only"][i]])
            s1, _, _ = cv_scores(F.design(bi, BSTAR + ["one"]), y, g)
            per_ch[ch] = {"auroc": M.auroc(y, s1), "auprc": M.auprc(y, s1)}

        ci_roc, dr = M.patient_bootstrap(y, g, scores, M.auroc, N_BOOT, SEED)
        ci_prc, dp = M.patient_bootstrap(y, g, scores, M.auprc, N_BOOT, SEED)
        rec = {"per_channel": per_ch, "arms": {}}
        for k in scores:
            if k == "B_star":
                continue
            rec["arms"][k] = {
                "auroc": ci_roc[k][0], "auprc": ci_prc[k][0],
                "dAUROC": M.paired_delta_ci(dr, k, "B_star"),
                "dAUPRC": M.paired_delta_ci(dp, k, "B_star")}
            a = rec["arms"][k]
            print(f"  {k:<22} dAUROC {a['dAUROC'][0]:+.4f} "
                  f"[{a['dAUROC'][1]:+.4f},{a['dAUROC'][2]:+.4f}]  "
                  f"dAUPRC {a['dAUPRC'][0]:+.5f} "
                  f"[{a['dAUPRC'][1]:+.5f},{a['dAUPRC'][2]:+.5f}]", flush=True)
        rec["B_star"] = {"auroc": ci_roc["B_star"][0], "auprc": ci_prc["B_star"][0]}
        print("  per-channel AUROC: " +
              "  ".join(f"{c}={per_ch[c]['auroc']:.4f}" for c in SHORT), flush=True)
        out["horizons"][hk] = rec
        print(flush=True)
    json.dump(out, open(os.path.join(RESULTS, "rs_attack_v2.json"), "w"),
              indent=1, default=float)
    print(f"-> analysis/results/rs_attack_v2.json ({(time.time()-t0)/60:.1f} min)")


if __name__ == "__main__":
    main()
