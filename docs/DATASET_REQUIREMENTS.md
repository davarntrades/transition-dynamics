<div align="center">

# DATASET REQUIREMENTS

**Resolution Arithmetic · Temporal Value · Base Rates**

![Constraint](https://img.shields.io/badge/Binding_Constraint-n__eff_≥_10p-b91c1c?style=flat-square)
![Primary](https://img.shields.io/badge/Primary-HiRID_~2min-1f2937?style=flat-square)
![Rule](https://img.shields.io/badge/Univariate-Not_Confirmatory-4c1d95?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)

</div>

---

*"The window must span many relaxation times of the slowest channel. Not many samples. Many relaxation times. Those are different requirements and only one of them is satisfied by sampling faster."*

*— Davarn Morrison, 2026*

---

## 1. Why Univariate Data Cannot Be Confirmatory

For a one-dimensional linear system

```
  ẋ = −k x + ξ
```

the restoring stiffness and the recovery rate are the **same parameter k**. The
stationary variance is σ²/2k, so "stiffness" and "resilience" are two names for
one number. **Interpretations M2 and M3 are mathematically degenerate in one
dimension**, and a univariate test confirms whichever was assumed.

They separate only in the multivariate case, because the stationary covariance
depends on **both** the restoring operator and the noise covariance:

```
  Λ_B = Σ₀⁻¹      depends on restoring structure AND noise structure
  Λ_A = I − A     depends on restoring structure only
```

```
════════════════════════════════════════════════════════════════════
  RULE, FIXED IN ADVANCE

  Univariate evidence may NOT be used as confirmatory evidence for
  distinguishing the competing physical interpretations of Λ.

  Univariate analyses are reported as descriptive only.
════════════════════════════════════════════════════════════════════
```

---

## 2. The Resolution Requirement, Derived

A covariance over p channels is estimable from a window only if the window
carries enough **independent** information. Physiological channels are strongly
autocorrelated, so raw sample count is the wrong measure:

```
  n_eff  =  n · (1−ρ) / (1+ρ)          ρ = mean lag-1 autocorrelation

  REQUIREMENT:   n_eff  ≥  10 p
```

### 2.1 This was learned by getting it wrong

The first version of the synthetic benchmark used a fine Euler integrator
without thinning. Consecutive samples were **99.9% autocorrelated**; an
800-sample window carried **n_eff ≈ 4.5** for p = 6. Every downstream statistic
was estimation noise, and the benchmark produced a spurious null result before
the cause was found.

The fix was not more samples. It was **a window spanning many relaxation times
of the slowest channel.** Sampling faster does not help — it adds correlated
samples and leaves n_eff unchanged.

### 2.2 Consequence for real data

| Slowest channel timescale | Required window | Feasible in ICU? |
|---|---|:--:|
| minutes (HR, RR, SpO₂) | ~1 h | yes |
| tens of minutes (MAP under titration) | ~4–8 h | yes |
| hours (temperature, lactate, urine output) | ~24–48 h | marginal |

**Including a slow channel forces a long window, which erodes lead time.** This
is a genuine design tension, not a tuning choice: the channels most strongly
defended homeostatically — and therefore most informative for A(t) — are often
the slowest. It is preregistered that the primary analysis uses a
**fast-channel panel** (HR, RR, SpO₂, MAP, and derived HRV where available)
with slow channels entering a secondary, longer-window analysis.

---

## 3. Dataset Assessment

### 3.1 HiRID — primary

| | |
|---|---|
| Size | ~34,000 ICU admissions, Bern University Hospital |
| Resolution | most vital signs ~**2 minutes** — highest of any public ICU dataset |
| Variables | ~700 |
| Endpoint | established physiology-defined circulatory failure |
| **Verdict** | **Primary cohort.** The only public ICU dataset meeting the n_eff requirement for a fast-channel panel |

### 3.2 MIMIC-IV — external validation, with a resolution caveat

| Hypothesis component | Verdict | Reason |
|---|:--:|---|
| ΔG / detection | marginal | vitals ~hourly and irregular; a 24 h window gives ~24 raw samples, and n_eff far lower |
| Q / persistence | weak | τ quantised to a handful of values |
| ‖ΛΔG‖, A(t) | marginal | Σ₀ estimable only with aggressive shrinkage, which distorts the Σ₀⁻¹ spectrum that A depends on |
| T_critical knee | weak | hourly sampling smears a knee into a gradient |
| β₁ higher-order | poor | insufficient temporal support for third-order co-occurrence |
| Decoupling (exploratory) | **cannot test** | contains clinician notes, not patient self-report |

**MIMIC-IV may be used where its resolution supports the analysis, and not
otherwise.** A null in MIMIC-IV is evidence about sampling rate, not about the
hypothesis, and must be reported in those terms.

### 3.3 Others

| Dataset | Role |
|---|---|
| eICU | second external validation; multi-centre, coarser |
| MIMIC-IV waveform / ECG subsets | resolution sensitivity analysis on a smaller cohort |
| AmsterdamUMCdb | candidate additional validation, high resolution |

```
════════════════════════════════════════════════════════════════════
  VERIFICATION REQUIREMENT

  PhysioNet was not reachable from the environment in which this
  document was written. Every figure above — record counts, sampling
  rates, variable coverage, endpoint definitions — is from secondary
  sources and MUST be re-verified against the authoritative dataset
  landing pages before execution.
════════════════════════════════════════════════════════════════════
```

---

## 4. Temporal Value

Prediction after ordinary clinical criteria already indicate collapse is not
early detection. It is documentation.

### 4.1 Preregistered horizons

| Setting | Horizons | Blanking | Alert definition |
|---|---|---|---|
| ICU (HiRID) | 2 h, 4 h, 8 h | 30 min pre-event excluded | ≥ 3 consecutive positive windows |
| ICU (MIMIC-IV) | 6 h, 12 h | 1 h excluded | ≥ 2 consecutive positive windows |

**The H1 restriction defines the value.** Analysis is restricted to windows
where **every** channel lies inside both its population reference range and its
person-specific baseline range. Within that restricted set — where conventional
monitoring says "normal" — the question is whether the structural quantities
discriminate. An alert firing after a marginal has already left range has
demonstrated nothing.

### 4.2 Metrics, all required

```
  discrimination      AUPRC (headline), AUROC (comparability only)
  calibration         intercept, slope, integrated calibration index
  sensitivity, specificity, PPV, NPV   at the true prevalence
  false alarms        per patient and per patient-day
  lead time           first sustained alert to event, with CI
  net benefit         decision-curve analysis
  uncertainty         cluster bootstrap BY PATIENT, 2,000 replicates
```

Bootstrapping by window would treat within-patient windows as independent and
produce intervals far too narrow.

---

## 5. Base Rates

Full arithmetic: [`../analysis/results/base_rate_tables.md`](../analysis/results/base_rate_tables.md).
Reproduce with `python3 analysis/base_rates.py`.

At sensitivity 0.80, specificity 0.95:

| Setting | prevalence | PPV | alerts per true event | false alerts/patient |
|---|:--:|:--:|:--:|:--:|
| ICU circulatory failure | 0.030 | 0.331 | 3.0 | 1.75 |
| ICU sepsis onset | 0.010 | 0.139 | 7.2 | 3.56 |
| Ward deterioration | 0.004 | 0.060 | 16.6 | 1.39 |

Specificity required for PPV ≥ 0.33 at sensitivity 0.80:

```
  ICU circulatory failure   0.9498
  ICU sepsis onset          0.9836
  Ward deterioration        0.9935
════════════════════════════════════════════════════════════════════
  Every setting except event-rich ICU circulatory failure demands
  specificity of 0.98 or higher. No published early-warning system
  in these domains achieves it.
════════════════════════════════════════════════════════════════════
```

**Reference floor.** The Epic Sepsis Model, deployed at hundreds of hospitals:
sensitivity 0.33, specificity 0.83, AUROC 0.63, PPV 0.12 on 38,455
hospitalisations, alerting on 18% of all admissions.

**A high AUROC with unusable PPV or alarm burden is not evidence of clinical
utility and may not be described as such.** See
[`CLAIM_LADDER.md`](CLAIM_LADDER.md) Level 6.

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   n_eff ≥ 10p, or the covariance is noise and everything             ║
║   downstream is a story about noise.                                 ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Dataset Requirements*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) · [`HYPOTHESIS.md`](HYPOTHESIS.md) · [`TRANSITION_TAXONOMY.md`](TRANSITION_TAXONOMY.md) · [`LIMITATIONS.md`](LIMITATIONS.md)
