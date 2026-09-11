# VitalDB model-adequacy result

## Verdict

# NOT SUPPORTED

The onset model's dynamical assumptions do **not** transfer to real
continuously-monitored human physiology. Two frozen gates failed, and a third
check shows the model's apparent success carries no exponential content at all.

This is a scientific determination, not an admissibility failure: **56
admissible recordings**, above the required 50.

---

## Dataset

VitalDB, PhysioNet open-access S3 mirror, v1.0.0, **CC-BY 4.0**. No
credentialing, no data use agreement, no access control bypassed. 2-second
numeric vital-sign tracks; 338 cases with ≥ 6.5 h recording; channels HR,
invasive MAP, SpO₂, EtCO₂. Per-case SHA-256 in
`analysis/results/vitaldb_manifest_*.json`. Raw files not retained or
redistributed.

Split frozen before any signal was examined: 40 calibration, 298 confirmatory,
disjoint.

---

## What failed

### 1. The exponential form contributes nothing — it degenerates to a step

Baseline-derived rates have a median of **63 /h**, a relaxation time of under a
minute. Over a multi-hour segment $1-e^{-k(t-t_0)}$ is therefore fully
saturated:

| check | result |
|---|:--:|
| cases where the exponential is saturated by segment end | **100%** |
| held-out MSE, M-exp | 75.02 |
| held-out MSE, explicit **step** model | 75.34 |
| relative difference | **0.28%** |
| cases where a step ties or beats M-exp | **57%** |

M-exp is a step-change detector wearing an exponential's clothes. Its victory
over the null, linear, spline and random-walk comparators says only that
physiological trajectories contain level shifts.

### 2. No advantage over surrogates

| quantity | value | 95% CI |
|---|:--:|:--:|
| M-exp selection rate | 62% | [50%, 75%] |
| phase-randomised surrogate rate | 56% | [50%, 61%] |
| **difference** | **+7%** | **[−6%, +19%]** |

The interval includes zero, failing the frozen gate. In **0 of 56** cases did
M-exp beat every one of its own surrogates. Leave-one-out gives +5.2% to +8.4%,
so this is a stable small effect, not one driven by a subset.

### 3. Baseline rates do not predict trajectory curvature — the central claim

| quantity | value |
|---|:--:|
| median rank correlation | **0.00** (95% CI [−0.15, +0.15]) |
| quartiles | [−0.45, 0.00, +0.45] |
| cases with correlation ≥ 0.5 | 25% |
| median $k_\text{curv}/k_\text{base}$ | **0.005** |

Perfectly symmetric about zero — the signature of no relationship. The frozen
requirement was ≥ 0.5.

This is the gate that matters most. The estimator's independence from
circularity rested entirely on baseline dynamics informing later trajectory
shape. On real physiology they are unrelated.

---

## Why, physically

Baseline autocorrelation measures **fast fluctuation decay**; trajectory
curvature reflects **slow regulation**. They are different physical quantities.

| baseline resolution | median rate | relaxation |
|:--:|:--:|:--:|
| 2 s | 63.4 /h | 0.9 min |
| 10 s | 51.5 /h | 1.2 min |
| 60 s | 26.0 /h | 2.3 min |
| **observed curvature** | **0.56 /h** | **107 min** |

No choice of baseline resolution reaches the timescale at which the
trajectories actually bend. This is not a tuning failure and cannot be fixed by
re-estimating rates.

---

## What survived

Only this: a **step-change** model predicts held-out multichannel physiological
trajectories better than null, constant, linear, spline or random-walk
comparators (mean rank 1.61). That is an unremarkable statement about
physiological data containing level shifts. It is not evidence for Transition
Dynamics, and it does not depend on any part of the framework.

---

## Scope and limitations

- **VitalDB is intraoperative.** Recorded in advance of the result: no window
  is treatment-quiet in the sense the original protocol intended for ICU
  baselines. A negative result could in principle reflect the intervention
  environment. However, failures 1 and 3 are **not** environment-dependent —
  they follow from the timescale mismatch, which is a property of physiological
  autocorrelation rather than of surgery.
- 196 of 298 cases were excluded for baseline non-stationarity even under the
  corrected screen. Real physiology genuinely drifts over hour-scale windows.
- This result concerns **model adequacy only**. It says nothing about whether
  structural deformation precedes deterioration, which was never tested.

---

## Consequences

The onset estimator is **not transferable** to real physiology as specified.
Per the frozen decision rule, no mechanism or early-detection claim may
proceed on its basis.

The exposure-control machinery built in Stages 1–4 depended on estimating
time-since-onset from trajectory curvature using baseline rates. That
dependency is now known to be unsupported on real data. The synthetic
identifiability results stand as stated — they were always labelled an internal
consistency result — but the route from them to real physiology is closed
unless onset can be estimated some other way.

**No new construct is introduced to rescue this.** The precise prediction that
failed is recorded above.

Reproduce: `analysis/adequacy/run_vitaldb_confirmatory.py`.
Tables: `analysis/results/vitaldb_confirmatory.md`, `vitaldb_confirmatory.json`.

---

© 2026 Davarn Morrison · Transition Dynamics
