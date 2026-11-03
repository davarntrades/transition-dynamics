"""
suite.py -- Phase-1 synthetic falsification suite and estimator comparison.

PRE-SPECIFIED (written before the first run of this file):

Seed sets
  selection : seed base 1_000_000 -- used to apply the admissibility criteria
  holdout   : seed base 2_000_000 -- independent replication, plus holdout-only
              scenario variants never used for selection

Statistics compared (all through the same repaired per-patient rule)
  pshape_hp (leakage-repaired candidate), shape_hp, shape_raw (run-2 choice),
  td3 (original combined estimator), dG_hp, corrFrob_hp, meanabsr_hp,
  logdet_hp, diagAIRM_hp, covFrob_hp, and conventional baselines conv_hr,
  conv_sdnn (unadjusted). Adjustment basis lin_dur_clip for all TD statistics.

Admissibility criteria (selection set; n = 80 resampled studies)
  A1  every null-family scenario: EXPLORATORY <= 1% and any positive
      structure-specific verdict <= 2%
  A2  every conventional-only scenario: any positive <= 2%
  A3  near-onset artefact (70% detected) and near-onset gaps: any positive <= 2%
  A4  95% t-interval coverage of the per-bin mean in [0.93, 0.97] (null, corr0.10)
Selection rule
  Among statistics meeting A1-A4, the provisional primary is the one whose
  DEFINITION matches the structure-specific hypothesis (multichannel
  structure beyond HR/HRV), not the one with the highest power. Power across
  precursor TYPES is reported for every admissible statistic. The holdout set
  re-evaluates A1-A4 and power; any admissibility failure in holdout
  invalidates the provisional choice.

SYNTHETIC ONLY. No real data.
Run: python3 analysis/vtvf/suite.py [--pool 400] [--studies 500]
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import pickle
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import beatsim2 as B  # noqa: E402
import repaired_rule2 as R  # noqa: E402

OUT = "analysis/results/vtvf_falsification_suite.json"
STATS = ["pshape_hp", "shape_hp", "shape_raw", "td3", "dG_hp", "corrFrob_hp", "meanabsr_hp",
         "logdet_hp", "diagAIRM_hp", "covFrob_hp", "conv_hr", "conv_sdnn"]
BASIS = "lin_dur_clip"
POSITIVE = ("EXPLORATORY_ASSOCIATION", "SINGLE_BIN_LONG_LEAD", "TRIGGER_PROXIMAL")

FAMILY = {
    # null family
    "null": ("null", {}), "null_homogeneous": ("null", {"het_patients": False}),
    "null_missing": ("null", {"gap_rate": 0.5}),
    "null_artefact": ("null", {"art_base": 4.0, "art_detect": 0.9}),
    "null_nn_artefact": ("null", {"nn_art_rate": 10.0, "nn_detect": 0.9}),
    "null_wander": ("null", {"wander": 1.0}),
    "null_gain_drift": ("null", {"gain_drift": 1.5}),
    # conventional-only
    "conv_hr2": ("conventional", {"conv_kappa": 2.0}),
    "conv_hrv50": ("conventional", {"conv_hrv": 0.5}),
    "conv_hr2_hrv50_rt0.6": ("conventional", {"conv_kappa": 2.0, "conv_hrv": 0.5, "rt_coupling": 0.6}),
    # near-onset acquisition problems
    "artefact_onset_70pct": ("acquisition", {"art_rate": 40.0, "art_detect": 0.7}),
    "gaps_near_onset": ("acquisition", {"gap_near_onset": 3.0}),
    # positive: precursor types and complications
    "corr0.05": ("positive", {"gamma": 0.05}),
    "corr0.10": ("positive", {"gamma": 0.10}),
    "corr0.10_het1.0": ("positive", {"gamma": 0.10, "het": 1.0}),
    "corr0.10_half_responders": ("positive", {"gamma": 0.10, "responders": 0.5}),
    "corr0.10_gain_drift": ("positive", {"gamma": 0.10, "gain_drift": 1.5}),
    "corr0.10_missing": ("positive", {"gamma": 0.10, "gap_rate": 0.5}),
    "corr0.10_artefact70": ("positive", {"gamma": 0.10, "art_rate": 40.0, "art_detect": 0.7}),
    "var0.5": ("positive", {"gamma": 0.5, "ptype": "var"}),
    "mean0.5": ("positive", {"gamma": 0.5, "ptype": "mean"}),
    "intermittent_corr0.15": ("positive", {"gamma": 0.15, "ptype": "intermittent_corr"}),
    "corr0.10_VF_only": ("subgroup", {"gamma": 0.10, "effect_class": "VF", "p_vf": 0.3}),
}
HOLDOUT_ONLY = {
    "null_slow_dynamics": ("null", {"phi_min": 0.98}),
    "conv_hr2_hrv50_rt0": ("conventional", {"conv_kappa": 2.0, "conv_hrv": 0.5, "rt_coupling": 0.0}),
    "nncorr0.15": ("positive", {"gamma": 0.15, "ptype": "nncorr"}),
    "corr0.10_VF_only_pvf0.6": ("subgroup", {"gamma": 0.10, "effect_class": "VF", "p_vf": 0.6}),
}


def _one(args):
    scen, sc, seed = args
    rng = np.random.default_rng(seed)
    T = float(rng.uniform(140, 1440))
    f = B.window_features(B.generate(rng, T, sc))
    offs = R.pseudo_offsets(T)
    out = {}
    for st in STATS:
        out[st] = {"true": R.patient_stats2(f, T, st, basis_kind=BASIS),
                   "pseudo": [R.patient_stats2(f, To, st, basis_kind=BASIS) for To in offs],
                   "perm": R.patient_stats2(f, T, st, basis_kind=BASIS, rng=rng, permute=True)}
    return scen, out


def build(seed_base, scen_map, pool, procs):
    jobs = []
    for i, (s, (_, sc)) in enumerate(scen_map.items()):
        jobs += [(s, sc, seed_base + 10_000 * i + j) for j in range(pool)]
    with mp.get_context("fork").Pool(procs) as p:
        res = p.map(_one, jobs, chunksize=4)
    pools = {}
    for s, o in res:
        pools.setdefault(s, []).append(o)
    return pools


def _eval_cell(args):
    pool, st, n, studies, seed, subgroup = args
    rng = np.random.default_rng(seed)
    cnt, lx, sg_flag, sg_pos = {}, 0, 0, 0
    for _ in range(studies):
        idx = rng.integers(0, len(pool), n)
        tr = [pool[i][st]["true"] for i in idx]
        d = R.decide(tr, [pool[i][st]["pseudo"] for i in idx], [pool[i][st]["perm"] for i in idx],
                     True, 0.10)
        cnt[d["verdict"]] = cnt.get(d["verdict"], 0) + 1
        lx += bool(d.get("large_excluded", False))
        if subgroup and d["verdict"] in POSITIVE:
            sg_pos += 1
            rep = R.subgroup_report(tr)
            sg_flag += any(rep[b]["driven_by_one_class"] for b in R.BINS)
    rates = {k: v / studies for k, v in cnt.items()}
    return {"rates": rates, "any_positive": sum(rates.get(k, 0) for k in POSITIVE),
            "exploratory": rates.get("EXPLORATORY_ASSOCIATION", 0.0),
            "large_excluded_0.10": lx / studies,
            "subgroup_flag_among_positive": (sg_flag / sg_pos) if sg_pos else None}


def coverage(pool, st, n, reps, rng):
    out = {}
    for b in R.BINS:
        allv = np.array([p[st]["true"][b]["s"] for p in pool]); truth = np.nanmean(allv)
        hit = 0
        for _ in range(reps):
            x = allv[rng.integers(0, len(allv), n)]; x = x[np.isfinite(x)]
            m, se = x.mean(), x.std(ddof=1) / np.sqrt(len(x)); q = R.one_sided_t  # noqa
            from scipy.stats import t as T
            hit += abs(m - truth) <= T.ppf(0.975, len(x) - 1) * se
        out[b] = hit / reps
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", type=int, default=400)
    ap.add_argument("--studies", type=int, default=500)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--cache", default="")
    a = ap.parse_args()
    sets = {"selection": (1_000_000, FAMILY), "holdout": (2_000_000, {**FAMILY, **HOLDOUT_ONLY})}
    pools = {}
    if a.cache and os.path.exists(a.cache):
        pools = pickle.load(open(a.cache, "rb"))
    for name, (base, smap) in sets.items():
        if name not in pools:
            pools[name] = build(base, smap, a.pool, a.procs)
            if a.cache:
                pickle.dump(pools, open(a.cache, "wb"))
    res = {"meta": {"synthetic_only": True, "pool": a.pool, "studies": a.studies, "basis": BASIS,
                    "stats": STATS, "families": {k: v[0] for k, v in {**FAMILY, **HOLDOUT_ONLY}.items()},
                    "scenarios": {k: v[1] for k, v in {**FAMILY, **HOLDOUT_ONLY}.items()}}}
    # per-patient means
    res["per_patient"] = {}
    for name, pp in pools.items():
        for s, pool in pp.items():
            for st in STATS:
                arr = np.array([[p[st]["true"][b]["s"] for b in R.BINS] for p in pool])
                res["per_patient"][f"{name}|{s}|{st}"] = {
                    "mean": dict(zip(R.BINS, np.nanmean(arr, 0).round(4).tolist())),
                    "se": dict(zip(R.BINS, (np.nanstd(arr, 0) / np.sqrt(np.isfinite(arr).sum(0))).round(4).tolist()))}
    # study-level cells, parallel
    cells, keys = [], []
    k = 0
    for name, pp in pools.items():
        smap = sets[name][1]
        for s, pool in pp.items():
            for st in STATS:
                for n in (40, 80):
                    k += 1
                    cells.append((pool, st, n, a.studies, 7_000_000 + k, smap[s][0] == "subgroup"))
                    keys.append(f"{name}|{s}|{st}|n{n}")
    with mp.get_context("fork").Pool(a.procs) as p:
        out = p.map(_eval_cell, cells, chunksize=2)
    res["studies"] = dict(zip(keys, out))
    rng = np.random.default_rng(11)
    res["coverage_n40"] = {}
    for name in pools:
        for s in ("null", "corr0.10"):
            for st in STATS:
                res["coverage_n40"][f"{name}|{s}|{st}"] = coverage(pools[name][s], st, 40, 1000, rng)
    # admissibility (A1-A4) per set
    adm = {}
    for name in pools:
        smap = sets[name][1]
        for st in STATS:
            fails = []
            for s, (fam, _) in smap.items():
                c = res["studies"][f"{name}|{s}|{st}|n80"]
                if fam == "null" and (c["exploratory"] > 0.01 or c["any_positive"] > 0.02):
                    fails.append(f"A1:{s}")
                if fam in ("conventional", "acquisition") and c["any_positive"] > 0.02:
                    fails.append(f"{'A2' if fam == 'conventional' else 'A3'}:{s}")
            for s in ("null", "corr0.10"):
                cv = res["coverage_n40"][f"{name}|{s}|{st}"]
                if any(not (0.93 <= v <= 0.97) for v in cv.values()):
                    fails.append(f"A4:{s}")
            adm[f"{name}|{st}"] = {"admissible": not fails, "failures": fails}
    res["admissibility"] = adm
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1, default=float)
    print("wrote", OUT)
    for k2, v in adm.items():
        print(k2, v)


if __name__ == "__main__":
    main()
