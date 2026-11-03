# VT/VF programme — protocol repair plan (causes, corrected logic, synthetic falsification tests)

> **Status: DESIGN RECORD. Synthetic only. No protocol frozen. No real
> VT/VF hypothesis test run.** Every number below comes from the beat-level
> synthetic calibration:
>
> - code: [`analysis/vtvf/beatsim.py`](../analysis/vtvf/beatsim.py),
>   [`analysis/vtvf/repaired_rule.py`](../analysis/vtvf/repaired_rule.py),
>   [`analysis/vtvf/calibrate.py`](../analysis/vtvf/calibrate.py)
> - results: [`analysis/results/vtvf_repair_calibration.json`](../analysis/results/vtvf_repair_calibration.json)
>   (run 2), and run 1 kept as a record in
>   [`vtvf_repair_calibration_run1.json`](../analysis/results/vtvf_repair_calibration_run1.json)
>
> Results are properties of the repaired statistical machinery under stated
> generative assumptions. **They are not evidence about VT/VF physiology.**

---

## 1. Root causes of the v2 failures

| # | v2 failure | Mathematical / implementation cause | Repair | Demonstrated in synthetic test |
|:--:|---|---|---|---|
| 1 | ACQUISITION-EXPLAINED fired on 88% of null studies | (a) **Vacuous quantifier**: "fails in every bin that would otherwise pass" is true when that set is empty. (b) **Ratio estimator** R = (AUROC(M0)−0.5)/(AUROC(M3)−0.5): the denominator is ≈ 0 and changes sign under H0, giving a Cauchy-like, unbounded ratio | Gates are evaluated **only on bins that pass the primary test**. **ACQUISITION_EXPLAINED requires two affirmative findings**: the pure-acquisition feature is itself significantly associated (one-sided α = 0.05), **and** the TD effect loses primary significance after conditioning on it. No ratios | null: ACQUISITION_EXPLAINED **0.0%** at every n (td3 and shape) |
| 2 | Pipeline band rejected 98% of valid pipelines | A **fixed band** (mean AUROC 0.45–0.55) is narrower than the null sampling SD of a ~20-patient cohort mean (0.06–0.09). It was never calibrated | **Negative control = within-patient label permutation**, null by construction even under drift, tested two-sided at α = 0.001/4 per bin. **Positive control = injected known effect**, whose power is designed a priori (§3) | null: PIPELINE_INVALID **0.1–1.2%**. A broken pipeline (labels shifted 75 min) gives PIPELINE_INVALID **93–97%** |
| 3 | Pseudo-onset control passed 15–30% of null studies | The null was built by resampling *which* offset each subject contributes (1–2 offsets per subject). That ignores the sampling variance of the observed mean | **Paired per-patient test**, $d_i = s_i^{\text{true}} - \overline{s_i^{\text{pseudo}}}$, as a one-sided t-test across patients. Plus an **affirmative drift test**: DRIFT_EXPLAINED requires the pseudo-onsets themselves to show the effect. Otherwise the result is UNRESOLVED | null: DRIFT_EXPLAINED ≤ 0.9%. Elapsed-time gain drift: td3 → DRIFT_EXPLAINED **98–99%** |
| 4 | Confidence intervals too narrow (coverage 84–92%) | **Leave-one-patient-out (LOPO) dependence**: fold models share n−2 of n−1 training patients, so per-patient Δᵢ are positively correlated | The primary per-patient statistic uses **no cross-patient training**: a within-patient residual AUROC (§2). Statistics are then independent across patients, and patient-level t-intervals are valid | 95% coverage **0.922–0.955** (mean 0.945), across bins, n ∈ {16, 40}, null and positive scenarios |
| 5 | The simulation did not represent the TD estimators | v2 simulated linear 5-min mean shifts, not S / ΔG / TD-3 on 256-beat windows | **Beat-level generator** with the actual estimators. Ledoit–Wolf and AIRM match `analysis/estimators.py` to ~1e-15 | `beatsim.py`. Equality check in the calibration log |
| 6 | Signal-quality masking removed 88% of windows | Threshold **relative** to a 30-min baseline (99th percentile) on slowly wandering features | **Absolute, physically defined** criteria (flagged-beat fraction > 0.20), plus **beat-level exclusion**: covariance windows use the last 256 *unflagged* beats | null: masked fraction **0%** of remote windows. With a heavy near-onset artefact, B5 is 36% masked (reported, not hidden) |
| 7 | Insufficient power | Structural: few independent patients, ≈ 1 effective observation per patient per bin | Not repairable by design. Quantified in [`VT_VF_STATISTICAL_FEASIBILITY.md`](VT_VF_STATISTICAL_FEASIBILITY.md) | — |
| 8 | Artefact and circadian confounding unresolved | Onset-locked artefacts are indistinguishable from precursors by timing. Clock-locked effects need clock time | **Beat-level artefact exclusion**, plus a **correlation-only primary statistic** (§2.2). Circadian: clock-time matching where timestamps exist; otherwise a declared limitation | 70%-detected artefact: shape statistic false positives ≈ 0 (td3: 22% EXPLORATORY + 67% TRIGGER-PROXIMAL at n = 150) |

---

## 2. The repaired primary statistic

### 2.1 Definition (operationalisation layer; not source mathematics)

For patient *i* and lead bin *b*:

1. Compute the windowed TD statistic $c(t)$ (§2.2) and the five conventional
   features M1(t): mean NN, SDNN, RMSSD, mean RTa, SD RTa. Each is
   standardised against that patient's baseline (median / MAD).
2. Regress $c$ on a **nonlinear** M1 basis (M1, M1², |ΔM1|), fitted on
   **that patient's remote windows only**, which are outcome-free. Remote
   residuals are blocked-cross-fitted in time (5 blocks). Bin windows use the
   full fit.
3. $s_{i,b} = \mathrm{AUROC}(\text{residual on bin-}b\text{ windows},\ \text{residual on remote windows}) - 0.5$.

This is "information beyond conventional features" made patient-specific
and free of training leakage. The cross-patient M1-vs-M4 LOPO model becomes
a **secondary, descriptive** analysis, reported with a refitting patient
bootstrap if it is used at all.

### 2.2 Which TD statistic is primary: a research decision (D-VT1), with a recommendation

| Statistic | Layer | Null | Conventional-only precursor (n = 150) | 70%-detected artefact (n = 150) | Elapsed-time gain drift | Real effect + drift | Power, γ = 0.10, n = 40 / 80 |
|---|---|---|---|---|---|---|---|
| **td3**: mean of S, ΔG (AIRM), TD-3 | protocol v2 TD block | ✓ | EXPL 4.4%, plus SINGLE 4.1%, TRIG 4.1% | **✗ EXPL 22%, TRIG 67%** | DRIFT_EXPLAINED 98–99% (correct) | **✗ DRIFT_EXPLAINED 99%: real effect suppressed** | 0.75 / 0.99 |
| **shape**: correlation-only AIRM + its persistence | C-b comparator in v2 | ✓ | EXPL 2.8%, plus SINGLE 5.0%, TRIG 5.3% | ✓ ≈ 0 | ✓ NOT SUPPORTED | ✓ EXPL 0.90 / 1.00 | 0.63 / 0.96 |

**Recommendation: the correlation-structure deformation ("shape") is the
primary TD statistic, and td3 is secondary.**

- **Why.** S and the scale part of ΔG respond to *marginal* change (means,
  variances, gain). Marginal change is what conventional features, drift
  and artefact also produce. The correlation-only component is the part of
  ΔG that is specifically *multivariate structure*. It is also the only
  candidate that survived every adversarial scenario simulated.
- **Cost.** About 12 points of power at γ = 0.10, n = 40.
- **Transparency.** This choice was informed by **synthetic** adversarial
  scenarios, not by real outcome data. Both statistics pass the null
  equally. It does not revive or rename any demoted object. ΔG remains an
  operationalisation; no stiffness or Λ reading is attached.

### 2.3 Known residual weaknesses (demonstrated, not hidden)

| # | Weakness | Evidence |
|:--:|---|---|
| W1 | **Conventional-feature leakage is reduced, not removed.** A heart-rate-only precursor (1 SD) leaves +0.03 to +0.05 residual TD signal. Spurious positive verdicts reach ≈ 13% (shape) and ≈ 13% (td3) at n = 150; EXPLORATORY alone ≈ 3–4% | `per_patient.conventional_only`; `verdicts *|n150|conventional_only` |
| W2 | **Mild label leakage (+0.3 SD on bin windows) is not caught** by within-study controls (EXPLORATORY ≈ 0.5–2%, but DRIFT_EXPLAINED rises to ≈ 11% at n = 150). Leakage must be excluded by **code guards and synthetic end-to-end validation**, not by on-data controls | `label_leak_null` |
| W3 | **Baseline-proximity bias.** Pseudo-onsets show s ≈ +0.03 to +0.04 under the null, because windows near the baseline are more similar to it. This makes the paired temporal test slightly conservative | `per_patient.null.pseudo_s_mean` |
| W4 | **Trigger-weighted precursors are essentially undetectable.** γ = 0.05 ramp: EXPLORATORY ≤ 0.8% at every n | `td_gamma0.05_ramp` |
| W5 | **Circadian / clock-locked confounding is not simulated or repaired.** It needs clock time | — |

---

## 3. Corrected decision logic (exhaustive, ordered)

```
0. Pre-execution (not on outcome data): synthetic end-to-end validation suite
   must pass. Null FP <= alpha, injected effects detected, leakage canaries,
   code assertions (feature code has no onset argument).
1. PIPELINE_INVALID  iff (label-permutation control significant, two-sided
   alpha 0.001/4 per bin)  OR  (injected positive control: mean s over B10/B15
   of 8 injected patients <= floor).
2. Per bin: primary = one-sided t (alpha 0.00625) AND one-sided sign test
   (alpha 0.00625) on s_i,b.
3. No bin passes primary -> NOT_SUPPORTED  (+ LARGE_EXCLUDED flag).
4. For each passing bin:
     temporal:    paired d_i test (alpha 0.05) PASS
                  | else pseudo-onset association significant -> DRIFT_AFFIRMED
                  | else INCONCLUSIVE (fewer than 8 subjects with pseudo-onsets: NON_EVALUABLE)
     acquisition: (acq association significant AND conditional s not significant)
                  -> ACQ_AFFIRMED, else PASS
5. No passing bin survives both controls ->
     ACQUISITION_EXPLAINED if any ACQ_AFFIRMED, else DRIFT_EXPLAINED if any
     DRIFT_AFFIRMED, else UNRESOLVED.
6. HARM (interval below 0 in >= 2 bins) overrides any positive verdict.
7. Surviving bins: >= 2 incl. B15/B30 -> EXPLORATORY_ASSOCIATION;
                   one of B15/B30 only -> SINGLE_BIN_LONG_LEAD;
                   B5/B10 only         -> TRIGGER_PROXIMAL.
```

**Pipeline positive-control power, designed a priori.**

- Run 1 used γ_pc = 0.10, a floor of 0.13 and 8 injected patients. Its false
  PIPELINE_INVALID rate under a correct pipeline was **11–20%**, the same
  class of defect as v2's band.
- Required false-fail rate ≤ 1% means $0.5\,\mu\sqrt{k}/\sigma \ge 2.33$.
- Run 2 uses γ_pc = 0.30 and a floor of 0.20, fixed **before** run 2 from
  the pilot's E[s | 0.30] ≈ 0.41 and SD ≈ 0.20. Observed false-fail is
  **0.1–1.2%**.
- **No α level was changed between runs.**

## 4. Synthetic falsification tests: required outcomes and results

Run 2; shape statistic unless stated; 1,000 resampled studies per cell;
pools of 600 synthetic patients per scenario.

| Test | Requirement | Result (n = 16 / 40 / 80 / 150) | Status |
|---|---|---|:--:|
| Null → no-effect or unresolved | NOT_SUPPORTED + UNRESOLVED ≥ 95% | 99.3 / 99.2 / 98.4 / 97.6% | ✓ |
| Null false EXPLORATORY | ≤ 0.5% | 0.0 / 0.1 / 0.1 / 0.0% | ✓ |
| ACQUISITION_EXPLAINED needs affirmative evidence | null → 0 | 0 / 0 / 0 / 0 | ✓ |
| PIPELINE_INVALID only on actual failure | null ≤ 2%; broken ≥ 90% | null 0.3 / 0.1 / 0.6 / 1.2%; broken 97 / 97 / 97 / 97% | ✓ |
| Positive control detectable (γ = 0.10) | rises with n | EXPLORATORY 13 / 63 / 96 / 99.5% | ✓ |
| Calibrated false-positive rate | per-bin primary pass under null ≈ α (0.625%) | 0.0–0.7% per bin across n (Monte Carlo SE ≈ 0.25 points) | ✓ |
| CIs account for clustering and training dependence | coverage ≈ 0.95 | 0.922–0.955 | ✓ |
| Drift identified affirmatively (td3) | DRIFT_EXPLAINED, not EXPLORATORY | 98–99% DRIFT; EXPLORATORY ≤ 0.7% | ✓ |
| Real effect not suppressed by drift (shape) | EXPLORATORY rises with n | 34 / 90 / 99.8 / 99.3% | ✓ |
| Conventional-only precursor not claimed as TD | EXPLORATORY ≤ α | 0.2 / 0.1 / 0.9 / **2.8%** | **✗ residual (W1)** |
| Undetected artefact not claimed (shape) | ≈ 0 | ≤ 0.1% | ✓ |

## 5. Remaining repairs needed before any freeze

| # | Severity | Repair |
|:--:|:--:|---|
| RP1 | **CRITICAL** | **Dataset.** No verified dataset supports the test (see the landscape and feasibility documents) |
| RP2 | MAJOR | **Close the conventional leakage (W1).** Options: a richer conventional basis, including HR-straddling-window indicators; attribution via the channel-shuffle and comparator contrasts; or a pre-specified leakage bound below which TD-specific wording is disallowed. **Must be re-calibrated, not assumed** |
| RP3 | MAJOR | **Real-data pipeline.** Own beat detector and classifier validated against an audited reference outside the sealed zone; beat-level artefact flags with **measured** detection sensitivity (the 70% scenario is the motivating case) |
| RP4 | MAJOR | **Clock time.** Required, or circadian confounding is declared unresolved (D6) |
| RP5 | MODERATE | **Decorrelation gap.** Baseline-proximity bias (W3): start the remote zone ≥ 60 min after the baseline, re-simulated for the chosen dataset |
| RP6 | MODERATE | **Leakage canaries (W2)** in the synthetic end-to-end suite, with a pass criterion |
| RP7 | MODERATE | **Subgroup machinery for pooled endpoint C** (VT vs VF heterogeneity test; see the endpoint assessment) |

---

© 2026 Davarn Morrison · Transition Dynamics
