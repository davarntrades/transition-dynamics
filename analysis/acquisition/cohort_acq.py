"""
cohort_acq.py -- frozen cohort for the acquisition-discrimination experiment.

THREE DISJOINT SETS
  PILOT   12 development caseids used to specify the beat detector and the
          injection transformation, and to size effects. Outcome-blind.
  TIER1   the remaining development caseids. Tier 1 uses NO outcome
          information, so these patients stay available for Tier 1 even though
          their outcomes were burned by earlier experiments.
  TIER2   600 fresh caseids never used by ANY experiment in this repository.

Eligibility rules are identical to the frozen structural protocol so results
remain directly comparable.
"""
from __future__ import annotations
import csv, json, os

_H = os.path.dirname(__file__)
RESULTS = os.path.join(_H, "..", "results")
DATA = os.path.join(_H, "..", "..", "data", "real", "vitaldb")
N_PILOT, N_TIER2 = 12, 600
MIN_ANE_HOURS = 2.0
PRIOR = ("vitaldb_split.json", "st_split.json", "sd_split.json", "rs_split.json")


def burned():
    used = set()
    for f in PRIOR:
        s = json.load(open(os.path.join(RESULTS, f)))
        for k in ("calibration", "confirmatory", "development"):
            used |= set(s.get(k, []))
    return used


def _dev():
    return sorted(set(json.load(open(os.path.join(RESULTS, "sd_split.json")))
                      ["confirmatory"]))


def fresh_eligible():
    used = burned()
    rows = list(csv.DictReader(open(os.path.join(DATA, "clinical_data.csv"))))
    key = [k for k in rows[0] if k.lstrip("﻿") == "caseid"][0]
    out = []
    for r in rows:
        c = int(r[key])
        if c in used or r["ane_type"] != "General":
            continue
        try:
            a, b = float(r["anestart"]), float(r["aneend"])
        except (TypeError, ValueError):
            continue
        if (b - a) / 3600.0 >= MIN_ANE_HOURS:
            out.append(c)
    return sorted(out)


def split():
    dev = _dev()
    e = fresh_eligible()
    return {"pilot": dev[:N_PILOT], "tier1": dev[N_PILOT:],
            "tier2": e[:N_TIER2], "n_fresh_eligible": len(e)}


if __name__ == "__main__":
    s = split()
    assert not set(s["pilot"]) & set(s["tier1"])
    assert not set(s["tier2"]) & burned()
    assert not set(s["tier2"]) & (set(s["pilot"]) | set(s["tier1"]))
    print(f"burned by previous experiments : {len(burned())}")
    print(f"pilot  (spec, outcome-blind)   : {len(s['pilot'])}  {s['pilot']}")
    print(f"tier1  (development, no outcomes used) : {len(s['tier1'])}")
    print(f"tier2  (fresh, untouched)      : {len(s['tier2'])}  {s['tier2'][:5]} ...")
    print(f"fresh eligible remaining       : {s['n_fresh_eligible']}")
    json.dump(s, open(os.path.join(RESULTS, "acq_split.json"), "w"), indent=1)
    print("-> analysis/results/acq_split.json")
