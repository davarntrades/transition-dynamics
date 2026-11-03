"""
phase0_sim_checks.py -- reproducibility and verified-metadata checks of the
SYNTHETIC design simulation (analysis/vf/design_sim.py).

Uses only outcome-blind metadata: the verified VF onset elapsed times
(labels, from SDDB headers; analysis/results/vf_phase0_metadata.json) and the
verified rhythm classification. Reads no ECG sample. Every physiological
quantity is still synthetic.

Stages (each saved as it completes):
  repro      exact rerun of the committed `power` stage (same seed) and
             comparison with analysis/results/vf_design_sim.json
  verified   power / MDE / large-effect flag on the verified eligible sets
  sens       sensitivity of power to generative assumptions (verified set A)
  seed       independent-seed replicate of the n=20 step30 MDE region

Usage: python3 analysis/vf/phase0_sim_checks.py --only repro,verified,sens,seed
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import design_sim as ds  # noqa: E402

META = "analysis/results/vf_phase0_metadata.json"
OUT = "analysis/results/vf_phase0_sim_checks.json"
SINUS_OR_INTERMITTENT = {"30", "31", "32", "33", "34", "38", "39", "41", "42",
                         "43", "44", "45", "46", "47", "48", "49", "51", "52"}
AF = {"35", "36", "37", "50"}


def verified_sets() -> dict:
    r = json.load(open(META))
    on = {x["record"]: x["vfon_s"] / 60 for x in r["records"] if x["vfon_s"] is not None}
    sets = {}
    for name, tmin in (("2h20", 140), ("2h50", 170), ("3h", 180), ("4h", 240)):
        a = sorted(k for k, m in on.items() if k in SINUS_OR_INTERMITTENT and m >= tmin)
        b = sorted(k for k, m in on.items() if (k in SINUS_OR_INTERMITTENT or k in AF) and m >= tmin)
        sets[f"A_{name}"] = {"records": a, "Tlist": [int(round(on[k])) for k in a]}
        sets[f"B_{name}"] = {"records": b, "Tlist": [int(round(on[k])) for k in b]}
    return sets


def summarise(studies, deltas=(0.10, 0.15, 0.20)) -> dict:
    reps = len(studies)
    bins = list(ds.BINS)
    pw = {k: sum(st["bins"][k]["pass"] for st in studies) / reps for k in bins}
    rule = 0
    for st in studies:
        sig = [k for k in bins if st["bins"][k]["pass"]]
        rule += len(sig) >= 2 and ("B15" in sig or "B30" in sig)
    return {"reps": reps,
            "power_per_bin": pw,
            "rule_rate_stats_only": rule / reps,
            "mean_delta": {k: float(np.nanmean([st["bins"][k]["mean"] for st in studies])) for k in bins},
            "sd_delta_i": {k: float(np.nanmedian([st["bins"][k]["sd"] for st in studies])) for k in bins},
            "per_bin_type1_or_power_lower_bound_pass": pw,
            "large_excluded_rate_by_delta": {
                str(dl): sum(all(st["bins"][k]["ub95"] < dl for k in bins) for st in studies) / reps
                for dl in deltas}}


def stage_verified(rng, reps):
    out = {}
    sets = verified_sets()
    out["sets"] = sets
    plan = [("A_2h20", "step30", (0.0, 1.0, 1.5, 2.0, 2.5, 3.0)),
            ("A_2h20", "ramp30", (0.0, 2.0, 3.0)),
            ("B_2h20", "step30", (0.0, 2.0, 2.5)),
            ("A_2h50", "step30", (0.0, 2.0, 2.5)),
            ("A_3h", "step30", (0.0, 2.0, 2.5)),
            ("A_4h", "step30", (0.0, 2.0, 2.5))]
    for setname, shape, bs in plan:
        for b in bs:
            sc = {"b": b, "shape": shape, "Tlist": sets[setname]["Tlist"]}
            st = ds.many(rng, sc, len(sc["Tlist"]), reps)
            key = f"{setname}_{shape}_b{b}"
            out[key] = summarise(st)
            print(key, out[key]["power_per_bin"], "rule", out[key]["rule_rate_stats_only"],
                  "mean", {k: round(v, 3) for k, v in out[key]["mean_delta"].items()},
                  "excl", out[key]["large_excluded_rate_by_delta"], flush=True)
    return out


def stage_sens(rng, reps):
    sets = verified_sets()
    T = sets["A_2h20"]["Tlist"]
    out = {}
    grid = {"reference": {}, "phi0.97": {"phi": 0.97}, "het0": {"het": 0.0},
            "het1.0": {"het": 1.0}, "rho0.2": {"rho": 0.2}, "rho0.8": {"rho": 0.8},
            "responders0.5": {"responders": 0.5}, "Tdist_short_n16": None}
    for name, extra in grid.items():
        for b in (0.0, 2.0):
            if extra is None:
                sc = {"b": b, "shape": "step30", "Tdist": "short"}
                st = ds.many(rng, sc, 16, reps)
            else:
                sc = {"b": b, "shape": "step30", "Tlist": T, **extra}
                st = ds.many(rng, sc, len(T), reps)
            key = f"{name}_b{b}"
            out[key] = summarise(st)
            print("sens", key, "rule", out[key]["rule_rate_stats_only"],
                  "mean", {k: round(v, 3) for k, v in out[key]["mean_delta"].items()},
                  "sd", {k: round(v, 3) for k, v in out[key]["sd_delta_i"].items()},
                  "excl", out[key]["large_excluded_rate_by_delta"], flush=True)
    return out


def stage_seed(reps):
    rng = np.random.default_rng(7)
    out = {}
    for b in (1.5, 2.0, 2.5):
        st = ds.many(rng, {"b": b, "shape": "step30"}, 20, reps)
        out[f"n20_step30_b{b}_seed7"] = summarise(st)
        print("seed7", b, out[f"n20_step30_b{b}_seed7"]["rule_rate_stats_only"],
              out[f"n20_step30_b{b}_seed7"]["mean_delta"], flush=True)
    return out


def stage_repro():
    """Exact rerun of design_sim's `power` stage with its default seed."""
    rng = np.random.default_rng(20261103)
    new = ds.exp_power(rng, 200)
    new_s = ds.exp_power(rng, 200, ns=(12, 20), shape="step30")
    old = json.load(open("analysis/results/vf_design_sim.json"))
    same = (json.dumps(new, sort_keys=True, default=float) ==
            json.dumps(old["power"], sort_keys=True, default=float)) and \
           (json.dumps(new_s, sort_keys=True, default=float) ==
            json.dumps(old["power_step30"], sort_keys=True, default=float))
    maxdiff = 0.0
    for o, nw in ((old["power"], new), (old["power_step30"], new_s)):
        for k in o:
            for b in ds.BINS:
                maxdiff = max(maxdiff, abs(o[k]["power_per_bin"][b] - nw[k]["power_per_bin"][b]),
                              abs(o[k]["mean_delta"][b] - nw[k]["mean_delta"][b]))
    print("repro identical:", same, "max abs diff:", maxdiff, flush=True)
    return {"identical_to_committed": bool(same), "max_abs_diff": maxdiff}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="verified,sens,seed,repro")
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--procs", type=int, default=4)
    a = ap.parse_args()
    ds.POOL = mp.get_context("fork").Pool(a.procs)
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    res["meta"] = {"synthetic_only": True, "uses_verified_onset_labels_only": True,
                   "seed_verified_sens": 20261104}

    def save():
        with open(OUT + ".tmp", "w") as f:
            json.dump(res, f, indent=1, default=float)
        os.replace(OUT + ".tmp", OUT)
    rng = np.random.default_rng(20261104)
    todo = a.only.split(",")
    if "verified" in todo:
        res["verified"] = stage_verified(rng, a.reps); save()
    if "sens" in todo:
        res["sensitivity"] = stage_sens(rng, a.reps); save()
    if "seed" in todo:
        res["independent_seed"] = stage_seed(a.reps); save()
    if "repro" in todo:
        res["reproduction"] = stage_repro(); save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
