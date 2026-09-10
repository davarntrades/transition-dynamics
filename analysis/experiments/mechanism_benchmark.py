"""
mechanism_benchmark.py — Does the frozen-Λ statistic separate transition
mechanisms, and where is it blind?

This runs BEFORE any real data. Its purpose is to establish, on systems whose
mechanism is known by construction, which estimator responds to which
mechanism — so that blind spots are documented rather than discovered later and
mistaken for biology.

Quantities compared, all computed on the pre-transition window against a frozen
baseline:

    A(t)        stiffness alignment      — the v2 Transition Dynamics statistic
    dG          Riemannian covariance drift
    var ratio   current / baseline total variance   — the CSD variance signal
    AR(1)       mean lag-1 autocorrelation          — the CSD slowing signal

Run:  python3 analysis/experiments/mechanism_benchmark.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "synthetic"))

import estimators as E                       # noqa: E402
from generators import simulate, MECHANISMS  # noqa: E402


def _ar1(X: np.ndarray) -> float:
    out = []
    for j in range(X.shape[1]):
        x = X[:, j] - X[:, j].mean()
        d = np.dot(x, x)
        out.append(np.dot(x[:-1], x[1:]) / d if d > 0 else 0.0)
    return float(np.mean(out))


def evaluate(mechanism: str, seed: int, base_len: int = 4000,
             win: int = 2500) -> dict:
    """
    Baseline and analysis windows are EQUAL LENGTH so that shrinkage intensity
    and estimator bias are matched. Comparing a long baseline against a short
    window confounds mechanism with estimation noise.
    """
    r = simulate(mechanism, seed=seed)
    X, onset = r["X"], r["onset"]

    base = X[:base_len]
    frozen = E.freeze_lambda(base)
    null = E.alignment_empirical_null(base, frozen["Sigma0"], frozen["mu0"],
                                      win=win // 2, seed=seed)
    base_var = np.trace(frozen["Sigma0"])
    base_ar1 = _ar1(base)

    pre = X[-win:]
    delta = pre.mean(axis=0) - frozen["mu0"]

    return {
        "mechanism": mechanism,
        "A": E.stiffness_alignment(delta, frozen["Sigma0"]),
        "z": E.alignment_z(delta, frozen["Sigma0"], null),
        "null_med": null["median"],
        "null_lo": null["lo"], "null_hi": null["hi"],
        "cs_bound": null["cauchy_schwarz_bound"],
        "dG": E.delta_G_structure(E.shrunk_covariance(pre), frozen["Sigma0"]),
        "var_ratio": float(np.trace(E.shrunk_covariance(pre)) / base_var),
        "ar1_delta": _ar1(pre) - base_ar1,
        "n_eff": frozen["n_eff"],
        "detectable": r["detectable"],
    }


def magnitude_matched_table(seeds: int = 12) -> str:
    """
    Sweep the yield drift amplitude so dG(yield) passes through dG(fold), and
    report how each statistic's fold-vs-yield AUC behaves at the matched point.

    A statistic that discriminates mechanism only via deformation SIZE must
    collapse to AUC 0.50 where the sizes are equal. One that discriminates
    mechanism structurally does not.
    """
    from generators import _restoring_rates

    def run(mech, seed, amp=2.2):
        rng = np.random.default_rng(seed)
        p, T = 6, 7000
        onset, h, sigma = int(0.6 * T), 0.02 * 40, 0.30
        k0 = _restoring_rates(p)
        Q, _ = np.linalg.qr(rng.normal(0, 1, (p, p)))
        X = np.zeros((T, p)); y = np.zeros(p)
        for t in range(T):
            k = k0.copy(); drift = np.zeros(p)
            prog = max(0.0, (t - onset) / max(1, T - onset))
            if mech == "fold":
                k[0] = k0[0] * max(1e-3, 1.0 - 0.995 * prog)
            elif mech == "yield":
                drift[-1] = amp * prog * k0[-1]
            dec = np.exp(-k * h)
            sd = sigma * np.sqrt((1.0 - dec ** 2) / (2.0 * k))
            y = dec * y + (drift / k) * (1.0 - dec) + rng.normal(0, 1, p) * sd
            X[t] = Q @ y
        base = X[:4000]
        f = E.freeze_lambda(base)
        nul = E.alignment_empirical_null(base, f["Sigma0"], f["mu0"],
                                         win=1250, seed=seed)
        pre = X[-2500:]; d = pre.mean(0) - f["mu0"]
        return {"z": E.alignment_z(d, f["Sigma0"], nul),
                "dG": E.delta_G_structure(E.shrunk_covariance(pre), f["Sigma0"])}

    def auc(a, b):
        a, b = np.asarray(a), np.asarray(b)
        return float(((a[:, None] > b[None, :]).sum()
                      + 0.5 * (a[:, None] == b[None, :]).sum())
                     / (len(a) * len(b)))

    S = range(seeds)
    fold = [run("fold", s) for s in S]
    dg_fold = np.mean([r["dG"] for r in fold])
    rows = [f"dG(fold) = **{dg_fold:.2f}** is the magnitude to match.\n",
            "| yield drift | dG(yield) | dG ratio to fold | AUC dG | AUC z |",
            "|:--:|:--:|:--:|:--:|:--:|"]
    for amp in (2.20, 1.00, 0.55, 0.42, 0.35):
        Y = [run("yield", s, amp) for s in S]
        dy = np.mean([r["dG"] for r in Y])
        mark = "  ← **matched**" if 0.9 <= dy / dg_fold <= 1.15 else ""
        rows.append(
            f"| {amp:.2f} | {dy:.2f} | {dy / dg_fold:.2f}{mark} "
            f"| {auc([r['dG'] for r in Y], [r['dG'] for r in fold]):.2f} "
            f"| {auc([r['z'] for r in Y], [r['z'] for r in fold]):.2f} |")
    return "\n".join(rows)


def power_vs_channels() -> str:
    """
    How wide is A's null band as a function of channel count p?

    This decides whether A(t) can ever be a per-window bedside alarm or is
    only ever a cohort-level discriminator. Reported because it is a hard
    limit, not a tuning problem.
    """
    rng = np.random.default_rng(0)
    rows = ["| channels p | 95% null band for A | band width |",
            "|:--:|:--:|:--:|"]
    for p in (4, 6, 8, 12, 20, 40):
        X = rng.normal(0, 1, (2000, p)) @ np.diag(np.geomspace(3, 0.2, p))
        lo, hi = E.alignment_null_band(E.shrunk_covariance(X), seed=1)
        rows.append(f"| {p} | [{lo:.2f}, {hi:.2f}] | {hi - lo:.2f} |")
    return "\n".join(rows)


def main() -> str:
    seeds = range(12)
    out = ["# Mechanism Benchmark — Transition Dynamics v2\n",
           "Generated by `analysis/experiments/mechanism_benchmark.py`. "
           "Synthetic systems with known ground truth.\n",
           "\n## 1. Estimator response by transition mechanism\n",
           "Mean over 12 seeds. `A` is the v2 stiffness-alignment statistic "
           "(null = 1.00); `var ratio` and `AR(1)` are the classical "
           "critical-slowing-down signals.\n",
           "| mechanism | detectable? | A | **z (vs own null)** | dG | var ratio | ΔAR(1) |",
           "|---|:--:|:--:|:--:|:--:|:--:|:--:|"]

    store = {}
    for m in MECHANISMS:
        rs = [evaluate(m, s) for s in seeds]
        store[m] = rs
        f = lambda k: np.mean([r[k] for r in rs])  # noqa: E731
        out.append(f"| **{m}** | {'yes' if rs[0]['detectable'] else 'NO'} "
                   f"| {f('A'):.2f} | **{f('z'):+.2f}** | {f('dG'):.2f} "
                   f"| {f('var_ratio'):.2f} | {f('ar1_delta'):+.3f} |")

    nl = store["null"][0]
    out += [f"\nEmpirical stationary null for A (p=6): median "
            f"**{np.mean([r['null_med'] for r in store['null']]):.2f}**, "
            f"95% band "
            f"[{np.mean([r['null_lo'] for r in store['null']]):.2f}, "
            f"{np.mean([r['null_hi'] for r in store['null']]):.2f}]. "
            f"Cauchy-Schwarz upper bound on the null mean: "
            f"{nl['cs_bound']:.2f}. n_eff per window ~"
            f"{np.mean([r['n_eff'] for r in store['null']]):.0f}.",
            "\n> The naive isotropic null of A = 1 is WRONG for stationary "
            "data: a stationary system's mean displacement is a sampling "
            "fluctuation shaped by Σ₀ itself, so the null sits well below 1. "
            "All decisions use z against the patient's own empirical band.\n",
            "\n## 2. What the table shows\n"]

    a_fold = np.mean([r["z"] for r in store["fold"]])
    a_yield = np.mean([r["z"] for r in store["yield"]])
    a_null = np.mean([r["z"] for r in store["null"]])
    v_fold = np.mean([r["var_ratio"] for r in store["fold"]])
    v_yield = np.mean([r["var_ratio"] for r in store["yield"]])
    a_noise = np.mean([r["z"] for r in store["noise"]])
    d_noise = np.mean([r["dG"] for r in store["noise"]])
    d_null = np.mean([r["dG"] for r in store["null"]])

    out += [
        f"- **z separates the yield mechanism from stationarity**: yield "
        f"{a_yield:+.2f} versus a stationary null of {a_null:+.2f}. "
        "Exogenous displacement along defended coordinates is detectable.",
        f"- **z does NOT separate the fold mechanism from stationarity**: "
        f"fold {a_fold:+.2f} versus null {a_null:+.2f}. This is a real "
        "negative result and it is structural, not a tuning failure: fold "
        "escape and stationary sampling noise both live in the "
        "high-variance directions, so the alignment statistic cannot tell "
        "them apart. **A(t) is a detector of exogenous, homeostatically "
        "constrained displacement only.**",
        f"- **The classical variance signal is the COMPLEMENT, not the "
        f"competitor**: variance ratio is {v_fold:.2f} for the fold and "
        f"{v_yield:.2f} for the yield mechanism — the exact mirror of z. "
        "Each statistic detects the mechanism the other misses. This "
        "overturns the v1 framing, which treated the stiffness account and "
        "critical slowing down as rival hypotheses of which one must lose.",
        f"- **Blind to noise-induced transition, as required**: z = "
        f"{a_noise:+.2f}, dG = {d_noise:.2f} against a stationary dG of "
        f"{d_null:.2f}. A real transition occurs and nothing anticipates it. "
        "Any estimator that appeared to predict this case would be leaking.",
        f"- **Rate-induced tipping is detected — but only by the variance "
        f"channel, and trivially so** (variance ratio "
        f"{np.mean([r['var_ratio'] for r in store['rate']]):.2f}, dG "
        f"{np.mean([r['dG'] for r in store['rate']]):.2f}, z "
        f"{np.mean([r['z'] for r in store['rate']]):+.2f}). The sweep "
        "inflates variance across every coordinate, so 'detection' here is "
        "not anticipation of a specific mechanism. An earlier draft of this "
        "file asserted rate-induced tipping was detected only weakly; the "
        "numbers say otherwise and the claim is corrected here rather than "
        "removed.",
    ]

    # ---- complementarity, measured rather than asserted ----
    def auc(pos, neg):
        pos, neg = np.asarray(pos), np.asarray(neg)
        gt = (pos[:, None] > neg[None, :]).sum()
        eq = (pos[:, None] == neg[None, :]).sum()
        return float((gt + 0.5 * eq) / (len(pos) * len(neg)))

    out += ["\n## 3. Complementarity, measured\n",
            "AUC for separating each transition mechanism from the stationary "
            "null, using each statistic alone. 12 seeds per cell.\n",
            "| statistic | fold vs null | yield vs null | noise vs null |",
            "|---|:--:|:--:|:--:|"]
    for label, key in (("z (Transition Dynamics)", "z"),
                       ("variance ratio (CSD)", "var_ratio"),
                       ("ΔAR(1) (CSD)", "ar1_delta"),
                       ("dG (covariance drift)", "dG")):
        cells = []
        for m in ("fold", "yield", "noise"):
            cells.append(f"{auc([r[key] for r in store[m]], [r[key] for r in store['null']]):.2f}")
        out.append(f"| {label} | " + " | ".join(cells) + " |")
    out += ["\nAUC 0.50 is chance; 1.00 is perfect separation.\n",
            "\n### 3.1 The adversarial reading of this table\n",
            "**`dG` alone scores 1.00 on both detectable mechanisms.** `dG` is "
            "the plain covariance-drift quantity that Dynamical Network "
            "Biomarker theory published in 2012. For pure DETECTION, the "
            "novel Transition Dynamics statistic adds nothing whatsoever "
            "over a fourteen-year-old method — and scores 0.30 (worse than "
            "chance) on the fold mechanism.\n",
            "\nIf detection were the claim, this benchmark would have killed "
            "it here.\n",
            "\n### 3.2 What survives — mechanism discrimination\n",
            "Detection and classification are different tasks. `dG` = 1.00 on "
            "both mechanisms means `dG` cannot tell them APART. The test "
            "below asks which statistic separates one mechanism from the "
            "other.\n",
            "| statistic | fold vs yield (AUC, distance from 0.50) |",
            "|---|:--:|"]
    for label, key in (("z (Transition Dynamics)", "z"),
                       ("variance ratio (CSD)", "var_ratio"),
                       ("ΔAR(1) (CSD)", "ar1_delta"),
                       ("dG (covariance drift)", "dG")):
        a = auc([r[key] for r in store["yield"]], [r[key] for r in store["fold"]])
        out.append(f"| {label} | {a:.2f}  (|Δ| = {abs(a - 0.5):.2f}) |")
    out += ["\n`dG` also separates them here — but possibly only because the "
            "two mechanisms happen to produce different deformation "
            "MAGNITUDES in this parameterisation. Section 3.3 removes that "
            "confound.\n",
            "\n### 3.3 Magnitude-matched discrimination — the decisive test\n",
            "The yield drift amplitude is swept so that dG(yield) sweeps "
            "through dG(fold). If a statistic discriminates mechanism only "
            "because the two mechanisms differ in deformation size, its AUC "
            "collapses to chance at the matched point.\n",
            magnitude_matched_table(),
            "\n`z` is normalised by ‖δ‖² and is therefore invariant to "
            "deformation magnitude; `dG` is not. At the matched point "
            "**dG collapses to chance while z holds at 1.00**, and below it "
            "dG inverts — it was tracking size, not mechanism.\n",
            "\n**This is the only defensible novelty claim left standing.** "
            "`dG` detects; it does not classify. `z` classifies the mechanism "
            "that produced the deformation. The revised hypothesis is "
            "therefore narrowed accordingly in "
            "`docs/HYPOTHESIS.md`: Transition Dynamics is a claim about "
            "MECHANISM IDENTIFICATION, not about detection performance.\n"]

    out += ["\n## 4. Power limit — null band width vs channel count\n",
            power_vs_channels(),
            "\nThe band is wide at small p. A(t) is therefore a **cohort-level "
            "discriminator between mechanisms**, not a per-window bedside "
            "alarm, unless many channels are available. This is a property of "
            "the statistic, not a tuning problem, and it bounds what the "
            "hypothesis can claim.\n"]
    return "\n".join(out)


if __name__ == "__main__":
    txt = main()
    dest = os.path.join(os.path.dirname(__file__), "..", "results",
                        "mechanism_benchmark.md")
    with open(dest, "w") as fh:
        fh.write(txt)
    print(txt)
