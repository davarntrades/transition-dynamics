"""
Calibration run -- 80 cases. Purpose, and only purpose:
  (a) channel coverage and exclusion accounting
  (b) event rate and per-horizon prevalence feasibility
  (c) smoke-test the harness for defects
No model comparison is decided here. The confirmatory set is not touched.
"""
from __future__ import annotations
import csv, json, os, sys, collections
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
import windows as W
from cohort import SHORT, RESULTS, DATA
from fetch import load_case

META = {}
_rows = list(csv.DictReader(open(os.path.join(DATA, "clinical_data.csv"))))
_key = [k for k in _rows[0] if k.lstrip("﻿") == "caseid"][0]
for r in _rows:
    META[int(r[_key])] = r


def case_rows(caseid, thresh=W.MAP_THRESH):
    d = load_case(caseid)
    m = META[caseid]
    i0, i1 = W.case_interval(d["X"].shape[0], float(m["anestart"]),
                             float(m["aneend"]), float(m["caseend"]))
    if (i1 - i0) * W.DT < W.MIN_ANALYSABLE_S:
        return None, f"analysable {(i1-i0)*W.DT/60:.0f} min < 60"
    prep, why = W.prepare_case(d["X"], i0, i1)
    if prep is None:
        return None, why
    rows, onsets = W.build_windows(prep, i0, i1, thresh)
    return {"prep": prep, "rows": rows, "onsets": onsets,
            "i0": i0, "i1": i1, "caseid": caseid}, None


if __name__ == "__main__":
    ids = json.load(open(os.path.join(RESULTS, "sd_split.json")))["calibration"]
    excl = collections.Counter()
    ok, allrows = [], 0
    per_h = {h: [0, 0] for h in W.HORIZONS}
    ev_patients, n_events, lead = 0, 0, []
    cover_fail = collections.Counter()
    for c in ids:
        try:
            res, why = case_rows(c)
        except Exception as e:
            excl[f"error: {type(e).__name__}"] += 1
            continue
        if res is None:
            excl[why.split(" ")[0] if "coverage" not in why else "coverage"] += 1
            if "coverage" in why:
                d = load_case(c)
                for j, p in enumerate(d["present"]):
                    if not p:
                        cover_fail[SHORT[j]] += 1
            continue
        ok.append(c)
        allrows += len(res["rows"])
        if len(res["onsets"]):
            ev_patients += 1
            n_events += len(res["onsets"])
        for r in res["rows"]:
            for h in W.HORIZONS:
                if r["keep"][h]:
                    per_h[h][r["labels"][h]] += 1
            if np.isfinite(r["next_onset_min"]):
                lead.append(r["next_onset_min"])

    print(f"cases attempted        {len(ids)}")
    print(f"cases usable           {len(ok)}")
    print("exclusions:", dict(excl))
    if cover_fail:
        print("missing channel counts:", dict(cover_fail))
    print(f"evaluation points      {allrows}")
    print(f"patients with >=1 event {ev_patients}   events {n_events}")
    print("\nhorizon   neg      pos    prevalence")
    for h in W.HORIZONS:
        neg, pos = per_h[h][0], per_h[h][1]
        tot = neg + pos
        print(f"{h//60:>4} min  {neg:>6}  {pos:>6}   "
              f"{(pos/tot if tot else 0):.4f}")
    json.dump({"usable": ok, "exclusions": dict(excl),
               "n_windows": allrows, "event_patients": ev_patients,
               "prevalence": {str(h//60): per_h[h] for h in W.HORIZONS}},
              open(os.path.join(RESULTS, "sd_calibration.json"), "w"), indent=1)
