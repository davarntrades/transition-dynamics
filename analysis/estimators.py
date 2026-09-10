"""
estimators.py — Reference estimators for the Transition Dynamics preregistration.

CRITICAL DISTINCTION ENFORCED THROUGHOUT THIS FILE
--------------------------------------------------
Every function here is a MEASUREMENT PROXY. None of them computes the
ORIGINAL MATHEMATICAL OBJECT.

  Original object                     Proxy implemented here
  ----------------------------------  ------------------------------------------
  H_k(Reach(X_t)) vs H_k(Reach(X_0))  metric drift of a windowed second-order
                                      structure estimate  (NOT a homology group)
  ΔG                                  affine-invariant Riemannian distance between
                                      covariance operators  (a scalar, not a group
                                      difference)
  Λ (stiffness reading)               baseline precision operator  Σ₀⁻¹
  Λ (recovery reading)                discrete restoring operator  I − A  from VAR(1)
  ‖ΛΔG‖                               deformation energy  √(δᵀ Σ₀⁻¹ δ)
  C(t) = ι(⋃ᵢ Nₜ(X,Iᵢ))               Betti numbers of the nerve of the
                                      co-deformation cover
  C ⟂ L                               [DEMOTED in v2 — see docs/DEMOTED_OBJECTS.md]
                                      retained only as exploratory decoupling

The substitutions above are declared, not silent. Section 2 of README.md states
exactly what each substitution costs in inferential strength.

Dependencies: numpy, scipy only. Deliberately no TDA library — persistent
homology is not used until the simpler estimators have been shown to fail.

VERSION 2 NOTE
-------------
Objects 1 (homological truth condition) and 6 (C ⟂ L) were DEMOTED after the
v1 audit and are no longer part of the primary hypothesis. Λ is now FROZEN as
Σ₀⁻¹ (see freeze_lambda below). The v2 additions begin at the section marked
"V2 ADDITIONS".

Run:  python3 analysis/estimators.py
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eigh, logm


# ----------------------------------------------------------------------------
# Second-order structure  (the ΔG substrate)
# ----------------------------------------------------------------------------

def shrunk_covariance(X: np.ndarray, alpha: float | None = None) -> np.ndarray:
    """
    Ledoit-Wolf style shrinkage toward a scaled identity.

    Required, not optional: at ICU sampling rates a window carries far too few
    samples for a well-conditioned p x p covariance, and an ill-conditioned
    Sigma makes every downstream distance unstable and non-reproducible.
    """
    X = np.asarray(X, dtype=float)
    n, p = X.shape
    Xc = X - X.mean(axis=0, keepdims=True)
    S = (Xc.T @ Xc) / max(1, n - 1)
    mu = np.trace(S) / p
    target = mu * np.eye(p)
    if alpha is None:
        # Ledoit-Wolf optimal intensity
        d2 = np.sum((S - target) ** 2)
        b2 = np.sum([np.sum((np.outer(x, x) - S) ** 2) for x in Xc]) / (n ** 2)
        alpha = 0.0 if d2 <= 0 else float(min(1.0, max(0.0, b2 / d2)))
    return (1.0 - alpha) * S + alpha * target


def _spd_guard(S: np.ndarray, floor_ratio: float = 1e-6) -> np.ndarray:
    """Project onto the SPD cone with a relative eigenvalue floor."""
    vals, vecs = eigh((S + S.T) / 2.0)
    floor = max(vals.max(), 1e-12) * floor_ratio
    return vecs @ np.diag(np.maximum(vals, floor)) @ vecs.T


def delta_G_structure(Sigma_t: np.ndarray, Sigma_0: np.ndarray) -> float:
    """
    ΔG proxy: affine-invariant Riemannian distance between covariance operators.

        d(Σ₀, Σ_t) = ‖ log( Σ₀^{-1/2} Σ_t Σ₀^{-1/2} ) ‖_F

    Chosen over the Frobenius distance because it is invariant to invertible
    linear re-parameterisation of the channels, so the value does not depend on
    the arbitrary units in which each physiological channel happens to be
    recorded. Dimensionless.

    NOTE: this is a geometric distance. It is NOT the statement
    H_k(Reach(X_t)) ≇ H_k(Reach(X_0)). A nonzero value here does not imply a
    homology change, and a homology change need not produce a large value here.
    """
    S0 = _spd_guard(np.asarray(Sigma_0, float))
    St = _spd_guard(np.asarray(Sigma_t, float))
    vals, vecs = eigh(S0)
    inv_sqrt = vecs @ np.diag(vals ** -0.5) @ vecs.T
    M = inv_sqrt @ St @ inv_sqrt
    M = (M + M.T) / 2.0
    ev = np.linalg.eigvalsh(M)
    ev = np.maximum(ev, 1e-12)
    return float(np.sqrt(np.sum(np.log(ev) ** 2)))


def delta_G_state(x_t: np.ndarray, mu_0: np.ndarray, Sigma_0: np.ndarray) -> float:
    """
    First-order companion to delta_G_structure: Mahalanobis displacement of the
    mean state from its own baseline, measured in the baseline metric.

    This IS ‖Λ_B ΔG‖ in the stiffness reading, up to a square root — see
    deformation_energy below.
    """
    d = np.asarray(x_t, float) - np.asarray(mu_0, float)
    P = np.linalg.pinv(_spd_guard(np.asarray(Sigma_0, float)))
    return float(np.sqrt(max(0.0, d @ P @ d)))


# ----------------------------------------------------------------------------
# Λ — the two preregistered readings.  They are NOT interchangeable.
# ----------------------------------------------------------------------------

def Lambda_B_stiffness(Sigma_0: np.ndarray) -> np.ndarray:
    """
    PRIMARY preregistered reading: Λ as structural constraint / stiffness.

    For a Gaussian equilibrium p(x) ∝ exp(−½ xᵀΣ₀⁻¹x), the potential's Hessian
    is exactly Σ₀⁻¹. The precision matrix IS the stiffness operator. Under this
    reading ‖ΛΔG‖ > T_critical is a yield criterion — stress = stiffness x strain
    — and the original equation is coherent as written, with no sign change.

    Dimensionless when channels are z-scored against their own baseline.
    """
    return np.linalg.pinv(_spd_guard(np.asarray(Sigma_0, float)))


def Lambda_A_recovery(X: np.ndarray) -> np.ndarray:
    """
    ALTERNATIVE preregistered reading: Λ as recovery-rate / resilience operator.

    Fit VAR(1)  x_{t+1} = A x_t + ε  and return the discrete restoring operator
    (I − A). Critical slowing down is the statement that the spectral radius of
    A tends to 1, hence (I − A) → 0.

    CONSEQUENCE, STATED IN ADVANCE: under this reading ‖ΛΔG‖ DECREASES toward a
    transition, so the criterion ‖ΛΔG‖ > T_critical can never fire. Testing
    reading A therefore requires the modified criterion ‖Λ⁻¹ΔG‖ > T_critical.
    That modification changes the original mathematics and is flagged as such
    wherever it is used.
    """
    X = np.asarray(X, float)
    Xc = X - X.mean(axis=0, keepdims=True)
    X0, X1 = Xc[:-1], Xc[1:]
    A, *_ = np.linalg.lstsq(X0, X1, rcond=None)
    A = A.T
    return np.eye(X.shape[1]) - A


def deformation_energy(delta: np.ndarray, Lambda: np.ndarray) -> float:
    """
    ‖ΛΔG‖ under the primary (stiffness) reading, in energy form:

        E = √( δᵀ Λ δ )     with Λ = Σ₀⁻¹

    This is the quantity compared against T_critical in H4.
    """
    d = np.asarray(delta, float)
    return float(np.sqrt(max(0.0, d @ np.asarray(Lambda, float) @ d)))


def spectral_radius(A_operator: np.ndarray) -> float:
    """Largest |eigenvalue|; used to report critical slowing down directly."""
    return float(np.max(np.abs(np.linalg.eigvals(np.asarray(A_operator, float)))))


# ----------------------------------------------------------------------------
# Q = ‖ΔG‖ · τ
# ----------------------------------------------------------------------------

def persistence_tau(dg_series: np.ndarray, theta: float, dt: float = 1.0) -> float:
    """
    τ: duration of the current uninterrupted excursion of ‖ΔG‖ above theta,
    measured backward from the end of the series.

    IDENTIFIABILITY WARNING, stated in advance: τ is defined by a threshold on
    ‖ΔG‖, so τ and ‖ΔG‖ are not independent quantities. H2 is therefore
    formulated as a constrained-exponent test (β₁ = β₂ = 1 on the log scale),
    not as a claim that Q carries information disjoint from its own factors.
    """
    s = np.asarray(dg_series, float)
    n = 0
    for v in s[::-1]:
        if v > theta:
            n += 1
        else:
            break
    return n * dt


def Q_deformation_persistence(dg_series: np.ndarray, theta: float,
                              dt: float = 1.0) -> float:
    """Q = ‖ΔG‖ · τ, evaluated at the end of the series."""
    s = np.asarray(dg_series, float)
    return float(s[-1] * persistence_tau(s, theta, dt))


def Q_integral(dg_series: np.ndarray, theta: float, dt: float = 1.0) -> float:
    """
    Comparator for H2: ∫‖ΔG‖dt over the excursion.

    The product ‖ΔG‖·τ is a rectangle approximation to this integral. If the
    integral form predicts strictly better, the specific product form in the
    original mathematics is wrong even though the underlying idea survives.
    """
    s = np.asarray(dg_series, float)
    tau_steps = int(persistence_tau(s, theta, dt) / dt)
    return float(np.sum(s[len(s) - tau_steps:]) * dt) if tau_steps else 0.0


# ----------------------------------------------------------------------------
# C(t) = ι( ⋃ᵢ Nₜ(X, Iᵢ) ) — nerve of the co-deformation cover
# ----------------------------------------------------------------------------

def _gf2_rank(M: np.ndarray) -> int:
    """Rank over GF(2) by Gaussian elimination."""
    M = (np.asarray(M, dtype=np.uint8) % 2).copy()
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c]:
                piv = i
                break
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        r += 1
        if r == rows:
            break
    return r


def codeformation_complex(Z: np.ndarray, theta: float = 2.0,
                          support: float = 0.30, max_dim: int = 2):
    """
    Build the nerve of the channel-deformation cover.

    Nₜ(X, Iᵢ) is realised as the set of time points at which channel i is
    deformed:  Nᵢ = { t : |z_i(t)| > theta }.  By the nerve construction a
    simplex {i₀…i_k} is included iff |Nᵢ₀ ∩ … ∩ N_ik| / T ≥ support.

    Intersection support is monotone decreasing under supersets, so the family
    is automatically downward closed and is a genuine simplicial complex.

    Returns {dim: [frozenset(vertices), ...]}.
    """
    Z = np.asarray(Z, float)
    T, p = Z.shape
    N = [np.abs(Z[:, i]) > theta for i in range(p)]
    need = support * T

    simplices = {0: [frozenset([i]) for i in range(p) if N[i].sum() >= need]}
    current = simplices[0]
    for dim in range(1, max_dim + 1):
        nxt, seen = [], set()
        for s in current:
            for v in range(p):
                if v in s:
                    continue
                cand = s | {v}
                if cand in seen:
                    continue
                seen.add(cand)
                inter = np.ones(T, dtype=bool)
                for u in cand:
                    inter &= N[u]
                if inter.sum() >= need:
                    nxt.append(cand)
        if not nxt:
            break
        simplices[dim] = nxt
        current = nxt
    return simplices


def betti_numbers(simplices: dict) -> tuple[int, int]:
    """
    (β₀, β₁) of the co-deformation complex over GF(2).

    β₀ = #components of co-deforming channel groups.
    β₁ = independent 1-cycles: channel groups that couple pairwise around a loop
         without co-deforming as a triple.

    β₁ is the quantity that makes H5 non-trivial. It is determined by which
    triangles are filled, i.e. by third-order co-deformation support, and is
    therefore NOT a function of the pairwise supports alone. A model containing
    every pairwise coupling can still be missing β₁.
    """
    V = simplices.get(0, [])
    E = simplices.get(1, [])
    F = simplices.get(2, [])
    if not V:
        return 0, 0
    vidx = {v: i for i, v in enumerate(V)}
    eidx = {e: i for i, e in enumerate(E)}

    d1 = np.zeros((len(V), len(E)), dtype=np.uint8)
    for e, j in eidx.items():
        for v in e:
            fv = frozenset([v])
            if fv in vidx:
                d1[vidx[fv], j] = 1
    r1 = _gf2_rank(d1) if E else 0

    d2 = np.zeros((len(E), len(F)), dtype=np.uint8)
    for f, j in enumerate(F):
        for v in f:
            face = frozenset(f - {v})
            if face in eidx:
                d2[eidx[face], j] = 1
    r2 = _gf2_rank(d2) if F else 0

    b0 = len(V) - r1
    b1 = (len(E) - r1) - r2
    return int(b0), int(max(0, b1))


# ----------------------------------------------------------------------------
# C ⟂ L — operational decoupling, not statistical independence
# ----------------------------------------------------------------------------

def structural_report_coupling(dg_struct: np.ndarray, dg_report: np.ndarray,
                               window: int = 8) -> np.ndarray:
    """
    Rolling Spearman coupling ρ(t) between the structural deformation series and
    the self-report deformation series.

    The claim under test is NOT ρ = 0 (the literal reading of C ⟂ L is already
    refuted by any verbal intervention that moves physiology). The claim under
    test is that ρ(t) DECLINES during the pre-transition window while the two
    series diverge in sign: structure deforming upward, self-report flat or
    improving.
    """
    from scipy.stats import spearmanr
    a, b = np.asarray(dg_struct, float), np.asarray(dg_report, float)
    out = np.full(len(a), np.nan)
    for t in range(window, len(a) + 1):
        sa, sb = a[t - window:t], b[t - window:t]
        if np.std(sa) > 0 and np.std(sb) > 0:
            out[t - 1] = spearmanr(sa, sb).statistic
    return out


def divergence_index(dg_struct: np.ndarray, dg_report: np.ndarray,
                     window: int = 8) -> np.ndarray:
    """
    Signed decoupling: structural deformation slope minus self-report
    deformation slope, both standardised.

    Positive and growing = the H6 prediction (structure deforms, report does not).
    """
    a, b = np.asarray(dg_struct, float), np.asarray(dg_report, float)
    out = np.full(len(a), np.nan)
    for t in range(window, len(a) + 1):
        x = np.arange(window, dtype=float)
        sa, sb = a[t - window:t], b[t - window:t]
        za = (sa - sa.mean()) / (sa.std() or 1.0)
        zb = (sb - sb.mean()) / (sb.std() or 1.0)
        out[t - 1] = np.polyfit(x, za, 1)[0] - np.polyfit(x, zb, 1)[0]
    return out


# ----------------------------------------------------------------------------
# Self-test: does the estimator suite separate a fold transition from a
# noise-induced one? It must, or H1-H4 are untestable in principle.
# ----------------------------------------------------------------------------

def _simulate(kind: str, T: int = 4000, p: int = 6, seed: int = 0):
    """
    'fold'  : restoring stiffness decays toward zero -> critical slowing down.
    'noise' : stiffness constant, a large shock throws the system across a
              separatrix -> a real transition with NO precursor.
    'null'  : stationary.
    """
    rng = np.random.default_rng(seed)
    X = np.zeros((T, p))
    B = rng.normal(0, 0.25, (p, p)) / np.sqrt(p)
    for t in range(1, T):
        if kind == "fold":
            k = 0.35 * (1.0 - 0.95 * (t / T) ** 2)
        else:
            k = 0.35
        A = (1.0 - k) * np.eye(p) + B * (0.4 if kind != "null" else 0.1)
        shock = np.zeros(p)
        if kind == "noise" and t == int(0.85 * T):
            shock = rng.normal(0, 6.0, p)
        X[t] = A @ X[t - 1] + rng.normal(0, 0.1, p) + shock
    return X


def _report(kind: str) -> str:
    X = _simulate(kind)
    base = X[:800]
    S0 = shrunk_covariance(base)
    mu0, sd0 = base.mean(0), base.std(0) + 1e-9
    LB = Lambda_B_stiffness(S0)

    rows = []
    for frac in (0.25, 0.50, 0.70, 0.84):
        end = int(frac * len(X))
        win = X[end - 600:end]
        dg = delta_G_structure(shrunk_covariance(win), S0)
        energy = deformation_energy(win.mean(0) - mu0, LB)
        rho = spectral_radius(np.eye(X.shape[1]) - Lambda_A_recovery(win))
        b0, b1 = betti_numbers(codeformation_complex((win - mu0) / sd0,
                                                     theta=1.5, support=0.10))
        rows.append(f"  t={frac:.2f}  ΔG={dg:6.3f}  ‖ΛΔG‖={energy:7.3f}  "
                    f"ρ(A)={rho:5.3f}  (β₀,β₁)=({b0},{b1})")
    return f"[{kind}]\n" + "\n".join(rows)


if __name__ == "__main__":
    print(__doc__.split("Run:")[0].strip()[:0] or "", end="")
    print("Estimator self-test — synthetic systems\n" + "=" * 62)
    for kind in ("null", "fold", "noise"):
        print(_report(kind))
        print()
    print("Read this before trusting any real-data result:")
    print("  * 'fold'  MUST show ΔG and ρ(A) rising before the transition.")
    print("  * 'noise' MUST NOT. A transition with no precursor is a real")
    print("    physical possibility, and any estimator that appears to")
    print("    anticipate it is reporting leakage, not dynamics.")


# ============================================================================
#                              V2  ADDITIONS
# ============================================================================
# Added after the v1 reconstruction demoted objects 1 and 6 and froze
# Λ = Σ₀⁻¹.  The central v2 quantity is the STIFFNESS ALIGNMENT A(t), which
# is what the frozen Λ actually predicts — see the correction note below.
#
# CORRECTION TO v1, RECORDED RATHER THAN QUIETLY DROPPED
# ------------------------------------------------------
# v1 stated that the stiffness reading predicts pre-transition variance FALLS.
# That claim does not follow from Λ = Σ₀⁻¹.
#
# Λ is frozen at BASELINE. It is a fixed metric, not a state variable, so it
# makes no prediction whatsoever about how current variance evolves. What it
# does predict is the DIRECTION in which the mean state displaces, measured in
# the baseline metric. The falling-variance claim is withdrawn and replaced by
# the alignment prediction below, which is narrower and actually derivable.
# ============================================================================


def freeze_lambda(X_baseline: np.ndarray) -> dict:
    """
    Compute and freeze all baseline quantities. Call ONCE per patient, on the
    baseline window only. Nothing downstream may re-estimate these.

        Λ  :=  Σ₀⁻¹        (stiffness / precision / resistance-to-deformation)

    Returns a frozen dict; downstream functions consume it read-only.
    """
    X = np.asarray(X_baseline, float)
    S0 = _spd_guard(shrunk_covariance(X))
    return {
        "mu0": X.mean(axis=0),
        "sd0": X.std(axis=0) + 1e-9,
        "Sigma0": S0,
        "Lambda": np.linalg.pinv(S0),      # Λ = Σ₀⁻¹
        "n_eff": effective_sample_size(X),
        "p": X.shape[1],
    }


def effective_sample_size(X: np.ndarray) -> float:
    """
    n_eff = n (1-ρ)/(1+ρ) with ρ the mean lag-1 autocorrelation.

    Physiological channels are strongly autocorrelated. Using the raw sample
    count would make every displacement look overwhelmingly significant, so
    n_eff is required wherever a null distribution is invoked.
    """
    X = np.asarray(X, float)
    n = len(X)
    rhos = []
    for j in range(X.shape[1]):
        x = X[:, j] - X[:, j].mean()
        d = np.dot(x, x)
        rhos.append(np.dot(x[:-1], x[1:]) / d if d > 0 else 0.0)
    rho = float(np.clip(np.mean(rhos), -0.99, 0.99))
    return max(2.0, n * (1.0 - rho) / (1.0 + rho))


# ----------------------------------------------------------------------------
# THE CENTRAL v2 STATISTIC — stiffness alignment
# ----------------------------------------------------------------------------

def stiffness_alignment(delta: np.ndarray, Sigma_0: np.ndarray) -> float:
    """
    A  =  (δᵀ Σ₀⁻¹ δ)  /  ( ‖δ‖² · tr(Σ₀⁻¹)/p )

    Dimensionless, unit-invariant, with an EXACT null:

        A = 1   displacement direction unrelated to baseline structure
        A < 1   displacement along SOFT, high-variance directions
                → the critical-slowing-down / fold prediction
        A > 1   displacement along STIFF, low-variance, homeostatically
                defended directions
                → the Transition Dynamics yield prediction

    E[A] = 1 exactly when δ is isotropically random and independent of Σ₀ —
    verified numerically to 1.003 over 20,000 draws. This is what makes the
    head-to-head test between the two accounts clean: they sit on opposite
    sides of a null the normalisation pins to unity.
    """
    d = np.asarray(delta, float)
    P = np.linalg.pinv(_spd_guard(np.asarray(Sigma_0, float)))
    nd = float(d @ d)
    if nd <= 0:
        return float("nan")
    p = len(d)
    return float((d @ P @ d) / (nd * np.trace(P) / p))


def alignment_null_band(Sigma_0: np.ndarray, n_draw: int = 20000,
                        alpha: float = 0.05, seed: int = 0) -> tuple[float, float]:
    """
    Monte-Carlo (1-alpha) interval for A under isotropic displacement.

    The null is NOT symmetric around 1 — A is a ratio of quadratic forms and is
    right-skewed — so a symmetric interval would be wrong. Report this band
    alongside every A(t), never a bare point estimate.
    """
    rng = np.random.default_rng(seed)
    P = np.linalg.pinv(_spd_guard(np.asarray(Sigma_0, float)))
    p = P.shape[0]
    scale = np.trace(P) / p
    d = rng.normal(0, 1, (n_draw, p))
    num = np.einsum("ij,jk,ik->i", d, P, d)
    A = num / (np.einsum("ij,ij->i", d, d) * scale)
    return float(np.quantile(A, alpha / 2)), float(np.quantile(A, 1 - alpha / 2))


def deformation_energy_chi2(delta: np.ndarray, frozen: dict) -> float:
    """
    ‖ΛΔG‖ expressed as a chi-square quantile rather than a raw magnitude.

        n_eff · δᵀΣ₀⁻¹δ  ~  χ²_p   under "no displacement from baseline"

    This solves the T_critical transferability problem in a principled way:
    a threshold stated in χ² quantile units is comparable across patients and
    across cohorts with different channel counts p, whereas a raw Mahalanobis
    threshold is not.

    Returns the chi-square CDF value in [0,1).
    """
    from scipy.stats import chi2
    d = np.asarray(delta, float)
    stat = frozen["n_eff"] * float(d @ frozen["Lambda"] @ d)
    return float(chi2.cdf(stat, df=frozen["p"]))


# ----------------------------------------------------------------------------
# Higher-order structure beyond pairwise — the sharp form of the H5 claim
# ----------------------------------------------------------------------------

def beta1_excess_over_pairwise(Z: np.ndarray, theta: float = 1.5,
                               support: float = 0.10, n_surr: int = 100,
                               seed: int = 0) -> dict:
    """
    Tests: does the co-deformation complex carry structure that CANNOT be
    reconstructed from pairwise couplings alone?

    Method. Gaussian surrogates matched to the window's mean and covariance
    preserve ALL pairwise second-order structure and nothing higher, by
    construction. So the surrogate distribution of β₁ is exactly "what β₁ would
    be if only pairwise structure existed".

        z  =  ( β₁_observed − mean β₁_surrogate ) / sd β₁_surrogate

    z significantly > 0 is the only result that supports genuine higher-order
    integration. Anything else means the integration operator is decorative and
    a pairwise-complete model suffices.

    This replaces the vaguer v1 formulation "β₁ adds information beyond
    pairwise couplings" with a quantity that has an explicit null.
    """
    rng = np.random.default_rng(seed)
    Z = np.asarray(Z, float)
    T, p = Z.shape

    _, b1_obs = betti_numbers(codeformation_complex(Z, theta, support))

    S = _spd_guard(shrunk_covariance(Z))
    mu = Z.mean(axis=0)
    L = np.linalg.cholesky(S)
    b1_surr = []
    for _ in range(n_surr):
        Zs = mu + rng.normal(0, 1, (T, p)) @ L.T
        b1_surr.append(betti_numbers(codeformation_complex(Zs, theta, support))[1])
    b1_surr = np.asarray(b1_surr, float)
    sd = b1_surr.std()
    return {
        "b1_obs": int(b1_obs),
        "b1_surr_mean": float(b1_surr.mean()),
        "b1_surr_sd": float(sd),
        "z": float((b1_obs - b1_surr.mean()) / sd) if sd > 1e-9 else 0.0,
    }


def alignment_empirical_null(X_baseline: np.ndarray, Sigma_0: np.ndarray,
                             mu_0: np.ndarray, win: int,
                             n_sub: int = 200, alpha: float = 0.05,
                             seed: int = 0) -> dict:
    """
    The EMPIRICAL null for A, estimated from the patient's own stationary
    baseline. This supersedes `alignment_null_band`, which is retained only to
    document the error it embodies.

    WHY THE ISOTROPIC NULL IS WRONG
    -------------------------------
    `alignment_null_band` assumes the displacement δ points in an isotropically
    random direction, which gives E[A] = 1. But for a stationary system δ is a
    SAMPLING FLUCTUATION of the window mean, distributed N(0, Σ₀/n_eff) — that
    is, Σ₀-SHAPED, not isotropic. Sampling noise lands preferentially in the
    high-variance directions, exactly where the fold mechanism also lives.

    Consequently the stationary null sits BELOW 1, bounded above by

        E[A]  <=  p² / ( tr(Σ₀) · tr(Σ₀⁻¹) )     (Cauchy–Schwarz)

    with equality only when Σ₀ ∝ I. For a realistically ill-conditioned
    physiological covariance this bound can be 0.3 or lower.

    Two consequences fixed here rather than discovered later:
      1. "A > 1" and "A < 1" are NOT the right decision rules. Everything must
         be stated relative to the patient's own empirical band.
      2. A has intrinsically poor power against the fold mechanism, because
         fold displacement and stationary sampling noise share a direction.
         See docs/LIMITATIONS.md.
    """
    rng = np.random.default_rng(seed)
    X = np.asarray(X_baseline, float)
    n = len(X)
    if n <= win:
        raise ValueError("baseline must be longer than the analysis window")
    vals = []
    for _ in range(n_sub):
        s = rng.integers(0, n - win)
        d = X[s:s + win].mean(axis=0) - mu_0
        a = stiffness_alignment(d, Sigma_0)
        if a == a:
            vals.append(a)
    v = np.asarray(vals, float)
    p = Sigma_0.shape[0]
    bound = p * p / (np.trace(Sigma_0) * np.trace(np.linalg.pinv(Sigma_0)))
    return {
        "median": float(np.median(v)),
        "lo": float(np.quantile(v, alpha / 2)),
        "hi": float(np.quantile(v, 1 - alpha / 2)),
        "cauchy_schwarz_bound": float(bound),
        "n": len(v),
    }


def alignment_z(delta: np.ndarray, Sigma_0: np.ndarray, null: dict) -> float:
    """
    A(t) expressed as a position within the patient's own empirical null band.

        z = 0   at the null median
        z = +1  at the upper 97.5% null bound  -> yield / exogenous direction
        z = -1  at the lower 2.5% null bound   -> soft / endogenous direction

    This, not raw A, is the quantity entering every hypothesis test.
    """
    a = stiffness_alignment(delta, Sigma_0)
    m = null["median"]
    span = (null["hi"] - m) if a >= m else (m - null["lo"])
    return float((a - m) / span) if span > 1e-12 else 0.0
