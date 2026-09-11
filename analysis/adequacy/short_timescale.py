"""
short_timescale.py — perturbation-response relaxation on compatible timescales.

Implements docs/PROTOCOL_SHORT_TIMESCALE.md. Nothing here is tuned after
seeing confirmatory data.
"""
from __future__ import annotations
import numpy as np

DT = 2.0                                     # VitalDB numeric sampling, seconds
BANDS = {"A_seconds": (4.0, 20.0, 60.0),     # (tau_lo, tau_hi, window W)
         "B_tens": (20.0, 90.0, 300.0),
         "C_minutes": (90.0, 400.0, 1200.0)}
BASELINE_S = 30 * 60                         # first 30 min


# ---------------------------------------------------------------- predictors
def _acf(x, kmax):
    x = np.asarray(x, float)
    x = x - x.mean()
    d = np.dot(x, x)
    if d <= 0:
        return np.zeros(kmax)
    return np.array([np.dot(x[:-k], x[k:]) / d for k in range(1, kmax + 1)])


def tau_ac1(x, dt=DT):
    r = _acf(x, 1)[0]
    r = min(max(r, 1e-6), 0.999999)
    return -dt / np.log(r)


def tau_int(x, dt=DT, kmax=None):
    """Integrated autocorrelation time, summed to first zero crossing."""
    kmax = kmax or min(len(x) // 4, 2000)
    r = _acf(x, kmax)
    z = np.argmax(r <= 0) if np.any(r <= 0) else len(r)
    return dt * (1.0 + 2.0 * float(np.sum(r[:z])))


def tau_hwhm(x, dt=DT, kmax=None):
    kmax = kmax or min(len(x) // 4, 2000)
    r = _acf(x, kmax)
    b = np.argmax(r <= 0.5) if np.any(r <= 0.5) else len(r)
    return dt * max(b, 1)


# ------------------------------------------------------------ perturbations
def find_perturbations(x, W, dt=DT, k_mad=4.0, quiet_mad=1.5, max_events=12):
    """
    Local extrema exceeding 4 MAD, preceded by a quiet window and followed by
    decay to below half amplitude. Uses no baseline rate.
    """
    n = len(x)
    w = int(W / dt)
    half = max(w // 2, 5)
    win = min(max(10 * w, 200), n)
    if n < win + 2 * w:
        return []
    # rolling robust centre/scale via coarse blocks (cheap, adequate)
    step = max(w // 2, 5)
    centres = np.arange(0, n, step)
    med = np.interp(np.arange(n), centres,
                    [np.median(x[max(0, c - win // 2):c + win // 2 + 1]) for c in centres])
    mad = np.interp(np.arange(n), centres,
                    [np.median(np.abs(x[max(0, c - win // 2):c + win // 2 + 1]
                                      - np.median(x[max(0, c - win // 2):c + win // 2 + 1])))
                     + 1e-9 for c in centres])
    dev = np.abs(x - med) / mad
    ev, i = [], half
    while i < n - w - 1:
        if dev[i] > k_mad and dev[i] >= dev[max(0, i - 3):i + 4].max():
            pre = dev[i - half:i]
            post = dev[i:i + w + 1]
            if pre.size and pre.max() < quiet_mad and post[-1] < 0.5 * dev[i]:
                ev.append(i)
                i += w
                if len(ev) >= max_events:
                    break
                continue
        i += 1
    return [(i, float(med[i]), float(mad[i])) for i in ev]


def tau_mrt(x, i, level, W, dt=DT):
    """Mean residence time from the excursion peak. Model-free."""
    w = int(W / dt)
    seg = x[i:i + w + 1] - level
    if seg.size < 4:
        return np.nan
    amp = seg[0]
    if abs(amp) < 1e-9:
        return np.nan
    frac = seg / amp
    frac = np.clip(frac, 0.0, None)          # ignore overshoot below baseline
    return float(np.sum(frac) * dt)


def tau_exp_free(x, i, level, W, dt=DT):
    """Free-rate exponential fit to the same excursion (comparator C3)."""
    w = int(W / dt)
    seg = x[i:i + w + 1] - level
    if seg.size < 5 or abs(seg[0]) < 1e-9:
        return np.nan
    y = seg / seg[0]
    t = np.arange(len(y)) * dt
    ok = y > 0.02
    if ok.sum() < 4:
        return np.nan
    s, _ = np.polyfit(t[ok], np.log(y[ok]), 1)
    return float(-1.0 / s) if s < 0 else np.nan


def tau_stretched(x, i, level, W, dt=DT):
    """Stretched exponential exp(-(t/tau)^b): returns tau (comparator C4)."""
    w = int(W / dt)
    seg = x[i:i + w + 1] - level
    if seg.size < 6 or abs(seg[0]) < 1e-9:
        return np.nan
    y = np.clip(seg / seg[0], 1e-3, None)
    t = np.arange(len(y)) * dt
    ok = (y > 0.02) & (t > 0)
    if ok.sum() < 5:
        return np.nan
    b, a = np.polyfit(np.log(t[ok]), np.log(-np.log(y[ok])), 1)
    return float(np.exp(-a / b)) if b > 0 else np.nan
