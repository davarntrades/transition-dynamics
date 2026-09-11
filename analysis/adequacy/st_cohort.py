"""Frozen cohort for the short-timescale experiment. Fresh subjects only."""
from __future__ import annotations
import csv, json, os
_H = os.path.dirname(__file__)
DATA = os.path.join(_H, "..", "..", "data", "real", "vitaldb")
PREV = json.load(open(os.path.join(_H, "..", "results", "vitaldb_split.json")))
USED = set(PREV["calibration"]) | set(PREV["confirmatory"])
MIN_HOURS, N_CAL, N_CONF = 2.0, 60, 200

def eligible():
    rows = list(csv.DictReader(open(os.path.join(DATA, "clinical_data.csv"))))
    key = [k for k in rows[0] if k.lstrip("﻿") == "caseid"][0]
    out = []
    for r in rows:
        try:
            h = (float(r["caseend"]) - float(r["casestart"])) / 3600.0
        except (TypeError, ValueError):
            continue
        c = int(r[key])
        if c not in USED and h >= MIN_HOURS:
            out.append(c)
    return sorted(out)

def split():
    e = eligible()
    return {"calibration": e[:N_CAL],
            "confirmatory": e[N_CAL:N_CAL + N_CONF], "n_eligible": len(e)}

if __name__ == "__main__":
    s = split()
    assert not set(s["calibration"]) & set(s["confirmatory"])
    assert not (set(s["calibration"]) | set(s["confirmatory"])) & USED
    print(f"eligible fresh: {s['n_eligible']}")
    print(f"calibration {len(s['calibration'])}: {s['calibration'][:6]}")
    print(f"confirmatory {len(s['confirmatory'])}: {s['confirmatory'][:6]}")
    print("disjoint from previous experiment: yes")
    json.dump(s, open(os.path.join(_H, "..", "results", "st_split.json"), "w"), indent=1)
