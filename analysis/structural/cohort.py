"""
cohort.py -- frozen cohort and patient-level split for the structural
displacement prediction experiment.

DATASET
-------
VitalDB, PhysioNet open-access mirror v1.0.0, CC-BY 4.0.
  s3://physionet-open/vitaldb/1.0.0/
No credentialing, no data use agreement, no access control bypassed.

ELIGIBILITY -- CLINICAL METADATA ONLY, FIXED BEFORE ANY SIGNAL WAS READ
----------------------------------------------------------------------
  1. caseid not used in either previous confirmatory experiment (598 cases)
  2. ane_type == "General"
  3. aneend - anestart >= 2.0 h   (30 min baseline + >= 60 min observation)
  4. anestart, aneend both present and finite

Sorted ascending by caseid (deterministic). Then:

  CALIBRATION    first  80 eligible   -- harness smoke-test, channel coverage,
                                         event-rate feasibility ONLY
  CONFIRMATORY   next  400 eligible   -- untouched until the protocol is frozen

Disjoint by construction, and disjoint from all 598 previously used cases.

CHANNEL PANEL -- FIXED HERE
---------------------------
Eight numeric Solar8000 tracks, chosen for availability and for carrying
genuinely distinct physiology, so that Sigma_0 has real off-diagonal
structure for a whitening metric to exploit.

  ART_SBP, ART_DBP, ART_MBP   arterial pressure triple (strongly coupled)
  HR                          chronotropy
  PLETH_SPO2                  oxygenation
  ETCO2                       ventilation / perfusion
  BT                          temperature
  RR_CO2                      respiratory rate from capnography

A case is usable only if ALL eight are present with >= 80% finite coverage
over the baseline window. This is a signal-level exclusion; it is prespecified
here and applied identically to every model arm, so it cannot favour one.
"""
from __future__ import annotations

import csv
import json
import os

BASE_URL = "https://physionet-open.s3.amazonaws.com/vitaldb/1.0.0"

CHANNELS = [
    "Solar8000/ART_SBP",
    "Solar8000/ART_DBP",
    "Solar8000/ART_MBP",
    "Solar8000/HR",
    "Solar8000/PLETH_SPO2",
    "Solar8000/ETCO2",
    "Solar8000/BT",
    "Solar8000/RR_CO2",
]
FETCHED = [c.split("/")[1] for c in CHANNELS]

# Amendment A2 (2026-09-11, calibration evidence only): BT and RR_CO2 are
# stored but excluded from analysis. Both fail the PRESPECIFIED >= 80% baseline
# coverage rule in a large fraction of cases for instrumentation reasons --
# the temperature probe is sampled intermittently early in the case, and
# capnography-derived RR drops out during airway manipulation. Neither has any
# bearing on the hypothesis. Decided from coverage counts alone, with no
# outcome examined. The .npz cache keeps all eight columns, so provenance is
# unchanged and the decision is reversible.
PANEL = ["ART_SBP", "ART_DBP", "ART_MBP", "HR", "PLETH_SPO2", "ETCO2"]
PANEL_IDX = [FETCHED.index(c) for c in PANEL]
SHORT = PANEL
MAP_IDX = PANEL.index("ART_MBP")

INTERVAL_S = 2
MIN_ANE_HOURS = 2.0
MIN_COVERAGE = 0.80
N_CALIB = 80
N_CONFIRM = 400

_H = os.path.dirname(__file__)
DATA = os.path.join(_H, "..", "..", "data", "real", "vitaldb")
RESULTS = os.path.join(_H, "..", "results")


def _previously_used():
    used = set()
    for f in ("vitaldb_split.json", "st_split.json"):
        s = json.load(open(os.path.join(RESULTS, f)))
        used |= set(s["calibration"]) | set(s["confirmatory"])
    return used


def eligible():
    used = _previously_used()
    rows = list(csv.DictReader(open(os.path.join(DATA, "clinical_data.csv"))))
    key = [k for k in rows[0] if k.lstrip("﻿") == "caseid"][0]
    out = []
    for r in rows:
        c = int(r[key])
        if c in used or r["ane_type"] != "General":
            continue
        try:
            start, end = float(r["anestart"]), float(r["aneend"])
        except (TypeError, ValueError):
            continue
        if (end - start) / 3600.0 >= MIN_ANE_HOURS:
            out.append((c, start, end))
    return sorted(out)


def split():
    e = eligible()
    cal = e[:N_CALIB]
    conf = e[N_CALIB:N_CALIB + N_CONFIRM]
    return {
        "calibration": [c for c, _, _ in cal],
        "confirmatory": [c for c, _, _ in conf],
        "ane_window": {str(c): [s, t] for c, s, t in cal + conf},
        "n_eligible": len(e),
    }


if __name__ == "__main__":
    s = split()
    used = _previously_used()
    assert not set(s["calibration"]) & set(s["confirmatory"])
    assert not (set(s["calibration"]) | set(s["confirmatory"])) & used
    print(f"previously used (excluded): {len(used)}")
    print(f"fresh eligible:             {s['n_eligible']}")
    print(f"calibration  {len(s['calibration']):>3}: {s['calibration'][:6]} ...")
    print(f"confirmatory {len(s['confirmatory']):>3}: {s['confirmatory'][:6]} ...")
    json.dump(s, open(os.path.join(RESULTS, "sd_split.json"), "w"), indent=1)
    print("-> analysis/results/sd_split.json")
