<div align="center">

# TRANSITION TAXONOMY

**Six Classes · Five Possible Outcomes · No Forced Universality**

![Classes](https://img.shields.io/badge/Classes-T1–T6-1f2937?style=flat-square)
![Outcomes](https://img.shields.io/badge/Outcomes-A_to_E-4c1d95?style=flat-square)
![Default](https://img.shields.io/badge/Default_Expectation-Not_Universal-b91c1c?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)

</div>

---

*"Collapse every deterioration into one outcome and you will find one answer. It will be the average of several different truths, and it will be wrong about all of them."*

*— Davarn Morrison, 2026*

---

## 1. The Classes

Defined where data permits. Each is analysed **separately** before any pooled
analysis is run.

| | Class | Endpoint (physiology-defined) | Expected mechanism | Expected z(t) |
|:--:|---|---|---|:--:|
| **T1** | Cardiac / circulatory deterioration | sustained MAP below threshold with lactate elevation | mixed | uncertain |
| **T2** | Sepsis-related deterioration | infection-associated organ dysfunction by physiological criteria | **exogenous insult** | **z > 0** |
| **T3** | Respiratory deterioration | sustained hypoxaemia / rising respiratory support requirement | exogenous, sometimes gradual | z > 0 |
| **T4** | Neurological transition | sustained GCS decline, seizure, ICP crossing | often endogenous or abrupt | z ≈ 0 or < 0 |
| **T5** | General ICU deterioration | composite, used only for power and comparison | mixed — uninterpretable mechanistically | uninterpretable |
| **T6** | Abrupt / noise-dominated | arrhythmic arrest from fixed substrate, massive PE, tamponade | **noise-induced** | **z ≈ 0 — no precursor** |

T6 is included **deliberately as a negative class**. It is where the hypothesis
is supposed to fail, and a positive finding there would be evidence of leakage,
not of sensitivity.

T5 is a power and comparability device only. **No mechanistic conclusion may be
drawn from T5**, because pooling mechanisms averages opposing predictions into
a meaningless middle.

---

## 2. The Question

> Does the same structural precursor appear across transition classes?

### 2.1 The five permitted outcomes

```
════════════════════════════════════════════════════════════════════
  A  UNIVERSAL PRECURSOR
     The same signature, same sign, in every powered class.

  B  FAMILY-SPECIFIC PRECURSOR
     Present in exogenous-insult classes (T2, T3), absent in
     endogenous and abrupt classes (T4, T6).

  C  MECHANISM-SPECIFIC PRECURSOR
     z sign varies by class in the direction the mechanism predicts:
     positive for exogenous, near-null or negative for endogenous.

  D  PREDICTIVE BUT NON-MECHANISTIC
     Structural quantities predict, but z carries no mechanistic
     information and the sign does not track class.

  E  NO PRECURSOR
     Nothing beyond M1 in any powered class.
════════════════════════════════════════════════════════════════════
```

### 2.2 Which outcome is expected

**B or C**, not A.

The synthetic benchmark shows z is a detector of **exogenous, homeostatically
constrained displacement only**. It failed on the fold mechanism (AUC 0.30) and
was blind to the noise mechanism (AUC 0.53). If the physiology mirrors the
mathematics, universality is not available.

```
┌──────────────────────────────────────────────────────────────────┐
│  Outcome A would be SURPRISING and should be treated with        │
│  suspicion, not celebration.                                      │
│                                                                   │
│  A signature that appears in every class — including T6, where    │
│  no precursor should exist — is the signature of a confound,      │
│  most likely acquisition behaviour (M0).                          │
└──────────────────────────────────────────────────────────────────┘
```

Outcome **D** is the most likely genuinely-positive result, and it is a
significant demotion: it would mean the structural quantities work as
statistics but the mechanistic story attached to them is decoration.

Outcome **E** is a real and reportable result.

---

## 3. Analysis Rules

| Rule | Reason |
|---|---|
| Each class analysed separately **before** any pooling | Pooling averages opposing sign predictions to zero |
| Class-specific power reported **before** any null is claimed | An underpowered null is "inconclusive", never "no precursor" |
| Sign predictions preregistered per class (table §1) | Otherwise class-specific findings are post-hoc storytelling |
| T6 treated as a **negative control class** | Detection there indicates leakage |
| T5 excluded from all mechanistic conclusions | Mechanistically uninterpretable by construction |
| Class assignment made from **physiological criteria and diagnosis codes only**, never from the model's own output | Otherwise the taxonomy is fitted to the result |

### 3.1 Minimum events per class

A class enters confirmatory analysis only with ≥ 80% power for the
preregistered effect size, estimated from the synthetic benchmark's effect
magnitudes and the cohort's realised event count. Classes below that threshold
are reported as **underpowered**, with their point estimates and intervals, and
carry no confirmatory weight.

---

## 4. The Mechanistic Prediction That Would Be Genuinely New

╔══════════════════════════════════════════════════════════════════════╗
║  If z(t) > 0 in T2/T3 (exogenous insult) and z(t) ≈ 0 in T6         ║
║  (abrupt), at MATCHED deformation magnitude ‖ΔG‖, then the           ║
║  direction of constrained deformation carries mechanistic            ║
║  information that magnitude alone does not.                          ║
║                                                                      ║
║  Nothing located in the early-warning literature claims this.        ║
║                                                                      ║
║  It is also the outcome most easily produced by class-correlated     ║
║  confounding — sepsis patients are monitored differently — which     ║
║  is why M0 is stratified BY CLASS, not merely run once overall.      ║
╚══════════════════════════════════════════════════════════════════════╝

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   T6 is where this is supposed to fail.                              ║
║   If it succeeds there, the finding is a confound.                   ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Transition Taxonomy*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) · [`HYPOTHESIS.md`](HYPOTHESIS.md) · [`COMPETING_MODELS.md`](COMPETING_MODELS.md) · [`DATASET_REQUIREMENTS.md`](DATASET_REQUIREMENTS.md)
