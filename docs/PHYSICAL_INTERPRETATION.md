<div align="center">

# PHYSICAL INTERPRETATION

**The Frozen Λ · The Withdrawn Prediction · The Narrowed Claim**

![Lambda](https://img.shields.io/badge/Λ-FROZEN_=_Σ₀⁻¹-047857?style=flat-square)
![Status](https://img.shields.io/badge/v1_Variance_Claim-WITHDRAWN-b91c1c?style=flat-square)
![Statistic](https://img.shields.io/badge/Primary-Stiffness_Alignment_A(t)-1f2937?style=flat-square)
![Null](https://img.shields.io/badge/Null-Empirical_not_Isotropic-4c1d95?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)

</div>

---

*"The equation was fixed. The interpretation was not. Freeze it, or you have predicted nothing."*

*— Davarn Morrison, 2026*

---

## 1. The Freeze

╔══════════════════════════════════════════════════════════════════════╗
║  PREREGISTERED PRIMARY INTERPRETATION — FROZEN                       ║
║                                                                      ║
║      Λ  :=  Σ₀⁻¹                                                     ║
║                                                                      ║
║  Σ₀  =  covariance of the multivariate physiological state over an   ║
║         explicitly defined, treatment-quiet baseline window          ║
║                                                                      ║
║  Λ is a STIFFNESS / PRECISION / RESISTANCE-TO-DEFORMATION operator.  ║
║  It is computed ONCE, on the baseline, and never re-estimated.       ║
╚══════════════════════════════════════════════════════════════════════╝

Implemented as `freeze_lambda()` in
[`../analysis/estimators.py`](../analysis/estimators.py). Every downstream
function consumes the frozen dict read-only.

### 1.1 Why this interpretation is mathematically coherent

For a system in Gaussian quasi-equilibrium,

```
  p(x)  ∝  exp( −½ (x−μ₀)ᵀ Σ₀⁻¹ (x−μ₀) )
```

the effective potential is U(x) = ½(x−μ₀)ᵀΣ₀⁻¹(x−μ₀), whose Hessian is

```
  ∇²U  =  Σ₀⁻¹
```

**The precision matrix is the stiffness operator — by construction, not by
analogy.** A direction with small baseline variance is one the system resists
being moved along; a direction with large baseline variance is one it explores
freely. That is exactly what "resistance to deformation" means.

The associated deformation quantity is therefore a **quadratic form**, not a
scalar product:

```
  δ(t)   =  μ(t) − μ₀                         mean displacement from baseline

  ‖ΛΔG‖  =  √( δᵀ Σ₀⁻¹ δ )                    deformation energy
           =  Mahalanobis distance in the baseline metric
           =  √(2 × work done to deform the system)
```

and the irreversibility criterion `‖ΛΔG‖ > T_critical` reads as a **yield
criterion**: stress = stiffness × strain, failure above a critical stress. The
original equation is coherent **as written, with no rearrangement and no sign
change**.

### 1.2 Why the alternative was not chosen

Under the resilience/recovery reading Λ_A = I − A, critical slowing down means
the spectral radius of A tends to 1, so Λ_A → 0 and:

```
  ‖ Λ_A ΔG ‖  →  0   as the transition is approached
```

The criterion `‖ΛΔG‖ > T_critical` **can never fire**. Testing that reading
requires inverting the operator, which modifies the original mathematics.

Since the instruction is to hold the mathematics fixed, only one reading leaves
it standing. The resilience reading is retained as a **separate competing model
with its own preregistered equations** (M2 in
[`COMPETING_MODELS.md`](COMPETING_MODELS.md)), never as a reinterpretation of
this one.

### 1.3 T_critical in transferable units

A raw Mahalanobis threshold is not comparable across patients with different
channel counts. Under the null of no displacement:

```
  n_eff · δᵀΣ₀⁻¹δ   ~   χ²_p
```

so T_critical is preregistered as a **χ² quantile**, which is comparable across
patients and cohorts. `n_eff` uses the autocorrelation-corrected effective
sample size — physiological channels are strongly autocorrelated, and raw
sample counts would make every displacement look overwhelming.

---

## 2. Withdrawn: the v1 Falling-Variance Prediction

╔══════════════════════════════════════════════════════════════════════╗
║  v1 CLAIM, NOW WITHDRAWN                                             ║
║                                                                      ║
║  "The stiffness reading predicts that variance FALLS before a        ║
║   transition, contradicting critical slowing down."                  ║
║                                                                      ║
║  THIS DOES NOT FOLLOW FROM Λ = Σ₀⁻¹.                                 ║
╚══════════════════════════════════════════════════════════════════════╝

**Why it was wrong.** Λ is frozen at baseline. It is a **fixed metric, not a
state variable**. It says nothing whatsoever about how the system's *current*
variance evolves. The v1 argument silently slid between two different objects:

| | Object | What it can predict |
|---|---|---|
| what was frozen | Λ = Σ₀⁻¹, the **baseline** precision | the DIRECTION in which the mean state displaces |
| what the v1 claim needed | Σ_t⁻¹, the **current** stiffness | how current variance evolves |

These are different quantities. Predicting variance change requires
preregistering the second, which is not what §3 of the revision instruction
freezes — and re-freezing Λ to rescue the prediction would be exactly the
post-hoc reinterpretation this programme forbids.

**The falling-variance prediction is withdrawn, not adjusted.** It is replaced
below by a narrower claim that is actually derivable from the frozen operator.

---

## 3. The Narrowed Prediction — Stiffness Alignment

What Λ = Σ₀⁻¹ *does* determine is the **direction** of displacement, measured
in the baseline metric. Decomposing δ in the eigenbasis of Σ₀ = Σᵢ λᵢ vᵢvᵢᵀ:

```
  δᵀΣ₀⁻¹δ  =  Σᵢ (δ·vᵢ)² / λᵢ
```

Displacement along **low-variance (stiff, tightly defended)** directions
contributes disproportionately. This motivates the primary v2 statistic:

╔══════════════════════════════════════════════════════════════════════╗
║  STIFFNESS ALIGNMENT                                                 ║
║                                                                      ║
║        A(t)  =  ( δᵀ Σ₀⁻¹ δ )  /  ( ‖δ‖² · tr(Σ₀⁻¹)/p )              ║
║                                                                      ║
║  Dimensionless. Unit-invariant. Invariant to the MAGNITUDE of δ.     ║
╚══════════════════════════════════════════════════════════════════════╝

The magnitude-invariance is the point: A(t) asks *where* the system is being
pushed, not *how hard*.

### 3.1 The physiological premise, stated separately

A(t) alone is a geometric quantity. Turning it into a prediction requires one
additional, explicitly separate, empirical premise:

> **HOMEOSTATIC PREMISE.** Physiological variables with low normal variance are
> low-variance *because* they are actively defended by control loops (pH, core
> temperature, mean arterial pressure). Normal variation does not move them.
> Pathology does. Therefore acute deterioration displaces the system
> preferentially along stiff, defended directions.

```
════════════════════════════════════════════════════════════════════
  THIS PREMISE IS NOT A CONSEQUENCE OF THE EQUATION.

  It is a physiological hypothesis bolted onto a geometric statistic,
  and it is the weakest link in the chain. It is stated separately so
  that it can be falsified separately.
════════════════════════════════════════════════════════════════════
```

### 3.2 Correction: the null is NOT A = 1

The normalisation gives E[A] = 1 when δ points in an **isotropically random**
direction — verified numerically at 1.003 over 20,000 draws. That is the wrong
null for physiological data.

For a **stationary** system, δ is a sampling fluctuation of the window mean,
distributed N(0, Σ₀/n_eff) — that is, **Σ₀-shaped, not isotropic**. Sampling
noise lands preferentially in high-variance directions. So the stationary null
sits well *below* 1, bounded by Cauchy–Schwarz:

```
  E[A]_stationary   ≤   p² / ( tr(Σ₀) · tr(Σ₀⁻¹) )
```

with equality only when Σ₀ ∝ I. For realistically ill-conditioned physiological
covariance this bound is 0.3 or lower — measured at **0.29** in the benchmark,
against an observed stationary null median of **0.17**.

```
┌──────────────────────────────────────────────────────────────────┐
│  CONSEQUENCE, FIXED BEFORE DATA CONTACT                          │
│                                                                   │
│  "A > 1" and "A < 1" are NOT valid decision rules.               │
│                                                                   │
│  Every decision uses z(t), the position of A within the          │
│  PATIENT'S OWN empirical stationary band, estimated from         │
│  held-out baseline sub-windows.                                   │
│      z = 0   at the null median                                   │
│      z = +1  at the upper 97.5% null bound                       │
└──────────────────────────────────────────────────────────────────┘
```

Implemented as `alignment_empirical_null()` and `alignment_z()`. The naive
`alignment_null_band()` is retained in the code **solely to document the error
it embodies**.

---

## 4. Head-to-Head With Critical Slowing Down

### 4.1 The two directional predictions

| | Transition Dynamics (frozen Λ) | Critical slowing down |
|---|---|---|
| **Quantity** | z(t), alignment vs own empirical null | variance ratio, lag-1 autocorrelation |
| **Window** | pre-transition window vs frozen baseline | same |
| **Baseline** | treatment-quiet baseline, Σ₀ frozen | same |
| **Expected sign** | z **> 0** — displacement along defended directions | variance **↑**, AR(1) **↑** |
| **Mechanism** | exogenous insult driving the system against its constraints | endogenous soft mode losing restoring force |
| **Uncertainty rule** | cluster-bootstrap 95% CI on mean z must exclude 0 | same on variance ratio vs 1 |

### 4.2 They are complementary, not rivals — corrected from v1

v1 framed these as competitors of which one must lose. The synthetic benchmark
([`../analysis/results/mechanism_benchmark.md`](../analysis/results/mechanism_benchmark.md))
shows that is wrong. AUC for separating each mechanism from stationarity:

| statistic | fold (endogenous) | yield (exogenous) | noise-induced |
|---|:--:|:--:|:--:|
| z — Transition Dynamics | **0.30** | **1.00** | 0.53 |
| variance ratio — CSD | **1.00** | 0.92 | 0.51 |
| ΔAR(1) — CSD | 0.95 | 0.98 | 0.50 |

**Each statistic detects the mechanism the other misses.** z fails on the fold
mechanism — and the failure is structural, not a tuning problem: fold escape
travels along high-variance directions, which is exactly where stationary
sampling noise also lives, so the two are not separable by alignment.

The corrected framing: **a combined model should beat either alone**, and the
mechanistic content lies in *which* statistic fires, not in whether one wins.

### 4.3 What is actually novel — the magnitude-matched test

Plain covariance drift `dG` scores **1.00 on both** detectable mechanisms. For
pure detection, Transition Dynamics adds nothing over a quantity Dynamical
Network Biomarker theory published in 2012.

`dG` appears to discriminate mechanism too — but only because the mechanisms
happened to produce different deformation *magnitudes*. Sweeping the exogenous
drift amplitude so that dG(yield) passes through dG(fold):

| yield drift | dG ratio to fold | AUC dG | AUC z |
|:--:|:--:|:--:|:--:|
| 2.20 | 2.09 | 1.00 | 1.00 |
| 1.00 | 1.05 ← **matched** | **0.56** | **1.00** |
| 0.55 | 0.56 | 0.03 | 1.00 |
| 0.35 | 0.39 | 0.00 | 1.00 |

At the matched point **dG collapses to chance while z holds at 1.00**, and
below it dG inverts — it was tracking deformation size, not mechanism.

╔══════════════════════════════════════════════════════════════════════╗
║  THE SURVIVING NOVELTY CLAIM, IN FULL                                ║
║                                                                      ║
║  Transition Dynamics is NOT a claim about detection performance.     ║
║  Covariance drift already detects, and detects at least as well.     ║
║                                                                      ║
║  It is a claim about MECHANISM IDENTIFICATION: z(t) discriminates    ║
║  the mechanism that produced a deformation, independently of the     ║
║  deformation's magnitude. Covariance drift cannot.                   ║
╚══════════════════════════════════════════════════════════════════════╝

---

## 5. Power Limit

The empirical null band for A narrows only slowly with channel count:

| channels p | 95% null band | width |
|:--:|:--:|:--:|
| 4 | [0.09, 2.84] | 2.74 |
| 8 | [0.21, 2.49] | 2.27 |
| 20 | [0.41, 1.91] | 1.49 |
| 40 | [0.56, 1.58] | 1.02 |

**A(t) is a cohort-level mechanism discriminator, not a per-window bedside
alarm**, unless many channels are available. This is a property of the
statistic, not a tuning problem, and it bounds what may be claimed.

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   Λ = Σ₀⁻¹ predicts WHERE the system is pushed,                      ║
║   not how much its variance changes.                                 ║
║                                                                      ║
║   The v1 variance prediction is withdrawn.                           ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Physical Interpretation*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) — Index
- [`MATHEMATICAL_OBJECTS.md`](MATHEMATICAL_OBJECTS.md) — Surviving objects
- [`COMPETING_MODELS.md`](COMPETING_MODELS.md) — M0–M4 and M_null
- [`LIMITATIONS.md`](LIMITATIONS.md) — Known limits
