# VT/VF programme: leakage repair, regression tests and synthetic falsification suite

> **Status: SYNTHETIC DESIGN EVIDENCE ONLY. Nothing here is a finding about
> real patients.**
>
> - No real VT/VF hypothesis test was run. No pre-event physiology was read.
> - No protocol is frozen. The seven hypotension outcomes,
>   [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) and all historical results
>   are unchanged.
> - A synthetic failure here is a failure of an **estimator or
>   operationalisation** inside one generative model. It is not evidence
>   for or against the Transition Dynamics hypothesis.

Code: `analysis/vtvf/beatsim2.py` (simulator), `repaired_rule2.py`
(per-patient statistics, VT/VF subgroup report; study-level rule reused
unchanged from `repaired_rule.decide`), `test_leakage.py` (regression tests),
`suite.py` (pre-specified suite) and `suite_report.py` (the tables below).
Results: `analysis/results/vtvf_leakage_tests_run1.json`,
`vtvf_leakage_tests.json` (run 2), `vtvf_falsification_suite.json`.

## 1. Estimand and inference (unchanged; patient-independent)

For patient *i* and lead bin *b* ∈ {B5 (2,5], B10 (5,10], B15 (10,15],
B30 (15,30] min}:

s_{i,b} = AUROC(residual statistic in bin-*b* windows vs the same patient's
remote windows, lead ≥ 60 min) − ½.

There is no cross-patient training, so patients are independent units. The
study-level rule (one-sided t **and** sign test, α = 0.00625 per bin,
pseudo-onset temporal control, permutation and injected positive pipeline
controls, drift and acquisition explanations) is unchanged from Phase 4. No
alpha, gate or threshold was altered in this phase.

## 2. Heart-rate leakage: mechanisms and repair

### 2.1 Mechanisms demonstrated in the beat simulator

| # | Mechanism | Effect on the Phase-4 statistic |
|---|---|---|
| L1 | Fixed 256-beat windows: a higher HR shortens the window in time, so the share of slow (minutes-scale) variance in each window changes, and so do the beat-to-beat correlations | +0.10 to +0.19 in s under an HR rise alone (td3) |
| L2 | Physiological RT–RR coupling: an HRV change alters the NN–RT correlation, which the correlation-structure statistics read as "structure" | up to +0.40 (td3), +0.26 to +0.41 (shape_hp) under HRV reduction |
| L3 | Regressing the zero-inflated 30-min persistence integral on conventional covariates | +0.026 null bias |
| L4 | Polynomial conventional adjustment extrapolated beyond the remote support | +0.13 to +0.16 at an HR rise of 3 SD |

### 2.2 Repair (design choices; see §4 of the estimator document for their cost)

1. **Local detrending** (`_hp`): a 21-beat centred moving average is removed
   inside each window before computing covariance or correlation (L1).
2. **NN-conditional structure** (`pshape_hp`): within each window, RT
   amplitude, T amplitude and ST are regressed on NN, and the structure
   statistic is computed on the residuals. This removes L2 **by
   construction**, and with it any genuine precursor that lives only in the
   HR-to-repolarisation coupling (§6, F3).
3. **Adjustment basis `lin_dur_clip`**: linear conventional features plus the
   window duration, clipped to the remote-window support (L4).
4. **Persistence on the residual**: the 30-min persistence integral is
   computed on the conventional-adjusted residual with a baseline-derived
   threshold, and is never regressed itself (L3).

### 2.3 Persistence bias diagnosis

The instantaneous component was unbiased under the null (+0.004). The
persistence component carried +0.026 when it was residualised. Computing it
on the residual series removed the bias. This is why `COMPOSITES2` in
`repaired_rule2.py` computes persistence after residualisation.

## 3. Regression tests: "HR/HRV changes alone cannot produce a structure-specific positive verdict"

The criteria were fixed before the first run and are **unchanged** between
runs:

- **T1:** every bin mean of s within ±0.04 under conventional-only scenarios.
- **T2:** at n = 80, any positive structure-specific verdict ≤ 2%.
- **T3:** a γ = 0.10 structural change is still detected (mean s ≥ 0.15 and
  EXPLORATORY ≥ 80%).
- **T4:** the null passes T1 and T2.
- **Power check:** the unrepaired `shape_hp` must visibly leak, which shows
  that the test can detect leakage at all.

| Scenario | Run 1 (pool 300) bin means; any+ | Run 2 (pool 1,200) bin means; any+ | Run 2 |
|---|---|---|---|
| HR +1 SD | −0.003…+0.009; 0.005 | +0.010…+0.012; 0.010 | pass |
| HR +3 SD | −0.008…+0.016; 0.007 | 0.000…+0.005; 0.005 | pass |
| HRV −30% | +0.026…**+0.051**; **0.065** | 0.000…+0.012; 0.003 | pass |
| HRV −50% | 0.000…+0.005; 0.007 | +0.005…+0.014; 0.017 | pass |
| HR +2 SD & HRV −50% | +0.003…+0.025; 0.018 | +0.001…+0.006; 0.003 | pass |
| same, RT–RR coupling 0.6 | +0.003…+0.026; 0.013 | +0.005…+0.022; **0.020** | pass (on the bound) |
| same, RT–RR coupling 0 | +0.008…+0.026; 0.020 | −0.004…+0.004; 0.000 | pass |
| null | −0.015…0.000; 0.000 | −0.003…+0.008; 0.010 | pass |
| structural γ = 0.10 | 0.148…0.284; 0.995 | 0.170…0.311; 0.997 | pass (T3) |
| power check: `shape_hp`, HR+HRV+RT 0.6 | — | **+0.263…+0.409** | leak seen |

**Run history.** Run 1 **failed** for HRV −30%. Three independent
600-patient diagnostic pools then gave HRV −30% means of −0.011 to +0.022,
against null pools of −0.005 to +0.034. This was read as pool fluctuation.
Run 2 kept the criteria, quadrupled the pool and **contains the run-1
patients**, so the failing evidence was not discarded. Run 1 is preserved
in `vtvf_leakage_tests_run1.json`.

**What the tests establish.** Under this simulator's HR, HRV and RT–RR
mechanisms, with recordings of 300–1,200 min, `pshape_hp` showed no
systematic leak beyond ±0.022 in s. Its spurious-positive rate was ≤ 2%.
**This is not a proof for real ECG.** Moreover, the strong-coupling
scenario has now given 0.013, 0.020, 0.030 and 0.026 across four
independent pools (run 1, run 2, suite selection, suite holdout). A
residual leak of about 0.01–0.02 in s under strong RT–RR coupling is
therefore **likely, not excluded** (§6, F2).

## 4. Pre-specified falsification suite

The full specification is the header of `analysis/vtvf/suite.py`, written
before its first run:

- **Seed sets:** selection uses base 1,000,000 and holdout 2,000,000. No
  pilot or leakage-test seed falls in these ranges (pilots used 0–5,547,
  70,000–98,399 and 700,000–920,599; leakage tests used 500,000–581,199).
- **Pool and studies:** 400 patients per scenario per set, recording length
  uniform 140–1,440 min, 500 resampled studies at n = 40 and n = 80.
- **Statistics:** ten TD-family statistics and two conventional baselines,
  all run through the same per-patient rule and the same adjustment basis.
- **Holdout-only scenarios** (never used for selection): slow-dynamics null
  (AR φ ≥ 0.98), HR+HRV without RT–RR coupling, NN-coupled structural
  precursor (`nncorr0.15`), and a VF-only effect with 60% VF.
- **Admissibility, at n = 80:**
  - **A1:** in every null scenario, EXPLORATORY ≤ 1% and any positive ≤ 2%.
  - **A2:** in every conventional-only scenario, any positive ≤ 2%.
  - **A3:** with near-onset artefacts (70% detected) and near-onset gaps,
    any positive ≤ 2%.
  - **A4:** 95% coverage in [0.93, 0.97] for the null and corr0.10 scenarios
    at n = 40.
- **Selection rule:** among admissible statistics, the one whose
  **definition** matches the structure-specific hypothesis, not the most
  powerful. The holdout must confirm it.

### 4.1 Pre-specified outcome

**No statistic is admissible in either set. By the pre-specified rule, no
provisional primary estimator is selected.**

## 5. Results (generated by `suite_report.py`)

#### selection set: rate of any positive structure-specific verdict, n = 80 (EXPLORATORY rate in brackets for null scenarios)

| family | scenario | pshape | shape_hp | shape_raw | td3 | dG_hp | corrFrob | meanabsr | logdet | diagAIRM | covFrob | conv_hr | conv_sdnn |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| null | null | 0.016 (0.004) | 0.018 (0.004) | 0.020 (0.006) | 0.004 (0.002) | 0.018 (0.000) | 0.008 (0.000) | 0.004 (0.000) | 0.000 (0.000) | 0.010 (0.000) | 0.018 (0.000) | **0.026 (0.000)** | 0.016 (0.000) |
| null | null_artefact | 0.012 (0.002) | 0.002 (0.000) | **0.030 (0.004)** | 0.002 (0.000) | 0.004 (0.000) | **0.026 (0.000)** | 0.016 (0.000) | 0.002 (0.000) | 0.002 (0.000) | 0.000 (0.000) | 0.012 (0.000) | 0.008 (0.000) |
| null | null_gain_drift | 0.000 (0.000) | 0.000 (0.000) | 0.002 (0.002) | **0.080 (0.032)** | **0.028 (0.006)** | 0.000 (0.000) | 0.002 (0.000) | **0.150 (0.034)** | **0.024 (0.002)** | **0.726 (0.298)** | 0.000 (0.000) | 0.008 (0.000) |
| null | null_homogeneous | 0.000 (0.000) | 0.000 (0.000) | 0.006 (0.000) | 0.002 (0.000) | 0.004 (0.000) | 0.006 (0.000) | **0.044 (0.000)** | 0.006 (0.000) | 0.012 (0.000) | 0.010 (0.000) | 0.010 (0.002) | 0.010 (0.000) |
| null | null_missing | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | 0.006 (0.000) | 0.004 (0.000) | 0.006 (0.000) | 0.002 (0.000) | 0.008 (0.002) | 0.004 (0.000) | **0.052 (0.008)** | 0.004 (0.000) |
| null | null_nn_artefact | 0.004 (0.000) | 0.000 (0.000) | 0.000 (0.000) | 0.000 (0.000) | 0.006 (0.000) | 0.004 (0.000) | **0.036 (0.000)** | 0.008 (0.000) | 0.004 (0.000) | 0.000 (0.000) | 0.014 (0.002) | 0.014 (0.000) |
| null | null_wander | 0.004 (0.000) | 0.002 (0.000) | 0.000 (0.000) | **0.118 (0.078)** | 0.004 (0.000) | 0.004 (0.000) | **0.026 (0.000)** | 0.000 (0.000) | 0.002 (0.000) | 0.006 (0.000) | 0.006 (0.002) | **0.030 (0.000)** |
| conventional | conv_hr2 | 0.006 | 0.010 | **0.152** | **0.988** | 0.020 | 0.008 | 0.002 | **0.056** | 0.014 | 0.012 | **0.992** | 0.000 |
| conventional | conv_hr2_hrv50_rt0.6 | **0.030** | **1.000** | **0.996** | **0.998** | **1.000** | **0.998** | 0.000 | **0.996** | **0.998** | **0.998** | **0.992** | **0.998** |
| conventional | conv_hrv50 | 0.000 | **1.000** | **0.986** | **0.994** | **0.998** | **0.996** | 0.000 | **0.998** | **0.998** | **1.000** | 0.010 | **1.000** |
| acquisition | artefact_onset_70pct | **1.000** | **0.996** | **0.082** | **0.340** | **0.998** | **0.998** | 0.000 | **0.998** | **0.996** | **0.996** | 0.010 | 0.016 |
| acquisition | gaps_near_onset | 0.002 | 0.010 | 0.012 | 0.006 | 0.000 | 0.010 | **0.046** | 0.002 | 0.000 | 0.008 | **0.066** | **0.062** |
| positive | corr0.05 | 0.172 | 0.060 | 0.248 | 0.012 | 0.020 | 0.008 | 0.998 | 0.058 | 0.006 | 0.006 | 0.028 | 0.004 |
| positive | corr0.10 | 1.000 | 0.994 | 0.998 | 0.444 | 0.996 | 0.798 | 0.996 | 0.544 | 0.026 | 0.406 | 0.036 | 0.002 |
| positive | corr0.10_artefact70 | 1.000 | 0.998 | 0.960 | 0.712 | 0.998 | 0.996 | 0.002 | 0.998 | 0.998 | 1.000 | 0.006 | 0.010 |
| positive | corr0.10_gain_drift | 1.000 | 0.994 | 0.996 | 0.170 | 0.000 | 0.986 | 0.994 | 0.000 | 0.044 | 0.996 | 0.002 | 0.014 |
| positive | corr0.10_half_responders | 0.748 | 0.484 | 0.476 | 0.052 | 0.512 | 0.336 | 0.980 | 0.040 | 0.014 | 0.124 | 0.018 | 0.032 |
| positive | corr0.10_het1.0 | 0.980 | 0.978 | 0.990 | 0.600 | 0.992 | 0.922 | 1.000 | 0.866 | 0.006 | 0.700 | 0.002 | 0.022 |
| positive | corr0.10_missing | 1.000 | 0.998 | 0.992 | 0.586 | 0.982 | 0.756 | 0.996 | 0.748 | 0.020 | 0.430 | 0.012 | 0.002 |
| positive | intermittent_corr0.15 | 0.998 | 0.984 | 0.996 | 0.246 | 0.922 | 0.544 | 0.992 | 0.338 | 0.068 | 0.302 | 0.096 | 0.006 |
| positive | mean0.5 | 0.000 | 0.004 | 0.032 | 0.616 | 0.012 | 0.002 | 0.006 | 0.008 | 0.018 | 0.014 | 0.000 | 0.012 |
| positive | var0.5 | 0.000 | 0.970 | 0.080 | 0.992 | 0.998 | 0.920 | 0.000 | 0.994 | 0.996 | 1.000 | 0.024 | 0.002 |
| subgroup | corr0.10_VF_only | 0.030 | 0.158 | 0.036 | 0.042 | 0.106 | 0.086 | 0.368 | 0.032 | 0.008 | 0.022 | 0.000 | 0.004 |

Bold = violates the pre-specified admissibility bound (A1-A3).

#### holdout set: rate of any positive structure-specific verdict, n = 80 (EXPLORATORY rate in brackets for null scenarios)

| family | scenario | pshape | shape_hp | shape_raw | td3 | dG_hp | corrFrob | meanabsr | logdet | diagAIRM | covFrob | conv_hr | conv_sdnn |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| null | null | 0.002 (0.000) | 0.004 (0.000) | 0.008 (0.000) | 0.002 (0.002) | 0.006 (0.000) | 0.002 (0.000) | 0.010 (0.000) | 0.002 (0.000) | 0.004 (0.000) | 0.008 (0.000) | 0.004 (0.000) | 0.002 (0.000) |
| null | null_artefact | **0.056 (0.022)** | 0.020 (0.000) | 0.004 (0.000) | 0.000 (0.000) | 0.008 (0.000) | 0.016 (0.000) | **0.064 (0.002)** | 0.016 (0.000) | 0.006 (0.000) | **0.030 (0.000)** | 0.010 (0.000) | **0.026 (0.000)** |
| null | null_gain_drift | 0.002 (0.000) | 0.010 (0.000) | 0.010 (0.002) | **0.284 (0.160)** | **0.028 (0.002)** | 0.012 (0.000) | 0.002 (0.000) | **0.158 (0.032)** | 0.008 (0.002) | **0.762 (0.390)** | 0.014 (0.004) | 0.000 (0.000) |
| null | null_homogeneous | 0.012 (0.004) | 0.006 (0.002) | 0.018 (0.002) | 0.014 (0.004) | 0.006 (0.000) | 0.012 (0.000) | 0.006 (0.000) | 0.002 (0.000) | 0.000 (0.000) | 0.004 (0.000) | **0.044 (0.004)** | 0.008 (0.000) |
| null | null_missing | 0.000 (0.000) | 0.002 (0.000) | 0.008 (0.002) | 0.014 (0.004) | 0.010 (0.000) | 0.010 (0.000) | 0.010 (0.000) | 0.016 (0.000) | 0.010 (0.000) | 0.010 (0.000) | 0.012 (0.000) | 0.012 (0.000) |
| null | null_nn_artefact | 0.010 (0.002) | 0.004 (0.000) | 0.006 (0.000) | **0.066 (0.024)** | 0.004 (0.000) | 0.004 (0.000) | 0.004 (0.000) | 0.006 (0.000) | 0.002 (0.000) | 0.002 (0.000) | 0.008 (0.002) | **0.038 (0.002)** |
| null | null_slow_dynamics | 0.000 (0.000) | 0.012 (0.002) | 0.002 (0.000) | 0.002 (0.002) | 0.002 (0.000) | 0.008 (0.000) | 0.008 (0.002) | 0.008 (0.000) | 0.016 (0.000) | 0.010 (0.000) | 0.012 (0.002) | **0.022 (0.000)** |
| null | null_wander | 0.006 (0.000) | 0.012 (0.004) | 0.002 (0.000) | 0.016 (0.008) | 0.008 (0.000) | 0.018 (0.000) | 0.016 (0.000) | 0.008 (0.000) | **0.024 (0.002)** | 0.018 (0.000) | **0.046 (0.006)** | 0.018 (0.000) |
| conventional | conv_hr2 | **0.036** | **0.032** | **0.256** | **0.996** | **0.022** | 0.004 | 0.006 | 0.016 | 0.016 | 0.008 | **1.000** | 0.000 |
| conventional | conv_hr2_hrv50_rt0 | 0.004 | **0.046** | **0.642** | **0.996** | **0.992** | 0.004 | **0.392** | **0.998** | **1.000** | **0.998** | **1.000** | **1.000** |
| conventional | conv_hr2_hrv50_rt0.6 | **0.026** | **0.998** | **0.996** | **1.000** | **1.000** | **0.994** | 0.000 | **0.998** | **0.998** | **0.992** | **0.988** | **0.998** |
| conventional | conv_hrv50 | 0.020 | **1.000** | **0.996** | **1.000** | **1.000** | **0.994** | 0.000 | **1.000** | **0.998** | **1.000** | 0.006 | **1.000** |
| acquisition | artefact_onset_70pct | **0.998** | **0.996** | 0.014 | **0.162** | **0.998** | **0.996** | 0.000 | **1.000** | **0.992** | **0.998** | 0.008 | 0.000 |
| acquisition | gaps_near_onset | 0.000 | 0.000 | 0.010 | 0.000 | 0.002 | 0.006 | **0.028** | 0.012 | **0.022** | **0.040** | 0.000 | **0.190** |
| positive | corr0.05 | 0.312 | 0.152 | 0.206 | 0.022 | 0.110 | 0.050 | 0.998 | 0.054 | 0.016 | 0.032 | 0.042 | 0.012 |
| positive | corr0.10 | 0.998 | 0.994 | 0.996 | 0.502 | 0.994 | 0.776 | 0.998 | 0.498 | 0.016 | 0.468 | 0.008 | 0.004 |
| positive | corr0.10_artefact70 | 0.996 | 1.000 | 0.972 | 0.906 | 1.000 | 0.990 | 0.004 | 0.998 | 0.998 | 0.998 | 0.004 | 0.014 |
| positive | corr0.10_gain_drift | 0.998 | 1.000 | 0.996 | 0.110 | 0.000 | 0.916 | 0.994 | 0.000 | 0.020 | 0.974 | 0.024 | 0.040 |
| positive | corr0.10_half_responders | 0.782 | 0.648 | 0.730 | 0.126 | 0.676 | 0.196 | 0.982 | 0.302 | 0.010 | 0.168 | 0.000 | 0.024 |
| positive | corr0.10_het1.0 | 0.966 | 0.902 | 0.974 | 0.398 | 0.988 | 0.952 | 0.996 | 0.896 | 0.148 | 0.850 | 0.008 | 0.014 |
| positive | corr0.10_missing | 1.000 | 0.994 | 0.996 | 0.378 | 0.986 | 0.748 | 0.998 | 0.596 | 0.036 | 0.446 | 0.016 | 0.018 |
| positive | intermittent_corr0.15 | 0.956 | 0.882 | 0.874 | 0.452 | 0.670 | 0.138 | 0.998 | 0.176 | 0.008 | 0.036 | 0.002 | 0.012 |
| positive | mean0.5 | 0.000 | 0.002 | 0.100 | 0.664 | 0.010 | 0.002 | 0.018 | 0.018 | 0.002 | 0.006 | 0.004 | 0.002 |
| positive | nncorr0.15 | 0.000 | 0.996 | 0.716 | 0.182 | 0.928 | 0.380 | 0.998 | 0.002 | 0.202 | 0.580 | 0.000 | 0.018 |
| positive | var0.5 | 0.034 | 0.994 | 0.018 | 0.996 | 1.000 | 0.982 | 0.000 | 0.994 | 0.996 | 0.996 | 0.022 | 0.008 |
| subgroup | corr0.10_VF_only | 0.460 | 0.280 | 0.382 | 0.018 | 0.312 | 0.094 | 0.678 | 0.044 | 0.010 | 0.054 | 0.014 | 0.014 |
| subgroup | corr0.10_VF_only_pvf0.6 | 0.810 | 0.816 | 0.768 | 0.212 | 0.734 | 0.150 | 0.998 | 0.366 | 0.020 | 0.062 | 0.006 | 0.024 |

Bold = violates the pre-specified admissibility bound (A1-A3).

#### Admissibility

| statistic | selection | holdout |
|---|---|---|
| pshape_hp | FAIL: A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A1:null_artefact, A2:conv_hr2, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct, A4:corr0.10 |
| shape_hp | FAIL: A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A2:conv_hr2, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct, A2:conv_hr2_hrv50_rt0 |
| shape_raw | FAIL: A1:null_artefact, A2:conv_hr2, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A2:conv_hr2, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A2:conv_hr2_hrv50_rt0 |
| td3 | FAIL: A1:null_wander, A1:null_gain_drift, A2:conv_hr2, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A1:null_nn_artefact, A1:null_gain_drift, A2:conv_hr2, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct, A2:conv_hr2_hrv50_rt0 |
| dG_hp | FAIL: A1:null_gain_drift, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A1:null_gain_drift, A2:conv_hr2, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct, A2:conv_hr2_hrv50_rt0 |
| corrFrob_hp | FAIL: A1:null_artefact, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct |
| meanabsr_hp | FAIL: A1:null_homogeneous, A1:null_nn_artefact, A1:null_wander, A3:gaps_near_onset | FAIL: A1:null_artefact, A3:gaps_near_onset, A2:conv_hr2_hrv50_rt0 |
| logdet_hp | FAIL: A1:null_gain_drift, A2:conv_hr2, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A1:null_gain_drift, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct, A2:conv_hr2_hrv50_rt0 |
| diagAIRM_hp | FAIL: A1:null_gain_drift, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A1:null_wander, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct, A3:gaps_near_onset, A2:conv_hr2_hrv50_rt0 |
| covFrob_hp | FAIL: A1:null_gain_drift, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct | FAIL: A1:null_artefact, A1:null_gain_drift, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:artefact_onset_70pct, A3:gaps_near_onset, A2:conv_hr2_hrv50_rt0 |
| conv_hr | FAIL: A1:null, A1:null_missing, A2:conv_hr2, A2:conv_hr2_hrv50_rt0.6, A3:gaps_near_onset | FAIL: A1:null_homogeneous, A1:null_wander, A2:conv_hr2, A2:conv_hr2_hrv50_rt0.6, A2:conv_hr2_hrv50_rt0 |
| conv_sdnn | FAIL: A1:null_wander, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:gaps_near_onset | FAIL: A1:null_artefact, A1:null_nn_artefact, A2:conv_hrv50, A2:conv_hr2_hrv50_rt0.6, A3:gaps_near_onset, A1:null_slow_dynamics, A2:conv_hr2_hrv50_rt0 |

#### Coverage of the 95% t-interval, n = 40 (B5, B10, B15, B30)

| statistic | sel. null | sel. corr0.10 | hold. null | hold. corr0.10 |
|---|---|---|---|---|
| pshape_hp | 0.943 / 0.945 / 0.944 / 0.948 | 0.940 / 0.938 / 0.939 / 0.950 | 0.946 / 0.947 / 0.951 / 0.953 | 0.925 / 0.936 / 0.934 / 0.952 |
| shape_hp | 0.951 / 0.961 / 0.954 / 0.958 | 0.947 / 0.956 / 0.945 / 0.946 | 0.952 / 0.953 / 0.952 / 0.950 | 0.946 / 0.950 / 0.952 / 0.957 |
| shape_raw | 0.949 / 0.936 / 0.952 / 0.945 | 0.953 / 0.942 / 0.959 / 0.942 | 0.951 / 0.955 / 0.939 / 0.949 | 0.937 / 0.931 / 0.942 / 0.932 |
| td3 | 0.946 / 0.944 / 0.957 / 0.935 | 0.950 / 0.940 / 0.943 / 0.952 | 0.953 / 0.959 / 0.940 / 0.958 | 0.947 / 0.957 / 0.952 / 0.940 |
| dG_hp | 0.958 / 0.960 / 0.952 / 0.953 | 0.942 / 0.944 / 0.945 / 0.948 | 0.951 / 0.958 / 0.954 / 0.938 | 0.946 / 0.947 / 0.953 / 0.954 |
| corrFrob_hp | 0.945 / 0.943 / 0.949 / 0.944 | 0.937 / 0.945 / 0.952 / 0.952 | 0.943 / 0.954 / 0.950 / 0.953 | 0.949 / 0.953 / 0.951 / 0.946 |
| meanabsr_hp | 0.945 / 0.932 / 0.937 / 0.949 | 0.947 / 0.954 / 0.948 / 0.948 | 0.952 / 0.948 / 0.943 / 0.942 | 0.943 / 0.948 / 0.949 / 0.947 |
| logdet_hp | 0.933 / 0.945 / 0.950 / 0.953 | 0.937 / 0.945 / 0.950 / 0.944 | 0.957 / 0.946 / 0.964 / 0.947 | 0.942 / 0.954 / 0.966 / 0.946 |
| diagAIRM_hp | 0.953 / 0.954 / 0.947 / 0.957 | 0.950 / 0.949 / 0.952 / 0.953 | 0.954 / 0.946 / 0.951 / 0.958 | 0.939 / 0.946 / 0.951 / 0.949 |
| covFrob_hp | 0.955 / 0.945 / 0.961 / 0.961 | 0.937 / 0.958 / 0.958 / 0.946 | 0.959 / 0.948 / 0.954 / 0.961 | 0.954 / 0.946 / 0.954 / 0.957 |
| conv_hr | 0.943 / 0.948 / 0.944 / 0.959 | 0.960 / 0.946 / 0.946 / 0.955 | 0.935 / 0.953 / 0.950 / 0.949 | 0.947 / 0.932 / 0.944 / 0.948 |
| conv_sdnn | 0.948 / 0.949 / 0.954 / 0.952 | 0.956 / 0.949 / 0.955 / 0.944 | 0.949 / 0.947 / 0.945 / 0.951 | 0.949 / 0.946 / 0.950 / 0.950 |

### 5.1 Per-patient mean s for the repaired candidate (`pshape_hp`; pool SE ≈ 0.013–0.015 per bin)

| Scenario | Selection (B5/B10/B15/B30) | Holdout |
|---|---|---|
| null | +0.017 / +0.002 / +0.001 / +0.007 | +0.005 / −0.001 / +0.002 / −0.005 |
| null_artefact | +0.005 / +0.003 / +0.016 / +0.020 | +0.029 / +0.035 / +0.031 / +0.013 |
| conv_hr2 | +0.015 / +0.008 / −0.002 / +0.006 | +0.023 / +0.031 / +0.035 / +0.031 |
| conv_hr2_hrv50_rt0.6 | +0.009 / +0.018 / +0.019 / +0.014 | +0.012 / +0.020 / +0.019 / +0.020 |
| artefact_onset_70pct | **+0.364 / +0.355 / +0.341 / +0.273** | **+0.367 / +0.349 / +0.324 / +0.257** |
| corr0.05 | +0.079 / +0.067 / +0.052 / +0.020 | +0.101 / +0.094 / +0.081 / +0.044 |
| corr0.10 | +0.297 / +0.292 / +0.274 / +0.154 | +0.312 / +0.293 / +0.273 / +0.144 |
| nncorr0.15 (holdout only) | — | −0.018 / −0.009 / −0.006 / −0.010 |
| corr0.10_VF_only (30% VF) | +0.052 / +0.052 / +0.042 / +0.008 | +0.109 / +0.107 / +0.093 / +0.051 |

The per-patient SD of s under the null is about 0.28 (SE 0.014 × √400).

### 5.2 VT/VF subgroup reporting

The subgroup report (VT and VF estimates, heterogeneity z-test,
"driven by one class" rule) was computed for every positive study in the
subgroup scenarios:

| Scenario (pshape_hp, n = 80) | any positive | positives flagged "driven by one class" |
|---|---|---|
| corr0.10_VF_only, 30% VF, selection | 0.030 | 100% (15 of 15) |
| corr0.10_VF_only, 30% VF, holdout | 0.460 | 93.9% |
| corr0.10_VF_only_pvf0.6, holdout only | 0.810 | 99.5% |

So when an effect exists in one class only, a pooled positive is almost
always flagged. A pooled "VT/VF" claim would then be blocked, and only the
class-specific result could be reported.

**Untested:** how often the flag fires when **both** classes respond
equally. The heterogeneity component (p < 0.05 in any of 4 bins) alone
implies a false-flag rate on the order of 10–20%. That rate must be
measured, and the rule possibly corrected for 4 bins, **before** any
freeze (§6, F6).

## 6. Failure classification

### Gross failures (unambiguous: rates near 1 or far above the bound)

- **F1. Undetected near-onset artefact mimics structural change.** 40
  noise bursts per hour near onset, with 30% undetected, produce
  positive verdicts in 99.2–100% of studies (EXPLORATORY ≥ 98.6%) for
  `pshape_hp`, `shape_hp`, `dG_hp`,
  `corrFrob_hp`, `logdet_hp`, `diagAIRM_hp` and `covFrob_hp`.
  - Mechanism: any statistic measuring *deviation* from baseline structure
    rises when independent noise is added.
  - `ACQUISITION_EXPLAINED` conditions only on the *detected* artefact
    fraction, so it cannot catch the undetected remainder.
  - `meanabsr_hp` escapes only because simulated artefacts *decorrelate*
    the leads and its test is one-sided. Common-mode real artefacts would
    not be decorrelating.
  - **This is now the primary unresolved methodological failure.**
- **F4. The original combined estimator `td3` is not specific.**
  - Spurious positives in 98.8–99.6% under an HR rise alone and 99.4–100%
    under HRV reduction.
  - 8–28% under gain drift, 12% under baseline wander (selection).
  - Lower power at γ = 0.10 (0.44–0.50) than any detrended correlation
    statistic.
- **F5. Covariance competitors respond to variance and gain.**
  - `covFrob_hp` gives positives in 73–76% under a pure gain drift.
  - `dG_hp`, `logdet_hp`, `diagAIRM_hp` and `covFrob_hp` give positives in
    ≥ 98% under HRV reduction.
  - They also detect a pure variance precursor (var0.5), which is not
    structure-specific.
- **Unrepaired correlation statistics leak under HRV change.**
  `shape_hp`, `shape_raw` and `corrFrob_hp` give positives in 98.6–100%
  under HRV −50%. This confirms that the NN-conditioning in `pshape_hp` is
  needed.

### Marginal failures (ambiguous at this precision)

- **F2. `pshape_hp`:**
  - Conventional-only: selection 0.030 (HR+HRV+RT 0.6); holdout 0.036
    (HR +2 SD), 0.026 (HR+HRV+RT 0.6) and 0.020 (HRV −50%, on the bound).
  - Null artefact (holdout) 0.056.
  - Coverage 0.925 in B5 (holdout corr0.10).
  - Holdout-only HR+HRV without coupling and the slow-dynamics null both
    pass (0.004, 0.000).
  - The same scenarios pass in the other set and in the 1,200-patient
    leakage test (HR +3 SD: 0.005), except strong RT–RR coupling, which
    exceeds or touches 2% in 3 of 4 pools.
- **Precision of the suite itself.** With 400 patients per pool, a pool-mean
  offset of 1–2 SE (0.015–0.03) is inherited by every resampled study.
  Across all 174 null-family cells without a gross failure, the median
  any-positive rate is 0.008, but **12.6% of cells exceed 0.02**.
  A statistic must pass about 13–15 such cells at once. So the conjunction
  rule as specified would reject even a well-calibrated statistic **with
  high probability**.
  - This is a **design flaw of the admissibility criteria**, identified
    after the run.
  - It does **not** rescue any statistic: gross failures F1, F4 and F5 are
    unaffected.
  - The criteria were not changed post hoc. A corrected design must be
    pre-specified before the next run (§7).

### Failures by design (coverage of the hypothesis)

- **F3. `pshape_hp` is blind to HR-coupled structure.**
  - nncorr0.15: 0.000 positives; s ≈ −0.01.
  - var0.5 and mean0.5: 0.000–0.034.
  - Specificity was bought by excluding these precursor types. A genuine
    precursor that changes the coupling between heart rate and
    repolarisation would be reported as NOT_SUPPORTED. This is a scientific
    scope decision, not an error, and must be stated in any protocol.
- **F6.** The false-flag rate of the subgroup rule is untested (§5.2).

### Calibration properties that held

- Coverage was within [0.93, 0.97] in 191 of 192 statistic × scenario × set
  × bin cells; the exception is 0.925.
- `pshape_hp` detected corr0.10 in ≥ 96.6% of n = 80 studies under
  missingness, gain drift and heterogeneity (SD 1.0), and in 74.8–78.2%
  with only half the patients responding.
  - Other statistics lost much of this robustness: `diagAIRM_hp` ≤ 14.8%
    (outside the artefact scenario); `dG_hp` and `logdet_hp` 0% under gain
    drift; `td3` 11–60%.
  - The 70%-detected-artefact positive scenario is not evidence of
    robustness, because of F1.
- Near-onset gaps did not create positives for `pshape_hp` (0.000–0.002).
- Conventional baselines (`conv_hr`, `conv_sdnn`) detect their own
  mechanisms (≥ 99%) and rarely detect correlation precursors (≤ 4.2% at
  corr0.10 and corr0.05; up to 9.6% for the intermittent precursor).
  The TD statistics are therefore not merely re-measuring conventional
  features **in this simulator**.

## 7. Requirements before any further estimator selection

These are proposals, not yet executed:

1. **Artefact identifiability (F1).** Add a signal-quality index computed
   independently of the structure statistic. Add a negative-control
   requirement: the effect must be absent in leads or segments with matched
   noise but no physiological change. Test against undetected-artefact
   rates of 10–50% and common-mode (correlating) noise as well as
   independent noise.
   - If no repair restores A3 while keeping power at corr0.10, the
     **deviation-statistic family should be recorded as non-identifiable
     against undetected near-onset artefact**. That would be an estimator
     failure, not a hypothesis falsification.
2. **Suite precision.** Pre-specify, before the next run:
   - pool ≥ 1,600;
   - the criteria applied to the pooled cell rate with a binomial upper
     bound, or an explicit family-wise allowance across cells;
   - an independent seed base (≥ 3,000,000).
3. Measure the subgroup false-flag rate when both classes respond.
4. **Independent scenario authorship.** Have a reviewer who did not design
   the estimators write a fresh holdout scenario set (different artefact,
   coupling and drift models).

---

© 2026 Davarn Morrison · Transition Dynamics
