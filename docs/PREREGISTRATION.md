<div align="center">

# PREREGISTRATION

**Transition Dynamics v2 · Frozen Before Data Contact**

![Version](https://img.shields.io/badge/Version-2.0-1f2937?style=flat-square)
![Lambda](https://img.shields.io/badge/Λ-FROZEN_Σ₀⁻¹-047857?style=flat-square)
![Data](https://img.shields.io/badge/Real_Data_Analysed-NONE-b91c1c?style=flat-square)
![Level](https://img.shields.io/badge/Claim_Level-0-ca8a04?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)

</div>

---

*"Preregistration is a promise made to your future self, who will want very badly to break it."*

*— Davarn Morrison, 2026*

---

## Status

```
════════════════════════════════════════════════════════════════════
  VERSION            2.0
  REAL DATA          NONE ANALYSED
  CLAIM LEVEL        0
  SYNTHETIC WORK     complete; establishes estimator behaviour only,
                     and does NOT constitute Level 1 evidence
════════════════════════════════════════════════════════════════════
```

---

## 1. Frozen Commitments

These may not change after data contact. Any change is a **deviation**, logged
with date and reason, with the pre-deviation analysis reported alongside.

### 1.1 The operator

╔══════════════════════════════════════════════════════════════════════╗
║      Λ  :=  Σ₀⁻¹                                                     ║
║                                                                      ║
║  Σ₀ = shrunk covariance over the treatment-quiet baseline window.    ║
║  Computed ONCE per patient. Never re-estimated downstream.           ║
║  Interpretation: stiffness / precision / resistance to deformation.  ║
║                                                                      ║
║  The resilience/recovery reading is NOT an alternative reading of    ║
║  this operator. It is competing model M2, with its own equations.    ║
╚══════════════════════════════════════════════════════════════════════╝

### 1.2 The primary claim

**Mechanism identification, not detection.** z(t) discriminates transition
mechanism at matched deformation magnitude, where ΔG cannot.

### 1.3 Directional predictions, per transition class

| Class | Predicted mean z(t) | Basis |
|:--:|:--:|---|
| T2 sepsis-related | **> 0** | exogenous insult against defended coordinates |
| T3 respiratory | **> 0** | exogenous |
| T4 neurological | ≈ 0 or < 0 | often endogenous or abrupt |
| T6 abrupt/noise | **≈ 0** | no precursor — negative control class |
| T1 cardiac/circulatory | undirected | mechanism mixed; exploratory |
| T5 general ICU | **no prediction** | mechanistically uninterpretable; power only |

### 1.4 The decision rule

Not A > 1. **z(t) against the patient's own empirical stationary null**,
estimated from held-out baseline sub-windows. Cluster-bootstrap 95% CI by
patient, 2,000 replicates, must exclude 0 with the preregistered sign.

### 1.5 Fixed analysis parameters

| Parameter | Value | Fixed because |
|---|---|---|
| θ (deformation threshold) | baseline 95th percentile of ΔG | per patient, before analysis |
| ρ (co-deformation support) | 0.10–0.30, sensitivity-analysed | two free parameters must be bounded in advance |
| shrinkage | Ledoit–Wolf, automatic intensity | prevents post-hoc tuning of the Σ₀⁻¹ spectrum |
| n_eff requirement | ≥ 10p per window | derived, see [`DATASET_REQUIREMENTS.md`](DATASET_REQUIREMENTS.md) |
| blanking | 30 min pre-event (HiRID) | treatment contamination, reverse causation |
| alert definition | ≥ 3 consecutive positive windows | suppresses single-window noise |
| headline metric | AUPRC | AUROC is cosmetically flattering at these prevalences |
| validation split | **by site**, never random | random splits share institutional practice |
| multiplicity | Holm–Bonferroni across C1–C6 | C7 is exploratory and carries no confirmatory weight |

---

## 2. Prohibited Moves

```
════════════════════════════════════════════════════════════════════
  Redefining Λ after seeing results.
      If the stiffness reading fails, it is ABANDONED, not adjusted.
      Work continues under M2 with its modification declared.

  Reporting AUROC without PPV at the true prevalence.

  Promoting a class-specific result to a general claim by pooling.

  Describing decoupling results as evidence for C ⟂ L.

  Introducing persistent homology before the covariance and
  nerve-complex estimators have been shown, in writing, to fail.

  Running a negative control after seeing a positive result.

  Claiming novelty for detection. Covariance drift already detects.

  Any clinical claim before the base-rate utility gate is cleared.
════════════════════════════════════════════════════════════════════
```

---

## 3. Execution Order — Binding

```
  1  Verify dataset properties against authoritative sources
     (PhysioNet was unreachable when this was written)
  2  Build pipeline; pass label-shuffle and patient-shuffle at chance
  3  Synthetic controls: fold detected by M2, noise NOT detected
  4  M0 timestamp-only gate
     → CRITICAL verdict: STOP. Report and end.
  5  M1, M2 baselines
  6  C1 on HiRID, marginals-in-range restriction
     → C1 dies: C2–C6 not run
  7  C2, C3, C4, C5
  8  C6 — magnitude-matched mechanism discrimination, by class
  9  External validation by site
 10  Base-rate translation for every surviving result
 11  C7 exploratory, on CrossCheck, timing-only control FIRST
```

Steps 3 and 4 before step 6 are non-negotiable.

---

## 4. Reporting Commitments

- All of C1–C6 reported, including failures.
- All negative controls with their numbers, in the primary table.
- Base-rate table adjacent to every discrimination metric.
- Class-specific power reported **before** any null is claimed.
- Effect sizes with cluster-bootstrap intervals; no bare p-values.
- Masked and unmasked intervention analyses both reported.
- Every deviation from this document logged with date and reason.

---

## 5. Amendment Log

| Date | Version | Change | Reason |
|---|:--:|---|---|
| 2026-09-10 | 1.0 | Initial preregistration | — |
| 2026-09-10 | 2.0 | Objects 1 and 6 demoted | Non-identifiable; literal form already refuted |
| 2026-09-10 | 2.0 | Λ frozen as Σ₀⁻¹ | Underdetermined by the equations; freeze required before any prediction exists |
| 2026-09-10 | 2.0 | v1 falling-variance prediction **withdrawn** | Does not follow from a baseline-frozen Λ |
| 2026-09-10 | 2.0 | "Competing with CSD" reframed as complementary | Synthetic benchmark: each detects the mechanism the other misses |
| 2026-09-10 | 2.0 | Primary claim narrowed to mechanism identification | Covariance drift already achieves detection at AUC 1.00 |
| 2026-09-10 | 2.0 | A = 1 null **corrected** to empirical per-patient null | Stationary displacement is Σ₀-shaped, not isotropic |
| 2026-09-10 | 2.0 | Consciousness/qualia terminology separated from biomedical claim | Not operationally required by anything measured |

All amendments were made **before any real physiological data was analysed**.

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   Λ = Σ₀⁻¹.  Frozen.                                                 ║
║   If it fails, it is abandoned — not adjusted.                       ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Preregistration v2.0*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) · [`HYPOTHESIS.md`](HYPOTHESIS.md) · [`PHYSICAL_INTERPRETATION.md`](PHYSICAL_INTERPRETATION.md) · [`FALSIFICATION_CRITERIA.md`](FALSIFICATION_CRITERIA.md)
