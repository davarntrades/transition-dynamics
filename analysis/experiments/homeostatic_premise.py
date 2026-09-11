"""
homeostatic_premise.py — Falsification test of the homeostatic premise.

THE PREMISE UNDER TEST
----------------------
"Physiological variables with low baseline variance are low-variance because
they are actively defended. Pathology therefore displaces the system
preferentially along those defended (stiff) directions."

The premise is what licenses the inference

    A(t) above the patient's own stationary null  =>  homeostatic targeting

WHAT THIS FILE CAN AND CANNOT DECIDE
------------------------------------
It CANNOT decide whether real deteriorating patients displace along defended
directions. That needs clinical data, which was not reachable from this
environment (PhysioNet, UCI, Zenodo and Figshare are all blocked here).

It CAN decide something logically prior and, if it fails, decisive:

    Is A a VALID INSTRUMENT for inferring homeostatic targeting at all?

If A cannot separate a targeted insult from an untargeted one on systems where
the ground truth is known by construction, then no clinical result obtained
with A could support the premise, and every downstream claim resting on it must
be demoted regardless of what physiology does.

This is a falsification test of the instrument, run before touching patient
data rather than after.

PREREGISTERED DECISION RULES — fixed before the code below was run
------------------------------------------------------------------
Let dA = mean A(targeted-stiff) - mean A(isotropic), both at MATCHED
displacement magnitude and MATCHED exposure duration, with cluster CIs.

  (A) SUPPORTS the premise as an instrument
      AUC(targeted vs isotropic) >= 0.80 at matched magnitude AND matched
      exposure, AND the class-stratified sampling control cannot reproduce
      a comparable separation, AND the result is stable across baseline
      window choice and across n_eff.

  (B) UNRESOLVED
      Separation present at matched magnitude but confounded by exposure
      duration (i.e. exposure alone produces a comparable shift), or power
      inadequate (null band too wide at the dimensionality used).

  (C) FALSIFIES the instrument
      AUC(targeted vs isotropic) < 0.65 at matched magnitude and exposure,
      OR the sampling control alone reproduces the separation, OR A's
      response to exposure duration exceeds its response to targeting.

Run:  python3 analysis/experiments/homeostatic_premise.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import estimators as E                                   # noqa: E402

# ---------------------------------------------------------------------------
# System. Exact Ornstein-Uhlenbeck transitions; no Euler discretisation error.
# ---------------------------------------------------------------------------
P = 8
K = np.geomspace(0.30, 4.80, P)          # restoring rates; stiff = large k
H = 0.30                                 # observation interval
SIGMA = 1.0
BASE_N = 4000                            # baseline window (for Sigma_0)
PRE_N = 400                              # pre-transition window (for delta)


def simulate(force_dir, force_scale, exposure, seed, n_extra=0,
             p=P, k=K, h=H, noise=True):
    """
    Baseline segment, then a pre-transition window during which a sustained
    force has been acting for `exposure` time units, counted to the END of the
    series.

    force_dir : unit vector in the EIGENBASIS of the system (so 'stiff' and
                'soft' are unambiguous), or None for no force.
    noise     : False gives the deterministic twin, used for exact calibration.

    NOTE ON A FIXED BUG. An earlier version placed the force onset relative to
    the end of the whole series while measuring delta over the pre-window,
    so a short exposure covered only a few of the 400 window samples and the
    signal was diluted ~40x. Combined with a target magnitude at the noise
    floor, every condition returned the stationary value and the experiment
    measured nothing. Exposure is now clamped so the force always spans at
    least the analysis window when it is meant to.
    """
    rng = np.random.default_rng(seed)
    n = BASE_N + PRE_N + n_extra
    X = np.zeros((n, p))
    y = np.zeros(p)
    decay = np.exp(-k * h)
    sd = SIGMA * np.sqrt((1.0 - decay ** 2) / (2.0 * k)) if noise else np.zeros(p)
    on_idx = n - int(round(exposure / h))
    if force_dir is not None and on_idx < BASE_N:
        raise ValueError(
            f"exposure {exposure} puts force onset at index {on_idx}, inside "
            f"the baseline window (0..{BASE_N}). That contaminates mu_0 and "
            f"Sigma_0. Maximum admissible exposure is {PRE_N * h:g}.")
    for t in range(n):
        f = (force_scale * force_dir) if (force_dir is not None and t >= on_idx) \
            else np.zeros(p)
        y = decay * y + (f / k) * (1.0 - decay) + rng.normal(0, 1, p) * sd
        X[t] = y
    return X


def noise_floor(p=P, k=K, h=H, pre_n=PRE_N):
    """E||delta|| produced by stationary sampling alone. The signal must
    clear this or nothing is being measured."""
    Sig0 = np.diag(SIGMA ** 2 / k)
    ac = float(np.mean(np.exp(-k * h)))
    n_eff = pre_n * (1 - ac) / (1 + ac)
    return float(np.sqrt(np.trace(Sig0) / n_eff))


def measure(X, base_n=BASE_N, pre_n=PRE_N, n_sub=150, seed=0):
    """Frozen baseline, then A / z / dG / univariate on the pre-window."""
    base = X[:base_n]
    pre = X[base_n:base_n + pre_n] if len(X) >= base_n + pre_n else X[base_n:]
    fz = E.freeze_lambda(base)
    null = E.alignment_empirical_null(base, fz["Sigma0"], fz["mu0"],
                                      win=pre_n, n_sub=n_sub, seed=seed)
    delta = pre.mean(axis=0) - fz["mu0"]
    z_uni = np.abs(delta) / (fz["sd0"] / np.sqrt(max(1.0, len(pre))))
    return {
        "A": E.stiffness_alignment(delta, fz["Sigma0"]),
        "z": E.alignment_z(delta, fz["Sigma0"], null),
        "dG": E.delta_G_structure(E.shrunk_covariance(pre), fz["Sigma0"]),
        "uni": float(np.max(z_uni)),
        "mag": float(np.linalg.norm(delta)),
        "null_med": null["median"],
        "n_eff": fz["n_eff"],
    }


def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    gt = (pos[:, None] > neg[None, :]).sum()
    eq = (pos[:, None] == neg[None, :]).sum()
    return float((gt + 0.5 * eq) / (len(pos) * len(neg)))


def boot_ci(v, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    v = np.asarray(v, float)
    m = [rng.choice(v, len(v), replace=True).mean() for _ in range(n)]
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


# Directions in the eigenbasis: stiffest coordinate, softest, isotropic.
STIFF = np.eye(P)[-1]
SOFT = np.eye(P)[0]


def isotropic_dir(seed):
    r = np.random.default_rng(1000 + seed).normal(0, 1, P)
    return r / np.linalg.norm(r)


_CAL_CACHE = {}


def calibrate(force_dir_fn, exposure, target_mag, seeds=range(6), tag=None):
    """
    Exact scale calibration on the DETERMINISTIC twin.

    The system is linear, so delta is proportional to the force scale and one
    pass is exact. Calibrating on noisy runs (the earlier approach) cannot
    converge when the target sits near the sampling noise floor, because the
    measured magnitude is then dominated by noise rather than by the force.
    """
    key = (tag or id(force_dir_fn), exposure, target_mag)
    if key in _CAL_CACHE:
        return _CAL_CACHE[key]
    d = force_dir_fn(0)
    if d is None:
        _CAL_CACHE[key] = 0.0
        return 0.0
    X = simulate(d, 1.0, exposure, 0, noise=False)
    det = X[BASE_N:BASE_N + PRE_N].mean(axis=0) - X[:BASE_N].mean(axis=0)
    m = float(np.linalg.norm(det))
    s = target_mag / m if m > 1e-12 else 0.0
    _CAL_CACHE[key] = s
    return s


def main() -> str:
    out, w = [], lambda s: out.append(s)
    SEEDS = range(30)

    w("# Homeostatic Premise — Falsification Test\n")
    w("Generated by `analysis/experiments/homeostatic_premise.py`.\n")
    w("\n**The premise:** low-baseline-variance directions are low-variance "
      "because they are defended, so pathology displaces the system "
      "preferentially along them. This licenses the inference "
      "*A above the stationary null implies homeostatic targeting*.\n")
    w("\n**What this file tests:** whether A is a valid instrument for that "
      "inference, on systems whose ground truth is known by construction. "
      "It does **not** test whether real patients behave this way — clinical "
      "data was not reachable from this environment.\n")

    # ---------------------------------------------------------------
    w("\n## 1. What follows from Λ = Σ₀⁻¹ alone (mathematical consequence)\n")
    Sig0 = np.diag(SIGMA ** 2 / K)
    Lam = np.linalg.inv(Sig0)
    tr = np.trace(Lam)
    Af = lambda d: float((d @ Lam @ d) / ((d @ d) * tr / P))
    rng = np.random.default_rng(0)
    stat_null = float(np.mean([Af(np.linalg.cholesky(Sig0) @ rng.normal(0, 1, P))
                               for _ in range(20000)]))
    w("For a linear system at equilibrium with restoring operator $K$ and "
      "isotropic noise, $\\Sigma_0 \\propto K^{-1}$, so $\\Lambda = \\Sigma_0^{-1} "
      "\\propto K$. A sustained force $f$ produces equilibrium displacement "
      "$\\delta = K^{-1} f$ — **stiff directions displace less for equal "
      "force**, by exactly the factor that makes them stiff.\n")
    w("\n| quantity | value |")
    w("|---|:--:|")
    w(f"| stationary sampling null E[A] | {stat_null:.3f} |")
    w(f"| sustained **isotropic** force, full equilibrium | "
      f"{np.mean([Af((f := rng.normal(0,1,P))/K) for _ in range(20000)]):.3f} |")
    w(f"| force along the **stiffest** coordinate | {Af(STIFF/K[-1]):.3f} |")
    w(f"| force along the **softest** coordinate | {Af(SOFT/K[0]):.3f} |")
    w("\nThese are consequences of the frozen operator. Nothing physiological "
      "has been assumed yet.\n")

    # ---------------------------------------------------------------
    w("\n## 2. The exposure-duration confound (mathematical consequence)\n")
    w("A step force acting for duration $T$ gives "
      "$\\delta_i = (f_i/k_i)(1-e^{-k_i T})$. For $T \\ll 1/k_i$ this is "
      "$\\approx f_i T$, **independent of stiffness**; for $T \\gg 1/k_i$ it is "
      "$f_i/k_i$, fully attenuated by stiffness. So A depends on how long the "
      "insult has acted relative to channel timescales — with **no targeting "
      "anywhere**.\n")
    w("\n| exposure T | E[A], isotropic force | vs stationary null |")
    w("|:--:|:--:|:--:|")
    for T in (0.05, 0.2, 1.0, 5.0, 20.0, 100.0):
        v = float(np.mean([Af((f := rng.normal(0, 1, P)) / K * (1 - np.exp(-K * T)))
                           for _ in range(6000)]))
        w(f"| {T:g} | {v:.3f} | {'**above**' if v > stat_null else 'below'} |")
    w("\n> **A short-exposure isotropic insult sits ABOVE the stationary null.** "
      "So `A > null` does not imply displacement along defended directions. "
      "The inference the premise depends on is not valid unless exposure "
      "duration is controlled.\n")
    w("\n> This also **inverts the preregistered class prediction**. Recent, "
      "abrupt insults (short exposure) give high A; slowly developing sepsis "
      "(long exposure) gives low A. The preregistration predicted the "
      "opposite ordering.\n")

    # ---------------------------------------------------------------
    w("\n## 3. Matched-magnitude, matched-exposure test (the decisive one)\n")
    FLOOR = noise_floor()
    TARGET_MAG, EXPO = 10.0 * FLOOR, 60.0   # max admissible is PRE_N*H = 120
    conds = {
        "stationary":      (lambda i: None, 0.0),
        "isotropic":       (isotropic_dir, EXPO),
        "targeted-stiff":  (lambda i: STIFF, EXPO),
        "targeted-soft":   (lambda i: SOFT, EXPO),
    }
    res = {}
    for name, (dirfn, expo) in conds.items():
        scale = 0.0 if dirfn(0) is None else calibrate(dirfn, expo, TARGET_MAG, tag=name)
        res[name] = [measure(simulate(dirfn(i), scale, expo, i)) for i in SEEDS]

    w(f"All forced conditions calibrated on the deterministic twin to the same "
      f"displacement magnitude ‖δ‖ ≈ {TARGET_MAG:.2f}, same exposure "
      f"T = {EXPO:g}. Stationary sampling noise floor for ‖δ‖ is "
      f"{FLOOR:.2f}, so the signal clears it by {TARGET_MAG/FLOOR:.0f}×. "
      f"{len(list(SEEDS))} seeds. n_eff ≈ "
      f"{np.mean([r['n_eff'] for r in res['stationary']]):.0f} "
      f"(requirement ≥ 10p = {10*P}).\n")
    w("\n| condition | ‖δ‖ | A | z vs own null | dG | max univariate |")
    w("|---|:--:|:--:|:--:|:--:|:--:|")
    for name, rs in res.items():
        f_ = lambda kk: np.mean([r[kk] for r in rs])       # noqa: E731
        w(f"| {name} | {f_('mag'):.2f} | {f_('A'):.3f} | {f_('z'):+.2f} "
          f"| {f_('dG'):.2f} | {f_('uni'):.1f} |")

    lo, hi = boot_ci([r["A"] for r in res["targeted-stiff"]])
    lo2, hi2 = boot_ci([r["A"] for r in res["isotropic"]])
    a_ti = auc([r["A"] for r in res["targeted-stiff"]],
               [r["A"] for r in res["isotropic"]])
    w(f"\nA(targeted-stiff) 95% CI [{lo:.3f}, {hi:.3f}] · "
      f"A(isotropic) 95% CI [{lo2:.3f}, {hi2:.3f}]\n")
    w("\n| discrimination at matched magnitude and exposure | AUC |")
    w("|---|:--:|")
    w(f"| **A: targeted-stiff vs isotropic** | **{a_ti:.2f}** |")
    w(f"| A: targeted-soft vs isotropic | "
      f"{auc([r['A'] for r in res['targeted-soft']], [r['A'] for r in res['isotropic']]):.2f} |")
    w(f"| dG (covariance drift / DNB): targeted-stiff vs isotropic | "
      f"{auc([r['dG'] for r in res['targeted-stiff']], [r['dG'] for r in res['isotropic']]):.2f} |")
    w(f"| max univariate z: targeted-stiff vs isotropic | "
      f"{auc([r['uni'] for r in res['targeted-stiff']], [r['uni'] for r in res['isotropic']]):.2f} |")

    # --------------------------------------------------------------
    w("\n## 4. Is A's response to TARGETING larger than to EXPOSURE?\n")
    w("If exposure moves A more than targeting does, A cannot be read as a "
      "targeting measure in data where exposure is unknown — which is the "
      "normal clinical situation.\n")
    expo_rows = []
    for T in (1.0, 12.0, 120.0):
        sc = calibrate(isotropic_dir, T, TARGET_MAG, tag='iso')
        rs = [measure(simulate(isotropic_dir(i), sc, T, i)) for i in SEEDS]
        expo_rows.append((T, float(np.mean([r["A"] for r in rs])),
                          [r["A"] for r in rs]))
    w("\n| isotropic force, exposure T | mean A |")
    w("|:--:|:--:|")
    for T, m, _ in expo_rows:
        w(f"| {T:g} | {m:.3f} |")
    expo_span = max(m for _, m, _ in expo_rows) - min(m for _, m, _ in expo_rows)
    targ_span = abs(np.mean([r["A"] for r in res["targeted-stiff"]])
                    - np.mean([r["A"] for r in res["isotropic"]]))
    w(f"\n- A moved by **{expo_span:.3f}** across exposure alone (no targeting).")
    w(f"- A moved by **{targ_span:.3f}** from targeting at fixed exposure.")
    w(f"- ratio exposure/targeting = **{expo_span/max(targ_span,1e-9):.2f}**\n")
    auc_expo = auc(expo_rows[0][2], expo_rows[-1][2])
    w(f"AUC separating short-exposure from long-exposure isotropic insults: "
      f"**{auc_expo:.2f}** — both with no targeting whatsoever.\n")

    # --------------------------------------------------------------
    w("\n## 5. Class-stratified monitoring / sampling control\n")
    w("Physiology identical across classes; only the **observation process** "
      "differs, as it does between real event classes. If A separates the "
      "classes here, class-specific geometry can be manufactured by "
      "monitoring behaviour alone.\n")

    def sampled(X, mode, seed):
        """Thin the pre-window: 'escalating' mimics rising clinical concern."""
        rng = np.random.default_rng(seed)
        base, pre = X[:BASE_N], X[BASE_N:BASE_N + PRE_N]
        if mode == "regular":
            keep = np.ones(len(pre), bool)
        else:
            prob = np.linspace(0.25, 1.0, len(pre))
            keep = rng.random(len(pre)) < prob
        keep[-1] = True
        return np.vstack([base, pre[keep]]), int(keep.sum())

    w("\n| class (observation process) | A | z | n kept |")
    w("|---|:--:|:--:|:--:|")
    samp = {}
    samp_scale = calibrate(isotropic_dir, EXPO, TARGET_MAG, tag='iso')
    for mode in ("regular", "escalating"):
        vals = []
        for i in SEEDS:
            X = simulate(isotropic_dir(i), samp_scale, EXPO, i)
            Xs, nk = sampled(X, mode, i)
            m = measure(Xs, pre_n=len(Xs) - BASE_N)
            m["nk"] = nk
            vals.append(m)
        samp[mode] = vals
        w(f"| {mode} | {np.mean([v['A'] for v in vals]):.3f} "
          f"| {np.mean([v['z'] for v in vals]):+.2f} "
          f"| {np.mean([v['nk'] for v in vals]):.0f} |")
    auc_samp = auc([v["A"] for v in samp["escalating"]],
                   [v["A"] for v in samp["regular"]])
    w(f"\nAUC separating the two observation processes on identical "
      f"physiology: **{auc_samp:.2f}**\n")

    # --------------------------------------------------------------
    w("\n## 6. Sensitivity: baseline window and effective sample size\n")
    w("\n| baseline window (obs) | n_eff | stationary null median A | A targeted-stiff |")
    w("|:--:|:--:|:--:|:--:|")
    sens = []
    stiff_scale = calibrate(lambda i: STIFF, EXPO, TARGET_MAG, tag='stiff')
    for bn in (1000, 2000, 4000):
        sc = stiff_scale
        rs = [measure(simulate(STIFF, sc, EXPO, i), base_n=bn) for i in SEEDS]
        sens.append((bn, np.mean([r["A"] for r in rs])))
        w(f"| {bn} | {np.mean([r['n_eff'] for r in rs]):.0f} "
          f"| {np.mean([r['null_med'] for r in rs]):.3f} "
          f"| {np.mean([r['A'] for r in rs]):.3f} |")
    w(f"\nA(targeted) varies by {max(s[1] for s in sens)-min(s[1] for s in sens):.3f} "
      f"across baseline-window choice.\n")

    w("\n| channels p | 95% null band for A | width |")
    w("|:--:|:--:|:--:|")
    for p in (4, 8, 16, 32):
        kk = np.geomspace(0.30, 4.80, p)
        S = np.diag(SIGMA ** 2 / kk)
        blo, bhi = E.alignment_null_band(S, seed=2)
        w(f"| {p} | [{blo:.2f}, {bhi:.2f}] | {bhi-blo:.2f} |")

    # --------------------------------------------------------------
    w("\n## 7. Verdict against the preregistered rules\n")
    verdict = ("C" if (a_ti < 0.65 or auc_samp >= 0.80
                       or expo_span > targ_span) else
               "A" if (a_ti >= 0.80 and auc_samp < 0.80) else "B")
    w(f"\n| criterion | value | threshold |")
    w("|---|:--:|:--:|")
    w(f"| AUC targeted vs isotropic (matched) | {a_ti:.2f} | A ≥ 0.80 / C < 0.65 |")
    w(f"| sampling control AUC | {auc_samp:.2f} | C if ≥ 0.80 |")
    w(f"| exposure span vs targeting span | {expo_span:.3f} vs {targ_span:.3f} "
      f"| C if exposure > targeting |")
    w(f"\n### Verdict: **{verdict}**\n")
    return "\n".join(out)


if __name__ == "__main__":
    txt = main()
    dest = os.path.join(os.path.dirname(__file__), "..", "results",
                        "homeostatic_premise.md")
    with open(dest, "w") as fh:
        fh.write(txt)
    print(txt)
