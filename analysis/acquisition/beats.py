"""
beats.py -- beat-aligned arterial pressure derivation and the frozen
acquisition-injection transformation.

Beat detection is strictly UPSTREAM of injection: W and W+inj share the same
detected beats and the same per-beat means, so the only difference between them
is the injected acquisition process.
"""
from __future__ import annotations
import numpy as np

FS = 500
BIN_S = 2.0

# --- beat-detector specification (frozen after pilot) ---------------------
MIN_RR_S = 0.25          # 240 bpm ceiling
MAX_RR_S = 2.00          # 30 bpm floor
MIN_PP = 10.0            # mmHg, minimum pulse pressure for a valid beat
MAX_PP = 150.0
MIN_MEAN, MAX_MEAN = 20.0, 180.0
MAX_ABS, MIN_ABS = 300.0, -20.0


def _lowpass(x, fs=FS, fc=10.0):
    """Zero-phase moving-average lowpass. No SciPy dependency, no edge bias."""
    n = max(3, int(round(fs / fc)))
    k = np.ones(n) / n
    y = np.convolve(x, k, mode="same")
    return np.convolve(y[::-1], k, mode="same")[::-1]


def detect_beats(w, fs=FS):
    """Systolic peaks by derivative upstroke with a refractory period.
    Returns beat boundary indices (diastolic minima) and per-beat statistics."""
    ok = np.isfinite(w)
    if ok.sum() < fs * 5:
        return None
    x = np.where(ok, w, np.nan)
    x = np.nan_to_num(x, nan=np.nanmedian(x))
    s = _lowpass(x, fs)
    d = np.diff(s, prepend=s[0])
    thr = np.percentile(d, 98) * 0.3
    if not np.isfinite(thr) or thr <= 0:
        return None
    cand = np.flatnonzero((d[:-1] <= thr) & (d[1:] > thr))
    refr = int(MIN_RR_S * fs)
    ups = []
    for c in cand:
        if not ups or c - ups[-1] >= refr:
            ups.append(c)
    ups = np.array(ups, dtype=int)
    if len(ups) < 3:
        return None
    # diastolic minimum just before each upstroke bounds the beat
    bounds = []
    for u in ups:
        lo = max(0, u - int(0.15 * fs))
        bounds.append(lo + int(np.argmin(s[lo:u + 1])) if u > lo else u)
    bounds = np.unique(np.array(bounds, dtype=int))
    beats = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        seg = w[a:b]
        seg = seg[np.isfinite(seg)]
        dur = (b - a) / fs
        if len(seg) < 5 or not (MIN_RR_S <= dur <= MAX_RR_S):
            continue
        mx, mn = float(seg.max()), float(seg.min())
        mean = float(seg.mean())
        pp = mx - mn
        if not (MIN_PP <= pp <= MAX_PP and MIN_MEAN <= mean <= MAX_MEAN
                and mx < MAX_ABS and mn > MIN_ABS):
            continue
        beats.append((a / fs, b / fs, mean, mx, mn))
    return np.array(beats) if beats else None


def bin_beats(beats, n_bins, bin_s=BIN_S, col=2):
    """Average per-beat values into fixed bins by beat midpoint.
    Bins containing no valid beat are NaN -- never interpolated."""
    out = np.full(n_bins, np.nan)
    if beats is None or len(beats) == 0:
        return out
    mid = (beats[:, 0] + beats[:, 1]) / 2.0
    idx = np.floor(mid / bin_s).astype(int)
    g = (idx >= 0) & (idx < n_bins)
    idx, val = idx[g], beats[g, col]
    if len(idx) == 0:
        return out
    s = np.bincount(idx, weights=val, minlength=n_bins)
    c = np.bincount(idx, minlength=n_bins)
    nz = c > 0
    out[nz] = s[nz] / c[nz]
    return out


# --- frozen acquisition-injection transformation --------------------------
def inject(series, quant_mmhg, hold_s, bin_s=BIN_S):
    """Apply a KNOWN acquisition process downstream of W.

    quant_mmhg : quantisation step, or None for no quantisation
    hold_s     : refresh cadence; the value updates every hold_s seconds and is
                 held (zero-order) in between. hold_s == bin_s means no hold.

    Missing values are held like any other sample only if the source bin was
    missing at a refresh instant; they are never invented.
    """
    x = np.asarray(series, float).copy()
    step = int(round(hold_s / bin_s))
    if step > 1:
        out = np.full_like(x, np.nan)
        for start in range(0, len(x), step):
            out[start:start + step] = x[start]
        x = out
    if quant_mmhg:
        x = np.where(np.isfinite(x), np.round(x / quant_mmhg) * quant_mmhg, np.nan)
    return x


def lag1(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 120:
        return np.nan
    x = x - x.mean()
    d = np.dot(x, x)
    return np.dot(x[:-1], x[1:]) / d if d > 0 else np.nan
