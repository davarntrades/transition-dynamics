<div align="center">

# MATHEMATICAL AUDIT

**Adversarial Examination of the Six Transition Dynamics Objects**

![Mode](https://img.shields.io/badge/Mode-Adversarial-b91c1c?style=flat-square)
![Test](https://img.shields.io/badge/Test-Coherence_·_Dimensions_·_Identifiability-1f2937?style=flat-square)
![Rule](https://img.shields.io/badge/Rule-No_Silent_Repair-4c1d95?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)
![Rights](https://img.shields.io/badge/©-Davarn_Morrison-555555?style=flat-square)

</div>

---

*"Repairing an equation quietly is how a field dies. Name the break. Then decide, in the open, whether to work around it."*

*— Davarn Morrison, 2026*

---

## Audit Standard

Each object is tested against four questions. A failure on any one is recorded
and **not repaired in place**.

```
════════════════════════════════════════════════════════════════════
  INTERNAL CONSISTENCY   do the symbols mean one thing throughout?
  DIMENSIONAL COHERENCE  do the units combine legally?
  IDENTIFIABILITY        can the quantity be recovered from data,
                         even in principle, with infinite samples?
  UNIQUE PREDICTION      does it force one empirical expectation
                         rather than permitting several?
════════════════════════════════════════════════════════════════════
```

Where a workaround is adopted, it appears as a **DECLARED SUBSTITUTION** with
its inferential cost stated. Silent substitution is the one prohibited move.

---

## Object 1 — Structural Deformation / Truth Condition

```
  ∃k :  H_k(Reach(X_t))  ≇  H_k(Reach(X_0))
```

### Finding 1.1 — Reach is not observable. **FAILS IDENTIFIABILITY.**

Reach(X) is the set of states accessible from X under admissible inputs. A
person emits **one trajectory**, not a set. Recovering a reachable set from one
realisation requires assuming the trajectory explores the accessible region
within the observation window — an ergodicity or quasi-stationarity assumption.

This produces a circularity that cannot be worked around by better estimation:

```
┌──────────────────────────────────────────────────────────────────┐
│  To estimate Reach(X_t) we assume quasi-stationarity on the      │
│  window.                                                          │
│  The hypothesis under test is that quasi-stationarity is failing. │
│  The estimator therefore assumes the negation of the thing it is  │
│  meant to detect.                                                 │
└──────────────────────────────────────────────────────────────────┘
```

Delay embedding of a windowed trajectory estimates the **attractor**, which is
a proper subset of the reachable set. Attractor ⊂ Reach. These are different
mathematical objects, and evidence about one is not evidence about the other.

### Finding 1.2 — Reach is generically contractible. **FAILS UNIQUE PREDICTION.**

For a controlled dynamical system with connected input set and no excluded
region, the reachable tube is path-connected and simply connected. Then:

```
  H₀(Reach) = ℤ        H_k(Reach) = 0  for all k ≥ 1
```

at **every** t. The condition `∃k : H_k(Reach(X_t)) ≇ H_k(Reach(X_0))` is then
not merely rarely satisfied. It is **never** satisfied.

Nontrivial homology requires holes, and holes require an excluded region — the
Ω of the safety invariant. The truth condition therefore has empirical content
**only relative to a physically realised Ω**, and the framework as presented
does not supply one for human physiology. Absent Ω, object 1 is vacuous rather
than false.

This is the strongest single finding in the audit. It is not fatal to the
research programme, because the programme can proceed on a declared metric
proxy — but it is fatal to any claim that a result here is evidence *about
homology*.

### Finding 1.3 — ΔG as written is a category error. **FAILS CONSISTENCY.**

The companion definition is:

```
  ΔG = Topology(X_t) − Topology(X_0)
```

If `Topology(·)` returns a homology group, this subtracts groups. **Subtraction
is not defined in the category of groups.** There is no group difference
operation; the closest legal constructions are quotients (requiring a normal
subgroup relationship that does not generally hold here) or connecting
homomorphisms in a long exact sequence, neither of which yields the intended
"how far has it bent" scalar.

The expression becomes meaningful only after choosing a numerical functor. The
choice is an empirical commitment:

| Functor | ΔG becomes | Cost |
|---|---|---|
| Betti vector β = (β₀,…,β_k) | β(t) − β(0), an integer vector | Integer-quantised. Sub-threshold deformation returns **exactly zero**. No graded early warning possible |
| Persistence diagram | Wasserstein / bottleneck distance | Continuous and stable, but this is a **metric on a filtration summary**, not a homology comparison |
| Covariance operator | Riemannian distance d(Σ₀,Σ_t) | Continuous, well-conditioned, cheap — and abandons topology entirely |

### DECLARED SUBSTITUTION 1

> **Adopted:** covariance-operator distance, `delta_G_structure`.
> **Cost:** a nonzero value does not imply homology change, and a homology
> change need not produce a large value. The two are logically independent.
> The truth condition of object 1 **remains untested** by this protocol.
> **Justification:** the instruction to prefer the simplest estimator capable
> of falsifying, and Finding 1.2 — there is no homology signal to estimate
> until Ω is specified.

### Grade — Object 1: **D**

Not empirically testable as written. Non-identifiable, generically vacuous, and
containing an undefined operation.

---

## Object 2 — Qualia / Deformation-Persistence

```
  Q_i = ‖ΔG_i‖ · τ_i
```

### Finding 2.1 — Dimensionally coherent, conditionally. **PASSES.**

With channels z-scored against their own baseline, ‖ΔG‖ is dimensionless and τ
carries time, so Q carries time. Legal.

**Condition:** without standardisation, ‖ΔG‖ mixes mmHg, beats·min⁻¹ and
dimensionless saturations inside one norm, which is not a legal operation.
Standardisation is therefore **mandatory**, not stylistic.

### Finding 2.2 — τ is not independent of ‖ΔG‖. **FAILS UNIQUE PREDICTION as stated.**

τ is "persistence duration of the deformation". Duration of what condition?
Any operational answer requires a threshold on ‖ΔG‖:

```
  τ = |{ t : ‖ΔG(t)‖ > θ }|      (contiguous, ending at now)
```

So Q = ‖ΔG‖ · τ(‖ΔG‖, θ). Q is a **deterministic function of ‖ΔG‖ and one
tuning constant.** The hypothesis "Q carries information beyond ‖ΔG‖ and τ" is
therefore not well-posed — Q is definitionally determined by them.

Further, ‖ΔG‖·τ is a **rectangle approximation** to the quantity the physical
story actually describes:

```
  Q_true = ∫ ‖ΔG(t)‖ dt   over the excursion
```

The product form equals the integral only if ‖ΔG‖ is constant across the
excursion, which it is not.

### DECLARED REFORMULATION 2

> The claim is restated as a **constrained-exponent test**:
>
> ```
>   logit(P) = β₀ + β₁·log‖ΔG‖ + β₂·log τ
>   Morrison product form  ⟺  β₁ = β₂
> ```
>
> This is sharp, unit-invariant (units move only the intercept), testable by
> Wald test and AIC, and comparable against the integral form.
> **This reformulation is ours, not the framework's.** The framework as written
> does not generate it.

### Grade — Object 2: **A**

Coherent and immediately falsifiable after standardisation and the
constrained-exponent reformulation.

---

## Object 3 — Governed Qualia / Constraint Operator

```
  Q_G = Λ · Q
```

### Finding 3.1 — Λ is underdetermined by the mathematics. **FAILS UNIQUE PREDICTION.**

The equations are equally consistent with Λ as stiffness and Λ as recovery
capacity. These predict **opposite signs** for the pre-transition change in
variance. The mathematics does not choose. An external interpretive commitment
is required before any prediction exists.

This is not a defect of rigour in the framework's presentation — it is a
structural feature. `Q_G = Λ·Q` constrains Λ only to be a linear operator.

### Finding 3.2 — Λ's role is inconsistent across objects 3 and 4. **FAILS CONSISTENCY.**

Stated semantics elsewhere in the Morrison stack: high Λ means stable,
coherent, resilient; Λ → 0 means collapse.

Object 4 states that collapse occurs when `‖ΛΔG‖ > T_critical`.

```
┌──────────────────────────────────────────────────────────────────┐
│  Under "high Λ = resilient", a MAXIMALLY RESILIENT system         │
│  crosses the irreversibility threshold at the SMALLEST            │
│  deformation.                                                     │
│                                                                   │
│  Under those semantics the criterion should be  ΔG / Λ > T_crit.  │
│  It is written  Λ · ΔG > T_crit.                                  │
│                                                                   │
│  The written form and the stated semantics disagree in sign.      │
└──────────────────────────────────────────────────────────────────┘
```

This is a genuine inconsistency between the resilience gloss on Λ and the
multiplicative form of the irreversibility criterion. It is **not repaired
here.** It is resolved by choosing the interpretation under which the written
mathematics is coherent — the stiffness reading — and recording that the
resilience gloss is thereby given up.

### Finding 3.3 — The two readings are degenerate in one dimension. **DESIGN CONSTRAINT.**

For ẋ = −kx + ξ, the restoring stiffness and the recovery rate are the same
parameter k. Interpretations A and B are **indistinguishable** univariately.

They separate multivariately, because the stationary covariance Σ depends on
both the restoring operator A and the noise covariance, so:

```
  Λ_B = Σ₀⁻¹        depends on restoring structure AND noise
  Λ_A = I − A       depends on restoring structure only
```

**Consequence for design:** any univariate test of Λ confirms whichever reading
was assumed. Univariate findings are excluded from confirmatory analysis in
advance.

### Grade — Object 3: **B**

Coherent, but requires an external interpretive choice the mathematics does not
force. Carries a sign inconsistency with the stated resilience semantics.

---

## Object 4 — Irreversibility / Critical Deformation

```
  ‖ Λ ΔG ‖  >  T_critical
```

### Finding 4.1 — Coherent as a yield criterion. **PASSES, under one reading only.**

Reading Λ as the baseline precision operator Σ₀⁻¹ makes this exactly Hooke's law
with a yield threshold:

```
  stress = stiffness × strain          σ = E ε
  failure when stress exceeds yield    ‖Σ₀⁻¹ δ‖ > T_crit
```

For a Gaussian equilibrium p(x) ∝ exp(−½xᵀΣ₀⁻¹x), the potential's Hessian is
Σ₀⁻¹. The precision matrix is the stiffness operator by construction, not by
analogy. Under this reading the object is dimensionally clean, physically
motivated, and coherent **as written with no rearrangement.**

### Finding 4.2 — The alternative reading makes the criterion unfireable. **DECISIVE.**

Under Λ = Λ_A = I − A, critical slowing down means the spectral radius of A
tends to 1, hence Λ_A → 0. Therefore:

```
  ‖ Λ_A ΔG ‖  →  0   as the transition is approached
```

The criterion `‖ΛΔG‖ > T_critical` **can never fire** under the resilience
reading. Reading A is not an alternative interpretation of the same equation —
it is incompatible with the equation's form, and testing it requires inverting
the operator.

> **This is the decisive argument for preregistering the stiffness reading.**
> Given the instruction to hold the mathematics fixed, only one reading leaves
> the mathematics standing.

### Finding 4.3 — Λ as operator, not scalar. **STRENGTHENS the object.**

`ΛΔG` with a norm around it reads most naturally as matrix acting on vector.
This is the richer and better version: Λ is **anisotropic**, stiff in some
eigen-directions and compliant in others, and:

```
  ‖Λ_B ΔG‖ = √( δᵀ Σ₀⁻¹ δ )   —  a Mahalanobis deformation energy
```

which is standard, cheap, well-conditioned under shrinkage, and generates the
substantive prediction that pre-transition deformation is **directed along
stiff eigen-directions**. A scalar Λ would carry no such prediction.

### Finding 4.4 — T_critical units differ between readings. **BOOKKEEPING.**

Λ_B is dimensionless; Λ_A carries time⁻¹. Thresholds fitted under the two
readings are not comparable and must be reported as separate experiments.

### Finding 4.5 — The separatrix claim is stronger than the predictive claim.

`> T_critical` asserts a **discontinuity**, not a gradient. A model in which
hazard increases smoothly and monotonically with ‖ΛΔG‖ would be predictively
useful and would **falsify the separatrix**. These outcomes must never be
conflated. This distinction is the primary test in H4 precisely because it is
the only claim here that existing early-warning literature does not already
make.

### Grade — Object 4: **A**

Coherent and immediately falsifiable under the preregistered reading, with a
unique directional prediction (a hazard knee) and a stated kill condition.

---

## Object 5 — Consciousness / Integrated Deformation

```
  C(t) = τ( ⋃ᵢ Nₜ(X, Iᵢ) )
```

### Finding 5.1 — Symbol collision. **FAILS CONSISTENCY.**

`τ` denotes a **duration** (a positive real) in object 2, and a **topological
integration mapping** (a functional on sets) in object 5. These are
incompatible types sharing one symbol.

**Recorded, not silently repaired.** This document writes the integration map
as `ι` and reserves `τ` for duration. Any downstream reader of the original
notation must resolve the collision by context, which is an avoidable source of
error in a formal system.

### Finding 5.2 — A naive union is trivial; the nerve is not. **REPAIRABLE — and productive.**

If the Nₜ(X, Iᵢ) are overlapping neighbourhoods covering a connected region,
their union is connected and its invariants are trivial. Read that way, C(t)
carries no information.

The nerve theorem supplies the non-trivial reading: for a good cover, the
homotopy type of the union equals that of the **nerve** of the cover. So:

```
  C(t) = topology of the NERVE of the channel-deformation cover
```

which is directly computable. Realising Nᵢ as the set of time points at which
channel i is deformed, a simplex {i₀…i_k} is included iff the channels
co-deform on at least a support fraction ρ of the window. Intersection support
is monotone decreasing under supersets, so the family is **automatically
downward closed** and is a genuine simplicial complex. No repair needed beyond
the reading.

### Finding 5.3 — β₁ is a genuine higher-order quantity. **STRENGTHENS the object.**

β₀ is largely recoverable from pairwise co-deformation. β₁ is not:

```
  β₁ depends on WHICH TRIANGLES ARE FILLED,
  i.e. on third-order co-deformation support.
  It is provably not a function of the pairwise supports alone.
```

A model containing every pairwise channel coupling can still be missing β₁.
This makes H5 a real higher-order claim rather than the already-established
"multivariate beats univariate", and gives it a clean kill condition.

### Grade — Object 5: **A**

Well-defined and computable under the nerve reading, generating a genuine
higher-order prediction. Conditional on resolving the τ symbol collision.

---

## Object 6 — Orthogonality Law

```
  C ⟂ L        ∀Δℓ ∈ L,  ΔR_C(t) = 0
```

### Finding 6.1 — The literal form asserts a null. **UNCONFIRMABLE BY CONSTRUCTION.**

A universally quantified zero-effect statement cannot be confirmed by evidence.
It can only be refuted. Any accumulation of near-zero measurements is
consistent with a small nonzero effect. As a scientific proposition, the
literal form has one possible empirical fate: refutation.

### Finding 6.2 — The literal form is already refuted. **FAILS.**

A single counterexample suffices, and several are routine:

```
  psychotherapy          verbal intervention → measured physiological change
  verbal instruction     changes respiration, heart rate, cortisol
  placebo suggestion     changes measured pain response and autonomic state
  hypnotic suggestion    changes measured autonomic and nociceptive markers
```

Each is a Δℓ confined to language producing ΔR_C ≠ 0. `∀Δℓ ∈ L, ΔR_C(t) = 0`
is false as a statement about human beings.

### Finding 6.3 — Notation is not evidence for the property it names.

Writing `⟂` does not establish statistical independence, geometric
orthogonality, or causal isolation. These are three distinct properties and the
symbol asserts none of them. Any inference of the form "the notation is
orthogonality, therefore the quantities are uncorrelated" is invalid.

### DECLARED REFORMULATION 6

> The tested proposition is **not** C ⟂ L. It is:
>
> ```
>   Coupling ρ(t) between structural deformation and self-report
>   deformation DECLINES during the pre-transition window, with signed
>   divergence: structure deforming upward while self-report is flat or
>   improving.
> ```
>
> **This is a different proposition.** Decoupling is a graded, local, and
> directional claim. Orthogonality is a global zero-effect claim. Evidence for
> decoupling is **not** evidence for C ⟂ L, and this must never be reported as
> though it were.

### Finding 6.4 — The reformulation has a severe confound. **DESIGN REQUIREMENT.**

Declining self-report compliance is itself an established relapse predictor. A
measured "decoupling" could be pure missingness artifact: fewer responses,
noisier estimates, apparent decorrelation.

**Mandatory control, preregistered:** a model using *only the timing* of
responses — never their content — must fail to reproduce the effect. If timing
alone reproduces it, the finding is compliance, not decoupling.

### Grade — Object 6: **D**

The literal form is unconfirmable and already refuted. What survives is a
different and weaker proposition that must be labelled as such.

---

## Summary

| Object | Consistency | Dimensions | Identifiability | Unique prediction | Grade |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 — H_k(Reach) | ✗ group subtraction | n/a | ✗ Reach unobservable | ✗ generically vacuous | **D** |
| 2 — Q = ‖ΔG‖τ | ✓ | ✓ if standardised | ✓ | ✗ → ✓ after reformulation | **A** |
| 3 — Q_G = ΛQ | ✗ sign vs semantics | ✓ | ✓ | ✗ Λ underdetermined | **B** |
| 4 — ‖ΛΔG‖ > T | ✓ under stiffness only | ✓ | ✓ | ✓ hazard knee | **A** |
| 5 — C(t) = ι(⋃Nᵢ) | ✗ τ collision | ✓ | ✓ | ✓ β₁ higher-order | **A** |
| 6 — C ⟂ L | ✓ | n/a | ✗ null | ✗ already refuted | **D** |

### Declared substitutions, collected

```
════════════════════════════════════════════════════════════════════
 1  Homology comparison        →  covariance-operator distance
    COST: no homological inference is licensed by any result here
 2  Q = ‖ΔG‖·τ                 →  constrained-exponent test β₁ = β₂
    COST: the reformulation is ours; the framework does not force it
 3  Λ                          →  Σ₀⁻¹, stiffness reading
    COST: the resilience gloss on Λ is given up
 5  ι(⋃ᵢ Nᵢ)                   →  Betti numbers of the nerve
    COST: none material; this is the nerve theorem, not a weakening
 6  C ⟂ L                      →  graded pre-transition decoupling
    COST: a different and weaker proposition, never to be reported
          as evidence for orthogonality
════════════════════════════════════════════════════════════════════
```

### The audit's central conclusion

Four of six objects survive as testable propositions **after substitutions that
are declared rather than hidden.** Two do not survive in their written form.

Had the substitutions been made silently — homology quietly becoming a
covariance distance, orthogonality quietly becoming decoupling — the framework
would appear to be grade A and would in fact be untestable, because no result
could ever contradict a claim whose terms shift on contact with data.

**Disclosure is what makes the difference between B and D here.**

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        Λ is not determined by the equations.                         ║
║        The equations are consistent with two opposite worlds.        ║
║        Choose one in writing, or predict nothing.                    ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Mathematical Audit*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) — Preregistration
- [`LITERATURE.md`](LITERATURE.md) — Literature comparison
- [`PROTOCOL.md`](PROTOCOL.md) — Experimental protocol
- [`FALSIFICATION-MATRIX.md`](FALSIFICATION-MATRIX.md) — Kill conditions
