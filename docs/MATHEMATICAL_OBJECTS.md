<div align="center">

# MATHEMATICAL OBJECTS

**The Surviving Equations · Full Specification**

![Objects](https://img.shields.io/badge/Surviving-Objects_2_·_4_·_5-047857?style=flat-square)
![Rule](https://img.shields.io/badge/Observed_≠_Estimated-Enforced-1f2937?style=flat-square)
![Novelty](https://img.shields.io/badge/Multivariate_&gt;_Univariate-NOT_the_Novelty-b91c1c?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)

</div>

---

*"Every symbol gets a unit, an observable, and a way to die. Anything else is decoration."*

*— Davarn Morrison, 2026*

---

## 0. Standing Distinction

```
════════════════════════════════════════════════════════════════════
  OBSERVED    a number that comes off an instrument
  ESTIMATED   a number computed from observations under assumptions
  LATENT      an object the theory names but no instrument returns
════════════════════════════════════════════════════════════════════
```

Every object below is tagged. Objects that are LATENT with no estimator are in
[`DEMOTED_OBJECTS.md`](DEMOTED_OBJECTS.md), not here.

**Symbol collision resolved.** v1 used `τ` for both a duration and a topological
integration map. Throughout v2: **τ is a duration**; the integration map is
**ι**.

---

## 1. Structural Deformation — the substrate

### Equation

```
  ΔG(t)  =  d( Σ₀ , Σ_t )  =  ‖ log( Σ₀^{-1/2} Σ_t Σ₀^{-1/2} ) ‖_F
```

| Field | Specification |
|---|---|
| **Physical interpretation** | How far the joint second-order structure of the physiological state has been bent from its own baseline |
| **Variables** | Σ₀ = baseline covariance (p×p); Σ_t = window covariance; d = affine-invariant Riemannian distance |
| **Units** | Dimensionless. Invariant to invertible linear reparameterisation of channels, so the value does not depend on recording units |
| **Observed** | The p channel values on a regular grid |
| **Estimated** | Σ₀, Σ_t — both under Ledoit–Wolf shrinkage, mandatory |
| **Latent** | None |
| **Estimator** | `delta_G_structure` |
| **Direction approaching transition** | ΔG **rises** |
| **Null prediction** | ΔG stays within its own stationary band |
| **Falsifies it** | ΔG shows no rise on windows where all marginals are in range, in primary **and** external cohorts |

```
┌──────────────────────────────────────────────────────────────────┐
│  DECLARED SUBSTITUTION, CARRIED FORWARD FROM v1                  │
│                                                                   │
│  This is a METRIC distance, not the homology comparison of the   │
│  demoted Object 1. A nonzero ΔG does not imply a homology        │
│  change and a homology change need not produce a large ΔG.       │
│  No homological inference is licensed by any ΔG result.          │
└──────────────────────────────────────────────────────────────────┘
```

**Priority note.** ΔG is essentially the covariance-drift quantity of Dynamical
Network Biomarker theory (2012). It is **not novel** and is used here as the
established comparator, not as a contribution.

---

## 2. Deformation-Persistence — surviving Object 2

### Equation, reproduced exactly

```
  Q_i  =  ‖ΔG_i‖ · τ_i
```

| Field | Specification |
|---|---|
| **Physical interpretation** | Deformation magnitude combined multiplicatively with how long the system has stayed bent. A large brief excursion and a small sustained one are not equivalent |
| **Variables** | ‖ΔG_i‖ = deformation magnitude for channel-set i, dimensionless; τ_i = contiguous excursion duration above threshold θ |
| **Units** | Q carries **time** (dimensionless × time). Unit-invariance of the test is preserved because units move only the regression intercept |
| **Observed** | Channel values; the clock |
| **Estimated** | ΔG, τ, θ (θ = baseline 95th percentile of ΔG, fixed per patient before analysis) |
| **Latent** | None |
| **Estimator** | `Q_deformation_persistence`; comparator `Q_integral` |
| **Direction approaching transition** | Q **rises**, and its advantage over ΔG alone **grows with horizon** |
| **Null prediction** | β₂ = 0 — τ contributes nothing and Q is a rescaling of ΔG |
| **Falsifies it** | β₂ CI includes 0, **or** unconstrained exponents beat the constrained form by ΔAIC > 10, **or** the integral form beats the product form by ΔAIC > 10 |

### The identifiability problem and its declared repair

τ is defined by a threshold on ‖ΔG‖, so **Q is a deterministic function of
‖ΔG‖ and one tuning constant.** "Q carries information beyond its own factors"
is not a coherent claim. The testable claim is that the exponents are equal:

```
  logit(P) = β₀ + β₁·log‖ΔG‖ + β₂·log τ

  Morrison product form   ⟺   H₀: β₁ = β₂        (Wald test)
  Require additionally    β₁ > 0  and  β₂ > 0
```

**This reformulation is ours, not the framework's.** It is declared, not
smuggled in. `Q_integral` = ∫‖ΔG‖dt is the physically correct functional of
which the product is a rectangle approximation; if the integral wins, the idea
survives and the written product form does not.

**Terminology.** This object is referred to as *deformation-persistence*. The
"qualia" reading is demoted — see [`DEMOTED_OBJECTS.md`](DEMOTED_OBJECTS.md).

---

## 3. Constrained Deformation and Critical Threshold — surviving Object 4

### Equation, reproduced exactly

```
  ‖ Λ ΔG ‖  >  T_critical
```

with Λ **frozen** as Σ₀⁻¹ — see [`PHYSICAL_INTERPRETATION.md`](PHYSICAL_INTERPRETATION.md).

| Field | Specification |
|---|---|
| **Physical interpretation** | A yield criterion. Stress = stiffness × strain; the regime changes when constrained deformation exceeds a critical stress |
| **Variables** | δ = μ(t) − μ₀, mean displacement; Λ = Σ₀⁻¹, stiffness operator, dimensionless when channels are z-scored to baseline; T_critical stated as a χ² quantile |
| **Quadratic form** | `‖ΛΔG‖ = √(δᵀ Σ₀⁻¹ δ)` — a Mahalanobis norm in the baseline metric, **not** a scalar product |
| **Units** | Dimensionless. n_eff·δᵀΣ₀⁻¹δ ~ χ²_p under the no-displacement null, which is what makes T_critical transferable across cohorts with different p |
| **Observed** | Channel values |
| **Estimated** | μ₀, Σ₀ (frozen at baseline); μ(t); n_eff via autocorrelation correction |
| **Latent** | T_critical — fitted, and its transferability is the central open question |
| **Estimator** | `deformation_energy`, `deformation_energy_chi2` |
| **Direction approaching transition** | Energy **rises**; and the hazard as a function of it contains a **knee**, not a smooth gradient |
| **Null prediction** | Hazard rises smoothly and monotonically. No knee |
| **Falsifies it** | Smooth monotone hazard fits as well as or better than a threshold model (ΔAIC ≤ 10 favouring smooth), **or** between-cohort CV of fitted T_critical exceeds 0.5 |

### The directional companion — stiffness alignment

```
  A(t)  =  ( δᵀ Σ₀⁻¹ δ )  /  ( ‖δ‖² · tr(Σ₀⁻¹)/p )
```

| Field | Specification |
|---|---|
| **Physical interpretation** | *Where* the system is being pushed, independent of *how hard*. Magnitude-invariant by construction |
| **Direction approaching transition** | z(t) **> 0** against the patient's own empirical stationary null — displacement along homeostatically defended directions |
| **Null prediction** | z within the patient's own baseline band |
| **Falsifies it** | Mean z cluster-bootstrap 95% CI includes 0, or is negative, in exogenous-insult transition classes |

**Critical caveat, established empirically.** The decision rule is **not**
A > 1. The stationary null for A is Σ₀-shaped and sits well below 1. All
inference uses z against the patient's own empirical band. See
[`PHYSICAL_INTERPRETATION.md`](PHYSICAL_INTERPRETATION.md) §3.2.

---

## 4. Higher-Order Integration — surviving Object 5

### Equation, reproduced exactly

```
  C(t)  =  ι( ⋃ᵢ Nₜ(X, Iᵢ) )
```

| Field | Specification |
|---|---|
| **Physical interpretation** | Integrated multichannel deformation: the shape of how channels co-deform, not merely how many do |
| **Variables** | Nₜ(X,Iᵢ) = { t : \|zᵢ(t)\| > θ }, the times channel i is deformed; ι = topological integration map, realised as the **nerve** of the cover |
| **Units** | Betti numbers are integer counts, dimensionless |
| **Observed** | Channel values |
| **Estimated** | The complex, via co-deformation support; β₀, β₁ over GF(2) |
| **Latent** | None |
| **Estimator** | `codeformation_complex` → `betti_numbers` → `beta1_excess_over_pairwise` |
| **Direction approaching transition** | β₁ excess **rises** above its pairwise-matched surrogate null |
| **Null prediction** | z-score of β₁ excess = 0 — the complex carries nothing beyond pairwise |
| **Falsifies it** | β₁ excess z-score CI includes 0, or a pairwise-complete model matches the β₁-augmented model |

### Why the union is non-trivial

A naive union of overlapping neighbourhoods is connected and its invariants are
trivial. The **nerve theorem** supplies the content: for a good cover the
homotopy type of the union equals that of the nerve. A simplex {i₀…i_k} is
included iff those channels co-deform on at least a support fraction ρ of the
window. Intersection support is monotone decreasing under supersets, so the
family is **automatically downward closed** — a genuine simplicial complex with
no repair required.

### The strong claim, formalised

╔══════════════════════════════════════════════════════════════════════╗
║  "MULTIVARIATE BEATS UNIVARIATE" IS NOT THE NOVELTY.                 ║
║                                                                      ║
║  That is established (Network Physiology, DNB) and is not tested     ║
║  here as a contribution.                                             ║
║                                                                      ║
║  THE CLAIM IS: higher-order structural information exists that       ║
║  CANNOT be reconstructed from pairwise supports alone.               ║
╚══════════════════════════════════════════════════════════════════════╝

**The observable that tests it.** Gaussian surrogates matched to the window's
mean and covariance preserve **all** pairwise second-order structure and
nothing higher, by construction. So the surrogate distribution of β₁ is exactly
"what β₁ would be if only pairwise structure existed":

```
  z_β₁  =  ( β₁_observed − mean β₁_surrogate ) / sd β₁_surrogate
```

β₁ is determined by which **triangles are filled** — third-order co-deformation
support — and is provably not a function of the pairwise supports alone. A
model containing every pairwise coupling can still be missing β₁.

**z_β₁ significantly > 0 is the only result that supports higher-order
integration.** Anything else means the integration operator is decorative and a
pairwise-complete model suffices. Implemented as `beta1_excess_over_pairwise`.

---

## 5. Summary Table

| Object | Equation | Observed | Estimated | Latent | Direction | Kill condition |
|:--:|---|---|---|---|:--:|---|
| ΔG | d(Σ₀,Σ_t) | channels | Σ₀, Σ_t | — | ↑ | no rise with marginals in range |
| Q | ‖ΔG‖·τ | channels, clock | ΔG, τ, θ | — | ↑ | β₂ = 0, or integral form wins |
| ‖ΛΔG‖ | √(δᵀΣ₀⁻¹δ) | channels | μ₀, Σ₀, n_eff | T_critical | ↑ with a knee | smooth hazard fits as well |
| A(t) | normalised quadratic form | channels | Σ₀, empirical null | — | z > 0 | mean z CI includes 0 |
| C(t) | ι(⋃Nᵢ) → β₁ | channels | complex, surrogates | — | z_β₁ ↑ | z_β₁ CI includes 0 |

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   Higher-order means: not reconstructible from pairwise.             ║
║   The surrogate is the test. Anything else is a slogan.              ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Mathematical Objects*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) — Index
- [`PHYSICAL_INTERPRETATION.md`](PHYSICAL_INTERPRETATION.md) — The frozen Λ
- [`DEMOTED_OBJECTS.md`](DEMOTED_OBJECTS.md) — Objects 1 and 6
- [`FALSIFICATION_CRITERIA.md`](FALSIFICATION_CRITERIA.md) — Canonical table
