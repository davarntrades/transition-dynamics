<div align="center">

# EXPERIMENTAL PROTOCOL

**Cohorts · Windows · Estimators · Statistics · Validation**

![Primary](https://img.shields.io/badge/Primary_Cohort-HiRID-1f2937?style=flat-square)
![Validation](https://img.shields.io/badge/External-MIMIC--IV_·_eICU-4c1d95?style=flat-square)
![Metric](https://img.shields.io/badge/Headline_Metric-AUPRC_not_AUROC-b91c1c?style=flat-square)
![Topology](https://img.shields.io/badge/Persistent_Homology-Deferred_By_Design-047857?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)
![Rights](https://img.shields.io/badge/©-Davarn_Morrison-555555?style=flat-square)

</div>

---

> ## ⚠ SUPERSEDED — v1 ARCHIVE
>
> This document is the **version 1** record. It is preserved because the
> reasoning it contains produced the v2 demotions and corrections, and that
> reasoning must remain inspectable.
>
> **Superseded by:** docs/DATASET_REQUIREMENTS.md, docs/COMPETING_MODELS.md and docs/PREREGISTRATION.md
>
> Claims in this file that v2 withdrew — notably the prediction that
> pre-transition variance falls, and the framing of Transition Dynamics as a
> competitor to critical slowing down — are recorded as withdrawn in
> `docs/LIMITATIONS.md`. **Do not cite this file for current claims.**

---


*"Choose the endpoint before you choose the estimator. Otherwise the estimator will choose the endpoint for you."*

*— Davarn Morrison, 2026*

---

## 1. Why MIMIC-IV Is Not the Primary Cohort

MIMIC-IV was evaluated first, as instructed, and **demoted**.

| Hypothesis | Verdict | Reason |
|:--:|:--:|---|
| H1 | Marginal | Vitals charted ~hourly and irregularly. A 24 h window yields ~24 samples for a 10-dimensional covariance. Ill-conditioned without aggressive shrinkage, which itself suppresses the deformation signal |
| H2 | Weak | τ is an excursion duration. At hourly spacing τ is quantised to a handful of values and the constrained-exponent test loses nearly all power |
| H3 | Marginal | Λ_B estimable with shrinkage. Λ_A requires a VAR(1) fit, which is poorly identified at hourly spacing with irregular gaps |
| H4 | Weak | Locating a hazard knee needs a well-sampled ‖ΛΔG‖ trajectory. Hourly sampling smears the knee into the gradient |
| H5 | Marginal | Channel count is adequate; temporal support for third-order co-occurrence is not |
| H6 | **CANNOT TEST** | MIMIC contains **clinician** notes, not patient self-report. Observer language is not the L subspace. Pain scores and RASS are the only patient-sourced items and are far too sparse |

```
════════════════════════════════════════════════════════════════════
  DECISION FIXED IN ADVANCE

  A null result in MIMIC-IV would be evidence about SAMPLING RATE,
  not about the hypothesis. Running it as primary would generate an
  uninformative null and invite the wrong conclusion.

  MIMIC-IV is the EXTERNAL VALIDATION cohort.
════════════════════════════════════════════════════════════════════
```

---

## 2. Cohorts

### 2.1 Primary — HiRID

| | |
|---|---|
| Size | ~34,000 ICU admissions, Bern University Hospital |
| Resolution | Most vital signs at **~2 minutes** — the highest of any public ICU dataset |
| Variables | ~700, covering vitals, labs, treatments |
| Endpoint | Established physiology-defined circulatory failure |

**Inclusion.** Adults; ≥ 12 h of recording; ≥ 8 continuous channels available at
≥ 80% completeness through baseline and pre-transition windows.

**Exclusion.** Admissions in which the transition event occurs inside the
baseline window; recordings with > 20% flagged artifact; readmissions after the
first (independence).

### 2.2 External validation — MIMIC-IV, then eICU

Validation is **by site**, never by random split. A random split shares
institutional practice patterns between train and test and inflates
performance in exactly the way this framework's claims are vulnerable to.

### 2.3 H6 — CrossCheck (primary), GLOBEM / RADAR-MDD (generalisation)

CrossCheck is primary because it is the only located public dataset combining
daily EMA, passive smartphone sensing, **and** a clinically adjudicated
transition event of the required severity (psychotic relapse).

---

## 3. Transition Event Definition

╔══════════════════════════════════════════════════════════════════════╗
║  THE ENDPOINT IS PHYSIOLOGY, NOT CLINICIAN BEHAVIOUR                 ║
╚══════════════════════════════════════════════════════════════════════╝

Vasopressor initiation is a **treatment decision** made by clinicians reading
the same vital signs the model reads. A model predicting it is partly
predicting clinician behaviour, and a "lead time" so obtained is partly the
interval between a clinician noticing and a clinician acting.

**Preregistered endpoint (ICU):** HiRID's physiology-defined circulatory
failure — sustained mean arterial pressure below threshold with concurrent
lactate elevation, per the published definition. Order-entry events are
recorded as a **secondary, clearly labelled** endpoint and never reported as
the primary result.

**Preregistered endpoint (H6):** clinically adjudicated relapse as defined in
the source dataset. Self-reported symptom scales are **not** the endpoint —
they are one of the two measured subspaces, and using them as ground truth
would make H6 circular.

---

## 4. Windows

```
════════════════════════════════════════════════════════════════════
  BASELINE         first 8 h of stable recording; no active titration
                   → yields  Σ₀,  μ₀,  Λ_B = Σ₀⁻¹,  θ = p95(‖ΔG‖)

  PRE-TRANSITION   8 h immediately before event onset

  BLANKING         30 min immediately pre-event — EXCLUDED
                   → treatment contamination and reverse causation

  CONTROL          length-of-stay matched admissions with no event,
                   sampled at matched relative times

  PLACEBO          a pre-baseline interval; must show NO effect
════════════════════════════════════════════════════════════════════
```

Sliding evaluation: 2 h analysis window, 30 min stride (HiRID); 6 h window,
1 h stride (MIMIC-IV, resolution-constrained).

**Resampling.** All channels forward-filled onto a regular grid with a maximum
fill horizon of 2 sampling intervals. Longer gaps are marked missing and the
window is dropped. This is stated in advance because the fill rule directly
controls the covariance estimate.

---

## 5. Estimators

All implemented in [`../analysis/estimators.py`](../analysis/estimators.py).

| Quantity | Function | Definition |
|---|---|---|
| Σ estimate | `shrunk_covariance` | Ledoit–Wolf shrinkage to scaled identity. **Mandatory** — a window carries too few samples for a well-conditioned p×p covariance |
| ΔG structural | `delta_G_structure` | Affine-invariant Riemannian distance d(Σ₀, Σ_t). Invariant to channel re-parameterisation, so results do not depend on recording units |
| ΔG state | `delta_G_state` | Mahalanobis displacement of mean state in the baseline metric |
| Λ primary | `Lambda_B_stiffness` | Σ₀⁻¹, the baseline precision / Hessian operator |
| Λ alternative | `Lambda_A_recovery` | I − A from VAR(1). **Requires the modified criterion** — see Audit §4.2 |
| ‖ΛΔG‖ | `deformation_energy` | √(δᵀΛδ) |
| τ | `persistence_tau` | Contiguous excursion length above θ, ending at now |
| Q | `Q_deformation_persistence` | ‖ΔG‖·τ |
| Q comparator | `Q_integral` | ∫‖ΔG‖dt over the excursion |
| C(t) | `codeformation_complex` → `betti_numbers` | (β₀, β₁) of the nerve of the co-deformation cover |
| ρ(t) | `structural_report_coupling` | Rolling Spearman, structure vs self-report |
| divergence | `divergence_index` | Signed slope difference, standardised |

### 5.1 Persistent homology is deferred by design

```
┌──────────────────────────────────────────────────────────────────┐
│  Persistent homology is NOT used in the primary analysis.        │
│                                                                   │
│  It is introduced only after the covariance and nerve-complex     │
│  estimators are shown insufficient, and its introduction          │
│  requires a written statement of exactly what the simpler         │
│  estimators failed to resolve.                                    │
│                                                                   │
│  A more sophisticated estimator that is reached for before the    │
│  simple one has failed is a way of generating a positive result,  │
│  not a way of testing a hypothesis.                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Mandatory Negative Controls

**Any positive result is void without all four.**

### 6.1 Sampling-rate-only model — the critical one

Build a model from **measurement times alone**: inter-measurement intervals,
counts per window, which channels were sampled. **No values whatsoever.**

Clinicians measure more often when they are worried. That worry precedes the
event and leaks the label directly into the covariance structure — a window
sampled twice as often has a different empirical covariance for reasons that
have nothing to do with physiology.

```
════════════════════════════════════════════════════════════════════
  IF THE SAMPLING-RATE-ONLY MODEL APPROACHES THE REAL MODEL,
  THE ENTIRE RESULT IS LEAKAGE — H1 THROUGH H5 TOGETHER.
════════════════════════════════════════════════════════════════════
```

### 6.2 Intervention masking

Windows containing fluid bolus, vasopressor titration, sedation change,
transfusion or ventilator adjustment are flagged and analysed separately.
Treatments deform covariance structure directly; an unmasked "deformation
signal" may be a treatment signal.

Primary analysis reports both masked and unmasked results. If the effect
survives only unmasked, it is a treatment effect.

### 6.3 Label shuffle and patient shuffle

Both must return chance-level performance. Non-chance performance under shuffle
indicates a pipeline defect, and no substantive result may be reported until it
is found.

### 6.4 Placebo window

A pre-baseline interval, analysed identically, must show no effect.

---

## 7. Statistical Model

**Primary.** Discrete-time survival with time-varying covariates, person-level
random intercepts, landmark analysis at fixed horizons (2 h, 4 h, 8 h ICU;
7 d, 14 d psychiatric).

**Nested comparisons.** Each hypothesis is a likelihood-ratio or AIC comparison
between explicitly nested models:

```
  M0  marginals only (each channel's current value)
  M1  M0 + ‖ΔG‖                             → H1
  M2  M1 + log τ, unconstrained exponents    → H2
  M3  M2 + ‖Λ_B ΔG‖                          → H3
  M4  M3 with threshold term in ‖Λ_B ΔG‖     → H4
  M5  M4 + all pairwise couplings            → H5 comparator
  M6  M5 + β₁                                → H5
```

**Headline metric: AUPRC, not AUROC.** At the prevalences in
[`../analysis/base_rates.py`](../analysis/base_rates.py), AUROC is cosmetically
flattering and nearly uninformative about utility. AUROC is reported for
comparability with prior literature only, and never as the primary claim.

**Calibration.** Calibration intercept, calibration slope, integrated
calibration index. Reported for every model, in every cohort. A model that
discriminates but does not calibrate cannot support any threshold claim, and H4
is a threshold claim.

**Decision analysis.** Net benefit across the plausible threshold-probability
range.

**Uncertainty.** Cluster bootstrap **by patient**, 2,000 replicates, for all
interval estimates. Bootstrapping by window would treat within-patient windows
as independent and would produce intervals that are far too narrow.

**Multiplicity.** Six preregistered hypotheses. Holm–Bonferroni across the six
primary tests. Secondary and exploratory analyses are labelled as such and
carry no confirmatory weight.

---

## 8. Hypothesis-Specific Procedures

### H1 — the restriction that makes it meaningful

Restrict to windows where **every** channel lies inside both its population
reference range and its person-specific baseline range (mean ± 2 SD of the
patient's own baseline). Within that restricted set — where conventional
monitoring says "normal" — test whether ΔG discriminates.

Lead time is measured from **first sustained alert** (defined as ≥ 3
consecutive positive windows, to suppress single-window noise) to event onset.

### H2 — the constrained-exponent test

```
  logit(P) = β₀ + β₁ log‖ΔG‖ + β₂ log τ

  Morrison product form  ⟺  H₀: β₁ = β₂     (Wald test)
  Compare: constrained vs unconstrained vs integral form, by AIC
  Require: β₁ > 0 and β₂ > 0
```

### H3 — the sign competition

Two things are tested and reported separately:

1. **Incremental value.** Does ‖Λ_B ΔG‖ improve on ‖ΔG‖ and Q?
2. **Direction.** Do channel variance and effective dimensionality **fall**
   (Λ_B) or **rise** (Λ_A) before transition?

Effective dimensionality is reported as the participation ratio of the
covariance eigenvalue spectrum. This is the measurement that adjudicates
between the two literatures.

### H4 — separatrix versus gradient

Fit a threshold (changepoint) hazard model and a smooth monotone hazard model
in ‖Λ_B ΔG‖. Compare by AIC. Then fit T_critical in cohort A and evaluate it,
unchanged, in cohort B; report the between-cohort coefficient of variation.

```
  ΔAIC ≤ 10 favouring smooth        → separatrix falsified
  CV(T_critical) > 0.5              → threshold does not transfer;
                                       "critical" is a fitted parameter
```

Both outcomes leave a possibly useful predictor and kill the irreversibility
claim. They must be reported that way, not as partial support.

### H5 — higher-order gain

M6 (with β₁) versus M5 (pairwise-complete). Because β₁ depends on which
triangles are filled — third-order co-deformation support — it is provably not
a function of pairwise supports alone, so the comparison is meaningful rather
than a re-parameterisation.

### H6 — decoupling, with the control that decides it

Structural deformation from passive sensing; self-report deformation from EMA.
Rolling coupling ρ(t) and signed `divergence_index` over the 14 days before
adjudicated relapse, against the person's own baseline coupling.

```
════════════════════════════════════════════════════════════════════
  RESPONSE-TIMING-ONLY NEGATIVE CONTROL

  A model using ONLY when EMA responses arrived — never their
  content — must FAIL to reproduce the effect.

  Declining compliance is itself a known relapse predictor. If
  timing alone reproduces the decoupling, H6 is measuring
  compliance, not decoupling, and is dead.
════════════════════════════════════════════════════════════════════
```

Compliance-matched sensitivity analysis is run regardless of the control's
outcome.

---

## 9. Reporting Standards

**Fixed in advance:**

- All six primary tests are reported, including those that fail.
- Effect sizes with cluster-bootstrap intervals; no bare p-values.
- Both masked and unmasked intervention analyses.
- All four negative controls, with their numbers, in the primary table.
- The base-rate table at the setting's true prevalence, adjacent to every
  discrimination metric.
- Any deviation from this protocol documented as a deviation, with its date and
  reason, and the pre-deviation analysis reported alongside.

**Prohibited:**

- Reporting AUROC without the matching PPV at true prevalence.
- Redefining Λ after seeing results. The interpretation is fixed in README §3.
  If it fails, it is **abandoned**, not adjusted.
- Introducing persistent homology before the simple estimators have been shown
  to fail, in writing.
- Describing decoupling results as evidence for C ⟂ L.
- Any clinical claim before the README §10 utility gate is cleared.

---

## 10. Execution Order

```
  1  Verify all dataset specifications against source landing pages
  2  Build pipeline; pass label-shuffle and patient-shuffle at chance
  3  Run the sampling-rate-only control FIRST
     → if it approaches the real model, STOP. Fix the pipeline.
  4  H1 on HiRID, restricted windows
     → if H1 dies, H2–H5 are not run
  5  H2, H3, H4, H5 in order
  6  External validation by site: MIMIC-IV, then eICU
  7  H6 on CrossCheck, with the timing-only control run FIRST
  8  Base-rate translation for every surviving result
```

Step 3 before step 4, and step 3 of the H6 arm before its analysis, are the two
non-negotiable orderings. Running the negative control after seeing a positive
result is how a leakage artifact becomes a publication.

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   If the sampling-rate-only model works, everything here is          ║
║   measuring how often a worried nurse takes a reading.               ║
║                                                                      ║
║   Run that control first.                                            ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Experimental Protocol*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) — Preregistration
- [`MATHEMATICAL-AUDIT.md`](MATHEMATICAL-AUDIT.md) — Adversarial audit
- [`LITERATURE.md`](LITERATURE.md) — Literature comparison
- [`FALSIFICATION-MATRIX.md`](FALSIFICATION-MATRIX.md) — Kill conditions
