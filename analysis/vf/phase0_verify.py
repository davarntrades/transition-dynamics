"""
phase0_verify.py -- Phase 0 metadata verification for the SDDB (outcome-blind).

Reads ONLY: header (.hea) files, the SHA256SUMS.txt manifest, and annotation
(.ari / .atr) files. Never reads or decodes signal (.dat) samples.

Annotation read policy (enforced below, not merely documented):
  P1  Format: parse validity, annotation count, first/last annotation time,
      presence of rhythm (aux) annotations. Code vocabularies are pooled
      across the database, never reported per record.
  P2  Event label: times of VF-type markers ('[', '!', aux '(VF', '(VFL',
      '(VFIB') -- the event definition itself -- and whether any precedes
      the header #vfon by more than 2 min.
  P3  Baseline zone [15, 45) min: beat count, rhythm labels, .ari/.atr beat
      agreement. Only when the baseline ends >= 60 min before #vfon.
  P4  NOTHING else from the pre-onset period: no counts of ventricular beats,
      VT runs or rhythm changes in remote, grey or warning-bin zones.
  P5  Event-label corroboration, POST-ONSET ONLY: number of beat annotations
      (and of normal 'N' beats) in [vfon, vfon+60 s) and [vfon+60, vfon+180 s).
      No annotation earlier than vfon is read by P5.

Usage:  python3 -I analysis/vf/phase0_verify.py <dir with sddb files> <out.json>
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np
import wfdb

FS_EXPECTED = 250
BASE_LO, BASE_HI = 15 * 60, 45 * 60          # seconds
SEAL_MIN = 60                                  # minutes before onset
BEAT_SYMBOLS = set("NLRBAaJSVrFejnE/fQ?")
VF_AUX = ("(VF", "(VFL", "(VFIB")
VF_SYM = {"[", "!"}
T_RULES_MIN = {"2h20": 140, "2h50": 170, "3h": 180, "4h": 240}
SETTLE, BASE, W, GREY_PLUS_BIN = 15, 30, 5, 60


def hms(s: str) -> float:
    parts = [float(p) for p in s.strip().split(":")]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def fmt(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 3600:02d}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_header(path: str) -> dict:
    lines = [l.rstrip("\n") for l in open(path)]
    rec = lines[0].split()
    out = {"record": rec[0], "n_sig": int(rec[1]), "fs": float(rec[2]),
           "n_samples": int(rec[3]),
           "base_time": rec[4] if len(rec) > 4 else None,
           "base_date": rec[5] if len(rec) > 5 else None,
           "signals": [], "comments": []}
    for l in lines[1:1 + out["n_sig"]]:
        f = l.split()
        out["signals"].append({"file": f[0], "format": f[1], "gain": f[2],
                               "adc_res": f[3], "adc_zero": f[4],
                               "description": " ".join(f[8:])})
    for l in lines[1 + out["n_sig"]:]:
        if l.startswith("#"):
            out["comments"].append(l[1:].strip())
    vf = [c for c in out["comments"] if c.lower().startswith("vfon:")]
    out["vfon"] = vf[0].split(":", 1)[1].strip() if vf else None
    return out


def ann_summary(d: str, rec: str, ext: str, onset_s, vocab: dict) -> dict | None:
    p = os.path.join(d, f"{rec}.{ext}")
    if not os.path.exists(p):
        return None
    a = wfdb.rdann(os.path.join(d, rec), ext)
    t = np.asarray(a.sample, float) / FS_EXPECTED
    sym = list(a.symbol)
    aux = [x if x else "" for x in a.aux_note]
    # P1 -- vocabularies pooled across the database (no per-record counts)
    vocab.setdefault(ext + "_symbols", set()).update(sym)
    vocab.setdefault(ext + "_aux", set()).update(x.strip("\x00") for x in aux if x)
    out = {"n_annotations": int(len(t)),
           "first_s": float(t.min()) if len(t) else None,
           "last_s": float(t.max()) if len(t) else None,
           "has_rhythm_aux": bool(any(x.startswith("(") for x in aux))}
    # P2 -- VF-type event markers
    isvf = np.array([(s in VF_SYM) or any(x.startswith(v) for v in VF_AUX)
                     for s, x in zip(sym, aux)], bool)
    if isvf.any():
        first = float(t[isvf].min())
        out["first_vf_marker_s"] = first
        out["first_vf_marker"] = fmt(first)
        if onset_s is not None:
            out["first_vf_marker_minus_vfon_s"] = first - onset_s
            early = t[isvf] < onset_s - 120
            out["n_vf_markers_more_than_2min_before_vfon"] = int(early.sum())
            out["earliest_vf_marker_before_vfon"] = (fmt(float(t[isvf][early].min()))
                                                     if early.any() else None)
    else:
        out["first_vf_marker_s"] = None
    # P5 -- post-onset corroboration of the event label (never before onset)
    if onset_s is not None:
        isbeat = np.array([s_ in BEAT_SYMBOLS for s_ in sym], bool)
        isN = np.array([s_ == "N" for s_ in sym], bool)
        for lo, hi, tag in ((0, 60, "0_60s"), (60, 180, "60_180s")):
            m = (t >= onset_s + lo) & (t < onset_s + hi)
            out[f"post_onset_beats_{tag}"] = int((m & isbeat).sum())
            out[f"post_onset_N_{tag}"] = int((m & isN).sum())
    # P3 -- baseline zone only, and only if it ends >= SEAL_MIN before onset
    base_ok = onset_s is None or (BASE_HI <= onset_s - SEAL_MIN * 60)
    out["baseline_readable"] = bool(base_ok)
    if base_ok:
        m = (t >= BASE_LO) & (t < BASE_HI)
        beats = m & np.array([s in BEAT_SYMBOLS for s in sym], bool)
        out["baseline_beats"] = int(beats.sum())
        out["baseline_beat_times"] = t[beats]          # internal; stripped later
        out["baseline_beat_symbols"] = [x for x, b in zip(sym, beats) if b]  # internal
        # rhythm in force during the baseline: last rhythm label before BASE_HI
        r = [(tt, x) for tt, x in zip(t, aux) if x.startswith("(") and tt < BASE_HI]
        out["baseline_rhythm_labels"] = sorted({x.strip("\x00") for tt, x in r
                                               if tt >= BASE_LO} |
                                              ({r[-1][1].strip("\x00")} if r else set()))
    return out


def beat_agreement(t1, t2, s1, s2, tol: float = 0.15) -> dict:
    """Baseline-zone agreement of unaudited (.ari) vs reference (.atr) beats.
    Class agreement is reported as a fraction only (N-vs-non-N), never as
    ectopy counts."""
    if len(t1) == 0 or len(t2) == 0:
        return {"n_ari": int(len(t1)), "n_atr": int(len(t2))}
    idx = np.searchsorted(t2, t1)
    lo = np.clip(idx - 1, 0, len(t2) - 1)
    hi = np.clip(idx, 0, len(t2) - 1)
    use_hi = np.abs(t2[hi] - t1) < np.abs(t2[lo] - t1)
    j = np.where(use_hi, hi, lo)
    d = np.abs(t2[j] - t1)
    m = d <= tol
    matched = int(m.sum())
    a = np.array(s1)[m]
    b = np.array(s2)[j[m]]
    same_class = float(np.mean((a == "N") == (b == "N"))) if matched else float("nan")
    return {"n_ari": int(len(t1)), "n_atr": int(len(t2)), "matched_150ms": matched,
            "sensitivity_ari_vs_atr": matched / len(t2),
            "ppv_ari_vs_atr": matched / len(t1),
            "class_agreement_N_vs_nonN": same_class}


def main():
    d, out_path = sys.argv[1], sys.argv[2]
    recs = [l.strip() for l in open(os.path.join(d, "RECORDS")) if l.strip()]
    sums = {}
    for l in open(os.path.join(d, "SHA256SUMS.txt")):
        h, f = l.split()
        sums[f] = h
    manifest_sha = sha256(os.path.join(d, "SHA256SUMS.txt"))
    local_ok = {f: (sha256(os.path.join(d, f)) == h)
                for f, h in sums.items() if os.path.exists(os.path.join(d, f))}
    vocab = {}
    rows = []
    for r in recs:
        hd = parse_header(os.path.join(d, f"{r}.hea"))
        dur = hd["n_samples"] / hd["fs"]
        onset = hms(hd["vfon"]) if hd["vfon"] else None
        row = {"record": r, "fs": hd["fs"], "n_sig": hd["n_sig"],
               "formats": sorted({s["format"] for s in hd["signals"]}),
               "gains": [s["gain"] for s in hd["signals"]],
               "signal_descriptions": [s["description"] for s in hd["signals"]],
               "n_samples": hd["n_samples"], "duration": fmt(dur), "duration_s": dur,
               "base_time": hd["base_time"], "base_date": hd["base_date"],
               "header_comments": hd["comments"], "vfon": hd["vfon"],
               "vfon_s": onset,
               "expected_dat_bytes_fmt212": hd["n_samples"] * 3 if hd["n_sig"] == 2 else None}
        if onset is not None:
            row["onset_within_record"] = bool(0 < onset < dur)
            row["post_onset_s"] = dur - onset
            for name, tmin in T_RULES_MIN.items():
                row[f"eligible_{name}"] = bool(onset >= tmin * 60)
            # geometry: remote-zone minutes available (outcome-blind, from labels only)
            row["remote_zone_min"] = max(0.0, onset / 60 - SETTLE - BASE - W - GREY_PLUS_BIN)
        for ext in ("ari", "atr"):
            s = ann_summary(d, r, ext, onset, vocab)
            row[ext] = s
        if row["ari"] and row["atr"] and row["ari"].get("baseline_readable"):
            row["baseline_ari_vs_atr"] = beat_agreement(
                row["ari"]["baseline_beat_times"], row["atr"]["baseline_beat_times"],
                row["ari"]["baseline_beat_symbols"], row["atr"]["baseline_beat_symbols"])
        for ext in ("ari", "atr"):
            if row[ext]:
                row[ext].pop("baseline_beat_times", None)
                row[ext].pop("baseline_beat_symbols", None)
        rows.append(row)
    out = {"dataset": "sddb", "version": "1.0.0",
           "source": "https://physionet-open.s3.amazonaws.com/sddb/1.0.0/",
           "manifest_sha256": manifest_sha,
           "n_files_in_manifest": len(sums),
           "local_files_verified": int(sum(local_ok.values())),
           "local_files_failed": sorted(f for f, ok in local_ok.items() if not ok),
           "read_policy": "P1-P4 (see module docstring); .dat never read",
           "vocabulary_pooled": {k: sorted(v) for k, v in vocab.items()},
           "records": rows}
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
