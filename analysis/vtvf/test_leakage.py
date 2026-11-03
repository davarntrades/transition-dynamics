"""
test_leakage.py -- regression tests: heart-rate / HRV changes ALONE must not
produce a spurious structure-specific positive verdict (synthetic, tested
conditions only).

Criteria fixed BEFORE the first run of this file (they are not tuned):
  T1  per-patient mean s of the candidate statistic, per bin, within +/-0.04
      of zero under every conventional-only scenario (pool of 1200 patients
      in run 2; SE of a bin mean ~0.008);
  T2  resampled n = 80 studies: rate of ANY positive structure-specific
      verdict (EXPLORATORY_ASSOCIATION, SINGLE_BIN_LONG_LEAD, TRIGGER_PROXIMAL)
      <= 0.02 under every conventional-only scenario;
  T3  the same statistic still detects a genuine structural change
      (gamma = 0.10 correlation precursor): pooled mean s >= 0.15 and
      EXPLORATORY_ASSOCIATION rate at n = 80 >= 0.80;
  T4  the null scenario itself satisfies T1 and T2 (sanity).
Run history (kept, not overwritten):
  run 1 (POOL = 300): FAILED T1/T2 for hrv_drop_30pct (bin means up to +0.051,
  any-positive 6.5%), while hrv_drop_50pct passed. Diagnosis with three
  independent 600-patient pools showed hrv 0.3 means of -0.011..+0.022 versus
  null pools of -0.005..+0.034, i.e. a pool-level fluctuation of the test, not
  a leak (results: analysis/results/vtvf_leakage_tests_run1.json).
  run 2: criteria UNCHANGED; precision increased to POOL = 1200 per scenario.
  The run-1 patients (same seeds) are a subset of the run-2 pool, so the
  failing evidence is retained, not discarded.

A FAILURE of the unrepaired statistics is also asserted (negative control of
the test itself): shape_hp (no NN conditioning) must violate T1 under HRV
reduction with RT-RR coupling, otherwise the test lacks power to see leakage.

Run:  python3 analysis/vtvf/test_leakage.py        (exit code 0 = all pass)
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import beatsim2 as B  # noqa: E402
import repaired_rule2 as R  # noqa: E402

CANDIDATE, BASIS = "pshape_hp", "lin_dur_clip"
POOL, STUDIES, N = 1200, 400, 80
CONV = {
    "hr_rise_1sd": {"conv_kappa": 1.0},
    "hr_rise_3sd": {"conv_kappa": 3.0},
    "hrv_drop_30pct": {"conv_hrv": 0.3},
    "hrv_drop_50pct": {"conv_hrv": 0.5},
    "hr2_hrv50": {"conv_kappa": 2.0, "conv_hrv": 0.5},
    "hr2_hrv50_rt0.6": {"conv_kappa": 2.0, "conv_hrv": 0.5, "rt_coupling": 0.6},
    "hr2_hrv50_rt0": {"conv_kappa": 2.0, "conv_hrv": 0.5, "rt_coupling": 0.0},
}
OTHER = {"null": {}, "structural_gamma0.10": {"gamma": 0.10}}
POSITIVE = ("EXPLORATORY_ASSOCIATION", "SINGLE_BIN_LONG_LEAD", "TRIGGER_PROXIMAL")


def _one(args):
    name, seed = args
    sc = {**CONV, **OTHER}[name]
    rng = np.random.default_rng(seed)
    T = float(rng.uniform(300, 1200))
    f = B.window_features(B.generate(rng, T, sc))
    out = {}
    for stat, bk in ((CANDIDATE, BASIS), ("shape_hp", BASIS)):
        out[stat] = {"true": R.patient_stats2(f, T, stat, basis_kind=bk),
                     "pseudo": [R.patient_stats2(f, To, stat, basis_kind=bk) for To in R.pseudo_offsets(T)],
                     "perm": R.patient_stats2(f, T, stat, basis_kind=bk, rng=rng, permute=True)}
    return name, out


def main() -> int:
    names = list(CONV) + list(OTHER)
    jobs = [(n, 500_000 + 10_000 * i + j) for i, n in enumerate(names) for j in range(POOL)]
    with mp.get_context("fork").Pool(4) as p:
        res = p.map(_one, jobs, chunksize=4)
    pools = {n: [o for m, o in res if m == n] for n in names}
    rng = np.random.default_rng(42)
    report, ok = {}, True

    def study_rates(pool, stat, n=N):
        cnt = {}
        for _ in range(STUDIES):
            idx = rng.integers(0, len(pool), n)
            d = R.decide([pool[i][stat]["true"] for i in idx], [pool[i][stat]["pseudo"] for i in idx],
                         [pool[i][stat]["perm"] for i in idx], True, 0.10)
            cnt[d["verdict"]] = cnt.get(d["verdict"], 0) + 1
        return {k: v / STUDIES for k, v in cnt.items()}

    for n in names:
        pool = pools[n]
        means = {b: float(np.nanmean([p[CANDIDATE]["true"][b]["s"] for p in pool])) for b in R.BINS}
        rates = study_rates(pool, CANDIDATE)
        pos = sum(rates.get(k, 0) for k in POSITIVE)
        rec = {"bin_means": means, "verdict_rates_n80": rates, "any_positive_n80": pos}
        if n in CONV or n == "null":
            t1 = all(abs(m) <= 0.04 for m in means.values())
            t2 = pos <= 0.02
            rec.update(T1=t1, T2=t2); ok &= t1 and t2
        else:
            t3 = np.mean(list(means.values())) >= 0.15 and rates.get("EXPLORATORY_ASSOCIATION", 0) >= 0.80
            rec.update(T3=bool(t3)); ok &= bool(t3)
        report[n] = rec
        print(n, json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in rec.items()
                             if k != "verdict_rates_n80"}), flush=True)
    # negative control of the test: unrepaired statistic must show leakage
    ctrl = {b: float(np.nanmean([p["shape_hp"]["true"][b]["s"] for p in pools["hr2_hrv50_rt0.6"]]))
            for b in R.BINS}
    sees_leak = any(abs(m) > 0.04 for m in ctrl.values())
    report["test_power_check_shape_hp_hr2_hrv50_rt0.6"] = {"bin_means": ctrl, "leak_detected": sees_leak}
    print("test power check (shape_hp must leak):", sees_leak, {b: round(v, 3) for b, v in ctrl.items()})
    ok &= sees_leak
    report["ALL_PASS"] = bool(ok)
    with open("analysis/results/vtvf_leakage_tests.json", "w") as f:
        json.dump(report, f, indent=1)
    print("ALL_PASS", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
