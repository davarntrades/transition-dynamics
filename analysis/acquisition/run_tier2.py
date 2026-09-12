"""
run_tier2.py -- Tier 2, predictive attribution. ONE SHOT, fresh cohort only.

Identification rests on W vs W+inj. M is descriptive/reference and appears in
NO binding rule.

Frozen: B*, endpoint MAP<65 for >=60 s, horizons 10 and 15 min, grouped 5-fold
patient CV, Bonferroni alpha = 0.05/2, 2000 patient-level bootstrap.
Feature block = the ABP-only AC pair (rho, tau_AC1), 2 features, added to B*.
"""
from __future__ import annotations
import hashlib, json, os, sys, time, urllib.request, warnings
import numpy as np

_H = os.path.dirname(__file__)
_S = os.path.join(_H, "..", "structural")
_R = os.path.join(_H, "..", "repsearch")
sys.path.insert(0, _H); sys.path.insert(0, _S); sys.path.insert(0, _R)
warnings.filterwarnings("ignore")
import beats as BT, admissible as AD
import windows as W_, features as F, models as M
import persistence as PR
import blocks as B
from run_confirmatory import cv_scores
from run_calibration import case_rows
from cohort_acq import split, RESULTS
from cohort import CHANNELS, PANEL_IDX

BSTAR = ["signed", "slope", "disp", "maxz", "aggz", "elapsed", "meanabsz"]
HORIZONS = (600, 900)                      # 10 and 15 min, primary
ALPHA = 0.05 / 2
N_BOOT, SEED = 2000, 20260912
PRIMARY_INJ = (1.0, 4.0)
MIN_CASES, MIN_EVENT_PATIENTS, MIN_PREV = 150, 30, 0.01


def _tau_ac(ac):
    a = np.clip(ac, 1e-3, 0.999)
    return np.where(np.isfinite(ac) & (ac > 0), -W_.DT / np.log(a), 0.0)


def ac_pair(series, t_bins):
    """(rho, log1p(tau_AC1)) over the 5 min window ending at each t bin."""
    out = np.zeros((len(t_bins), 2))
    for i, tb in enumerate(t_bins):
        lo = tb - 150
        if lo < 0:
            continue
        r = BT.lag1(series[lo:tb])
        if np.isfinite(r):
            out[i] = [r, np.log1p(_tau_ac(np.array([r]))[0])]
    return out


def main():
    t0 = time.time()
    ids = split()["tier2"]
    rep = {"frozen": True, "n_requested": len(ids), "horizons": {}}
    cases, excl = [], {}
    for i, c in enumerate(ids):
        try:
            AD.extract(c)
            rec, why = AD.load(c)
            if rec is None:
                excl[c] = why; continue
            ok, why = AD.gate(rec)
            if not ok:
                excl[c] = why; continue
            r, why2 = case_rows(c)            # frozen structural harness
            if r is None or not r["rows"]:
                excl[c] = why2 or "no evaluation points"; continue
            r["W"], r["Mnum"] = rec["W"], rec["M"]
            cases.append(r)
        except Exception as e:
            excl[c] = f"error: {type(e).__name__}"
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(ids)} ok={len(cases)}", flush=True)
    print(f"usable {len(cases)}/{len(ids)}", flush=True)
    rep["n_usable"] = len(cases)
    rep["exclusions"] = {k: v for k, v in list(excl.items())[:0]} or {}
    rep["n_excluded"] = len(excl)
    if len(cases) < MIN_CASES:
        rep["verdict"] = "UNDERPOWERED (usable ABP cases)"
        json.dump(rep, open(os.path.join(RESULTS, "acq_tier2.json"), "w"),
                  indent=1, default=float)
        return rep

    blocks, groups, labels, keeps, arms = [], [], [], [], {"M": [], "W": [], "Winj": []}
    for c in cases:
        pf = PR.persistence_features(c["prep"], c["i0"], c["i1"], 1.0, 30)
        tb = [int(round(r["t_idx"] * W_.DT / BT.BIN_S)) for r in c["rows"]]
        Winj = BT.inject(c["W"], PRIMARY_INJ[0], PRIMARY_INJ[1])
        pm, pw, pi = (ac_pair(c["Mnum"], tb), ac_pair(c["W"], tb),
                      ac_pair(Winj, tb))
        for j, row in enumerate(c["rows"]):
            b = B.base_blocks(row, c["prep"])
            k = PR.lookup(pf, row["t_idx"])
            if k is None:
                b["meanabsz"] = np.zeros(len(PANEL_IDX))
            else:
                lo = max(0, k - pf["max_steps"] + 1)
                b["meanabsz"] = np.nan_to_num(
                    np.nanmean(np.abs(pf["Z"][lo:k + 1]), axis=0), nan=0.0)
            blocks.append(b); groups.append(c["caseid"])
            labels.append(row["labels"]); keeps.append(row["keep"])
            arms["M"].append(pm[j]); arms["W"].append(pw[j]); arms["Winj"].append(pi[j])
    groups = np.array(groups)
    for k in arms:
        arms[k] = np.nan_to_num(np.array(arms[k]), nan=0.0, posinf=0.0, neginf=0.0)

    for H in HORIZONS:
        hk = f"{H//60}min"
        keep = np.array([kk[H] for kk in keeps])
        y = np.array([l[H] for l in labels], float)[keep]
        g = groups[keep]
        bl = [b for b, kp in zip(blocks, keep) if kp]
        ev = int(len(np.unique(g[y == 1])))
        XB = F.design(bl, BSTAR)
        sc = {}
        sB, _, pB = cv_scores(XB, y, g); sc["B_star"] = sB
        for nm in ("M", "W", "Winj"):
            s, _, _ = cv_scores(np.hstack([XB, arms[nm][keep]]), y, g)
            sc[nm] = s
        _, dp = M.patient_bootstrap(y, g, sc, M.auprc, N_BOOT, SEED)
        _, dr = M.patient_bootstrap(y, g, sc, M.auroc, N_BOOT, SEED)
        rec = {"n_rows": int(len(y)), "n_pos": int(y.sum()),
               "prevalence": float(y.mean()), "n_event_patients": ev,
               "powered": bool(ev >= MIN_EVENT_PATIENTS and y.mean() >= MIN_PREV)}
        for nm in ("M", "W", "Winj"):
            rec[f"dAUPRC_{nm}"] = M.paired_delta_ci(dp, nm, "B_star", ALPHA)
            rec[f"dAUROC_{nm}"] = M.paired_delta_ci(dr, nm, "B_star", ALPHA)
        rec["paired_Winj_minus_W_AUPRC"] = M.paired_delta_ci(dp, "Winj", "W", ALPHA)
        rep["horizons"][hk] = rec
        print(f"  {hk} dAUPRC W {rec['dAUPRC_W'][0]:+.5f} "
              f"Winj {rec['dAUPRC_Winj'][0]:+.5f} "
              f"paired {rec['paired_Winj_minus_W_AUPRC'][0]:+.5f}", flush=True)

    rep["verdict"] = decide(rep)
    rep["elapsed_min"] = (time.time() - t0) / 60
    json.dump(rep, open(os.path.join(RESULTS, "acq_tier2.json"), "w"),
              indent=1, default=float)
    print(f"\nVERDICT: {rep['verdict']}")
    return rep


def decide(rep):
    hs = ["10min", "15min"]
    h = rep["horizons"]
    if not all(h[k]["powered"] for k in hs):
        return "UNDERPOWERED"
    W_null = all(h[k]["dAUPRC_W"][1] <= 0 <= h[k]["dAUPRC_W"][2] for k in hs)
    W_pos = all(h[k]["dAUPRC_W"][1] > 0 for k in hs)
    inj_pos = all(h[k]["dAUPRC_Winj"][1] > 0 for k in hs)
    pair_pos = all(h[k]["paired_Winj_minus_W_AUPRC"][1] > 0 for k in hs)
    pair_neg = all(h[k]["paired_Winj_minus_W_AUPRC"][2] < 0 for k in hs)
    none_pos = all(h[k][f"dAUPRC_{n}"][1] <= 0 <= h[k][f"dAUPRC_{n}"][2]
                   for k in hs for n in ("M", "W", "Winj"))
    if W_null and inj_pos and pair_pos:
        return "H_instr SUPPORTED for the arterial predictive pathway"
    if W_pos and pair_neg:
        return "NEITHER MODEL ADEQUATE"
    if W_pos and pair_pos:
        return "UNRESOLVED (additive contributions)"
    if W_pos and not pair_pos:
        return ("H_instr not sufficient to explain the arterial predictive "
                "increment; the signal survives removal of the tested "
                "hold/quantisation process")
    if none_pos:
        return "PREDICTIVE ATTRIBUTION UNRESOLVED (no arm shows an increment)"
    return "UNRESOLVED"


if __name__ == "__main__":
    main()
