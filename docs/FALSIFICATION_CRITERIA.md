<div align="center">

# FALSIFICATION CRITERIA

**The Canonical Map of the Hypothesis**

![Status](https://img.shields.io/badge/Fixed-Before_Data_Contact-047857?style=flat-square)
![Scope](https://img.shields.io/badge/Canonical-Claim_Map-1f2937?style=flat-square)

</div>

---

*"If you cannot fill in the 'falsifying result' column, you do not have a claim. You have a preference."*

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
> **Specific to this document:** C6 is labelled "the surviving novelty claim".
> That label is historical. C6 was tested and is not supported.

---

## Global Kill Conditions

Any one ends the programme regardless of individual claim outcomes.

| # | Condition | Consequence |
|:--:|---|---|
| **G1** | M0 (timestamp-only) reaches AUPRC ratio ≥ 0.90 vs M3 | Everything is acquisition behaviour. All results void |
| **G2** | Label shuffle or patient permutation returns above chance | Pipeline defect. No substantive result may be reported |
| **G3** | Synthetic noise-induced transitions are "detected" | Leakage proven in the pipeline itself |
| **G4** | The effect exists only in unmasked (treatment-containing) windows | It is a treatment effect |
| **G5** | Effect present in T6 (abrupt/noise class) at the same strength as T2/T3 | Class-correlated confounding, not mechanism |

---

## The Canonical Table

### C1 — Structural deformation precedes conventional criteria

| Field | Specification |
|---|---|
| **Equation** | ΔG(t) = d(Σ₀, Σ_t) |
| **Physical interpretation** | Joint second-order structure bends before any marginal leaves range |
| **Observable** | p channel values on a regular grid |
| **Estimator** | `delta_G_structure`, Ledoit–Wolf shrinkage mandatory |
| **Directional prediction** | ΔG rises on windows where every marginal is in range |
| **Competing explanation** | M0 acquisition behaviour; M1 marginals; DNB covariance drift (same quantity) |
| **Dataset** | HiRID primary; MIMIC-IV / eICU external |
| **Required resolution** | n_eff ≥ 10p per window; ~2 min sampling for a fast-channel panel |
| **Positive** | ΔAUPRC vs M1, lower 95% bound > 0, replicated by site |
| **Null** | No discrimination once marginals are in range |
| **Falsifying** | Lead-time CI includes zero vs M1 in primary **and** external cohorts |
| **Known limitation** | **Not novel.** Established by HeRO and DNB. Floor, not contribution |

### C2 — Deformation-persistence is multiplicative

| Field | Specification |
|---|---|
| **Equation** | Q = ‖ΔG‖·τ, tested as β₁ = β₂ on the log scale |
| **Physical interpretation** | Magnitude and duration combine multiplicatively |
| **Observable** | channel values, clock |
| **Estimator** | `Q_deformation_persistence`; comparator `Q_integral` |
| **Directional prediction** | β₁ > 0, β₂ > 0, β₁ ≈ β₂; advantage grows with horizon |
| **Competing explanation** | Q is a rescaling of ΔG; or ∫‖ΔG‖dt is the correct functional |
| **Dataset** | HiRID only — τ is quantised beyond use at hourly resolution |
| **Required resolution** | ≥ 20 τ-resolvable steps per excursion |
| **Positive** | β₂ CI excludes 0 and Wald test does not reject β₁ = β₂ |
| **Null** | β₂ = 0 |
| **Falsifying** | β₂ CI includes 0, **or** unconstrained or integral form wins by ΔAIC > 10 |
| **Known limitation** | τ is defined by a threshold on ΔG, so Q is not a function of independent quantities. Repair is ours, declared |

### C3 — Constrained deformation adds beyond ΔG and Q

| Field | Specification |
|---|---|
| **Equation** | ‖ΛΔG‖ = √(δᵀΣ₀⁻¹δ), Λ frozen |
| **Physical interpretation** | Deformation weighted by baseline stiffness — a stress, not a strain |
| **Observable** | channel values |
| **Estimator** | `deformation_energy`, `deformation_energy_chi2` |
| **Directional prediction** | Rises faster than ΔG alone; χ² quantile transfers across cohorts |
| **Competing explanation** | M2's Λ_A recovery-rate reading; isotropic deformation making Λ irrelevant |
| **Dataset** | HiRID primary |
| **Required resolution** | n_eff ≥ 10p; Σ₀⁻¹ spectrum sensitive to shrinkage intensity |
| **Positive** | Nested improvement over ΔG and Q, out of sample |
| **Null** | Λ weighting adds nothing; deformation isotropic w.r.t. baseline spectrum |
| **Falsifying** | Nested ΔAUPRC CI includes 0, **and** M2 outperforms M3 |
| **Known limitation** | Shrinkage directly shapes the Σ₀⁻¹ spectrum that this depends on |

### C4 — A critical threshold exists and transfers

| Field | Specification |
|---|---|
| **Equation** | ‖ΛΔG‖ > T_critical |
| **Physical interpretation** | A separatrix — yield, not a risk gradient |
| **Observable** | channel values |
| **Estimator** | changepoint hazard model vs monotone smooth hazard; T_critical as χ² quantile |
| **Directional prediction** | Hazard contains a knee; between-cohort CV(T_critical) < 0.5 |
| **Competing explanation** | A smooth monotone dose–response that is predictive but has no threshold |
| **Dataset** | HiRID fit, MIMIC-IV/eICU transfer |
| **Required resolution** | Well-sampled ‖ΛΔG‖ trajectory; hourly sampling smears the knee |
| **Positive** | Threshold model wins by ΔAIC > 10 **and** CV(T_critical) < 0.5 |
| **Null** | Smooth monotone hazard |
| **Falsifying** | ΔAIC ≤ 10 favouring smooth, **or** CV(T_critical) > 0.5 |
| **Known limitation** | Calibration drift between cohorts can masquerade as threshold shift. **Load-bearing:** this is the only claim distinguishing the framework from existing early-warning work on detection |

### C5 — Higher-order integration beyond pairwise

| Field | Specification |
|---|---|
| **Equation** | C(t) = ι(⋃ᵢ Nₜ(X,Iᵢ)) → β₁ |
| **Physical interpretation** | Channels couple in structures not reducible to pairs |
| **Observable** | channel values |
| **Estimator** | `beta1_excess_over_pairwise` — z vs Gaussian surrogates matched on mean and covariance |
| **Directional prediction** | z_β₁ > 0 pre-transition |
| **Competing explanation** | Pairwise-complete model suffices ("multivariate beats univariate" — already established, not tested as novel) |
| **Dataset** | HiRID only |
| **Required resolution** | Sufficient temporal support for third-order co-occurrence at support ρ |
| **Positive** | z_β₁ CI excludes 0, stable across θ and ρ |
| **Null** | z_β₁ = 0 |
| **Falsifying** | z_β₁ CI includes 0, **or** pairwise-complete model matches the β₁-augmented model |
| **Known limitation** | Two free parameters (θ, ρ); β₁ range depends on channel count, complicating cross-cohort comparison |

### C6 — Mechanism identification (the surviving novelty claim)

| Field | Specification |
|---|---|
| **Equation** | A(t) = (δᵀΣ₀⁻¹δ)/(‖δ‖²·tr(Σ₀⁻¹)/p), decided via z vs the patient's own empirical null |
| **Physical interpretation** | *Where* the system is pushed, independent of *how hard*. Requires the separately stated **homeostatic premise** |
| **Observable** | channel values; ≥ 3 strongly defended channels required |
| **Estimator** | `stiffness_alignment`, `alignment_empirical_null`, `alignment_z` |
| **Directional prediction** | z > 0 in exogenous classes T2/T3; z ≈ 0 in T6; **at matched ‖ΔG‖** |
| **Competing explanation** | ΔG magnitude alone; class-correlated monitoring differences |
| **Dataset** | HiRID primary, stratified by transition class |
| **Required resolution** | n_eff ≥ 10p; many channels for adequate power (§ null-band table) |
| **Positive** | Mean z CI excludes 0 with correct sign per class, **and** ΔG fails the same magnitude-matched discrimination |
| **Null** | z within the patient's own baseline band in all classes |
| **Falsifying** | Mean z CI includes 0 in all powered classes; **or** signs do not track class; **or** ΔG discriminates equally at matched magnitude |
| **Known limitation** | Fails on the fold mechanism by construction (synthetic AUC 0.30). Wide null band at small p. Rests on an untested physiological premise |

### C7 — Structure/self-report decoupling (EXPLORATORY, non-primary)

| Field | Specification |
|---|---|
| **Equation** | Graded decline in coupling ρ(t) with signed divergence — **not** C ⟂ L |
| **Physical interpretation** | Self-report ceases to track structural state pre-transition |
| **Observable** | passive sensing; EMA self-report |
| **Estimator** | `structural_report_coupling`, `divergence_index` |
| **Directional prediction** | ρ falls below own baseline; divergence > 0 and increasing |
| **Competing explanation** | **Declining EMA compliance** — itself a known relapse predictor |
| **Dataset** | CrossCheck primary; GLOBEM, RADAR-MDD secondary. **Not MIMIC** |
| **Required resolution** | Daily EMA + continuous passive sensing |
| **Positive** | Coupling decline with response-timing-only control at chance |
| **Null** | Coupling stable or rising |
| **Falsifying** | Response-timing-only control reproduces the effect |
| **Known limitation** | **Exploratory only.** The primary hypothesis does not depend on it. The literal C ⟂ L is already refuted — see [`DEMOTED_OBJECTS.md`](DEMOTED_OBJECTS.md) |

---

## Outcome Map

> **───────────────────────────────────────────────────────────────────**
>
> G1 acquisition leakage  →  EVERYTHING DIES
> C1 dies                 →  no signal to attribute. Programme over
> C2 dies                 →  ΔG survives; product form does not
> C3 dies                 →  Λ weighting decorative; M2 preferred
> C4 dies                 →  separatrix and irreversibility die;
> a predictor may survive
> C5 dies                 →  integration decorative
> C6 dies                 →  NO NOVELTY. The programme reduces to
> a replication of DNB (2012)
> C7 dies                 →  nothing in the primary hypothesis
> changes
> ───────────────────────────────────────────────────────────────────

**C6 is the load-bearing claim.** C1–C5 can all succeed while the programme
contributes nothing new, because covariance drift already achieves detection.
If C6 dies, the honest report is: *we replicated Dynamical Network Biomarker
theory on ICU data.*

---

<div align="center">

> **C1 through C5 can all pass and the result still be**
>
> a 2012 method in new clothes. C6 is the claim.

---

## Related Work

- [`../README.md`](../README.md) · [`MATHEMATICAL_OBJECTS.md`](MATHEMATICAL_OBJECTS.md) · [`COMPETING_MODELS.md`](COMPETING_MODELS.md) · [`CLAIM_LADDER.md`](CLAIM_LADDER.md)

---

© 2026 Davarn Morrison · Transition Dynamics · Falsification Criteria
