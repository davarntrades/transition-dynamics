<div align="center">

# THE REVISED HYPOTHESIS

**Transition Dynamics v2 · Physiological State Model · Transition Pipeline**

![Scope](https://img.shields.io/badge/Scope-Acute_Physiological_Transitions-1f2937?style=flat-square)
![Claim](https://img.shields.io/badge/Claim-Mechanism_Identification-047857?style=flat-square)
![Permitted](https://img.shields.io/badge/Permitted_Conclusion-NO_DETECTABLE_PRECURSOR-b91c1c?style=flat-square)

</div>

---

*"A hypothesis that cannot return the answer 'nothing is there' is not measuring anything."*

*— Davarn Morrison, 2026*

---

> ## ⚠ HISTORICAL — written before any real data was analysed
>
> This document records what was **proposed**. It is retained unchanged as part
> of the scientific record and is **not** a statement of current status.
>
> Seven experiments have since been run on real VitalDB data. Four returned
> NOT SUPPORTED, one SUPPORTED in a narrow measurement-level scope, one
> UNRESOLVED. In particular **mechanism identification is not a surviving
> contribution**, and the stiffness reading of $\Lambda=\Sigma_0^{-1}$ is
> demoted.
>
> **Current status: [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) governs.**
> `main` is the canonical branch.
>
> **Specific to this document:** the badge and framing describing the claim
> as *Mechanism Identification* record the v2 proposal. That claim was tested
> and is **not** supported on real physiology.

---

## 1. Statement

> **Primary hypothesis**
>
> In a subset of acute physiological state transitions, the multivariate
> structure of physiological measurements changes measurably before
> conventional transition criteria are satisfied.

The hypothesis tests five things:

1. Multivariate structural deformation appears before transition.
2. Deformation persistence adds information beyond magnitude alone.
3. Baseline structural constraint changes the significance of deformation.
4. The constrained deformation quantity shows reproducible transition-related
   behaviour.
5. Higher-order multichannel structure adds information beyond individual
   channels and pairwise relationships.

**It is not claimed that all transitions behave this way.** "No detectable
precursor" is an explicitly permitted outcome.

**The self-report / language decoupling hypothesis is not part of this
hypothesis.** It is exploratory and lives in
[`DEMOTED_OBJECTS.md`](DEMOTED_OBJECTS.md).

### 1.0 The distinguishing sub-claim — DEMOTED 2026-09-11

Previously load-bearing: that the **direction** of constrained deformation
identifies which mechanism produced a transition.

**Demoted, then partly restored.** The instrument test found that exposure
duration alone reproduced almost the whole effect in the operating regime, so
an observed alignment could not be attributed to mechanism.

A four-stage follow-up resolved the identifiability question. Under oracle
exposure control, alignment separates targeting at within-stratum AUC 0.939
(0.998 in the detectable regime, against 0.746 for covariance drift). Onset is
estimable from the displacement trajectory using only baseline-derived rates,
with median error 1.2 time units, and estimated-exposure control removes a
deliberately constructed spurious effect exactly, matching the oracle. See
[`RESULT_EXPOSURE_STAGES.md`](RESULT_EXPOSURE_STAGES.md) and
[`RESULT_HOMEOSTATIC_PREMISE.md`](RESULT_HOMEOSTATIC_PREMISE.md).

The claim is therefore **identifiable in principle and operationally
identifiable in the regime tested**, subject to three stated limits and one
structural caveat: the onset estimator assumes the same exponential-approach
form the simulator generates, so its validation is close to a consistency
check. Nothing here tests real physiology.

What survives is weaker and descriptive: alignment carries information that
neither conventional univariate monitoring nor covariance drift carries, above
a displacement floor of roughly 0.5 baseline SD. That is a statement about
independence from existing methods, **not** about mechanism.

### 1.1 What changed from v1, and why

| v1 claim | v2 status | Cause |
|---|---|---|
| Structure deforms before biomarkers | **Retained, but not novel** | Established by HeRO and DNB. Used as the floor, not the contribution |
| Λ predicts variance falls pre-transition | **WITHDRAWN** | Does not follow from Λ = Σ₀⁻¹. Λ is a frozen metric, not a state variable |
| Transition Dynamics vs critical slowing down: one must lose | **WITHDRAWN** | Benchmark shows they are complementary — each detects the mechanism the other misses |
| The contribution is detection | **NARROWED to mechanism identification** | Plain covariance drift scores AUC 1.00 on both detectable mechanisms. Detection adds nothing over 2012 methods |

The narrowing is not a retreat to safety. It is the **smallest claim the
evidence has not already killed**, which is the only kind worth preregistering.

### 1.2 What is explicitly NOT claimed

> **We do NOT claim that all cardiac arrests have detectable precursors.**
>
> We do NOT claim that all sepsis has detectable precursors.
> We do NOT claim that all catastrophic events have precursors.
> We do NOT claim this is a disease predictor.

**Noise-induced and genuinely abrupt transitions remain live failure classes.**
The benchmark confirms the estimator suite is blind to them by construction:
a real transition occurs and every statistic stays at its stationary null. Any
estimator that appeared to anticipate such a case would be reporting leakage.

> **THE FRAMEWORK IS PERMITTED — AND REQUIRED — TO CONCLUDE:**
>
> NO DETECTABLE PRECURSOR
> for a transition class, a cohort, or the whole hypothesis.
> That outcome is a result, not a failure of the study.

### 1.3 Candidate transition scope

Cardiac and circulatory deterioration; cardiac arrest **where a detectable
precursor actually exists**; sepsis-related deterioration; respiratory failure;
haemodynamic collapse; neurological transitions; multi-organ deterioration.

Scope is a hypothesis, not an assumption. Which of these classes carries a
precursor is the question of [`TRANSITION_TAXONOMY.md`](TRANSITION_TAXONOMY.md).

---

## 2. The Physiological State Model

### 2.1 State vector

```
  X(t)  =  [ x₁(t), x₂(t), …, x_n(t) ]ᵀ
```

Candidate channels, **not assumed present in any given dataset**:

| Channel | Typical resolution | Homeostatic defence |
|---|:--:|:--:|
| Heart rate | seconds–minutes | moderate |
| RR intervals / HRV indices | beat-to-beat | moderate |
| ECG-derived morphology features | beat-to-beat | — |
| Respiratory rate | seconds–minutes | moderate |
| SpO₂ | seconds–minutes | **high** |
| Systolic / diastolic / mean arterial pressure | minutes | **high** (MAP) |
| Core temperature | minutes–hours | **high** |
| Perfusion indices, capillary refill proxies | minutes | low |
| Lactate, base excess, pH | hours | **very high** (pH) |
| Urine output | hours | moderate |

The "homeostatic defence" column is not decoration: under the homeostatic
premise of [`PHYSICAL_INTERPRETATION.md`](PHYSICAL_INTERPRETATION.md) §3.1, the
strongly defended channels are precisely the low-variance, stiff directions
that A(t) weights most heavily. **A dataset without at least three strongly
defended channels cannot test the primary claim.**

### 2.2 Definitions

> **BASELINE                 W₀ = [t₀, t₀+ΔB], treatment-quiet**
>
> μ₀ = mean X over W₀            ESTIMATED
> Σ₀ = shrunk covariance over W₀ ESTIMATED
> Λ  = Σ₀⁻¹                      FROZEN
> LOCAL DEFORMATION        zᵢ(t) = (xᵢ(t) − μ₀ᵢ)/σ₀ᵢ      ESTIMATED
> per-channel, baseline-standardised
> MULTIVARIATE DEFORMATION ΔG(t) = d(Σ₀, Σ_t)             ESTIMATED
> δ(t)  = μ(t) − μ₀              ESTIMATED
> PERSISTENCE              τ(t) = contiguous duration of
> ‖ΔG‖ > θ, θ = baseline p95     ESTIMATED
> HIGHER-ORDER INTEGRATION C(t) = ι(⋃ᵢ Nₜ(X,Iᵢ)) → β₁     ESTIMATED
> tested against pairwise-matched
> Gaussian surrogates
> CONSTRAINED DEFORMATION  ‖ΛΔG‖ = √(δᵀΣ₀⁻¹δ)             ESTIMATED
> A(t), z(t) alignment            ESTIMATED
> CRITICAL TRANSITION      the physiology-defined event     OBSERVED
> (never an order-entry event)
> RECOVERY                 Λ_A = I − A from VAR(1)         ESTIMATED
> where resolution permits;
> belongs to competing model M2

### 2.3 Observables versus latents

| | Object |
|---|---|
| **OBSERVED** | channel values; measurement timestamps; the transition event |
| **ESTIMATED** | μ₀, Σ₀, Λ, ΔG, δ, τ, θ, β₁, A, z, n_eff, Λ_A |
| **LATENT — fitted, never observed** | T_critical; the transition mechanism class |
| **LATENT — no estimator exists** | Reach(X); H_k(Reach(X)) — demoted, see [`DEMOTED_OBJECTS.md`](DEMOTED_OBJECTS.md) |

---

## 3. The Transition Pipeline

The framework suggests a sequence. **It is not assumed.** Each arrow is a
separate falsifiable proposition, and each may fail independently.

```mermaid
flowchart LR
    A[Stable regime]
    B[Structural deformation]
    C[Persistent deformation]
    D[Critical regime]
    E[State transition]
    A -. P1 .-> B
    B -. P2 .-> C
    C -. P3 .-> D
    D -. P4 .-> E
```

Dashed arrows mark the pathway as **hypothesised, not established**.

| Arrow | Proposition | Direction | Falsified if |
|:--:|---|:--:|---|
| **P1** | Deformation begins while every channel remains inside its person-specific and population range | ΔG rises with marginals in range | ΔG rise is simultaneous with, or later than, marginal departure |
| **P2** | Deformation that persists and integrates across channels carries more information than transient or isolated deformation | Q and β₁-excess add over ΔG | β₂ = 0 and z_β₁ CI includes 0 |
| **P3** | Constrained deformation crosses a **threshold**, not merely a gradient | hazard in ‖ΛΔG‖ has a knee | a smooth monotone hazard fits as well (ΔAIC ≤ 10) |
| **P4** | Crossing precedes the clinical transition with usable lead time | median lead ≥ 2 h, marginals in range at alert | lead-time CI includes zero versus a marginals-only model |

### 3.1 Where the sequence should NOT occur

Stated in advance so that its absence is a prediction, not an excuse:

| Mechanism | Expected pipeline behaviour |
|---|---|
| **Noise-induced tipping** | P1 fails. A stochastic excursion crosses the separatrix with no precursor. Confirmed blind in the benchmark |
| **Rate-induced tipping** | P1 may fire via variance inflation, but P3 should fail — there is no threshold crossing, only a sweep |
| **Exogenous catastrophe** (massive pulmonary embolus, tamponade, arrhythmic arrest from a fixed substrate) | P1 fails. The insult is the transition |
| **Endogenous fold** | P1 and P3 may fire, but **A(t) will not discriminate it** — fold escape shares its direction with stationary sampling noise |

> **If most real deterioration turns out to be noise-induced or**
>
> exogenous-catastrophic, the hypothesis is not false — it is
> detecting a small and possibly clinically minor subset.
> That outcome must be reported as a bound on scope, in those words,
> and not as a positive finding about the subset that worked.

---

## 4. What Would Make This Worth Continuing

The minimum result, all four required:

```
  1  ΔG rises on windows where every marginal is in range,
     ΔAUPRC over marginals-only with lower 95% bound > 0
  2  M0, the timestamp-only model, at ACCEPTABLE leakage
  3  Mean z(t) CI excluding 0 in at least one transition class,
     with the sign matching the preregistered direction
  4  The effect surviving intervention masking
```

Item 3 is the actual Transition Dynamics claim. Items 1, 2 and 4 establish only
that there is a real signal to attribute — and item 1 alone would replicate
Dynamical Network Biomarker theory, not extend it.

---

<div align="center">

> **Covariance drift already detects.**
>
> The open question is whether the DIRECTION of deformation
> identifies the mechanism. That is the whole hypothesis.

---

## Related Work

- [`../README.md`](../README.md) — Index
- [`MATHEMATICAL_OBJECTS.md`](MATHEMATICAL_OBJECTS.md) · [`PHYSICAL_INTERPRETATION.md`](PHYSICAL_INTERPRETATION.md)
- [`TRANSITION_TAXONOMY.md`](TRANSITION_TAXONOMY.md) · [`COMPETING_MODELS.md`](COMPETING_MODELS.md)

---

© 2026 Davarn Morrison · Transition Dynamics · Revised Hypothesis
