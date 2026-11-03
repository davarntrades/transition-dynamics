"""
landscape_verify.py -- metadata-only verification of candidate VT/VF datasets
on PhysioNet's open-data mirror (s3://physionet-open, via HTTPS).

Reads ONLY: file listings, RECORDS/ANNOTATORS, headers, documentation tables,
and rhythm-label annotations (event labels). Never reads ECG samples. For the
RR-only mvtdb, beat annotations are read only for POOLED per-record counts
and spans (event and control records together, never stratified by type),
because the RR series itself is the pre-event physiology.

Usage: python3 -I analysis/vtvf/landscape_verify.py <workdir> <out.json>
"""
from __future__ import annotations

import collections
import json
import os
import re
import subprocess
import sys

import numpy as np

MIRROR = "https://physionet-open.s3.amazonaws.com/"


def get(path: str, dst: str) -> str:
    if not os.path.exists(dst):
        subprocess.run(["curl", "-sS", "-m", "60", "-o", dst, MIRROR + path], check=True)
    return dst


def listing(prefix: str) -> list[tuple[str, int]]:
    keys, token = [], None
    while True:
        args = ["curl", "-sS", "-m", "60", "-G", MIRROR,
                "--data-urlencode", "list-type=2", "--data-urlencode", f"prefix={prefix}"]
        if token:
            args += ["--data-urlencode", f"continuation-token={token}"]
        x = subprocess.run(args, capture_output=True, text=True).stdout
        keys += list(zip(re.findall(r"<Key>(.*?)</Key>", x),
                         map(int, re.findall(r"<Size>(\d+)</Size>", x))))
        m = re.search(r"<NextContinuationToken>(.*?)</NextContinuationToken>", x)
        if "<IsTruncated>true" in x and m:
            token = m.group(1)
        else:
            return keys


def verify_mvtdb(w: str) -> dict:
    import wfdb
    d = os.path.join(w, "mvtdb"); os.makedirs(d, exist_ok=True)
    recs = [l.strip() for l in open(get("mvtdb/1.0/data/RECORDS", f"{d}/RECORDS")) if l.strip()]
    pat = collections.defaultdict(collections.Counter)
    for r in recs:
        p, t = r.split("_"); pat[p][t[:2]] += 1
    n_ann, span, sym, aux, nsig = [], [], collections.Counter(), collections.Counter(), set()
    for r in recs:
        get(f"mvtdb/1.0/data/{r}.hea", f"{d}/{r}.hea")
        get(f"mvtdb/1.0/data/{r}.qrs", f"{d}/{r}.qrs")
        h = wfdb.rdheader(f"{d}/{r}"); nsig.add(h.n_sig)
        a = wfdb.rdann(f"{d}/{r}", "qrs")
        n_ann.append(len(a.sample)); span.append((a.sample[-1] - a.sample[0]) / 1000 / 60)
        sym.update(set(a.symbol)); aux.update(set(x for x in a.aux_note if x))
    ev = collections.Counter(c["vt"] + c["vf"] for c in pat.values())
    out = {"records": len(recs), "patients": len(pat),
           "vt_records": sum(c["vt"] for c in pat.values()),
           "vf_records": sum(c["vf"] for c in pat.values()),
           "control_records": sum(c["mr"] for c in pat.values()),
           "events_per_patient_distribution": dict(sorted(ev.items())),
           "patients_with_vf": sum(1 for c in pat.values() if c["vf"]),
           "patients_with_vt": sum(1 for c in pat.values() if c["vt"]),
           "patients_with_both": sum(1 for c in pat.values() if c["vt"] and c["vf"]),
           "signals_per_record": sorted(nsig),
           "beat_annotations_per_record_pooled": [int(min(n_ann)), int(np.median(n_ann)), int(max(n_ann))],
           "record_span_minutes_pooled_p5_p50_p95_max":
               [round(float(x), 1) for x in np.percentile(span, [5, 50, 95, 100])],
           "annotation_symbols_pooled": sorted(sym), "aux_labels_pooled": sorted(aux)}
    try:
        import pandas as pd
        get("mvtdb/1.0/phys.xls", f"{d}/phys.xls")
        t = pd.read_excel(f"{d}/phys.xls", header=0)
        t = t[t["Patient No"].notna()]
        out["clinical_table_rows"] = int(len(t))
        out["clinical_device_class"] = {str(k): int(v) for k, v in t["Device Class"].value_counts().items()}
        out["clinical_episode_time_present"] = int(t["Episode time"].notna().sum())
        out["clinical_antiarrhythmic_meds"] = {str(k): int(v) for k, v in
                                               t["Current Antiarrhythmic Meds Y/N"].value_counts().items()}
    except Exception as e:  # xlrd optional
        out["clinical_table_error"] = repr(e)
    return out


def verify_rhythm_db(w: str, db: str, ver: str = "1.0.0") -> dict:
    import wfdb
    d = os.path.join(w, db); os.makedirs(d, exist_ok=True)
    recs = [l.strip() for l in open(get(f"{db}/{ver}/RECORDS", f"{d}/RECORDS")) if l.strip()]
    tot, firsts, durs, fs, nsig = collections.Counter(), [], [], set(), set()
    for r in recs:
        get(f"{db}/{ver}/{r}.hea", f"{d}/{r}.hea"); get(f"{db}/{ver}/{r}.atr", f"{d}/{r}.atr")
        h = wfdb.rdheader(f"{d}/{r}"); fs.add(h.fs); nsig.add(h.n_sig)
        durs.append(h.sig_len / h.fs / 60)
        a = wfdb.rdann(f"{d}/{r}", "atr")
        t = np.asarray(a.sample) / h.fs
        aux = [x.strip("\x00") for x in a.aux_note]
        tot.update(x for x in aux if x.startswith("("))
        vent = [tt for tt, x in zip(t, aux) if x.startswith(("(VT", "(VF", "(VFL", "(VFIB"))]
        vent += [tt for tt, s in zip(t, a.symbol) if s == "["]
        firsts.append(min(vent) / 60 if vent else None)
    f = [x for x in firsts if x is not None]
    return {"records": len(recs), "fs": sorted(fs), "n_signals": sorted(nsig),
            "duration_min_median_max": [round(min(durs), 1), round(float(np.median(durs)), 1), round(max(durs), 1)],
            "rhythm_label_counts": dict(tot),
            "records_with_ventricular_tachyarrhythmia_label": len(f),
            "minutes_before_first_ventricular_label_min_median_max":
                [round(min(f), 1), round(float(np.median(f)), 1), round(max(f), 1)] if f else None,
            "records_first_onset_ge_15min": sum(1 for x in f if x >= 15),
            "records_first_onset_ge_30min": sum(1 for x in f if x >= 30)}


def verify_music(w: str) -> dict:
    import pandas as pd
    d = os.path.join(w, "music"); os.makedirs(d, exist_ok=True)
    t = pd.read_csv(get("music-sudden-cardiac-death/1.0.1/subject-info.csv", f"{d}/subject-info.csv"), sep=";")
    recs = [l.strip() for l in open(get("music-sudden-cardiac-death/1.0.1/RECORDS", f"{d}/RECORDS")) if l.strip()]
    hea = get(f"music-sudden-cardiac-death/1.0.1/{recs[0]}.hea", f"{d}/first.hea")
    vc = lambda c: {str(k): int(v) for k, v in t[c].value_counts(dropna=False).items()}
    return {"subjects": int(len(t)), "records_listed": len(recs),
            "cause_of_death_codes": vc("Cause of death"),
            "holter_available": vc("Holter available"),
            "holter_VT_flag_codes": vc("Ventricular Tachycardia"),
            "holter_NSVT_flag": vc("Non-sustained ventricular tachycardia (CH>10)"),
            "holter_onset_clock_present": int(t["Holter onset (hh:mm:ss)"].notna().sum()),
            "follow_up_days_median": float(t["Follow-up period from enrollment (days)"].median()),
            "first_holter_header": open(hea).read().strip().splitlines()}


def main():
    w, out = sys.argv[1], sys.argv[2]
    os.makedirs(w, exist_ok=True)
    res = {"source": MIRROR, "note": "metadata only; no ECG samples read"}
    top = subprocess.run(["curl", "-sS", "-m", "60", "-G", MIRROR, "--data-urlencode", "list-type=2",
                          "--data-urlencode", "delimiter=/"], capture_output=True, text=True).stdout
    prefixes = [p.strip("/") for p in re.findall(r"<Prefix>(.*?)</Prefix>", top) if p]
    res["mirror_open_datasets"] = len(prefixes)
    for name in ("vtac", "challenge-2015", "mimic3wdb", "mimic3wdb-matched", "mimic4wdb"):
        res[f"on_mirror_{name}"] = name in prefixes
    res["mvtdb"] = verify_mvtdb(w)
    for db in ("vfdb", "cudb", "incartdb"):
        res[db] = verify_rhythm_db(w, db)
    res["music_sudden_cardiac_death"] = verify_music(w)
    res["ahadb_on_mirror_records"] = [l.strip() for l in
                                      open(get("ahadb/1.0.0/RECORDS", f"{w}/ahadb_RECORDS")) if l.strip()]
    with open(out, "w") as f:
        json.dump(res, f, indent=1, default=str)
    print("wrote", out)


if __name__ == "__main__":
    main()
