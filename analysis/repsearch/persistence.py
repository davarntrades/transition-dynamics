"""
persistence.py -- Candidate family 1: deformation persistence.

    Q_i(t) = || dG_i(t) ||  *  tau_i(t)

tau_i is operationalised STRICTLY as the duration for which a measurable
displacement of channel i has persisted. No consciousness, qualia, stiffness,
homeostatic or mechanistic reading is attached, asserted or tested.

Two implementation points that decide whether the test is honest:

1. tau is computed on a CONTINUOUS 60 s grid spanning the whole analysable
   interval, independent of the label-exclusion rules. Computing run-lengths
   only over retained evaluation points would break runs wherever a window was
   dropped for being hypotensive or refractory, manufacturing structure.

2. tau is capped at a bounded lookback L and carries a saturation indicator.
   Uncapped, tau grows with time-into-case and would proxy for elapsed time --
   which is why elapsed time is also placed in the BASELINE, not here.
"""
from __future__ import annotations
import os, sys
import numpy as np

_S = os.path.join(os.path.dirname(__file__), "..", "structural")
sys.path.insert(0, _S)
import windows as W  # noqa
from cohort import SHORT  # noqa

P = len(SHORT)
STRIDE_S = 60
MED_S = 60


def z_grid(prep, i0, i1):
    """Continuous 60 s-stride z-series over the analysable interval.

    Returns (times_idx, Z) where Z[k, i] is the z-score of channel i from the
    60 s median ending at times_idx[k]. Uses only samples at or before that
    time. Rows with any non-finite channel are marked by `ok`.
    """
    Xi = prep["Xi"]
    mu0, sig = prep["mu0"], prep["sigma"]
    step = int(STRIDE_S / W.DT)
    med_n = int(MED_S / W.DT)
    start = prep["b1"] + med_n
    ts = np.arange(start, min(i1, Xi.shape[0]) + 1, step, dtype=int)
    Z = np.full((len(ts), P), np.nan)
    for k, t in enumerate(ts):
        tail = Xi[t - med_n:t]
        with np.errstate(invalid="ignore"):
            m = np.where(np.isfinite(tail).any(axis=0),
                         np.nanmedian(np.where(np.isfinite(tail), tail, np.nan),
                                      axis=0), np.nan)
        Z[k] = (m - mu0) / sig
    return ts, Z


def run_lengths(Z, theta, max_steps):
    """R[k, i] = number of consecutive steps up to and including k for which
    |Z[.,i]| > theta, capped at max_steps. A non-finite sample breaks the run.

    Causal by construction: R[k] depends only on rows <= k.
    """
    n, p = Z.shape
    R = np.zeros((n, p), dtype=float)
    A = np.isfinite(Z) & (np.abs(Z) > theta)
    for i in range(p):
        r = 0
        for k in range(n):
            r = min(r + 1, max_steps) if A[k, i] else 0
            R[k, i] = r
    return R


def persistence_features(prep, i0, i1, theta, lookback_min):
    """tau (minutes), Q = |z| * tau, and saturation flags, indexed by sample."""
    ts, Z = z_grid(prep, i0, i1)
    max_steps = int(lookback_min * 60 / STRIDE_S)
    R = run_lengths(Z, theta, max_steps)
    tau = R * (STRIDE_S / 60.0)                       # minutes
    absz = np.nan_to_num(np.abs(Z), nan=0.0)
    Q = absz * tau
    sat = (R >= max_steps).astype(float)
    return {"t_idx": ts, "tau": tau, "Q": Q, "sat": sat, "Z": Z,
            "theta": theta, "lookback_min": lookback_min, "max_steps": max_steps}


def lookup(pf, t_idx):
    """Nearest grid point at or before t_idx. Never reads forward."""
    k = np.searchsorted(pf["t_idx"], t_idx, side="right") - 1
    return None if k < 0 else k


def blocks_for(pf, k):
    """The candidate's feature block at grid index k."""
    tau, Q, sat = pf["tau"][k], pf["Q"][k], pf["sat"][k]
    return {
        "tau": np.log1p(tau),
        "Q": np.log1p(Q),
        "tau_agg": np.array([np.log1p(tau.max()), np.log1p(tau.sum()),
                             float(sat.sum())]),
        "Q_agg": np.array([np.log1p(Q.max()), np.log1p(Q.sum()),
                           np.log1p(np.linalg.norm(Q))]),
    }


def shuffled_persistence(pf, rng, lookback_steps):
    """DECISIVE CONTROL. Recompute tau from the same channel's z-values with
    their ORDER destroyed inside the lookback window: the marginal distribution
    of |z| over that window is preserved exactly, only the run structure is
    broken. If the shuffled version predicts as well, what carries the signal is
    how displaced the channel has been on average -- not for how long
    continuously. This is the direct analogue of the covariance shuffle that
    settled the S(t) experiment.
    """
    Z = pf["Z"]
    n, p = Z.shape
    tau = np.zeros((n, p))
    for k in range(n):
        lo = max(0, k - lookback_steps + 1)
        w = Z[lo:k + 1]
        perm = rng.permutation(w.shape[0])
        ws = w[perm]
        A = np.isfinite(ws) & (np.abs(ws) > pf["theta"])
        for i in range(p):
            r = 0
            for j in range(A.shape[0]):
                r = r + 1 if A[j, i] else 0
            tau[k, i] = min(r, pf["max_steps"]) * (STRIDE_S / 60.0)
    absz = np.nan_to_num(np.abs(Z), nan=0.0)
    return {"t_idx": pf["t_idx"], "tau": tau, "Q": absz * tau,
            "sat": np.zeros_like(tau), "Z": Z, "theta": pf["theta"],
            "lookback_min": pf["lookback_min"], "max_steps": pf["max_steps"]}
