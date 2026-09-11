"""
fast_ac.py -- a reduced fast path for the autocorrelation grid used ONLY by the
200-permutation destructive controls.

It must produce output BIT-IDENTICAL to variability.grids(...)["ac"]. The frozen
grids() also computes spectral edge, band-power ratio and permutation entropy,
none of which the controls need and none of which consume RNG. This replicates
grids()'s loop order and its exact sequence of rng.permutation calls, skipping
only the unused computations.

This is an optimisation, not a specification change -- the same device used
earlier in this programme for the AR(1) simulator, and verified the same way:
by asserting bit-identity against the frozen implementation before use.
"""
from __future__ import annotations
import os, sys
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
import variability as V  # noqa
sys.path.insert(0, os.path.join(_H, "..", "structural"))
import windows as W  # noqa


def ac_grid(prep, i0, i1, shuffle_within_window, seed):
    """Identical to variability.grids(...)["ac"], computed without the unused
    spectral and entropy terms. RNG call order is preserved exactly."""
    rng = np.random.default_rng(seed)
    Xi = prep["Xi"]
    step = int(V.STRIDE_S / W.DT)
    vw = int(V.VAR_WIN_S / W.DT)
    start = prep["b1"] + vw
    ts = np.arange(start, min(i1, Xi.shape[0]) + 1, step, dtype=int)
    ac = np.full((len(ts), V.P), np.nan)
    for k, t in enumerate(ts):
        Wn = Xi[t - vw:t]
        for i in range(V.P):
            col = Wn[:, i]
            f = col[np.isfinite(col)]
            if len(f) < 30:
                continue
            work = rng.permutation(f) if shuffle_within_window else f
            ac[k, i] = V._lag1(work)
    return ts, ac


def verify(prep, i0, i1, seed=12345):
    """Assert bit-identity with the frozen grids() in both modes."""
    for sh in (False, True):
        ts_f, ac_f = ac_grid(prep, i0, i1, sh, seed)
        G = V.grids(prep, i0, i1, shuffle_within_window=sh, seed=seed)
        assert np.array_equal(ts_f, G["t_idx"]), "grid times differ"
        a, b = ac_f, G["ac"]
        same = np.array_equal(a[np.isfinite(a)], b[np.isfinite(b)]) and \
            np.array_equal(np.isfinite(a), np.isfinite(b))
        assert same, f"ac differs (shuffle={sh})"
    return True
