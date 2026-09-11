"""
vitaldb_fetch.py — download VitalDB cases, extract the frozen channel set,
record a SHA-256 for provenance, then delete the raw file.

Raw .vital files are tens of megabytes each and are not retained. What is kept
is a compact per-case .npz plus the hash of the source file, which is enough to
identify exactly what was analysed without storing the dataset.
"""
from __future__ import annotations
import hashlib, json, os, sys, urllib.request
import numpy as np

_HERE = os.path.dirname(__file__)
sys.path.insert(0, _HERE)
from vitaldb_cohort import BASE_URL, CHANNELS, INTERVAL_S, DATA, split  # noqa

CACHE = os.path.join(DATA, "npz")


def fetch_case(caseid, keep_raw=False):
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, f"{caseid:04d}.npz")
    if os.path.exists(out):
        return out
    url = f"{BASE_URL}/vital_files/{caseid:04d}.vital"
    raw = os.path.join("/tmp", f"{caseid:04d}.vital")
    urllib.request.urlretrieve(url, raw)
    h = hashlib.sha256(open(raw, "rb").read()).hexdigest()
    import vitaldb
    vf = vitaldb.VitalFile(raw)
    have = [c for c in CHANNELS if c in vf.get_track_names()]
    X = vf.to_numpy(have, INTERVAL_S) if have else np.zeros((0, 0))
    np.savez_compressed(out, X=X, channels=np.array(have),
                        interval_s=INTERVAL_S, sha256=h, caseid=caseid)
    if not keep_raw:
        os.remove(raw)
    return out


def load_case(caseid):
    d = np.load(os.path.join(CACHE, f"{caseid:04d}.npz"), allow_pickle=False)
    return {"caseid": int(d["caseid"]), "X": d["X"],
            "channels": [str(c) for c in d["channels"]],
            "interval_s": int(d["interval_s"]), "sha256": str(d["sha256"])}


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "calibration"
    ids = split()[which]
    man = {}
    for i, c in enumerate(ids):
        try:
            fetch_case(c)
            d = load_case(c)
            man[c] = {"sha256": d["sha256"], "shape": list(d["X"].shape),
                      "channels": d["channels"]}
            if (i + 1) % 10 == 0:
                print(f"  {i+1}/{len(ids)}", flush=True)
        except Exception as e:
            man[c] = {"error": str(e)[:120]}
            print(f"  case {c}: {e}", flush=True)
    p = os.path.join(_HERE, "..", "results", f"vitaldb_manifest_{which}.json")
    json.dump(man, open(p, "w"), indent=1)
    ok = sum(1 for v in man.values() if "sha256" in v)
    print(f"{which}: fetched {ok}/{len(ids)}; manifest -> {p}")
