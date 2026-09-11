"""
vitaldb_cohort.py — frozen cohort definition for the VitalDB model-adequacy test.

DATASET
-------
VitalDB: a high-fidelity multi-parameter vital signs database in surgical
patients. PhysioNet open-access mirror, version 1.0.0, CC-BY 4.0. No
credentialing, no data use agreement, no access control bypassed.

  s3://physionet-open/vitaldb/1.0.0/

SPLIT — FIXED BEFORE ANY DATA WAS EXAMINED
------------------------------------------
Eligibility is a property of the clinical metadata only (recording duration),
never of the physiological signals.

  eligible      caseend - casestart >= 6.5 h          -> 338 cases
  sort          ascending by caseid (deterministic)
  CALIBRATION   first 40 eligible caseids
  CONFIRMATORY  next 100 eligible caseids
  disjoint by construction; no case appears in both

The calibration set exists solely to decide whether the preregistered
stationarity screen is statistically appropriate for continuously sampled
human physiology. The confirmatory set is NOT examined until that decision is
frozen.

CHANNELS — fixed here, chosen for coverage and physiological meaning
  Solar8000/HR           heart rate
  Solar8000/ART_MBP      invasive mean arterial pressure   (defended)
  Solar8000/PLETH_SPO2   pulse oximetry saturation          (defended)
  Solar8000/ETCO2        end-tidal CO2                      (defended)

Sampling interval 2 s. A case is usable only if all four channels are present
with >= 80% finite coverage over the analysed span.
"""

from __future__ import annotations

import csv
import json
import os

BASE_URL = "https://physionet-open.s3.amazonaws.com/vitaldb/1.0.0"
CHANNELS = ["Solar8000/HR", "Solar8000/ART_MBP",
            "Solar8000/PLETH_SPO2", "Solar8000/ETCO2"]
INTERVAL_S = 2
MIN_HOURS = 6.5
MIN_COVERAGE = 0.80
N_CALIB = 40
N_CONFIRM = 100

_HERE = os.path.dirname(__file__)
DATA = os.path.join(_HERE, "..", "..", "data", "real", "vitaldb")


def eligible_caseids():
    path = os.path.join(DATA, "clinical_data.csv")
    rows = list(csv.DictReader(open(path)))
    key = [k for k in rows[0] if k.lstrip("﻿") == "caseid"][0]
    out = []
    for r in rows:
        try:
            h = (float(r["caseend"]) - float(r["casestart"])) / 3600.0
        except (TypeError, ValueError):
            continue
        if h >= MIN_HOURS:
            out.append(int(r[key]))
    return sorted(out)


def split():
    e = eligible_caseids()
    return {"calibration": e[:N_CALIB],
            "confirmatory": e[N_CALIB:N_CALIB + N_CONFIRM],
            "n_eligible": len(e)}


if __name__ == "__main__":
    s = split()
    print(f"eligible (>= {MIN_HOURS} h): {s['n_eligible']}")
    print(f"calibration  n={len(s['calibration'])}: {s['calibration'][:8]} ...")
    print(f"confirmatory n={len(s['confirmatory'])}: {s['confirmatory'][:8]} ...")
    assert not set(s["calibration"]) & set(s["confirmatory"]), "sets overlap"
    print("disjoint: yes")
    with open(os.path.join(_HERE, "..", "results", "vitaldb_split.json"),
              "w") as fh:
        json.dump(s, fh, indent=1)
