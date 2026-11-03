"""
calibrate.py -- SYNTHETIC calibration of the repaired decision rule.

Stage 1 (pools): for each scenario, simulate a pool of independent synthetic
patients with the beat-level generator (beatsim.py) and compute every
per-patient statistic the rule needs (true-onset, pseudo-onset,
label-permutation), for two TD composites:
  td3   = protocol TD-1/TD-2/TD-3 composite, nonlinear (poly) M1 residualisation
  shape = correlation-only deformation + its persistence, poly residualisation
Stage 2 (studies): because the repaired per-patient statistics involve no
cross-patient training, studies of any size n can be formed by resampling
patients from the pools. Verdict rates, false-positive rates, power and CI
coverage are estimated from >= 1000 resampled studies per cell.

No real data. No thresholds are tuned: every alpha and the pipeline
positive-control floor are fixed in repaired_rule.py / below, before running.

Usage: python3 analysis/vtvf/calibrate.py [--pool 600] [--studies 1000]
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import beatsim as B  # noqa: E402
import repaired_rule as R  # noqa: E402

OUT = "analysis/results/vtvf_repair_calibration.json"
T_RANGE = (140.0, 1440.0)            # pre-onset minutes, uniform (SDDB-like range)
GAMMA_PC = 0.10                       # injected pipeline positive control
S_PC_FLOOR = 0.13                     # fixed before calibration: ~50% of the pilot E[s | GAMMA_PC]
N_PC = 8                              # injected patients per study
VARIANTS = {"td3": dict(composite="td3", basis_kind="poly"),
            "shape": dict(composite="shape", basis_kind="poly")}

SCENARIOS = {
    "null": {},
    "conventional_only": {"conv_kappa": 1.0},
    "artefact_detected": {"art_rate": 40.0, "art_detect": 1.0},
    "artefact_70pct_detected": {"art_rate": 40.0, "art_detect": 0.7},
    "elapsed_gain_drift": {"gain_drift": 1.5},
    "td_gamma0.05": {"td_gamma": 0.05},
    "td_gamma0.10": {"td_gamma": 0.10},
    "td_gamma0.10_plus_drift": {"td_gamma": 0.10, "gain_drift": 1.5},
    "td_gamma0.10_plus_conventional": {"td_gamma": 0.10, "conv_kappa": 1.0},
    "td_gamma0.05_ramp": {"td_gamma": 0.05, "td_shape": "ramp"},
    "td_gamma0.10_half_responders": {"td_gamma": 0.10, "responders": 0.5},
}
BROKEN = {"label_misaligned_75min": {"td_gamma": GAMMA_PC},   # stats at T-75: labels wrong
          "label_leak_null": {}}                               # leak=+0.3 on bin windows


def _stats_one(args):
    scen, seed, mode = args
    rng = np.random.default_rng(seed)
    T = float(rng.uniform(*T_RANGE))
    sc = SCENARIOS.get(scen, BROKEN.get(scen, {}))
    f = B.window_features(B.generate_patient(rng, T, sc))
    out = {"T": T}
    T_eff = T - 75.0 if scen == "label_misaligned_75min" else T
    leak = 0.3 if scen == "label_leak_null" else 0.0
    for vn, kw in VARIANTS.items():
        true = R.patient_stats(f, T_eff, leak=leak, **kw)
        pseudo = [R.patient_stats(f, To, **kw) for To in R.pseudo_offsets(T_eff)]
        perm = R.patient_stats(f, T_eff, leak=leak, rng=rng, permute=True, **kw)
        out[vn] = {"true": true, "pseudo": pseudo, "perm": perm}
    return scen, out


def build_pools(n_pool: int, procs: int) -> dict:
    jobs = []
    base = 10_000
    for i, s in enumerate(list(SCENARIOS) + list(BROKEN)):
        n = n_pool if s in SCENARIOS else n_pool // 2
        jobs += [(s, base * (i + 1) + j, None) for j in range(n)]
    with mp.get_context("fork").Pool(procs) as p:
        res = p.map(_stats_one, jobs, chunksize=4)
    pools = {}
    for s, o in res:
        pools.setdefault(s, []).append(o)
    return pools


def run_study(rng, pool, pc_pool, n, vn, delta_ex, pc_override=None):
    idx = rng.integers(0, len(pool), size=n)
    pats = [pool[i][vn] for i in idx]
    true = [p["true"] for p in pats]
    pseudo = [p["pseudo"] for p in pats]
    perm = [p["perm"] for p in pats]
    pc = pc_override if pc_override is not None else pc_pool
    pcs = rng.integers(0, len(pc), size=N_PC)
    pc_s = np.nanmean([np.nanmean([pc[i][vn]["true"][b]["s"] for b in ("B10", "B15")]) for i in pcs])
    return R.decide(true, pseudo, perm, bool(pc_s > S_PC_FLOOR), delta_ex), true


def coverage(rng, pool, n, vn, b, reps, truth):
    hit = 0
    for _ in range(reps):
        idx = rng.integers(0, len(pool), size=n)
        x = np.array([pool[i][vn]["true"][b]["s"] for i in idx])
        x = x[np.isfinite(x)]
        m, se = x.mean(), x.std(ddof=1) / np.sqrt(len(x))
        q = R.t_ppf(0.975, len(x) - 1)
        hit += (m - q * se) <= truth <= (m + q * se)
    return hit / reps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", type=int, default=600)
    ap.add_argument("--studies", type=int, default=1000)
    ap.add_argument("--procs", type=int, default=4)
    a = ap.parse_args()
    pools = build_pools(a.pool, a.procs)
    rng = np.random.default_rng(20261105)
    res = {"meta": {"synthetic_only": True, "pool_per_scenario": a.pool, "studies_per_cell": a.studies,
                    "gamma_pc": GAMMA_PC, "s_pc_floor": S_PC_FLOOR, "n_pc": N_PC,
                    "alpha_bin": R.ALPHA_BIN, "alpha_ctrl": R.ALPHA_CTRL, "alpha_pipe": R.ALPHA_PIPE,
                    "T_range": T_RANGE, "scenarios": SCENARIOS, "broken": list(BROKEN)}}
    # per-patient summaries (means / SDs of s) -- the effect-size scale
    res["per_patient"] = {}
    for s, pool in pools.items():
        res["per_patient"][s] = {}
        for vn in VARIANTS:
            arr = np.array([[p[vn]["true"][b]["s"] for b in R.BINS] for p in pool])
            a_ = np.array([[p[vn]["true"][b]["a"] for b in R.BINS] for p in pool])
            ps = np.array([[np.nanmean([q[b]["s"] for q in p[vn]["pseudo"]]) if p[vn]["pseudo"] else np.nan
                            for b in R.BINS] for p in pool])
            res["per_patient"][s][vn] = {
                "s_mean": dict(zip(R.BINS, np.nanmean(arr, 0).round(4).tolist())),
                "s_sd": dict(zip(R.BINS, np.nanstd(arr, 0).round(4).tolist())),
                "acq_mean": dict(zip(R.BINS, np.nanmean(a_, 0).round(4).tolist())),
                "pseudo_s_mean": dict(zip(R.BINS, np.nanmean(ps, 0).round(4).tolist())),
                "frac_with_pseudo": float(np.mean([len(p[vn]["pseudo"]) > 0 for p in pool]))}
    # verdict rates
    res["verdicts"] = {}
    for vn in VARIANTS:
        for delta_ex in (0.10,):
            for n in (16, 20, 40, 80, 150):
                for s, pool in pools.items():
                    if s == "label_misaligned_75min":
                        pc_pool = pool              # the injected control is broken too
                    else:
                        pc_pool = pools["td_gamma0.10"]
                    cnt, flag, pbin = {}, 0, {b: 0 for b in R.BINS}
                    for _ in range(a.studies):
                        d, _t = run_study(rng, pool, pc_pool, n, vn, delta_ex)
                        cnt[d["verdict"]] = cnt.get(d["verdict"], 0) + 1
                        flag += bool(d.get("large_excluded", False))
                        for b in R.BINS:
                            pbin[b] += bool(d.get("bins", {}).get(b, {}).get("primary", False))
                    key = f"{vn}|n{n}|{s}"
                    res["verdicts"][key] = {
                        "rates": {k: v / a.studies for k, v in sorted(cnt.items())},
                        "large_excluded_rate_delta0.10": flag / a.studies,
                        "per_bin_primary_pass_rate": {b: v / a.studies for b, v in pbin.items()}}
                print(vn, n, "done", flush=True)
        # CI coverage of the per-bin 95% t-interval (truth = pool mean)
        for s in ("null", "td_gamma0.05", "td_gamma0.10"):
            pool = pools[s]
            for b in R.BINS:
                truth = float(np.nanmean([p[vn]["true"][b]["s"] for p in pool]))
                for n in (16, 40):
                    res.setdefault("coverage", {})[f"{vn}|{s}|{b}|n{n}"] = coverage(
                        rng, pool, n, vn, b, 2000, truth)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1, default=float)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
