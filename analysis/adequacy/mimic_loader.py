"""
mimic_loader.py — build multichannel vital-sign trajectories from a MIMIC-style
SQLite extract.

PROVENANCE. MIMIC-III Clinical Database Demo, an open-access (ODbL) subset
distributed by MIT-LCP, obtained from the public `MIT-LCP/mimic-workshop`
repository. No credentialed data is used and no access control is bypassed.

Written against the demo so that the same code runs unchanged on a full
MIMIC-III / MIMIC-IV extract: point DB_PATH at a larger SQLite file with the
same table and column names.
"""

from __future__ import annotations

import datetime as dt
import os
import sqlite3

import numpy as np

# Channels chosen for physiological meaning and charting frequency.
# 'defended' marks variables held near setpoint by active regulation.
TARGETS = {
    "HR":    (["Heart Rate"], False),
    "SPO2":  (["O2 saturation pulseoxymetry"], True),
    "RR":    (["Respiratory Rate"], False),
    "MAP":   (["Arterial Blood Pressure mean",
               "Non Invasive Blood Pressure mean"], True),
    "SBP":   (["Arterial Blood Pressure systolic",
               "Non Invasive Blood Pressure systolic"], True),
    "TEMP":  (["Temperature Fahrenheit", "Temperature Celsius"], True),
}


def _parse(s):
    return dt.datetime.fromisoformat(str(s).replace("T", " "))


def load_stays(db_path, grid_minutes=60, min_hours=6, ffill_limit=2,
               channels=("HR", "SPO2", "RR", "MAP")):
    """
    Returns list of dicts: {stay_id, names, X (n,p), grid_minutes, coverage}.
    X is on a regular grid; gaps longer than ffill_limit intervals stay NaN.
    """
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    label_to_id = {}
    for r in con.execute("select ITEMID, LABEL from D_ITEMS"):
        if r["LABEL"]:
            label_to_id.setdefault(r["LABEL"], []).append(r["ITEMID"])

    wanted = {}
    for ch in channels:
        labels, _ = TARGETS[ch]
        ids = [i for lab in labels for i in label_to_id.get(lab, [])]
        wanted[ch] = set(ids)

    rows = con.execute(
        "select ICUSTAY_ID, ITEMID, CHARTTIME, VALUENUM from CHARTEVENTS "
        "where VALUENUM is not null and ICUSTAY_ID is not null").fetchall()

    per = {}
    for r in rows:
        for ch, ids in wanted.items():
            if r["ITEMID"] in ids:
                per.setdefault(r["ICUSTAY_ID"], {}).setdefault(ch, []).append(
                    (_parse(r["CHARTTIME"]), float(r["VALUENUM"])))

    out = []
    for sid, chans in per.items():
        if not all(c in chans and len(chans[c]) >= 5 for c in channels):
            continue
        t0 = min(min(t for t, _ in v) for v in chans.values())
        t1 = max(max(t for t, _ in v) for v in chans.values())
        hours = (t1 - t0).total_seconds() / 3600
        if hours < min_hours:
            continue
        n = int(hours * 60 / grid_minutes) + 1
        grid = [t0 + dt.timedelta(minutes=grid_minutes * i) for i in range(n)]
        X = np.full((n, len(channels)), np.nan)
        for j, ch in enumerate(channels):
            obs = sorted(chans[ch])
            ti = np.array([(t - t0).total_seconds() / 60 / grid_minutes
                           for t, _ in obs])
            vi = np.array([v for _, v in obs])
            idx = np.round(ti).astype(int)
            keep = (idx >= 0) & (idx < n)
            X[idx[keep], j] = vi[keep]
            # forward fill with a hard limit
            last, gap = np.nan, 10 ** 9
            for i in range(n):
                if np.isfinite(X[i, j]):
                    last, gap = X[i, j], 0
                else:
                    gap += 1
                    if gap <= ffill_limit and np.isfinite(last):
                        X[i, j] = last
        cov = float(np.mean(np.isfinite(X)))
        out.append({"stay_id": sid, "names": list(channels), "X": X,
                    "grid_minutes": grid_minutes, "hours": hours,
                    "coverage": cov})
    return out


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..",
                       "data", "real", "mimicdata.sqlite")

if __name__ == "__main__":
    stays = load_stays(DB_PATH)
    print(f"stays with all 4 channels and >= 6 h: {len(stays)}")
    for s in sorted(stays, key=lambda d: -d["hours"]):
        X = s["X"]
        ok = np.isfinite(X).all(axis=1)
        print(f"  stay {s['stay_id']}  {s['hours']:6.1f} h  n={len(X):4d}  "
              f"complete rows={ok.sum():4d}  coverage={s['coverage']:.0%}")


def baseline_tradeoff(X, lengths=(4, 12, 24, 48, 96, 168)):
    """
    For a recording on an hourly grid: does ANY baseline window length satisfy
    both the effective-sample-size rule and the stationarity screen?

    Longer baselines raise n_eff but are less likely to be stationary. This
    reports the whole trade-off rather than a single pass/fail, because the
    interesting question is whether the two requirements are jointly
    satisfiable at this sampling resolution at all.
    """
    from adequacy import n_eff, MIN_NEFF_FACTOR
    X = X[np.isfinite(X).all(axis=1)]
    p = X.shape[1]
    rows = []
    for bh in lengths:
        nb = min(bh, len(X))
        if nb < 6:
            continue
        B = X[:nb]
        third = max(2, nb // 3)
        shift = float(np.max(np.abs(B[:third].mean(0) - B[-third:].mean(0))
                             / (B.std(0) + 1e-9)))
        ne = n_eff(B)
        rows.append({"hours": bh, "n": nb, "n_eff": ne, "max_shift": shift,
                     "neff_ok": ne >= MIN_NEFF_FACTOR * p,
                     "stationary_ok": shift <= 0.5})
    return rows
