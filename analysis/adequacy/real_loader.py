"""
real_loader.py — derive slow physiological channels from real recordings.

The framework operates on vital-sign-like channels sampled on the order of
seconds, not on raw waveforms. This module turns raw recordings into that
representation so the onset model is tested on the kind of signal it is
actually meant for.

Derived channels (all ~1 Hz):
    HR        instantaneous heart rate from ECG R-peaks
    HRV_SD    rolling short-term heart-rate variability
    RSP_RATE  respiration rate from RSP zero-crossings
    RSP_AMP   rolling respiration amplitude
    EDA_TON   tonic electrodermal level (slow component)

DATA PROVENANCE. Real human recordings from the NeuroKit project
(https://github.com/neuropsychology/NeuroKit, data/), 100 Hz, resting and
event-related protocols in healthy adults. These contain NO clinical
deterioration and NO transition events. They support only the reduced
pre-check defined in docs/PROTOCOL_MODEL_ADEQUACY.md, never a claim about
pre-transition dynamics.
"""

from __future__ import annotations

import numpy as np


def _rpeaks(ecg, fs):
    """Simple, dependency-free R-peak detector: bandpass-ish diff, then peaks."""
    x = np.asarray(ecg, float)
    x = x - np.convolve(x, np.ones(int(0.6 * fs)) / (0.6 * fs), mode="same")
    d = np.diff(x, prepend=x[0])
    e = d ** 2
    e = np.convolve(e, np.ones(int(0.08 * fs)) / (0.08 * fs), mode="same")
    thr = np.percentile(e, 98) * 0.35
    cand = np.where(e > thr)[0]
    if len(cand) == 0:
        return np.array([], int)
    peaks, grp = [], [cand[0]]
    for i in cand[1:]:
        if i - grp[-1] <= int(0.2 * fs):
            grp.append(i)
        else:
            peaks.append(grp[int(np.argmax(x[grp]))])
            grp = [i]
    peaks.append(grp[int(np.argmax(x[grp]))])
    return np.array(peaks, int)


def _rate_from_events(idx, n, fs, out_fs):
    """Interpolate an event-rate (per minute) onto a regular out_fs grid."""
    t_out = np.arange(0, n / fs, 1.0 / out_fs)
    if len(idx) < 3:
        return np.full(len(t_out), np.nan)
    t_ev = idx / fs
    rate = 60.0 / np.diff(t_ev)
    return np.interp(t_out, t_ev[1:], rate, left=rate[0], right=rate[-1])


def _roll(x, w):
    k = np.ones(w) / w
    return np.convolve(x, k, mode="same")


def derive_channels(raw: dict, fs: float = 100.0, out_fs: float = 1.0):
    """
    raw: {'ECG': array, 'RSP': array, 'EDA': array}
    Returns (names, X) with X shape (n_out, p).
    """
    n = len(next(iter(raw.values())))
    cols, names = [], []

    if "ECG" in raw:
        pk = _rpeaks(raw["ECG"], fs)
        hr = _rate_from_events(pk, n, fs, out_fs)
        cols += [hr, _roll(np.abs(np.diff(hr, prepend=hr[0])), int(20 * out_fs))]
        names += ["HR", "HRV_SD"]

    if "RSP" in raw:
        r = np.asarray(raw["RSP"], float)
        r = r - _roll(r, int(10 * fs))
        zc = np.where((r[:-1] < 0) & (r[1:] >= 0))[0]
        cols.append(_rate_from_events(zc, n, fs, out_fs))
        names.append("RSP_RATE")
        amp = _roll(np.abs(r), int(3 * fs))
        cols.append(np.interp(np.arange(0, n / fs, 1.0 / out_fs),
                              np.arange(n) / fs, amp))
        names.append("RSP_AMP")

    if "EDA" in raw:
        e = np.asarray(raw["EDA"], float)
        ton = _roll(e, int(15 * fs))
        cols.append(np.interp(np.arange(0, n / fs, 1.0 / out_fs),
                              np.arange(n) / fs, ton))
        names.append("EDA_TON")

    m = min(len(c) for c in cols)
    X = np.column_stack([c[:m] for c in cols])
    ok = np.isfinite(X).all(axis=1)
    return names, X[ok]


def load_csv(path):
    import csv
    with open(path) as fh:
        r = csv.reader(fh)
        hdr = next(r)
        rows = [[float(v) for v in row] for row in r]
    A = np.array(rows, float)
    out = {}
    for i, h in enumerate(hdr):
        key = h.strip().upper()
        if key in ("ECG", "RSP", "EDA"):
            out[key] = A[:, i]
    return out


if __name__ == "__main__":
    import os
    base = os.path.join(os.path.dirname(__file__), "..", "..", "data", "real")
    for f in ("bio_resting_8min_100hz.csv", "bio_eventrelated_100hz.csv"):
        raw = load_csv(os.path.join(base, f))
        names, X = derive_channels(raw)
        ac = [np.corrcoef(X[:-1, j], X[1:, j])[0, 1] for j in range(X.shape[1])]
        n_eff = len(X) * (1 - np.mean(ac)) / (1 + np.mean(ac))
        print(f"{f}")
        print(f"  channels {names}")
        print(f"  n={len(X)} at 1 Hz   mean lag-1 AC {np.mean(ac):.3f}   "
              f"n_eff {n_eff:.0f}  (need >= {10*X.shape[1]})")
        print(f"  lag-1 AC per channel {np.round(ac,3)}")
