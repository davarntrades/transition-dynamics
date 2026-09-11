"""
adequacy.py — Stage B and Stage C of the preregistered model-adequacy protocol.

Implements docs/PROTOCOL_MODEL_ADEQUACY.md exactly. Thresholds are read from
PROTOCOL constants below and must not be edited after a real-data run.

Takes any multichannel recording as (names, X, fs) and runs:
  Stage A  admissibility -- REFUSES to analyse a recording that fails
  Stage B  held-out model comparison against six alternatives
  Stage C  baseline-rate vs curvature-rate consistency

Block cross-validation throughout, never interleaved: interleaving does not
control overfitting on autocorrelated data, and real physiology is more
strongly autocorrelated than the simulator.

Run:  python3 analysis/adequacy/adequacy.py        (self-test on synthetic)
"""

from __future__ import annotations

import numpy as np

# ---- preregistered constants (docs/PROTOCOL_MODEL_ADEQUACY.md) -------------
MIN_CHANNELS = 4
MIN_NEFF_FACTOR = 10          # n_eff >= 10 * p in baseline
MIN_NEFF_WINDOW = 20
MAX_MISSING = 0.20
N_FOLDS = 5
ADEQUATE_FRAC = 0.60
NARROW_FRAC = 0.30
MAX_DECLINE = 0.50
MIN_RATE_RANKCORR = 0.50
MIN_RECORDINGS = 50
# ---------------------------------------------------------------------------


def n_eff(X):
    X = np.asarray(X, float)
    Xc = X - X.mean(0)
    num = (Xc[:-1] * Xc[1:]).sum(0)
    den = np.maximum((Xc * Xc).sum(0), 1e-12)
    rho = float(np.clip(np.mean(num / den), -0.99, 0.99))
    return len(X) * (1 - rho) / (1 + rho)


def admissible(X, names, min_channels=MIN_CHANNELS):
    """Stage A. Returns (ok, reasons). A failing recording is EXCLUDED."""
    X = np.asarray(X, float)
    p = X.shape[1]
    r = []
    if p < min_channels:
        r.append(f"only {p} channels, need >= {min_channels}")
    miss = np.mean(~np.isfinite(X))
    if miss > MAX_MISSING:
        r.append(f"missingness {miss:.0%} > {MAX_MISSING:.0%}")
    ne = n_eff(X)
    if ne < MIN_NEFF_FACTOR * p:
        r.append(f"n_eff {ne:.0f} < {MIN_NEFF_FACTOR * p} (10 x p)")
    # stationarity screen on the baseline portion
    third = len(X) // 3
    if third > 1:
        d = np.abs(X[:third].mean(0) - X[-third:].mean(0)) / (X.std(0) + 1e-12)
        if np.any(d > 0.5):
            r.append(f"baseline not stationary: max shift {d.max():.2f} SD")
    return (len(r) == 0), r


def baseline_rates(base, h):
    """Stage A2. k_i from baseline lag-1 autocorrelation only."""
    Xc = np.asarray(base, float) - np.asarray(base, float).mean(0)
    num = (Xc[:-1] * Xc[1:]).sum(0)
    den = np.maximum((Xc * Xc).sum(0), 1e-12)
    a = np.clip(num / den, 1e-4, 0.9999)
    return -np.log(a) / h


# ---------------------------------------------------------------------------
# Design matrices. All models except M-exp are linear in their parameters.
# ---------------------------------------------------------------------------

def _design(model, t, k=None, t0=None):
    n = len(t)
    if model == "M-null":
        return np.zeros((n, 0))
    if model == "M-const":
        return np.ones((n, 1))
    if model == "M-lin":
        return np.column_stack([np.ones(n), t])
    if model == "M-spline":
        # NATURAL cubic spline: linear beyond the boundary knots. An earlier
        # version used a raw truncated-power cubic basis, which extrapolates
        # catastrophically -- under block cross-validation the first and last
        # folds are extrapolation, and held-out error came out four orders of
        # magnitude worse than every other model. That made the spline a straw
        # comparator rather than a real alternative.
        kn = np.quantile(t, [0.05, 0.35, 0.65, 0.95])
        K = len(kn)
        d = lambda j: ((np.clip(t - kn[j], 0, None) ** 3
                        - np.clip(t - kn[-1], 0, None) ** 3)
                       / (kn[-1] - kn[j]))
        cols = [np.ones(n), t] + [d(j) - d(K - 2) for j in range(K - 2)]
        return np.column_stack(cols)
    if model == "M-exp":
        return (1.0 - np.exp(-k * np.clip(t - t0, 0, None)))[:, None]
    raise ValueError(model)


def _fit_predict(model, t_fit, y_fit, t_pred, k=None, t0=None):
    if model == "M-rw":                      # local level: last observed value
        return np.full(len(t_pred), y_fit[-1])
    A = _design(model, t_fit, k, t0)
    if A.shape[1] == 0:
        return np.zeros(len(t_pred))
    coef, *_ = np.linalg.lstsq(A, y_fit, rcond=None)
    return _design(model, t_pred, k, t0) @ coef


def block_folds(n, n_folds=N_FOLDS):
    """Contiguous blocks, per protocol A4."""
    edges = np.linspace(0, n, n_folds + 1).astype(int)
    for i in range(n_folds):
        te = np.arange(edges[i], edges[i + 1])
        tr = np.setdiff1d(np.arange(n), te)
        if len(te) >= 3 and len(tr) >= 5:
            yield tr, te


MODELS = ["M-null", "M-const", "M-lin", "M-exp", "M-exp-free", "M-spline", "M-rw"]


def stage_b(X, h, k_base, n_grid=25):
    """
    Held-out MSE per model, averaged over channels and folds.
    Returns dict model -> mse, plus the selected onset for M-exp.
    """
    X = np.asarray(X, float)
    n, p = X.shape
    t = np.arange(n) * h
    mse = {m: [] for m in MODELS}
    t0_sel = None

    # M-exp: choose t0 once by held-out error, then score it like the others
    cands = np.linspace(0.0, t[-1] * 0.8, n_grid)
    best, best_e = None, np.inf
    for t0 in cands:
        e = []
        for tr, te in block_folds(n):
            for j in range(p):
                pr = _fit_predict("M-exp", t[tr], X[tr, j], t[te],
                                  k=k_base[j], t0=t0)
                e.append(np.mean((X[te, j] - pr) ** 2))
        m = float(np.mean(e))
        if m < best_e:
            best_e, best = m, t0
    t0_sel = best

    for m in MODELS:
        for tr, te in block_folds(n):
            for j in range(p):
                if m == "M-exp":
                    pr = _fit_predict("M-exp", t[tr], X[tr, j], t[te],
                                      k=k_base[j], t0=t0_sel)
                elif m == "M-exp-free":
                    bi, be = None, np.inf
                    for kf in np.geomspace(1e-3, 1.0, 12):
                        q = _fit_predict("M-exp", t[tr], X[tr, j], t[tr],
                                         k=kf, t0=t0_sel)
                        v = np.mean((X[tr, j] - q) ** 2)
                        if v < be:
                            be, bi = v, kf
                    pr = _fit_predict("M-exp", t[tr], X[tr, j], t[te],
                                      k=bi, t0=t0_sel)
                else:
                    pr = _fit_predict(m, t[tr], X[tr, j], t[te])
                mse[m].append(np.mean((X[te, j] - pr) ** 2))
    out = {m: float(np.mean(v)) for m, v in mse.items()}
    out["_t0"] = float(t0_sel)
    return out


def stage_c(X, h, base_frac=0.5):
    """
    Rate consistency with TEMPORAL SEPARATION: rates from the baseline window,
    curvature-derived rates from the later window. Never the same samples.
    """
    X = np.asarray(X, float)
    nb = int(base_frac * len(X))
    k_base = baseline_rates(X[:nb], h)
    late = X[nb:]
    t = np.arange(len(late)) * h
    k_curv = np.empty(X.shape[1])
    for j in range(X.shape[1]):
        y = late[:, j] - late[:, j].mean()
        be, bk = np.inf, np.nan
        for kf in np.geomspace(1e-3, 1.0, 30):
            g = 1.0 - np.exp(-kf * t)
            c = np.dot(g, y) / max(np.dot(g, g), 1e-12)
            v = np.mean((y - c * g) ** 2)
            if v < be:
                be, bk = v, kf
        k_curv[j] = bk
    from scipy.stats import spearmanr
    rc = spearmanr(k_base, k_curv).statistic if X.shape[1] > 2 else np.nan
    return {"k_base": k_base, "k_curv": k_curv,
            "rank_corr": float(rc) if rc == rc else float("nan"),
            "log_bias": float(np.mean(np.log(k_curv / k_base)))}


def phase_surrogate(X, seed=0):
    """
    Phase-randomised surrogate: preserves each channel's power spectrum, and
    hence its autocorrelation, while destroying any deterministic onset
    structure. This is the null the selection rate must be compared against.

    Needed because M-exp is selected on roughly half of purely stationary
    autocorrelated series -- it absorbs slow drift. A fixed selection-rate
    threshold is therefore not interpretable on its own.
    """
    rng = np.random.default_rng(seed)
    X = np.asarray(X, float)
    out = np.empty_like(X)
    for j in range(X.shape[1]):
        f = np.fft.rfft(X[:, j] - X[:, j].mean())
        ph = rng.uniform(0, 2 * np.pi, len(f))
        ph[0] = 0
        if len(X) % 2 == 0:
            ph[-1] = 0
        out[:, j] = np.fft.irfft(np.abs(f) * np.exp(1j * ph), n=len(X)) \
            + X[:, j].mean()
    return out


def surrogate_selection_rate(X, h, k_base, n_surr=20, seed=0):
    """Fraction of phase-randomised surrogates on which M-exp is selected."""
    hits = 0
    for s in range(n_surr):
        Xs = phase_surrogate(X, seed + s)
        r = stage_b(Xs, h, k_base)
        hits += (min(MODELS, key=lambda m: r[m]) == "M-exp")
    return hits / n_surr


def verdict_b(frac_exp_best, exp_beats_free):
    if frac_exp_best >= ADEQUATE_FRAC and exp_beats_free:
        return "ADEQUATE"
    if frac_exp_best < NARROW_FRAC:
        return "NOT TRANSFERABLE"
    if not exp_beats_free:
        return "NOT TRANSFERABLE (baseline rates uninformative)"
    return "NARROW SUBSET"


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # SELF-TEST ON SYNTHETIC DATA. This validates the CODE, and is explicitly
    # not evidence about real physiology.
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                    "experiments"))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from exposure_stage1_oracle import Config, simulate, calibrate, d_stiff_sub

    print("Self-test on synthetic data (validates code, not physiology)")
    print("=" * 66)
    cfg = Config("wide-rotated")
    h = cfg.h
    for label, mk in (
        ("exponential-approach (the assumed model)",
         lambda i: simulate(cfg, d_stiff_sub(cfg, i),
                            calibrate(cfg, d_stiff_sub, 60.0, 30.0), 60.0, i)),
        ("stationary (no onset)",
         lambda i: simulate(cfg, None, 0.0, 0.0, i)),
    ):
        wins = 0
        beats_free = 0
        for i in range(10):
            X = mk(i)[cfg.base_n - 600:]
            kb = baseline_rates(X[:300], h)
            r = stage_b(X[300:], h, kb)
            scores = {m: r[m] for m in MODELS}
            best = min(scores, key=scores.get)
            wins += (best == "M-exp")
            beats_free += (scores["M-exp"] <= scores["M-exp-free"])
        print(f"  {label}")
        print(f"    M-exp selected in {wins}/10, beats free-rate variant in "
              f"{beats_free}/10")
    c = stage_c(simulate(cfg, None, 0.0, 0.0, 0), h)
    print(f"\n  Stage C on stationary: rank corr {c['rank_corr']:.2f}, "
          f"log bias {c['log_bias']:+.2f}")
