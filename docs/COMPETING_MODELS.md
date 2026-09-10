<div align="center">

# COMPETING MODELS

**M0 – M4 and M_null · The Comparison That Decides Everything**

![Gate](https://img.shields.io/badge/M0-Runs_First_Non_Negotiable-b91c1c?style=flat-square)
![Rule](https://img.shields.io/badge/Winning_≠_Predicting-1f2937?style=flat-square)
![Null](https://img.shields.io/badge/M__null-A_Permitted_Answer-047857?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)

</div>

---

*"A model that predicts the event is not thereby correct. It has to beat the boring explanation, and the boring explanation is usually the nurse."*

*— Davarn Morrison, 2026*

---

## The Model Set

| | Model | Inputs | What it represents |
|:--:|---|---|---|
| **M0** | Acquisition / clinician behaviour | timestamps, measurement frequency, missingness, inter-measurement intervals, channel-availability patterns. **No physiological values** | The signal is clinician concern, not physiology |
| **M1** | Conventional predictive baseline | current channel values, standard summaries, an appropriate ML baseline (gradient boosting) | Ordinary biometrics already suffice |
| **M2** | Classical critical slowing down | variance ratio, lag-1 autocorrelation, cross-correlation, recovery-rate operator Λ_A = I − A | The established early-warning account, including the resilience reading of Λ as its own preregistered model |
| **M3** | Transition Dynamics | ΔG, Q, ‖Λ_BΔG‖, A(t)/z(t), β₁-excess | The hypothesis under test |
| **M4** | Combined | M1 ∪ M3 (and M2 where resolution permits) | Whether the structural quantities add to conventional ones |
| **M_null** | No recoverable precursor | — | Nothing in the observed variables anticipates the transition |

M2 is where the **resilience/recovery-rate reading of Λ** lives. It is not a
reinterpretation of M3's frozen Λ; it is a separate model with its own
preregistered equations, including the modified criterion `‖Λ_A⁻¹ΔG‖ > T`
required to make that reading fire at all.

---

## 1. M0 — The Gate

╔══════════════════════════════════════════════════════════════════════╗
║  M0 RUNS BEFORE ANY PHYSIOLOGICAL MODEL IS INTERPRETED.              ║
║                                                                      ║
║  Not afterwards as a robustness check. First, as a gate.             ║
╚══════════════════════════════════════════════════════════════════════╝

Clinical measurements are not sampled on a schedule. A worried clinician
measures more often, orders more labs, re-checks sooner. That concern precedes
the event — and it contaminates the covariance estimate itself, because a
densely sampled window has different empirical second-order structure for
purely procedural reasons.

### Preregistered leakage verdicts

Implemented in [`../analysis/controls/timestamp_only.py`](../analysis/controls/timestamp_only.py).
Fixed before running. Not renegotiable afterwards.

| AUPRC(M0) / AUPRC(M3) | Verdict | Mandatory action |
|:--:|:--:|---|
| ≥ 0.90 | **CRITICAL** | Primary mechanistic claim **FAILS**. The result is acquisition behaviour |
| ≥ 0.70 | **SEVERE** | Claim downgraded to Level 1 at most (see [`CLAIM_LADDER.md`](CLAIM_LADDER.md)) |
| ≥ 0.50 | **MATERIAL** | M0 and M3 reported jointly in every table and abstract, always |
| < 0.50 | ACCEPTABLE | Acquisition behaviour does not account for the signal |

```
════════════════════════════════════════════════════════════════════
  DO NOT EXPLAIN THIS AWAY.

  There is no argument available at analysis time that converts a
  CRITICAL verdict into a publishable mechanistic claim. If M0 wins,
  the finding is about how often people took readings.
════════════════════════════════════════════════════════════════════
```

---

## 2. What "Winning" Requires

M3 predicting transitions is **not** evidence for Transition Dynamics. The
required demonstration is **incremental information beyond every competing
explanation**:

```
  M3 must beat M0    or the signal is clinician behaviour
  M3 must beat M1    or ordinary biometrics already suffice
  M3 must beat M2    or established early-warning theory already suffices
  M4 must beat M1    or the structural quantities add nothing usable
```

Nested likelihood-ratio and AIC comparisons; AUPRC as headline (not AUROC);
cluster bootstrap by patient, 2,000 replicates; Holm–Bonferroni across primary
tests.

### 2.1 The comparison that actually matters

The synthetic benchmark
([`../analysis/results/mechanism_benchmark.md`](../analysis/results/mechanism_benchmark.md))
already establishes that **M3 will not beat a plain covariance-drift model on
detection.** ΔG scores AUC 1.00 on both detectable mechanisms.

So the decisive comparison is not detection at all:

╔══════════════════════════════════════════════════════════════════════╗
║  DECISIVE TEST — MECHANISM DISCRIMINATION AT MATCHED MAGNITUDE       ║
║                                                                      ║
║  Stratify transitions into mechanism classes. Within a stratum       ║
║  matched on deformation MAGNITUDE ‖ΔG‖, does z(t) discriminate       ║
║  mechanism class where ΔG cannot?                                    ║
║                                                                      ║
║  Synthetic result: at matched magnitude, dG collapses to AUC 0.56    ║
║  while z holds at 1.00. Real data must reproduce this or the         ║
║  novelty claim dies.                                                 ║
╚══════════════════════════════════════════════════════════════════════╝

---

## 3. M_null Is a Permitted Answer

M_null is not a formality. It is the expected outcome for at least the
noise-induced and exogenous-catastrophic classes, and possibly for all of them.

**M_null is accepted for a transition class when**, on that class:

```
  ΔAUPRC(M3 vs M1)  95% CI includes zero,  AND
  ΔAUPRC(M2 vs M1)  95% CI includes zero,  AND
  mean z(t) CI includes zero,              AND
  the class has ≥ 80% power to detect the preregistered effect size
```

The power condition is essential: **an underpowered null is not a null.** A
class with too few events returns "inconclusive", never "no precursor".

---

## 4. Negative Controls

All are preregistered. **Any positive result is void without all of them.**

| Control | Must return | Kills |
|---|---|---|
| **M0 timestamp-only** | AUPRC ratio < 0.50 | Everything, at CRITICAL |
| **Shuffled transition times** | chance | Everything — pipeline defect |
| **Patient-level permutation** | chance | Everything — pipeline defect |
| **Univariate controls** | worse than M3 | The multivariate premise |
| **Conventional risk scores** (NEWS, SOFA, qSOFA where available) | worse than M4 | Clinical relevance |
| **Synthetic noise-induced transitions** | **no detection** | Everything — apparent detection here proves leakage |
| **Synthetic fold transitions** | detection by M2, weak/absent z | Estimator validity if it fails |
| **Stationary non-transition periods** | no alert | Specificity |
| **Estimator sensitivity** (θ, ρ, shrinkage, window) | conclusions stable | Robustness if conclusions flip |
| **Missingness / sampling perturbation** | conclusions stable | Everything, if fragile |

The synthetic controls are already implemented and run:
[`../analysis/synthetic/generators.py`](../analysis/synthetic/generators.py),
[`../analysis/experiments/mechanism_benchmark.py`](../analysis/experiments/mechanism_benchmark.py).

### 4.1 Intervention masking

Windows containing fluid bolus, vasopressor titration, sedation change,
transfusion or ventilator adjustment are flagged and analysed separately.
Treatments deform covariance directly. Both masked and unmasked results are
reported; **an effect surviving only unmasked is a treatment effect.**

### 4.2 The decoupling arm's own gate

For the exploratory decoupling hypothesis, a **response-timing-only** control
runs first: a model using only *when* self-reports arrived, never their
content. Declining compliance is itself a relapse predictor. If timing alone
reproduces the effect, the decoupling claim is dead.

---

## 5. Execution Order

```
  1  Verify dataset properties against authoritative sources
  2  Pipeline passes shuffle controls at chance
  3  Synthetic controls: fold detected, noise NOT detected
  4  M0 runs.  CRITICAL verdict -> STOP
  5  M1, M2 baselines established
  6  M3, then M4
  7  Mechanism-discrimination test at matched magnitude
  8  Base-rate translation for every surviving result
```

Steps 3 and 4 before step 6 are non-negotiable. Running a negative control after
seeing a positive result is how a leakage artifact becomes a publication.

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   If the timestamp-only model wins, the finding is about how         ║
║   often somebody took a reading. Run it first.                       ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Competing Models*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) · [`HYPOTHESIS.md`](HYPOTHESIS.md) · [`CLAIM_LADDER.md`](CLAIM_LADDER.md) · [`FALSIFICATION_CRITERIA.md`](FALSIFICATION_CRITERIA.md)
