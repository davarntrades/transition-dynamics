<div align="center">

# TRANSITION DYNAMICS

**A Preregistered Falsification Framework**

![Field](https://img.shields.io/badge/Field-Transition_Dynamics-1f2937?style=flat-square)
![Object](https://img.shields.io/badge/Object-Structural_Deformation-4c1d95?style=flat-square)
![Contrast](https://img.shields.io/badge/Contrast-Critical_Slowing_Down-b91c1c?style=flat-square)
![Method](https://img.shields.io/badge/Method-Preregistered_Falsification-047857?style=flat-square)
![Verdict](https://img.shields.io/badge/Provisional_Verdict-B-ca8a04?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)
![Rights](https://img.shields.io/badge/©-Davarn_Morrison-555555?style=flat-square)

</div>

---

*"A framework that cannot be killed is not a framework. It is a decoration. Pick the interpretation first. Write it down. Then let reality decide which half of you was wrong."*

*— Davarn Morrison, 2026*

---

## 0. What This Document Is

This is a **preregistration**, not a result. It fixes — in advance of any data
contact — the physical interpretation of each mathematical object, the
measurement proxy standing in for it, the direction of every predicted effect,
and the exact result that would end the hypothesis.

Three things are held apart everywhere in this repository and are never
silently exchanged:

```
════════════════════════════════════════════════════════════════════
  ORIGINAL MATHEMATICS   the object as written. Fixed. Not repaired.
  PHYSICAL INTERPRETATION  what the object is claimed to be in a body.
  MEASUREMENT PROXY      the computable quantity actually estimated.
════════════════════════════════════════════════════════════════════
```

The mathematics is treated as given. The empirical question is narrower and
harder: **can these objects be validly operationalised in human physiological
and cognitive dynamics at all?**

The answer this document reaches, in advance of data, is: *four of the six can,
one cannot as written, and one is already refuted in its literal form.* Those
findings are stated in §11 and §14 rather than buried.

**Companion documents**

| Document | Contents |
|---|---|
| [`docs/MATHEMATICAL-AUDIT.md`](docs/MATHEMATICAL-AUDIT.md) | Object-by-object adversarial audit: coherence, dimensions, identifiability |
| [`docs/LITERATURE.md`](docs/LITERATURE.md) | Established / related / apparently novel / unknown, with sources |
| [`docs/PROTOCOL.md`](docs/PROTOCOL.md) | Cohorts, windows, estimators, statistics, validation |
| [`docs/FALSIFICATION-MATRIX.md`](docs/FALSIFICATION-MATRIX.md) | Kill conditions per hypothesis |
| [`analysis/estimators.py`](analysis/estimators.py) | Reference implementations. Runnable. |
| [`analysis/base_rates.py`](analysis/base_rates.py) | Base-rate arithmetic. Runnable. |

---

## 1. Formal Transition Dynamics Hypothesis

╔══════════════════════════════════════════════════════════════════════╗
║  TRANSITION DYNAMICS — PRIMARY HYPOTHESIS                            ║
║                                                                      ║
║  In a multivariate physiological system approaching a state          ║
║  transition, the joint structure of the system deforms measurably    ║
║  before any individual channel departs its person-specific range;    ║
║  the deformation, weighted by the system's baseline constraint       ║
║  operator, crosses a reproducible critical magnitude; and the        ║
║  system's linguistic self-report progressively decouples from that   ║
║  deformation during the pre-transition interval.                     ║
║                                                                      ║
║  Reach(s₀) ∩ Ω = ∅  ⟶  ‖ΛΔG‖ > T_critical                            ║
╚══════════════════════════════════════════════════════════════════════╝

The hypothesis decomposes into four independently killable claims:

```
  STRUCTURE    the joint object moves before the marginals do
  PERSISTENCE  magnitude × duration beats either alone
  CONSTRAINT   the baseline stiffness operator adds information
  THRESHOLD    a separatrix exists, not merely a dose-response
```

Claim four is load-bearing. A framework built on a **separatrix** predicts a
discontinuity in hazard. A smooth monotone risk gradient — however predictive —
falsifies the separatrix while leaving a useful detector behind. §6/H4 makes
that distinction the primary test, because it is the only one that
distinguishes this framework from the existing early-warning literature.

---

## 2. Mathematical Definitions

### 2.1 Objects, interpretations, proxies

| Symbol | Original object | Physical interpretation | Measurement proxy |
|:--:|---|---|---|
| Reach(X) | Reachable set from X under admissible inputs | Set of physiological states accessible within the horizon | **Not estimated.** Windowed attractor sample via delay embedding — a strict subset |
| H_k(·) | k-th homology group | Invariant shape of reachable futures | **Not estimated.** See §2.2 |
| ΔG | Topology(X_t) − Topology(X₀) | Structural deformation from baseline | Affine-invariant Riemannian distance d(Σ₀, Σ_t) |
| τ_i | Persistence duration of deformation i | How long the system stays bent | Uninterrupted excursion length of ‖ΔG‖ above θ |
| Q | ‖ΔG‖ · τ | Deformation-persistence product | Same, with θ fixed at baseline 95th percentile |
| Λ | Structural constraint operator | **See §3.** Preregistered as stiffness | Baseline precision matrix Σ₀⁻¹ |
| T_critical | Irreversibility threshold | Separatrix / yield point | Fitted knee in the hazard function |
| C(t) | ι( ⋃ᵢ Nₜ(X, Iᵢ) ) | Integrated multichannel deformation | Betti numbers (β₀, β₁) of the nerve of the co-deformation cover |
| C ⟂ L | ∀Δℓ ∈ L, ΔR_C(t) = 0 | Structure/language orthogonality | **Reformulated.** See §6/H6 |

### 2.2 The substitution that must not be hidden

The truth condition is a statement about **homology groups**:

```
  ∃k :  H_k(Reach(X_t))  ≇  H_k(Reach(X_0))
```

Every estimator in this repository computes a **metric distance** instead.
This is a substitution, and it costs the following, stated once and never
walked back:

> A nonzero metric deformation **does not imply** a homology change.
> A homology change **need not produce** a large metric deformation.
> The two are logically independent. Evidence for the proxy is not evidence
> for the object.

The substitution is made anyway, for three reasons given in full in
[`docs/MATHEMATICAL-AUDIT.md`](docs/MATHEMATICAL-AUDIT.md) and summarised here:

1. **Reach is unobservable.** A person emits one trajectory, not a reachable
   set. Estimating Reach from one realisation requires quasi-stationarity over
   the window — the exact assumption a transition violates. The object is
   estimated by assuming the negation of what is being tested.
2. **Reach is generically contractible.** For a controlled system without
   forbidden holes, the reachable tube is path-connected and simply connected.
   Then H₀ = ℤ and H_k = 0 for all k ≥ 1, at every t. The truth condition is
   never satisfied — not rarely, *never*. It carries no empirical content until
   Ω is a physically realised excluded region.
3. **ΔG as written is a category error.** `Topology(X_t) − Topology(X_0)` subtracts
   groups. Subtraction is not defined on the category of groups. The expression
   acquires meaning only after choosing a numerical functor — Betti vector,
   persistence diagram, or covariance operator — and that choice is an
   empirical commitment, not a notational convenience.

Betti-vector differences were considered and rejected as the primary proxy:
they are integer-quantised, so sub-threshold deformation returns exactly zero
and no graded early warning is possible. Persistent homology is deferred by
design — see §8.6.

### 2.3 Dimensional statement

With every channel z-scored against its own baseline window:

| Quantity | Units |
|:--:|:--:|
| ‖ΔG‖ | dimensionless |
| τ | time |
| Q = ‖ΔG‖·τ | time |
| Λ_B = Σ₀⁻¹ | dimensionless |
| ‖Λ_B ΔG‖ | dimensionless |
| Λ_A = I − A | time⁻¹ |
| ‖Λ_A ΔG‖ | time⁻¹ |

**Consequence, fixed in advance:** T_critical carries different units under the
two readings of Λ. A threshold fitted under one reading is not comparable to a
threshold fitted under the other. They are separate experiments and are
reported separately.

---

## 3. Preregistered Interpretation of Λ

╔══════════════════════════════════════════════════════════════════════╗
║  PRIMARY:  Λ ≡ STRUCTURAL CONSTRAINT / STIFFNESS                     ║
║                                                                      ║
║  Λ_B  :=  Σ₀⁻¹     the baseline precision operator                   ║
║                                                                      ║
║  ‖ΛΔG‖ > T_critical  is a YIELD CRITERION:  stress = stiffness×strain ║
╚══════════════════════════════════════════════════════════════════════╝

**Why this reading and not the other.** For a system at Gaussian equilibrium
p(x) ∝ exp(−½ xᵀΣ₀⁻¹x), the Hessian of the potential is exactly Σ₀⁻¹. The
precision matrix *is* the stiffness operator — not by analogy, by construction.
Under this reading:

```
  ‖ΛΔG‖  =  √( δᵀ Σ₀⁻¹ δ )  =  √(2 × deformation energy)
```

and the irreversibility criterion is the Hookean yield condition, coherent
**as written, with no sign change and no rearrangement.** Since the instruction
is to treat the original mathematics as fixed, the interpretation that makes
the fixed mathematics coherent is the one that must be preregistered.

**Direction fixed in advance.** Λ_B is anisotropic: it is stiff in
tightly-constrained directions and compliant in loosely-constrained ones. The
prediction is that pre-transition deformation is disproportionately directed
along **stiff** eigen-directions of Σ₀⁻¹, so that ‖Λ_B ΔG‖ rises faster than
‖ΔG‖ alone. If deformation is isotropic with respect to the baseline spectrum,
Λ adds nothing and H3 dies.

**What this commits us to.** The stiffness reading predicts pre-transition
**loss of degrees of freedom** — variance concentrating into fewer directions,
coupling increasing, the system becoming more rigid. This is the
*decomplexification* direction. It is the opposite of the variance-increase
predicted by critical slowing down. The framework is therefore **not** a
relabelling of existing early-warning signals; it is in direct competition with
them, and one of the two must lose. That is the point.

---

## 4. Alternative Λ Interpretation

╔══════════════════════════════════════════════════════════════════════╗
║  ALTERNATIVE:  Λ ≡ RESILIENCE / RECOVERY CAPACITY                    ║
║                                                                      ║
║  Λ_A  :=  I − A     from  x_{t+1} = A x_t + ε                        ║
║                                                                      ║
║  REQUIRES MODIFIED CRITERION:  ‖Λ⁻¹ΔG‖ > T_critical                  ║
╚══════════════════════════════════════════════════════════════════════╝

Critical slowing down is the statement that the spectral radius of A tends to 1
as a transition is approached, hence Λ_A → 0.

**Stated in advance:** under this reading, ‖Λ_A ΔG‖ *decreases* toward the
transition, so the criterion `‖ΛΔG‖ > T_critical` **can never fire**. Reading A
is not merely a different interpretation — it is incompatible with the original
equation's form. Testing it requires inverting the operator, which **modifies
the original mathematics**. That modification is flagged wherever it appears
and is never presented as the original claim.

**The two readings are not always distinguishable.** For a one-dimensional
linear system ẋ = −kx + ξ, the restoring stiffness and the recovery rate are
the *same parameter k*. A and B are degenerate in one dimension. They separate
only in the multivariate case, where Σ₀ depends on both the restoring operator
A and the noise covariance, so Σ₀⁻¹ and (I − A) carry different information.

**This is why the study must be multivariate.** A univariate design cannot
discriminate the primary interpretation from the alternative, and would produce
a result that confirms whichever was assumed. Any univariate finding is
therefore excluded from the confirmatory analysis in advance.

### 4.1 The discriminating prediction

| | Λ_B — stiffness (primary) | Λ_A — recovery (alternative) |
|---|---|---|
| Variance before transition | **falls** (rigidification) | **rises** (slowing down) |
| Lag-1 autocorrelation | ambiguous | **rises** |
| Effective dimensionality | **falls** | ~unchanged |
| Channel coupling | **rises** | rises |
| Criterion form | `‖ΛΔG‖ > T` as written | `‖Λ⁻¹ΔG‖ > T`, modified |
| Existing support | HeRO: *reduced* HRV precedes neonatal sepsis | van de Leemput: *rising* variance precedes depression transition |

Both directions have published empirical support, in different systems. They
cannot both be the general law. The variance-direction test in H3 is designed
to make one of them lose, and is the single most informative measurement in
this preregistration.

---

## 5. Operationalisation Table

| # | Original mathematics | Physical interpretation | Operational variable | Measurement | Estimator |
|:--:|---|---|---|---|---|
| 1 | ∃k: H_k(Reach(X_t)) ≇ H_k(Reach(X₀)) | Reachable-future shape changes | `dG_struct` | 10–14 channel vitals, regular grid | `delta_G_structure` — Riemannian d(Σ₀,Σ_t) |
| 1b | — | State displacement from baseline | `dG_state` | same | `delta_G_state` — Mahalanobis |
| 2 | Q = ‖ΔG‖·τ | Deformation × persistence | `Q` | θ = baseline p95 of ‖ΔG‖ | `Q_deformation_persistence` |
| 2b | — | Comparator: true integral | `Q_int` | same | `Q_integral` — ∫‖ΔG‖dt |
| 3 | Q_G = ΛQ | Constrained deformation-persistence | `QG` | baseline precision operator | `Lambda_B_stiffness` ∘ `Q` |
| 4 | ‖ΛΔG‖ > T_critical | Yield / separatrix crossing | `energy` | — | `deformation_energy` |
| 4b | — | Alternative reading | `energy_A` | VAR(1) fit | `Lambda_A_recovery`, inverted |
| 5 | C(t) = ι(⋃ᵢ Nₜ(X,Iᵢ)) | Integrated multichannel deformation | `b0`, `b1` | per-channel z-excursions | `codeformation_complex` → `betti_numbers` |
| 6 | C ⟂ L | Structure/language decoupling | `rho_CL`, `div_CL` | EMA + passive sensing | `structural_report_coupling`, `divergence_index` |

Every estimator is implemented and runnable in
[`analysis/estimators.py`](analysis/estimators.py). The file's self-test
demonstrates that the suite detects a fold transition and **fails to detect a
noise-induced transition** — see §11.

---

## 6. Hypotheses H1–H6

Full specification per hypothesis — nulls, competing hypotheses, confounders,
falsification criteria — is in
[`docs/FALSIFICATION-MATRIX.md`](docs/FALSIFICATION-MATRIX.md). Core statements:

### H1 — Structural deformation precedes conventional threshold crossing

**Prediction.** Restrict analysis to time points at which *every* individual
channel lies inside both its population reference range and its person-specific
range. Within that restricted set, `dG_struct` discriminates windows preceding
a transition from windows that do not.

**Direction.** AUPRC(dG_struct) > AUPRC(chance) with a lower confidence bound
above the comparator built from the same channels' marginal values.

**Temporal.** Median lead time ≥ 2 h before the transition event (ICU); the
alert must fire while all marginals remain in range.

**Null.** dG_struct carries no discrimination once marginals are in range.

**Competing.** Deformation is detectable but only *simultaneously* with
marginal departure — the structure adds no lead time, only a restatement.

**Kills H1.** Lead-time advantage over a marginals-only model with a 95% CI
including zero, in the primary cohort *and* external validation.

### H2 — Q = ‖ΔG‖·τ beats magnitude or persistence alone

**Prediction.** Fit `logit(P) = β₀ + β₁·log‖ΔG‖ + β₂·log τ`. The Morrison
product form is the constraint **β₁ = β₂**.

**This is the sharp version.** Q is not independent of its own factors — τ is
defined by a threshold on ‖ΔG‖ — so "Q carries new information" is not a
coherent claim. The coherent claim is that the *exponents are equal*, i.e. that
the relationship is genuinely multiplicative. That is testable by Wald test and
by AIC against the unconstrained model. Because units affect only the
intercept, the test is unit-invariant.

**Kills H2.** β₂ not distinguishable from 0 (τ contributes nothing), **or** the
unconstrained model beats the constrained one by ΔAIC > 10, **or** the integral
form `Q_int` beats the product form by ΔAIC > 10 — in which case the *idea*
survives but the specific written product form does not.

### H3 — The preregistered Λ adds information beyond ΔG and Q

**Prediction.** `‖Λ_B ΔG‖` improves discrimination over `‖ΔG‖` and `Q` in a
nested model. Accompanied by the directional test in §4.1: effective
dimensionality and channel variance **fall** before transition.

**Competing.** Λ_A. Variance and autocorrelation **rise**; effective
dimensionality unchanged.

**Kills H3 (primary reading).** Pre-transition variance rises and effective
dimensionality is flat or rising, with Λ_A-based models outperforming Λ_B-based
models. The primary interpretation is then abandoned — **not redefined** — and
the framework continues under the explicitly modified criterion of §4.

### H4 — ‖ΛΔG‖ exhibits a reproducible critical threshold

**Prediction.** The hazard as a function of `‖Λ_B ΔG‖` contains a **knee**: a
threshold model fits better than a smooth monotone model, and the fitted
T_critical transfers across cohorts.

**This is the load-bearing test.** It is the only hypothesis that distinguishes
a separatrix from a risk gradient.

**Kills H4.** A monotone smooth hazard fits as well as or better than a
threshold model (ΔAIC ≤ 10 in favour of smooth), **or** the between-cohort
coefficient of variation of fitted T_critical exceeds 0.5. Either result
falsifies the *separatrix*, and with it the irreversibility claim, while
possibly leaving a useful predictor intact. Those two outcomes must be
reported separately and must not be conflated.

### H5 — Integrated multichannel deformation beats isolated channels

**Prediction — sharpened.** The weak form ("multivariate beats univariate") is
already established and is not tested as a novel claim. The tested claim is:
**β₁ of the co-deformation complex adds discrimination beyond the full set of
pairwise channel couplings.**

β₁ is determined by which triangles are filled, i.e. by third-order
co-deformation support, and is provably not a function of pairwise supports
alone. This makes H5 a genuine higher-order claim.

**Kills H5.** A model containing every pairwise coupling matches the
β₁-augmented model (ΔAUPRC 95% CI includes zero). The integration operator is
then decorative.

### H6 — C ⟂ L produces measurable pre-transition decoupling

**The literal form is not tested, because it is already false.** `∀Δℓ ∈ L,
ΔR_C(t) = 0` asserts that no change confined to language moves cognitive
reachable structure. Psychotherapy, verbal instruction, and placebo suggestion
each refute it with a single counterexample. It is also a null, and nulls
cannot be confirmed. See [`docs/MATHEMATICAL-AUDIT.md`](docs/MATHEMATICAL-AUDIT.md) §6.

**The tested form.** Coupling ρ(t) between structural deformation and
self-report deformation **declines** during the pre-transition window, with
**signed divergence**: structure deforming upward while self-report is flat or
improving.

**Direction.** `divergence_index` > 0 and increasing in the 14 days before
transition; ρ(t) lower than the person's own baseline coupling.

**Kills H6.** Coupling is stable or rises pre-transition; **or** the divergence
is fully explained by declining EMA compliance (see confounder below).

**Mandatory confounder control.** Declining self-report compliance is itself a
known relapse predictor. A "decoupling" produced by missingness is an artifact.
The preregistered control is a compliance-matched analysis plus a
**response-timing-only negative control model**: if a model using *only* when
responses arrived — never their content — reproduces the effect, H6 is dead.

---

## 7. Literature Comparison

Full detail and sources: [`docs/LITERATURE.md`](docs/LITERATURE.md).

### ALREADY ESTABLISHED — claimed by this framework, owned by others

```
════════════════════════════════════════════════════════════════════
 Critical slowing down as early warning        Scheffer et al.
 Rising variance/AR(1) before depression       van de Leemput 2014 PNAS
 Covariance-based pre-disease detection        Chen/Aihara DNB 2012
 Multichannel physiological network shifts     Bashan/Ivanov 2012
 Structure precedes conventional biomarkers    HeRO neonatal sepsis RCT
 Persistent homology on HRV                    multiple, established method
 Deterioration models fail on base rate        Wong 2021 JAMA Intern Med
════════════════════════════════════════════════════════════════════
```

**The core research question is already answered affirmatively in at least one
domain.** HeRO — reduced heart-rate variability plus decelerations — detects
neonatal sepsis before clinical signs, and displaying the score reduced
sepsis-associated mortality from ~20% to ~12% in a 3,003-infant randomised
trial. H1 in its generic form is **not novel**. Dynamical Network Biomarker
theory already covers the covariance-deformation core of H1 and H5. Any claim
of novelty for those must be withdrawn.

### RELATED BUT NOT EQUIVALENT

- TDA of physiological time series exists, but is used for **classification**,
  not preregistered pre-transition prediction against a mechanistic threshold.
- Resilience/recovery indices exist, but not as an operator Λ inside a yield
  criterion.
- Attractor-landscape reachability exists in cell biology, computed **from
  models**, not estimated from human physiological recordings.

### APPARENTLY NOVEL

- The constrained-exponent test of the product form Q = ‖ΔG‖·τ (H2).
- The yield-criterion reading of Λ as *rigidity*, tested head-to-head against
  the critical-slowing-down direction (H3/§4.1).
- β₁ of the co-deformation nerve as a higher-order predictor beyond all
  pairwise couplings (H5).
- Preregistered signed structure/report decoupling as an early-warning signal
  in its own right (H6).

**Novelty is claimed weakly and provisionally.** Absence of located prior work
is not evidence of novelty. The DNB literature is large and substantially
non-English; the covariance components of H1/H5 are likely covered somewhere in
it. This section is a hypothesis about the literature, and is itself subject to
revision on contact with a librarian.

### UNKNOWN / REQUIRES TESTING

- Whether T_critical is **reproducible across individuals** or purely personal.
  This is the make-or-break unknown. If it transfers, it is a genuinely new
  result. If it does not, the "critical threshold" is a per-person fitted
  parameter and the universality claim collapses.
- Whether ΔG carries any pre-transition signal at ~hourly EHR resolution.
- Whether the Λ_B / Λ_A sign is domain-dependent rather than universal.

### The adversarial findings that must be read first

Three published results directly threaten this framework and are placed here
rather than in a footnote:

1. **No evidence for critical slowing down prior to human epileptic seizures.**
   Wilkat, Rings & Lehnertz, *Chaos* 2019 — 28 subjects, 105 seizures,
   surrogate-controlled: variance and lag-1 autocorrelation showed no
   pre-seizure signature. The prototypical human critical transition does not
   display the prototypical early warning.
2. **Little support for early warning signals in clinical psychology.**
   *Nature Reviews Psychology* 2024 — floor effects, measurement error and
   measurement non-invariance undermine most positive EMA findings.
3. **Early warning signals are specific to fold bifurcations.** Noise-induced
   and rate-induced tipping produce transitions with **no precursor at all**.
   If human deterioration is predominantly noise-induced, this framework is
   unfalsifiable-in-practice rather than false: there is nothing to detect.

Point 3 is reproduced in this repository's own estimator self-test, which shows
the suite is blind to a noise-induced transition by construction.

---

## 8. Experimental Protocol

Full protocol: [`docs/PROTOCOL.md`](docs/PROTOCOL.md). Summary:

### 8.1 MIMIC-IV — evaluated first, and demoted

| Hypothesis | MIMIC-IV verdict | Reason |
|:--:|:--:|---|
| H1 | **Marginal** | Vitals ~hourly and irregular. A 24 h window gives ~24 samples for a 10-dim covariance — ill-conditioned without heavy shrinkage |
| H2 | **Weak** | τ estimation needs resolution MIMIC-IV does not have |
| H3 | **Marginal** | Λ_B estimable with shrinkage; Λ_A (VAR fit) poorly identified at hourly spacing |
| H4 | **Weak** | Threshold localisation needs a well-sampled ‖ΛΔG‖ trajectory |
| H5 | **Marginal** | Enough channels, insufficient temporal support for third-order co-occurrence |
| H6 | **CANNOT TEST** | MIMIC contains *clinician* notes, not patient self-report. Observer language is not the L subspace |

**Decision, fixed in advance: MIMIC-IV is not the primary cohort.** It is the
**external validation** cohort. Using it as primary would produce a weak null
that is uninformative about the hypothesis and informative only about sampling
rate.

**Primary cohort: HiRID** — ~34,000 admissions, most vital signs at **2-minute
resolution**, with an established physiology-defined circulatory-failure
endpoint. This is the only public ICU dataset with the temporal resolution the
estimators require.

*Dataset specifications above are from secondary sources; PhysioNet was not
directly reachable from this environment. Every figure must be re-verified
against the dataset landing pages before the protocol is executed.*

### 8.2 Endpoint — physiology, not clinician behaviour

Vasopressor initiation is a **treatment decision** made by clinicians reading
the same vitals. Predicting it from vitals partly predicts clinician
behaviour. The preregistered endpoint is HiRID's physiology-defined circulatory
failure (sustained MAP below threshold with concurrent lactate elevation), not
an order-entry event.

### 8.3 Windows

```
  BASELINE        first 8 h of stable recording, no active titration
  PRE-TRANSITION  8 h before event onset
  BLANKING        30 min immediately pre-event, excluded — treatment
                  contamination and reverse causation
  CONTROL         length-of-stay matched, never transitioning
```

### 8.4 Mandatory negative controls

Preregistered, and any positive result is void without them:

1. **Sampling-rate-only model.** Features built from *measurement times alone*,
   no values. Clinicians measure more often when worried; this leaks the label
   through the covariance structure. If this model approaches the real model,
   the finding is leakage.
2. **Intervention masking.** Windows containing fluid bolus, vasopressor
   titration, sedation change, transfusion or ventilator adjustment are flagged
   and analysed separately. Treatments deform covariance directly.
3. **Label shuffle** and **patient shuffle** — must return chance.
4. **Placebo window** — a pre-baseline interval must show no effect.

### 8.5 Statistics

Discrete-time survival with time-varying covariates; person-specific random
intercepts; landmark analysis at fixed horizons. **AUPRC is the headline
metric, not AUROC** — the class imbalance makes AUROC cosmetically flattering.
Calibration by intercept, slope and integrated calibration index. Decision
curve analysis. Out-of-sample validation by **hospital/site**, never by random
split.

### 8.6 Topology is deferred by design

Per the instruction to prefer the simplest estimator that can falsify:
persistent homology is **not used in the primary analysis**. It is introduced
only if, and only after, the covariance and nerve-complex estimators are shown
to be insufficient — and its introduction requires a documented statement of
what the simpler estimators failed to resolve.

### 8.7 C ⟂ L cohorts

MIMIC cannot test H6. Candidate datasets carrying both longitudinal
self-report and passive sensing:

| Dataset | Population | Carries |
|---|---|---|
| **CrossCheck** | Schizophrenia / schizoaffective | EMA + passive sensing + relapse events. **Primary for H6** |
| GLOBEM | Multi-year student cohort | Repeated-wave EMA + sensing; generalisation testing |
| StudentLife | Student cohort, 10 weeks | EMA + sensing; short horizon limits transition capture |
| RADAR-MDD | Major depressive disorder | Depression-organised, relapse endpoints |

CrossCheck is primary because it is the only one with a clinically adjudicated
transition event of the required severity.

---

## 9. Falsification Matrix

Full matrix: [`docs/FALSIFICATION-MATRIX.md`](docs/FALSIFICATION-MATRIX.md).

| H | Kill condition | What survives the kill |
|:--:|---|---|
| H1 | No lead time over marginals-only model, primary **and** external | Nothing. H1 is the floor |
| H2 | β₂ ≈ 0, or unconstrained/integral form wins by ΔAIC > 10 | Deformation predicts; the written product form does not |
| H3 | Variance rises + dimensionality flat + Λ_A wins | Framework continues under §4's *modified* criterion |
| H4 | Smooth hazard fits as well as threshold, or CV(T_crit) > 0.5 | A useful predictor with **no separatrix**. Irreversibility claim dies |
| H5 | Pairwise-complete model matches β₁-augmented model | Integration is decorative; multivariate core survives |
| H6 | Coupling stable, or explained by compliance decline | C ⟂ L has no physiological instantiation |
| **All** | Sampling-rate-only control approaches the real model | **Everything.** The entire result is leakage |

---

## 10. Base-Rate Analysis

Generated output: [`analysis/results/base_rate_tables.md`](analysis/results/base_rate_tables.md).
Reproduce: `python3 analysis/base_rates.py`.

At a strong operating point (sensitivity 0.80, specificity 0.95):

| Setting | Per-window prevalence | PPV | Alerts per true event | False alerts per patient |
|---|:--:|:--:|:--:|:--:|
| ICU circulatory failure | 0.030 | **0.331** | 3.0 | 1.75 |
| ICU sepsis onset | 0.010 | **0.139** | 7.2 | 3.56 |
| Ward deterioration | 0.004 | **0.060** | 16.6 | 1.39 |
| Psychosis relapse (weekly) | 0.008 | **0.117** | 8.5 | 1.98 |
| Depression recurrence (weekly) | 0.004 | **0.064** | 15.5 | 2.59 |

Specificity required to reach PPV ≥ 0.33 at sensitivity 0.80:

```
  ICU circulatory failure   0.9498
  ICU sepsis onset          0.9836
  Psychosis relapse         0.9865
  Depression recurrence     0.9930
  Ward deterioration        0.9935
════════════════════════════════════════════════════════════════════
  Every setting except event-rich ICU circulatory failure demands
  specificity in the 0.98–0.99+ region. No published early-warning
  system in these domains currently achieves it.
════════════════════════════════════════════════════════════════════
```

**Reference floor.** The Epic Sepsis Model — deployed at hundreds of hospitals —
achieved sensitivity 0.33, specificity 0.83, AUROC 0.63, PPV 0.12 on 38,455
hospitalisations, while alerting on 18% of all admissions. Any Transition
Dynamics estimator that does not beat this decisively is not worth discussing.

### The preregistered utility gate

A result may be described as **detection of structural transition dynamics** on
discrimination evidence alone. It may be described as a candidate for clinical
use **only** if it simultaneously achieves, out of sample, at the setting's true
prevalence: PPV ≥ 0.20, ≤ 1 false alert per patient per horizon, median lead
time ≥ 2 h (ICU) or ≥ 7 d (psychiatric), and calibration slope in [0.8, 1.25].

---

## 11. Capability and Limitation Boundary

### What this framework can do

- Detect joint-structure deformation while marginals remain in range.
- Provide a person-specific baseline metric rather than a population threshold.
- Test a genuine higher-order integration claim (β₁).
- Discriminate the rigidification direction from the slowing-down direction.

### What this framework cannot do — structural limits, not current gaps

```
┌──────────────────────────────────────────────────────────────────┐
│  BLIND TO NOISE-INDUCED TRANSITIONS                              │
│  Demonstrated in this repository's own estimator self-test.      │
│  A large shock crossing a separatrix leaves no precursor.        │
│  ΔG, ‖ΛΔG‖ and ρ(A) all remain at null levels until it happens.  │
│  If human deterioration is predominantly shock-driven, there is  │
│  nothing here to find — and that is not a failure of estimation. │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  CANNOT ESTIMATE Reach                                           │
│  One person emits one trajectory. The reachable set is not       │
│  observable. Everything computed is an attractor sample under a  │
│  quasi-stationarity assumption that a transition violates.       │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  CANNOT TEST HOMOLOGY CHANGE                                     │
│  Every estimator is metric. Metric evidence is not homological   │
│  evidence. The truth condition of §2.2 remains untested by this  │
│  protocol and is not claimed to be tested.                       │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  RESOLUTION-BOUND                                                │
│  At ~hourly EHR sampling the covariance estimate is              │
│  ill-conditioned and τ is barely defined. A null in MIMIC-IV     │
│  would be evidence about sampling rate, not about the hypothesis.│
└──────────────────────────────────────────────────────────────────┘
```

---

## 12. Minimum Experiment That Could Kill the Hypothesis

╔══════════════════════════════════════════════════════════════════════╗
║  THE KILL EXPERIMENT                                                 ║
║                                                                      ║
║  Cohort    HiRID, circulatory-failure endpoint, 2-min resolution     ║
║  Restrict  windows where EVERY channel is inside its person-specific ║
║            range — so conventional monitoring says "normal"          ║
║  Compute   dG_struct, ‖Λ_B ΔG‖, and the sampling-rate-only control   ║
║  Compare   against a marginals-only model on identical windows       ║
║  Validate  out of sample, by site, in MIMIC-IV and eICU              ║
║                                                                      ║
║  KILL:  ΔAUPRC 95% CI includes zero — or the sampling-rate-only      ║
║         control matches the real model.                             ║
╚══════════════════════════════════════════════════════════════════════╝

This is a single retrospective analysis on existing public data. It requires no
new collection, and it tests the floor claim H1. **If H1 dies, H2–H5 are not
worth running** — they are all refinements of a deformation signal that would
have been shown not to exist.

H6 requires a separate minimum experiment in CrossCheck, with the
response-timing-only control as its own kill condition.

---

## 13. Minimum Result That Would Justify Further Investigation

```
  1  ΔAUPRC over the marginals-only model, lower 95% bound > 0,
     on windows where every channel is in range
  2  Median lead time ≥ 2 h, replicated out of sample by site
  3  Sampling-rate-only control at or near chance
  4  Effect surviving intervention masking
```

All four. Not three. Item 3 is not negotiable: without it the result is
indistinguishable from clinicians measuring more often when worried.

This threshold justifies **further investigation only**. It does not license
any clinical claim — that requires the §10 utility gate.

---

## 14. Claims We Are NOT Entitled to Make

╔══════════════════════════════════════════════════════════════════════╗
║  NOT ENTITLED                                                        ║
╚══════════════════════════════════════════════════════════════════════╝

| We may not say | Because |
|---|---|
| "This measures consciousness" | C(t) here is the Betti number of a co-deformation complex. Nothing connects it to experience |
| "This measures qualia" | Q is a deformation-persistence product. The philosophical interpretation is untested and not testable by this protocol |
| "The topology of reachable futures changed" | No homology group was computed. Metric evidence ≠ homological evidence |
| "Λ is validated as a governance constant" | Only one numerical reading of Λ is tested, in one physiological setting |
| "T_critical is a universal constant" | Until it transfers across cohorts it is a fitted per-cohort parameter |
| "This is a disease predictor" | Until the §10 utility gate is cleared, the only permitted claim is *detection of structural transition dynamics* |
| "C ⟂ L is confirmed" | The literal form is already false. Only decoupling is tested, and decoupling is not orthogonality |
| "The Morrison Framework is empirically validated" | This tests one operationalisation of four objects in one domain. It cannot validate a general theory of intelligence |
| "Structural deformation precedes biomarkers — novel" | HeRO established this in neonatal sepsis, with a mortality-reducing RCT |
| "A null result refutes the mathematics" | It refutes *this operationalisation*. The objects may be valid and badly proxied |

The last row cuts both ways and is the honest cost of the proxy substitution in
§2.2: **this protocol can fail without the framework being wrong, and can
succeed without the framework being right.** It tests operationalisability, not
truth.

---

## 15. Provisional Classification

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   B — COHERENT BUT REQUIRES BETTER OPERATIONALISATION                ║
║                                                                      ║
║   with one component at A and two components at D                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

A single letter would be dishonest. The framework is not uniform:

| Object | Grade | Why |
|:--:|:--:|---|
| **1** — H_k(Reach(X_t)) ≇ H_k(Reach(X₀)) | **D** | Reach is unobservable from one trajectory; generically contractible so the condition never fires; `Topology(X_t) − Topology(X₀)` subtracts groups, which is undefined. Not empirically testable as written |
| **2** — Q = ‖ΔG‖·τ | **A** | Dimensionally coherent once channels are standardised. τ is not independent of ‖ΔG‖, but the constrained-exponent reformulation gives a unique, sharp, unit-invariant prediction |
| **3** — Q_G = ΛQ | **B** | Coherent, but Λ is not uniquely determined by the mathematics. Requires the preregistered §3 choice, which the equations do not force |
| **4** — ‖ΛΔG‖ > T_critical | **A** | Coherent as a yield criterion under the stiffness reading — and *only* under it. Generates the unique testable prediction of a hazard knee |
| **5** — C(t) = ι(⋃ᵢ Nₜ) | **A** | The nerve construction makes ι well-defined and computable, and β₁ yields a genuine higher-order prediction. Requires resolving the τ symbol collision |
| **6** — C ⟂ L | **D** | Literal form asserts a null (unconfirmable) and is already refuted by verbal interventions that move physiology. Only survives as a decoupling claim, which is a different proposition |

### Why B and not A

Three defects block A, and all three are defects of *operationalisation*, not
of arithmetic:

1. **Λ is not determined by the mathematics.** The equations are consistent with
   two readings that predict opposite signs. The framework requires an external
   choice to generate a prediction at all. §3 supplies one; the mathematics
   does not.
2. **Object 1 is non-identifiable**, and it is the framework's own stated truth
   condition. Everything downstream runs on an admitted proxy.
3. **τ is defined by a threshold on ‖ΔG‖**, so Q is not a function of
   independent quantities. Repairable — and repaired in H2 — but the repair is
   ours, not the framework's.

### Why B and not C

Underdetermination would mean no unique empirical prediction exists. That is
not the case. After the §3 preregistration, objects 2, 4 and 5 each generate a
unique, directional, falsifiable prediction with a stated kill condition, and
§12 specifies a single retrospective experiment on existing public data that
can end the primary claim. A framework with a defined kill experiment is not
underdetermined.

### Why not D overall

Two of six objects are D. Four are not. The framework survives as a whole
because objects 2, 4 and 5 remain coherent and testable after the substitutions
in §2 are made **explicitly**. Had those substitutions been made silently, the
correct grade would be D — and the difference between B and D here is entirely
a matter of disclosure.

### The single most important sentence in this document

> The primary interpretation of Λ predicts that variance **falls** before a
> transition. The dominant early-warning literature predicts that it **rises**.
> One of them is wrong, the disagreement is measurable in existing public data,
> and this preregistration commits to the answer before looking.

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              ‖ Λ ΔG ‖  >  T_critical                                 ║
║                                                                      ║
║        Preregistered. Directional. Killable.                         ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Preregistered Falsification Framework*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`docs/MATHEMATICAL-AUDIT.md`](docs/MATHEMATICAL-AUDIT.md) — Adversarial audit of the six objects
- [`docs/LITERATURE.md`](docs/LITERATURE.md) — Established / related / novel / unknown
- [`docs/PROTOCOL.md`](docs/PROTOCOL.md) — Experimental protocol
- [`docs/FALSIFICATION-MATRIX.md`](docs/FALSIFICATION-MATRIX.md) — Kill conditions
