"""Download VitalDB cases, extract the frozen eight-channel panel, record a
SHA-256 of the source file, then delete the raw .vital (tens of MB each)."""
from __future__ import annotations
import hashlib, json, os, sys, urllib.request
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
from cohort import BASE_URL, CHANNELS, INTERVAL_S, DATA, RESULTS, split  # noqa

CACHE = os.path.join(DATA, "npz_sd")
SCRATCH = os.environ.get("SD_SCRATCH", "/tmp")


def fetch_case(caseid):
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, f"{caseid:04d}.npz")
    if os.path.exists(out):
        return out
    raw = os.path.join(SCRATCH, f"sd_{caseid:04d}.vital")
    try:
        urllib.request.urlretrieve(
            f"{BASE_URL}/vital_files/{caseid:04d}.vital", raw)
        h = hashlib.sha256(open(raw, "rb").read()).hexdigest()
        import vitaldb
        vf = vitaldb.VitalFile(raw)
        names = set(vf.get_track_names())
        have = [c for c in CHANNELS if c in names]
        # Always emit a p-column array; absent channels become all-NaN so the
        # coverage rule -- not an index shift -- decides admissibility.
        X = np.full((0, len(CHANNELS)), np.nan)
        if have:
            got = vf.to_numpy(have, INTERVAL_S)
            X = np.full((got.shape[0], len(CHANNELS)), np.nan)
            for j, c in enumerate(have):
                X[:, CHANNELS.index(c)] = got[:, j]
        np.savez_compressed(out, X=X.astype(np.float32),
                            present=np.array([c in names for c in CHANNELS]),
                            interval_s=INTERVAL_S, sha256=h, caseid=caseid)
    finally:
        if os.path.exists(raw):
            os.remove(raw)
    return out


def load_case(caseid):
    d = np.load(os.path.join(CACHE, f"{caseid:04d}.npz"))
    return {"caseid": int(d["caseid"]), "X": d["X"].astype(np.float64),
            "present": d["present"], "interval_s": int(d["interval_s"]),
            "sha256": str(d["sha256"])}


def _worker(args):
    c, = args
    try:
        fetch_case(c)
        d = np.load(os.path.join(CACHE, f"{c:04d}.npz"))
        return c, {"sha256": str(d["sha256"]), "shape": list(d["X"].shape),
                   "present": [bool(b) for b in d["present"]]}
    except Exception as e:
        return c, {"error": f"{type(e).__name__}: {str(e)[:120]}"}


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "calibration"
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ids = split()[which]
    from multiprocessing import Pool
    man = {}
    with Pool(nproc) as pool:
        for i, (c, rec) in enumerate(pool.imap_unordered(
                _worker, [(c,) for c in ids], chunksize=1)):
            man[c] = rec
            if (i + 1) % 20 == 0:
                ok = sum(1 for v in man.values() if "sha256" in v)
                print(f"  {i+1}/{len(ids)}  ok={ok}", flush=True)
    p = os.path.join(RESULTS, f"sd_manifest_{which}.json")
    json.dump({str(k): man[k] for k in sorted(man)}, open(p, "w"), indent=1)
    ok = sum(1 for v in man.values() if "sha256" in v)
    print(f"{which}: {ok}/{len(ids)} fetched -> {p}")
