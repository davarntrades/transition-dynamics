"""
admissible.py -- waveform extraction and the FROZEN case-admissibility gate.

Applied identically to every arm. No arm can be favoured by it.
"""
from __future__ import annotations
import hashlib, os, sys, urllib.request
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
sys.path.insert(0, os.path.join(_H, "..", "structural"))
import beats as BT
from cohort_acq import DATA

BASE = "https://physionet-open.s3.amazonaws.com/vitaldb/1.0.0"
WAVE = "SNUADC/ART"
NUMERIC = "Solar8000/ART_MBP"
CACHE = os.path.join(DATA, "npz_acq")

# --- frozen feasibility thresholds ---------------------------------------
MIN_WAVE_COVERAGE = 0.80
MIN_BIN_YIELD = 0.70
MIN_BPM, MAX_BPM = 30.0, 200.0
SCRATCH = os.environ.get("ACQ_SCRATCH", "/tmp")


def extract(caseid):
    """Fetch, derive beat-aligned W and monitor M on a common 2 s grid,
    cache a compact summary, delete the raw file."""
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, f"{caseid:05d}.npz")
    if os.path.exists(out):
        return out
    raw = os.path.join(SCRATCH, f"acq_{caseid:05d}.vital")
    try:
        urllib.request.urlretrieve(f"{BASE}/vital_files/{caseid:04d}.vital", raw)
        h = hashlib.sha256(open(raw, "rb").read()).hexdigest()
        import vitaldb
        vf = vitaldb.VitalFile(raw)
        names = set(vf.get_track_names())
        if WAVE not in names or NUMERIC not in names:
            np.savez_compressed(out, ok=False, reason="missing track",
                                sha256=h, caseid=caseid)
            return out
        M = vf.to_numpy([NUMERIC], BT.BIN_S)[:, 0]
        wav = vf.to_numpy([WAVE], 1.0 / BT.FS)[:, 0]
        cov = float(np.isfinite(wav).mean())
        b = BT.detect_beats(wav)
        W = BT.bin_beats(b, len(M))
        yld = float(np.isfinite(W).mean())
        mins = len(wav) / BT.FS / 60.0
        bpm = (len(b) / mins) if (b is not None and mins > 0) else 0.0
        np.savez_compressed(out, ok=True, W=W.astype(np.float32),
                            M=M.astype(np.float32), coverage=cov,
                            bin_yield=yld, bpm=bpm, sha256=h, caseid=caseid)
    finally:
        if os.path.exists(raw):
            os.remove(raw)
    return out


def load(caseid):
    d = np.load(os.path.join(CACHE, f"{caseid:05d}.npz"), allow_pickle=False)
    if not bool(d["ok"]):
        return None, str(d["reason"])
    return ({"W": d["W"].astype(np.float64), "M": d["M"].astype(np.float64),
             "coverage": float(d["coverage"]), "bin_yield": float(d["bin_yield"]),
             "bpm": float(d["bpm"]), "sha256": str(d["sha256"]),
             "caseid": int(d["caseid"])}, None)


def gate(rec):
    """Frozen admissibility gate. Returns (admissible, reason)."""
    if rec["coverage"] < MIN_WAVE_COVERAGE:
        return False, f"waveform coverage {rec['coverage']:.2f} < {MIN_WAVE_COVERAGE}"
    if rec["bin_yield"] < MIN_BIN_YIELD:
        return False, f"beat bin yield {rec['bin_yield']:.2f} < {MIN_BIN_YIELD}"
    if not (MIN_BPM <= rec["bpm"] <= MAX_BPM):
        return False, f"bpm {rec['bpm']:.0f} outside [{MIN_BPM},{MAX_BPM}]"
    return True, ""
