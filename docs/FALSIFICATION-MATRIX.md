<div align="center">

# FALSIFICATION MATRIX

**Exact Kill Conditions · Fixed Before Data Contact**

![Rule](https://img.shields.io/badge/Rule-Abandon_Not_Adjust-b91c1c?style=flat-square)
![Scope](https://img.shields.io/badge/Hypotheses-H1–H6-1f2937?style=flat-square)
![Control](https://img.shields.io/badge/Global_Kill-Sampling_Rate_Leakage-4c1d95?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)
![Rights](https://img.shields.io/badge/©-Davarn_Morrison-555555?style=flat-square)

</div>

---

*"Write the kill condition before the data arrives. Afterwards, every threshold is a negotiation with your own hope."*

*— Davarn Morrison, 2026*

---

## Global Kill Conditions

Any one of these ends the programme regardless of H1–H6 outcomes.

| # | Condition | Consequence |
|:--:|---|---|
| G1 | The **sampling-rate-only** model approaches the full model | Everything is measurement-frequency leakage. All results void |
| G2 | Label shuffle or patient shuffle returns above-chance performance | Pipeline defect. No substantive result may be reported |
| G3 | The **placebo window** shows the effect | The estimator is detecting something other than proximity to transition |
| G4 | The effect exists only in **unmasked** windows | It is a treatment effect, not a deformation signal |

---

## H1 — Structural deformation precedes conventional threshold crossing

| Field | Specification |
|---|---|
| **Mathematical prediction** | On windows where every channel is inside its person-specific and population range, `dG_struct` discriminates pre-transition from control |
| **Physical interpretation** | The joint structure moves before any marginal leaves its range |
| **Operational variables** | `dG_struct` = d(Σ₀, Σ_t); comparator = channel current values |
| **Measurement** | HiRID, 8–14 channels, 2 h window / 30 min stride, regular grid |
| **Expected direction** | ΔG **rises** approaching transition |
| **Temporal prediction** | Median lead time ≥ 2 h from first sustained alert (≥ 3 consecutive positive windows) |
| **Null** | ΔG carries no discrimination once marginals are in range |
| **Competing** | Deformation is real but **simultaneous** with marginal departure — restatement, not anticipation |
| **Confounders** | Measurement frequency; interventions; artifact; circadian; immortal time; severity-of-illness at admission |
| **Falsification** | ΔAUPRC over marginals-only model has 95% CI including zero, in HiRID **and** external validation |
| **Forces abandonment** | H1 is the floor. If it dies, H2–H5 are refinements of a signal shown not to exist and are not run |

---

## H2 — Q = ‖ΔG‖·τ beats magnitude or persistence alone

| Field | Specification |
|---|---|
| **Mathematical prediction** | `logit(P) = β₀ + β₁log‖ΔG‖ + β₂log τ` with **β₁ = β₂** |
| **Physical interpretation** | Deformation and its persistence combine multiplicatively, not additively |
| **Operational variables** | `dG_struct`, `tau`, `Q`, `Q_int` |
| **Measurement** | θ = baseline 95th percentile of ‖ΔG‖, fixed per patient before analysis |
| **Expected direction** | β₁ > 0, β₂ > 0, β₁ ≈ β₂ |
| **Temporal prediction** | Q's advantage over ‖ΔG‖ grows with horizon — persistence should matter more at longer lead |
| **Null** | β₂ = 0. τ contributes nothing; Q is a rescaling of ‖ΔG‖ |
| **Competing** | The integral ∫‖ΔG‖dt is the correct functional; the product is a lossy approximation |
| **Confounders** | θ choice; excursion censoring at window edges; τ quantisation at coarse sampling |
| **Falsification** | β₂ CI includes 0, **or** unconstrained beats constrained by ΔAIC > 10, **or** `Q_int` beats `Q` by ΔAIC > 10 |
| **Forces modification** | If the integral wins, the **idea** survives and the **written product form** does not. Report as: object 2's functional form falsified, its content retained |

---

## H3 — The preregistered Λ adds information beyond ΔG and Q

| Field | Specification |
|---|---|
| **Mathematical prediction** | `‖Λ_B ΔG‖` improves on ‖ΔG‖ and Q in nested comparison; deformation is directed along **stiff** eigen-directions of Σ₀⁻¹ |
| **Physical interpretation** | Λ = structural stiffness. Pre-transition = **rigidification** |
| **Operational variables** | `energy` = √(δᵀΣ₀⁻¹δ); participation ratio of the covariance spectrum; per-channel variance |
| **Measurement** | Σ₀ from baseline with Ledoit–Wolf shrinkage |
| **Expected direction** | ‖Λ_B ΔG‖ rises **faster** than ‖ΔG‖; variance **falls**; effective dimensionality **falls** |
| **Temporal prediction** | The variance decline is detectable at or before the ΔG rise |
| **Null** | Λ_B weighting adds nothing; deformation is isotropic w.r.t. the baseline spectrum |
| **Competing** | **Λ_A.** Variance and lag-1 autocorrelation **rise**; effective dimensionality unchanged; Λ_A-based models win |
| **Confounders** | Shrinkage intensity directly shapes the Σ₀⁻¹ spectrum; artifact inflates variance; sedation reduces it |
| **Falsification** | Variance rises **and** dimensionality is flat or rising **and** Λ_A models outperform Λ_B models |
| **Forces abandonment** | The primary interpretation is **abandoned, not redefined**. Work continues under §4's explicitly modified criterion `‖Λ⁻¹ΔG‖ > T`, labelled as a modification of the original mathematics |

```
════════════════════════════════════════════════════════════════════
  H3 IS THE MOST INFORMATIVE MEASUREMENT IN THIS PREREGISTRATION.

  HeRO says rigidification precedes neonatal sepsis.
  van de Leemput says destabilisation precedes mood transition.
  Both are published. Both cannot be the general law.

  This test makes one of them lose on ICU data.
════════════════════════════════════════════════════════════════════
```

---

## H4 — ‖ΛΔG‖ exhibits a reproducible critical threshold

| Field | Specification |
|---|---|
| **Mathematical prediction** | The hazard in `‖Λ_B ΔG‖` contains a **knee**; fitted T_critical transfers across cohorts |
| **Physical interpretation** | A separatrix exists. Yield, not strain gradient |
| **Operational variables** | `energy`; threshold-model vs smooth-model AIC; between-cohort CV of T_critical |
| **Measurement** | Changepoint hazard model vs monotone smooth hazard; fit in cohort A, evaluate unchanged in cohort B |
| **Expected direction** | Threshold model wins; CV(T_critical) < 0.5 |
| **Temporal prediction** | Hazard rises sharply within a bounded interval after crossing, not gradually before it |
| **Null** | Hazard is smooth and monotone. No knee |
| **Competing** | A useful risk gradient with **no separatrix** — predictive, but not the claim being made |
| **Confounders** | Calibration drift between cohorts masquerading as threshold shift; case-mix; unit practice |
| **Falsification** | ΔAIC ≤ 10 favouring the smooth model, **or** CV(T_critical) > 0.5 |
| **Forces abandonment** | The **irreversibility claim** and the separatrix die. A predictor may survive. These outcomes are reported separately and must **never** be presented as partial support for the threshold |

```
════════════════════════════════════════════════════════════════════
  H4 IS LOAD-BEARING.

  It is the only hypothesis distinguishing this framework from the
  existing early-warning literature. Everything else, in its weak
  form, is already published.
════════════════════════════════════════════════════════════════════
```

---

## H5 — Integrated multichannel deformation beats isolated channels

| Field | Specification |
|---|---|
| **Mathematical prediction** | β₁ of the co-deformation nerve adds discrimination **beyond the full set of pairwise couplings** |
| **Physical interpretation** | Genuine higher-order integration, not merely multivariate aggregation |
| **Operational variables** | `b0`, `b1` from `codeformation_complex`; comparator = all pairwise co-deformation supports |
| **Measurement** | θ = 1.5 baseline SD per channel; support ρ = 0.10–0.30, sensitivity-analysed |
| **Expected direction** | β₁ **rises** pre-transition — channels couple around loops without co-deforming as triples |
| **Temporal prediction** | β₁ change is detectable no later than the ΔG rise |
| **Null** | β₁ adds nothing over pairwise-complete |
| **Competing** | The weak form — multivariate beats univariate — which is already established and is **not** tested as novel |
| **Confounders** | θ and ρ are two free parameters; the complex is sensitive to both. Channel count differs between cohorts, changing the achievable β₁ range |
| **Falsification** | ΔAUPRC (M6 vs M5) 95% CI includes zero |
| **Forces modification** | The integration operator is **decorative**. Object 5 loses its higher-order claim; the multivariate core of H1 survives untouched |

---

## H6 — C ⟂ L produces measurable pre-transition decoupling

| Field | Specification |
|---|---|
| **Mathematical prediction** | ρ(t) between structural and self-report deformation **declines** pre-transition, with **signed divergence** > 0 |
| **Physical interpretation** | Self-report ceases to track structural state before the transition |
| **Operational variables** | `rho_CL`, `div_CL`; comparator = self-report level alone |
| **Measurement** | CrossCheck: passive sensing → structure; EMA → self-report; adjudicated relapse → event |
| **Expected direction** | ρ falls below the person's baseline coupling; divergence positive and increasing |
| **Temporal prediction** | Detectable within the 14 days before adjudicated relapse |
| **Null** | Coupling is stable or rises pre-transition |
| **Competing** | **Compliance artifact.** Fewer, noisier EMA responses produce apparent decorrelation with no change in the underlying relationship |
| **Confounders** | EMA compliance decline; floor effects on symptom scales; measurement non-invariance across states; medication changes; phone-usage confounds in both subspaces simultaneously |
| **Falsification** | Coupling stable or rising, **or** the response-timing-only control reproduces the effect |
| **Forces abandonment** | C ⟂ L has no physiological instantiation. Note this kills only the **reformulated** claim; the literal C ⟂ L is already refuted independently (Audit §6.2) |

---

## Outcome Map

What survives which death:

```
┌───────────────────────────────────────────────────────────────────┐
│  G1 sampling leakage    →  EVERYTHING DIES                        │
│  H1 dies                →  H2–H5 not run. Programme over          │
│  H2 dies                →  ΔG survives; the product form does not │
│  H3 dies                →  Λ_B abandoned; continue under Λ_A with │
│                            the modification declared              │
│  H4 dies                →  Separatrix and irreversibility die;    │
│                            a predictor may survive                │
│  H5 dies                →  Integration decorative; core intact    │
│  H6 dies                →  Structure/language claim has no        │
│                            physiological instantiation            │
└───────────────────────────────────────────────────────────────────┘
```

### The strongest survivable outcome

H1 ✓, H2 ✗ (integral wins), H3 ✗ (Λ_A wins), H4 ✗ (smooth hazard), H5 ✗, H6 ✗.

That outcome is: **a covariance-deformation detector with lead time, already
anticipated by Dynamical Network Biomarker theory and by HeRO, with no
separatrix, no higher-order structure, and the constraint operator pointing the
opposite way from the preregistered choice.**

It would be a modest, real, publishable result — and a comprehensive
falsification of what makes this framework distinct. That distinction is the
whole point of writing the conditions down first.

### The outcome that would be genuinely new

H1 ✓, H3 ✓ with variance **falling**, H4 ✓ with T_critical transferring across
cohorts, H5 ✓ with β₁ beating pairwise-complete.

That would establish a transferable critical threshold in constrained
structural deformation, in the rigidification direction, with irreducible
higher-order structure. Nothing located in the literature claims this.

It is also the outcome most likely to be produced by leakage — which is why
G1 runs first.

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   Every row above was written before any data was touched.           ║
║   That is the only thing that makes them kill conditions             ║
║   rather than descriptions.                                          ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Falsification Matrix*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) — Preregistration
- [`MATHEMATICAL-AUDIT.md`](MATHEMATICAL-AUDIT.md) — Adversarial audit
- [`LITERATURE.md`](LITERATURE.md) — Literature comparison
- [`PROTOCOL.md`](PROTOCOL.md) — Experimental protocol
