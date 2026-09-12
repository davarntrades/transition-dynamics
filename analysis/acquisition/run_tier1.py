"""
run_tier1.py -- Tier 1, measurement-level acquisition identification.

USES NO OUTCOME INFORMATION OF ANY KIND. No labels, no endpoint, no model.

BINDING VERDICT (frozen): ACQUISITION SUFFICIENT (measurement level)
iff T1.1 AND T1.3 pass. T1.2, T1.4, T1.5 are characterisation only and
CANNOT overturn a successful controlled W-vs-W+inj intervention.
"""
from __future__ import annotations
import json, os, sys, time, warnings
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
sys.path.insert(0, os.path.join(_H, "..", "structural"))
warnings.filterwarnings("ignore")
import beats as BT, admissible as AD
import models as M
from cohort_acq import split, RESULTS

WIN_BINS, STRIDE_BINS = 150, 30          # 5 min window, 60 s stride, 2 s grid
HOLDS = (2.0, 4.0, 6.0, 8.0)
QUANTS = (None, 1.0)
PRIMARY = (1.0, 4.0)                      # quant 1 mmHg, hold 4 s
N_BOOT, SEED = 2000, 20260912
MIN_CASES, MIN_WINDOWS = 100, 500
MONITOR_HOLD_FRACTION = 0.560             # measured, frozen
# frozen thresholds
T11_MIN_DAC, T13_MIN_DAC = 0.05, 0.05
T13_MIN_SPEARMAN, T13_SAT_RATIO = 0.60, 2.0
T12_MIN_G, T12_MIN_BASE_GAP = 0.50, 0.05
T14_MAX_ERR, T15_MIN_ABS = 0.05, 0.02


def implied_hold_fraction(hold_s):
    k = int(round(hold_s / BT.BIN_S))
    return 0.0 if k <= 1 else 1.0 - 1.0 / k


def windows_for(rec):
    W, Mo = rec["W"], rec["M"]
    n = min(len(W), len(Mo))
    rows = []
    for st in range(0, n - WIN_BINS, STRIDE_BINS):
        w = W[st:st + WIN_BINS]
        if np.isfinite(w).sum() < 120:
            continue
        r = {"W": BT.lag1(w), "M": BT.lag1(Mo[st:st + WIN_BINS])}
        for q in QUANTS:
            for h in HOLDS:
                r[(q, h)] = BT.lag1(BT.inject(w, q, h))
        if np.isfinite(r["W"]):
            rows.append(r)
    return rows


def _boot(stat, groups, n_boot=N_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    uniq = np.unique(groups)
    idx = {g: np.flatnonzero(groups == g) for g in uniq}
    out = []
    for _ in range(n_boot):
        gs = rng.choice(uniq, size=len(uniq), replace=True)
        sel = np.concatenate([idx[g] for g in gs])
        v = stat(sel)
        if np.isfinite(v):
            out.append(v)
    a = np.array(out)
    return float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))


def main():
    t0 = time.time()
    ids = split()["tier1"]
    rows, groups, excl = [], [], {}
    for i, c in enumerate(ids):
        try:
            AD.extract(c)
            rec, why = AD.load(c)
        except Exception as e:
            excl[c] = f"error: {type(e).__name__}"; continue
        if rec is None:
            excl[c] = why; continue
        ok, why = AD.gate(rec)
        if not ok:
            excl[c] = why; continue
        rs = windows_for(rec)
        rows += rs
        groups += [c] * len(rs)
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(ids)} cases, {len(rows)} windows "
                  f"({time.time()-t0:.0f}s)", flush=True)
    groups = np.array(groups)
    n_cases = len(np.unique(groups))
    print(f"\nusable cases {n_cases}  windows {len(rows)}", flush=True)

    rep = {"n_cases": int(n_cases), "n_windows": len(rows),
           "n_excluded": len(excl), "exclusions": _tally(excl),
           "feasible": bool(n_cases >= MIN_CASES and len(rows) >= MIN_WINDOWS)}
    if not rep["feasible"]:
        rep["verdict"] = "UNRESOLVED (feasibility)"
        _save(rep); return rep

    acW = np.array([r["W"] for r in rows])
    acM = np.array([r["M"] for r in rows])
    cell = {(q, h): np.array([r[(q, h)] for r in rows]) for q in QUANTS for h in HOLDS}

    # ---- T1.1 paired within-window effect, primary cell
    d = cell[PRIMARY] - acW
    med = float(np.nanmedian(d))
    lo, hi = _boot(lambda s: np.nanmedian(d[s]), groups)
    rep["T1_1"] = {"median_dAC": med, "ci": [lo, hi],
                   "frac_positive": float(np.nanmean(d > 0)),
                   "pass": bool(med >= T11_MIN_DAC and lo > 0)}

    # ---- T1.3 saturating shape (binding)
    base = float(np.nanmedian(cell[(1.0, 2.0)]))
    levels, sat = {}, {}
    for h in HOLDS[1:]:
        dh = cell[(1.0, h)] - cell[(1.0, 2.0)]
        m = float(np.nanmedian(dh))
        l, u = _boot(lambda s, dh=dh: np.nanmedian(dh[s]), groups)
        levels[str(h)] = {"median_dAC_vs_2s": m, "ci": [l, u],
                          "pass": bool(m >= T13_MIN_DAC and l > 0)}
    meds = [float(np.nanmedian(cell[(1.0, h)])) for h in HOLDS]
    hf = [implied_hold_fraction(h) for h in HOLDS]
    rho = float(np.corrcoef(M._rankdata(np.array(hf)),
                            M._rankdata(np.array(meds)))[0, 1])
    inc = [meds[i + 1] - meds[i] for i in range(3)]
    sat_ok = bool(inc[0] >= T13_SAT_RATIO * max(inc[1], inc[2], 1e-12))
    rep["T1_3"] = {"levels": levels, "median_by_hold": dict(zip(map(str, HOLDS), meds)),
                   "implied_hold_fraction": hf, "spearman": rho,
                   "increments": inc, "saturation_ok": sat_ok,
                   "pass": bool(all(v["pass"] for v in levels.values())
                                and rho >= T13_MIN_SPEARMAN and sat_ok)}

    # ---- T1.2 gap closure -- CHARACTERISATION ONLY (M is descriptive)
    mW, mM = float(np.nanmedian(acW)), float(np.nanmedian(acM))
    gap = abs(mW - mM)
    if gap < T12_MIN_BASE_GAP:
        rep["T1_2"] = {"status": "NOT EVALUABLE", "base_gap": gap,
                       "binding": False}
    else:
        mI = float(np.nanmedian(cell[PRIMARY]))
        G = 1.0 - abs(mI - mM) / gap
        gl, gh = _boot(lambda s: 1.0 - abs(np.nanmedian(cell[PRIMARY][s])
                                           - np.nanmedian(acM[s]))
                       / max(abs(np.nanmedian(acW[s]) - np.nanmedian(acM[s])), 1e-9),
                       groups)
        rep["T1_2"] = {"median_W": mW, "median_M": mM, "median_Winj": mI,
                       "base_gap": gap, "G": G, "ci": [gl, gh],
                       "meets_threshold": bool(G >= T12_MIN_G and gl > 0),
                       "binding": False}

    # ---- T1.4 dose-response at the monitor's measured hold fraction
    pred = float(np.interp(MONITOR_HOLD_FRACTION, hf, meds))
    rep["T1_4"] = {"predicted_AC_at_monitor_hold_fraction": pred,
                   "observed_median_AC_M": mM, "abs_error": abs(pred - mM),
                   "meets_threshold": bool(abs(pred - mM) <= T14_MAX_ERR),
                   "binding": False}

    # ---- T1.5 quantisation component
    q = {}
    for h in HOLDS:
        dq = cell[(1.0, h)] - cell[(None, h)]
        m = float(np.nanmedian(dq))
        l, u = _boot(lambda s, dq=dq: np.nanmedian(dq[s]), groups)
        q[str(h)] = {"median": m, "ci": [l, u],
                     "contributory": bool(abs(m) >= T15_MIN_ABS and (l > 0 or u < 0))}
    rep["T1_5"] = {"by_hold": q, "binding": False,
                   "verdict": "CONTRIBUTORY" if any(v["contributory"] for v in q.values())
                   else "NON-CONTRIBUTORY"}

    rep["verdict"] = ("ACQUISITION SUFFICIENT (measurement level)"
                      if (rep["T1_1"]["pass"] and rep["T1_3"]["pass"])
                      else "ACQUISITION INSUFFICIENT"
                      if not rep["T1_1"]["pass"] else "UNRESOLVED")
    rep["elapsed_min"] = (time.time() - t0) / 60
    _save(rep)
    print(f"\nT1.1 {rep['T1_1']['pass']}  T1.3 {rep['T1_3']['pass']}"
          f"  ->  {rep['verdict']}")
    return rep


def _tally(e):
    t = {}
    for v in e.values():
        k = v.split(" ")[0] + " " + (v.split(" ")[1] if len(v.split(" ")) > 1 else "")
        t[k.strip()] = t.get(k.strip(), 0) + 1
    return t


def _save(rep):
    p = os.path.join(RESULTS, "acq_tier1.json")
    json.dump(rep, open(p, "w"), indent=1, default=float)
    print(f"-> {p}")


if __name__ == "__main__":
    main()
