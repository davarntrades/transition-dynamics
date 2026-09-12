"""
cohort_rs.py -- frozen cohort for the representation search.

DEVELOPMENT POOL -- already burned, and that is what it is for
    The 480 cases of the structural-displacement experiment (80 calibration +
    400 confirmatory), of which 166 are usable. Every operationalisation
    choice, every threshold, and the frozen baseline are decided here.

CONFIRMATORY -- fresh, never touched by any experiment in this repository
    Eligibility from clinical metadata only, identical rules to the structural
    experiment so the two are directly comparable:
      caseid not in the 1,078 used by ANY previous experiment
      ane_type == "General"
      aneend - anestart >= 2.0 h
    3,453 fresh cases remain. Sorted ascending by caseid, the first 600 form
    the confirmatory set. At the structural experiment's observed yield
    (166/400 = 41.5%) that projects to ~250 usable patients -- more than the
    166 the baseline was established on, so the confirmatory test is better
    powered than the development work behind it.

The confirmatory set is evaluated ONCE, after the protocol is frozen.
"""
from __future__ import annotations
import csv, json, os

_H = os.path.dirname(__file__)
RESULTS = os.path.join(_H, "..", "results")
DATA = os.path.join(_H, "..", "..", "data", "real", "vitaldb")
N_CONFIRM = 600
MIN_ANE_HOURS = 2.0

PRIOR_SPLITS = ("vitaldb_split.json", "st_split.json", "sd_split.json")


def burned():
    used = set()
    for f in PRIOR_SPLITS:
        s = json.load(open(os.path.join(RESULTS, f)))
        used |= set(s["calibration"]) | set(s["confirmatory"])
    return used


def development():
    """The structural experiment's cases -- the representation-search pool."""
    s = json.load(open(os.path.join(RESULTS, "sd_split.json")))
    return sorted(set(s["confirmatory"]))


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
    e = fresh_eligible()
    return {"development": development(),
            "confirmatory": e[:N_CONFIRM],
            "n_fresh_eligible": len(e)}


if __name__ == "__main__":
    s = split()
    u = burned()
    assert not set(s["confirmatory"]) & u, "confirmatory overlaps burned cases"
    assert not set(s["confirmatory"]) & set(s["development"])
    print(f"burned by previous experiments : {len(u)}")
    print(f"fresh eligible remaining       : {s['n_fresh_eligible']}")
    print(f"development (burned, for search): {len(s['development'])}")
    print(f"confirmatory (fresh, untouched) : {len(s['confirmatory'])}"
          f"  {s['confirmatory'][:6]} ...")
    json.dump(s, open(os.path.join(RESULTS, "rs_split.json"), "w"), indent=1)
    print("-> analysis/results/rs_split.json")
