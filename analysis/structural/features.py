"""
features.py -- assemble the frozen feature sets and the structural metric.

Every feature here is computed from samples at or before its evaluation
point t. Nothing reads forward.
"""
from __future__ import annotations
import os, sys
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
from cohort import SHORT  # noqa

P = len(SHORT)


# ------------------------------------------------------------- the metric S(t)
def metric_inverse(Sigma0, kind, rng=None, other=None):
    """The matrix that plays the role of Sigma_0^{-1} in S(t).

    kind:
      patient   -- inv(Sigma_0) for this patient                     (primary)
      diagonal  -- inv(diag(Sigma_0)): pure per-channel rescaling
      identity  -- scaled identity matching mean precision
      shuffled  -- off-diagonals randomly permuted, nearest-PSD projected
      subject   -- another patient's Sigma_0 (passed as `other`)
      population-- pooled training-fold Sigma_0 (passed as `other`)
    """
    if kind == "patient":
        M = Sigma0
    elif kind == "diagonal":
        M = np.diag(np.diag(Sigma0))
    elif kind == "identity":
        M = np.eye(P) * (np.trace(Sigma0) / P)
    elif kind == "shuffled":
        M = _shuffle_offdiag(Sigma0, rng)
    elif kind in ("subject", "population"):
        M = other
    else:
        raise ValueError(kind)
    return np.linalg.inv(M)


def _shuffle_offdiag(S, rng):
    """Permute the off-diagonal entries, keep the diagonal, restore symmetry,
    then project to the nearest PSD matrix with a small ridge so it inverts."""
    p = S.shape[0]
    iu = np.triu_indices(p, 1)
    vals = rng.permutation(S[iu])
    M = np.diag(np.diag(S)).astype(float)
    M[iu] = vals
    M[(iu[1], iu[0])] = vals
    w, V = np.linalg.eigh(M)
    w = np.maximum(w, 1e-6 * np.trace(S) / p)
    return V @ np.diag(w) @ V.T


def S_literal(Pinv, delta):
    return float(np.linalg.norm(Pinv @ delta))


def S_mahalanobis(Pinv, delta):
    q = float(delta @ Pinv @ delta)
    return float(np.sqrt(max(q, 0.0)))


# ------------------------------------------------------------------ feature sets
def row_blocks(r, prep):
    """Per-window building blocks. All marginal except `cov`."""
    d, z = r["delta"], r["z"]
    sd = np.nan_to_num(r["sd_w"], nan=0.0)
    sl = np.nan_to_num(r["slope"], nan=0.0)
    sig = prep["sigma"]
    b = {
        "absdelta": np.abs(d),
        "absz": np.abs(z),
        "maxz": np.array([np.max(np.abs(z))]),
        "aggz": np.array([np.sum(np.abs(z)), np.linalg.norm(z)]),
        "disp": np.concatenate([sig, sd]),
        "slope": sl,
        "raw": np.concatenate([r["x"], prep["mu0"]]),
        "signed": np.concatenate([d, z]),
    }
    b["cov"] = _cov_block(r["cov_w"], prep["Sigma0"])
    return b


def _cov_block(Cw, S0):
    """Covariance-drift / DNB-style features. Cross-channel, no whitening."""
    if Cw is None:
        return np.zeros(3)
    drift = np.linalg.norm(Cw - S0, "fro") / max(np.linalg.norm(S0, "fro"), 1e-12)
    dw = np.sqrt(np.clip(np.diag(Cw), 1e-12, None))
    R = Cw / np.outer(dw, dw)
    iu = np.triu_indices(P, 1)
    mean_abs_corr = float(np.mean(np.abs(R[iu])))
    d0 = np.sqrt(np.clip(np.diag(S0), 1e-12, None))
    # DNB composite: within-group correlation x dispersion, relative to baseline
    dnb = mean_abs_corr * float(np.mean(dw / d0))
    return np.array([drift, mean_abs_corr, dnb])


SETS = {
    "M1_raw_marginal":  ["absdelta"],
    "M2_z_marginal":    ["absz"],
    "M4_agg_z":         ["aggz"],
    "M5_dispersion":    ["disp"],
    "M6_trend":         ["slope"],
    "M7_cov_drift":     ["cov"],
    "M8_marginal_LR":   ["signed", "slope", "disp"],
    "M9_strong_marginal": ["raw", "signed", "absdelta", "absz", "disp",
                           "slope", "aggz", "maxz"],
}
M9 = SETS["M9_strong_marginal"]


def design(blocks_list, keys, extra=None):
    X = np.array([np.concatenate([b[k] for k in keys]) for b in blocks_list])
    if extra is not None:
        X = np.hstack([X, np.asarray(extra).reshape(len(X), -1)])
    return np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
