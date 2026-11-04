# VT/VF programme: estimator comparison, selection record, design-stage optimisation and provisional SESOI

> **Status: DESIGN RECORD. SYNTHETIC ONLY. NO PRIMARY ESTIMATOR IS SELECTED.**
>
> - No real data were examined. No protocol is frozen.
> - Source mathematics, interpretations, operationalisations, estimators and
>   tests are kept distinct below. A failing *estimator* does not falsify
>   the *source equation* or the Transition Dynamics hypothesis.
> - Results: [`VT_VF_FALSIFICATION_SUITE.md`](VT_VF_FALSIFICATION_SUITE.md).

## 1. Levels kept distinct

| Level | Object in this phase |
|---|---|
| Source equation | ΔG: geometric (affine-invariant Riemannian, AIRM) distance between a reference and a current second-order structure of physiological state; persistence of supra-threshold deviation |
| Interpretation | a loss of regulatory stability shows up as a change in the multichannel *structure* of beat-to-beat dynamics before the transition |
| Operationalisation | beats → 4 channels (NN, RT amplitude, T amplitude, ST); 256-clean-beat windows ending every minute; baseline = minutes 20–45 of the recording; Ledoit–Wolf shrinkage |
| Estimator (per window) | the statistics in §2 |
| Per-patient estimand | s_{i,b} = AUROC(bin-b windows vs remote windows) − ½ on the conventional-adjusted residual |
| Test | unchanged repaired study-level rule (`repaired_rule.decide`) |

## 2. Statistics compared (all through the identical per-patient pipeline)

Notation: Σ₀ and Σ_w are the shrunk covariances of the baseline and of
window w. R = corr(Σ). Subscript *h* means locally detrended (a 21-beat
moving average removed). Subscript *p* means NN-conditional (morphology
channels residualised on NN within the window). The AIRM distance is
d(A, B) = ‖log(A^{-½} B A^{-½})‖_F.

| Statistic | Definition | Role |
|---|---|---|
| `td3` | ½[z(S) + z(d(Σ₀, Σ_w))] combined with the persistence Q; S = Mahalanobis mean shift | **original combined estimator** |
| `dG_hp` | d(Σ₀h, Σ_wh) | full covariance ΔG (detrended) |
| `shape_raw` | d(R₀, R_w) + persistence | **correlation-only ΔG** (Phase-4 choice) |
| `shape_hp` | d(R₀h, R_wh) + persistence | correlation-only ΔG, detrended |
| `pshape_hp` | d(R₀hp, R_whp) + persistence on residual | correlation-only ΔG, detrended, NN-conditional (**leakage-repaired candidate**) |
| `corrFrob_hp` | ‖R_wh − R₀h‖_F | ordinary correlation statistic |
| `meanabsr_hp` | mean of the off-diagonal \|r\| in R_wh | ordinary correlation statistic (DNB-style "rising correlation") |
| `logdet_hp` | \|log det Σ_wh − log det Σ₀h\| | covariance competitor (generalised variance) |
| `diagAIRM_hp` | ‖log(diag Σ_wh / diag Σ₀h)‖ | covariance competitor (variances only, no structure) |
| `covFrob_hp` | ‖Σ_wh − Σ₀h‖_F | covariance competitor (Euclidean) |
| `conv_hr` | −mean NN (5-min), unadjusted | conventional ECG baseline |
| `conv_sdnn` | −SDNN (5-min), unadjusted | conventional ECG baseline |

**Not compared:** QT/QTc, ectopy burden, T-wave alternans and RMSSD as
stand-alone baselines. The simulator does not generate ectopy or
alternans, and these remain real-data baselines in the protocol repair
plan.

## 3. Comparison summary (n = 80 studies; selection / holdout; full tables in the suite document)

| Statistic | Worst conventional-only false positive | Undetected near-onset artefact | Gain-drift null | corr0.10 power | corr0.05 | var0.5 | nncorr0.15 (holdout) | Admissible |
|---|---|---|---|---|---|---|---|---|
| `td3` | 0.998 / 1.000 | 0.340 / 0.162 | 0.080 / 0.284 | 0.444 / 0.502 | 0.012 / 0.022 | 0.992 / 0.996 | 0.182 | no / no |
| `dG_hp` | 1.000 / 1.000 | 0.998 / 0.998 | 0.028 / 0.028 | 0.996 / 0.994 | 0.020 / 0.110 | 0.998 / 1.000 | 0.928 | no / no |
| `shape_raw` | 0.996 / 0.996 | 0.082 / 0.014 | 0.002 / 0.010 | 0.998 / 0.996 | 0.248 / 0.206 | 0.080 / 0.018 | 0.716 | no / no |
| `shape_hp` | 1.000 / 1.000 | 0.996 / 0.996 | 0.000 / 0.010 | 0.994 / 0.994 | 0.060 / 0.152 | 0.970 / 0.994 | 0.996 | no / no |
| `pshape_hp` | **0.030 / 0.036** | **1.000 / 0.998** | 0.000 / 0.002 | 1.000 / 0.998 | 0.172 / 0.312 | 0.000 / 0.034 | **0.000** | no / no |
| `corrFrob_hp` | 0.998 / 0.994 | 0.998 / 0.996 | 0.000 / 0.012 | 0.798 / 0.776 | 0.008 / 0.050 | 0.920 / 0.982 | 0.380 | no / no |
| `meanabsr_hp` | 0.002 / **0.392** | 0.000 / 0.000 | 0.002 / 0.002 | 0.996 / 0.998 | 0.998 / 0.998 | 0.000 / 0.000 | 0.998 | no / no |
| `logdet_hp` | 0.998 / 1.000 | 0.998 / 1.000 | 0.150 / 0.158 | 0.544 / 0.498 | 0.058 / 0.054 | 0.994 / 0.994 | 0.002 | no / no |
| `diagAIRM_hp` | 0.998 / 1.000 | 0.996 / 0.992 | 0.024 / 0.008 | 0.026 / 0.016 | 0.006 / 0.016 | 0.996 / 0.996 | 0.202 | no / no |
| `covFrob_hp` | 1.000 / 0.998 | 0.996 / 0.998 | 0.726 / 0.762 | 0.406 / 0.468 | 0.006 / 0.032 | 1.000 / 0.996 | 0.580 | no / no |
| `conv_hr` | 0.992 / 1.000 | 0.010 / 0.008 | 0.000 / 0.014 | 0.036 / 0.008 | 0.028 / 0.042 | 0.024 / 0.022 | 0.000 | no / no (comparator) |
| `conv_sdnn` | 1.000 / 1.000 | 0.016 / 0.000 | 0.008 / 0.000 | 0.002 / 0.004 | 0.004 / 0.012 | 0.002 / 0.008 | 0.018 | no / no (comparator) |

"Power" is the rate of any positive structure-specific verdict. corr0.10
and corr0.05 are the generative correlation-perturbation strengths γ, not
the estimand s. γ = 0.10 gives s ≈ 0.15–0.31 by bin; γ = 0.05 gives
s ≈ 0.02–0.10, which is the SESOI region.

### Answers to the comparison requested

1. **Correlation-only ΔG vs the original combined estimator.**
   - The combined estimator `td3` is dominated. It is non-specific under HR
     and HRV changes (≈ 99–100% spurious positives), gain drift and wander,
     and it has the lowest power at γ = 0.10 among the correlation-sensitive
     statistics.
   - Correlation-only ΔG removes the gain and variance sensitivity
     (`shape_raw` and `shape_hp` do not react to gain drift, and `shape_raw`
     barely to var0.5).
   - Only the NN-conditional version (`pshape_hp`) removes the HR and HRV
     leakage.
2. **Against ordinary correlation statistics.**
   - `corrFrob_hp`, which is not NN-conditioned, leaks like `shape_hp` and
     has lower power.
   - `meanabsr_hp` has the highest power in this simulator (≥ 99.8% even at
     γ = 0.05) and is not triggered by independent-noise artefacts. That is
     **only because** its one-sided "rising correlation" direction is
     opposite to what simulated independent noise does.
   - It fails nulls (homogeneous, NN-artefact, wander and artefact cells;
     up to 6.4%), near-onset gaps, and **HR+HRV without RT coupling
     (39.2%, holdout only)**.
3. **Against covariance competitors.** `dG_hp`, `logdet_hp`, `diagAIRM_hp`
   and `covFrob_hp` respond to variance and gain changes and to HRV. They
   are not structure-specific. `diagAIRM_hp`, a variance-only statistic,
   detects no correlation precursor, which confirms that the positive
   scenarios are genuinely structural.
4. **Against conventional ECG baselines.** `conv_hr` and `conv_sdnn` detect
   their own mechanisms and rarely detect correlation precursors (≤ 9.6%).
   Structure precursors and conventional changes are therefore separable
   **in this simulator**. Whether they are separable in real ECG is unknown.

## 4. Selection process (recorded) and design-stage optimisation

### 4.1 Chronology of design decisions taken after seeing synthetic output

| Step | Observation that prompted it | Change | Seeds used to decide |
|---|---|---|---|
| D1 | Phase-4 pilot: `td3` and `shape_raw` positive under HR and HRV changes alone | local detrending (`_hp`) | `pilot.py` 0–5,039; `pilot2.py` 5,000–5,547 |
| D2 | `shape_hp` still leaks under HRV with RT–RR coupling | NN-conditional structure (`pshape_hp`) | `leakpilot.py` 70,000–75,319 |
| D3 | +0.03–0.04 null bias in `shape_hp` and `pshape_hp` | persistence computed on the residual, not residualised | `biasdiag.py` 90,000–90,399; `biasdiag2.py` 91,000–95,399 |
| D4 | HR +3 SD leak +0.14–0.16 after D3 | choice among 5 adjustment bases → `lin_dur_clip` | `basiscmp.py` 93,000–98,399 |
| D5 | leakage-test run 1 failed for HRV −30% | pool 300 → 1,200 with the run-1 patients retained; criteria unchanged | `hrvdiag.py` 700,000–920,599 |
| D6 | (none: pre-specified) | suite with selection and holdout seed sets and holdout-only scenarios | 1,000,000+ and 2,000,000+ |

Pilot scripts are kept in the session scratchpad, not the repository. Their
outputs were inspected interactively and **not all were archived**. That
is a provenance limitation, recorded here.

### 4.2 Size of the design search

- At least 4 instantaneous structure definitions (`shape`, `shape_hp`,
  `pshape_hp`, `corrFrob_hp`).
- 5 adjustment bases in D4, plus `poly` in Phase 4.
- 2 persistence treatments.

That is at least 40 analysis configurations evaluated on the same
generative model before the suite. The final candidate (`pshape_hp` +
`lin_dur_clip` + persistence on the residual) was the configuration that
best passed the **HR/HRV leakage scenarios that the same analyst designed**.

### 4.3 Consequences and how they are accounted for

1. **Selection-set performance of `pshape_hp` on conventional-only
   scenarios is optimistic.** Its own failure modes were the design target.
   The holdout set and the holdout-only scenarios are the less-biased
   check, and the holdout **did** show marginal failures (holdout HR +2 SD
   0.036, null artefact 0.056, coverage 0.925).
2. **Circularity.** The repairs remove the leak mechanisms the simulator
   contains (window-duration effects, linear RT–RR coupling). Passing
   leakage tests built on the same mechanisms is partly circular. The
   claim is restricted to "**under the tested conditions**".
3. **No estimator was selected.** The pre-specified rule returned none, so
   no power estimate in this document is attached to a "chosen" estimator.
4. **`meanabsr_hp` was not promoted** despite the highest power. That would
   be selection by performance in the current simulation, which the
   programme owner explicitly prohibited. It also fails A1, A2 and A3.
5. **Requirements for any future selection:**
   - A fresh seed base and a scenario set written by someone who did not
     design the estimators (different artefact, coupling and drift models).
   - The full configuration count (≥ 40, plus later steps) reported in the
     protocol.
   - Power taken from the holdout run only.
   - Every non-selected admissible statistic reported as a sensitivity
     analysis on real data.
   - The estimator frozen **before** any data access.
6. **Real-data guard.** Before any outcome window is examined, the frozen
   pipeline must pass outcome-free negative controls on the real dataset:
   remote-only pseudo-onsets and conventional-matched pseudo-onsets. Each
   synthetic guarantee is conditional on a model that real ECG can violate.

## 5. Provisional smallest effect size of interest (SESOI)

### 5.1 Mathematical definition

For patient *i*, bin *b*, let R⁺ be the residual statistic of a randomly
drawn bin-*b* window and R⁻ that of a randomly drawn remote window from
the same patient (lead ≥ 60 min, start ≥ 50 min, conventional adjustment
`lin_dur_clip` fitted on remote windows).

- θ_{i,b} = P(R⁺ > R⁻) + ½ P(R⁺ = R⁻) − ½.
- Its plug-in estimator is s_{i,b}, which equals the Mann–Whitney AUROC − ½.
- The population estimand is Θ_b = E_i[θ_{i,b}] over independent eligible
  patients (one first event per patient).
- **Provisional SESOI: Θ_b = 0.10 (within-patient AUROC 0.60), applied per
  bin.**
- The same value is the exclusion margin δ: `LARGE_EXCLUDED` holds when the
  one-sided 95% upper bound of Θ_b is < 0.10 in every bin
  (intersection–union).

### 5.2 Scales on which 0.10 can be read

These are approximations:

| Θ | within-patient AUROC | binormal d (equal variance) | sensitivity at FPR 0.05 | sensitivity at FPR 0.20 | n for 80% power, one bin (α = 0.00625 one-sided, SD 0.28) |
|---|---|---|---|---|---|
| 0.05 | 0.55 | 0.178 | 0.071 | 0.253 | ≈ 350 |
| **0.10** | **0.60** | **0.358** | **0.099** | **0.314** | **≈ 87** |
| 0.15 | 0.65 | 0.545 | 0.136 | 0.383 | ≈ 39 |

- The between-patient SD of s under the null is ≈ 0.28 (suite, `pshape_hp`).
  So 0.10 is about 0.36 of the between-patient SD.
- The sample sizes use a normal approximation and ignore the sign-test
  conjunction and the multi-bin EXPLORATORY requirement. Real n
  requirements are higher.
- The resulting rates at n = 80 are:

  | Quantity | Selection | Holdout |
  |---|---|---|
  | γ = 0.05 (s ≈ 0.02–0.10), any positive | 0.172 | 0.312 |
  | γ = 0.05, EXPLORATORY | 0.064 | 0.096 |
  | Null, `LARGE_EXCLUDED` | 0.698 | 0.826 |

### 5.3 Scientific interpretation

- **What 0.10 means.** In a typical patient, a window in the lead bin has a
  60% chance of showing more structure deviation, beyond what conventional
  features explain, than a window from the same patient's own remote
  period.
- **Mechanistic signal, not alarm performance.** At this size, about 10% of
  pre-onset windows would be flagged at a 5% within-patient false-alarm
  rate. That is a **mechanistic signal** worth pursuing prospectively. It
  is **not** clinically useful prediction, and must never be reported as
  such.
- **Why not smaller.** Effects below 0.10 need about 350 or more
  independent patients per bin. That exceeds any plausible near-term
  adjudicated cohort. They would also be hard to separate from residual
  synthetic leakage of about 0.01–0.03 (F2) and from undetected-artefact
  bias in real data.
- **Why not larger.** A SESOI of 0.15 would make the study insensitive to
  effects (0.10–0.15) that are still mechanistically informative, and would
  make a "large effect excluded" result easier to obtain and less
  meaningful.
- **Population vs individual.** Θ_b = 0.10 is an average. It is compatible
  with every patient at 0.10 or with half the patients at 0.20 and half at
  0. The study cannot tell these apart without the heterogeneity analysis.
  Therefore, a significant population effect must not be read as a
  per-patient predictive property.
- **Subgroups.** The same SESOI applies to VT and VF separately. With fewer
  patients per class, the class-specific results are expected to be
  exploratory unless each class reaches about 87 or more eligible patients.

### 5.4 Status

**Provisional** (research decision D-VT2). It is not derived from any
VT/VF data. It may be revised only before a protocol freeze, with the
reason recorded, and never after outcome data have been seen.

---

© 2026 Davarn Morrison · Transition Dynamics
