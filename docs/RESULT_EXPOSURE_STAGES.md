# Exposure confound — four-stage result

**Conclusion: the mechanism-identification claim survives oracle control and
survives estimated control in the regime tested, with three stated limits and
one structural caveat that bounds how much any of it means.**

---

## Stage 1 — oracle exposure control

Preregistered verdict **UNRESOLVED**, recorded unamended: median within-stratum
AUC 0.939 clears the 0.75 bar, 67% of strata exceed 0.65 against a 70% bar.

108 strata: 6 baseline structures × 6 exposures × 3 severities × 25 seeds,
targeted and untargeted matched within every stratum on true exposure and on
conventional observability.

| | AUC |
|---|:--:|
| Unconditional (exposure not controlled) | 0.783 |
| Within-stratum median | **0.939** |
| Within-stratum median, detectable regime | **0.998** |
| Covariance drift, same strata, detectable regime | 0.746 |

**Controlling exposure improves separation** (0.783 → 0.939). This corrects the
earlier reading. Exposure shifts the absolute level of alignment; it does not
destroy discriminability of targeting at fixed exposure.

All 36 sub-threshold strata are exactly the lowest severity, which sits below
the noise floor of the matching variable itself, where no statistic detects
anything. That observation is post-hoc and does not change the verdict.

---

## Stages 2–3 — independent onset estimation

Model: the existing dynamics, unchanged. Rates from baseline autocorrelation
only; the estimator never sees alignment or the targeting label; onset fitted
on odd-indexed samples, alignment computed on even-indexed samples.

| | |
|---|:--:|
| Median MAE of estimated exposure | **1.2 time units** |
| Median bias | −0.0 |
| Identifiable | 81% of cases |
| Declines on stationary trajectories | 80–95% |
| Baseline rate recovery, channels = eigen-coordinates | 3% error |
| Baseline rate recovery, rotated (geometric mean only) | 28% low |

**Failure mode, mapped.** Small displacement combined with long exposure: the
system has approached equilibrium and the trajectory has lost the curvature
onset is inferred from. The estimator declines in most such runs, which is
required behaviour — but when it does fire there it is wrong by roughly half
the true exposure.

---

## Stage 4 — ran, tested nothing

Returned SURVIVES with no control 0.982, oracle 0.982, estimated 0.988.

The verdict is empty. Both groups were drawn from the same exposure grid, so
their exposure distributions were identical and there was no confound to
remove. Three conditions agreeing to within six thousandths shows that
estimated control does not *hurt*, not that it *rescues*. Retained with the
limitation recorded.

---

## Stage 4b — the confound actually constructed

Exposure deliberately correlated with group, as it plausibly is across
transition classes where an abrupt event is recent and a slow one established.

### Spurious effect — the decisive result

Both groups untargeted, so the correct answer is 0.50.

| | bias from 0.50 |
|---|:--:|
| Naive, no control | **0.119** |
| Oracle true-exposure control | 0.008 |
| **Estimated-exposure control** | **0.008** |

Exposure imbalance alone manufactures an apparent targeting effect. Estimated
control removes it and **matches the oracle to three decimals**, which is the
result this whole exercise was built to obtain.

### Masking did not occur

| scenario | naive | oracle | estimated | masking? |
|---|:--:|:--:|:--:|:--:|
| strong targeting, 1.5 SD | 0.998 | 1.000 | 1.000 | no |
| weak targeting, 0.5 SD | 0.946 | 0.968 | 0.965 | no |

The targeting effect (AUC 0.95–1.00) is much larger than the exposure effect
(AUC 0.62), so exposure **can create a false positive where there is no
targeting but cannot hide genuine targeting**. That asymmetry was not
predicted in advance and is recorded as a finding.

---

## Three limits, stated rather than smoothed over

**1. Differential decline — a selection bias inside the control.** At weak
displacement the estimator declines at different rates by group:

| group | true exposure | identifiable |
|---|:--:|:--:|
| untargeted | recent | 46/46 |
| untargeted | established | **2/14** |
| targeted | recent | 15/15 |
| targeted | established | **13/45** |

The identifiable subset is not a random sample, so any stratified estimate
computed on it is conditioned on a group-dependent filter. This is not
quantified here and is an open problem.

**2. Stratification collapses where support is thin.** In the weak-displacement
scenario only one exposure bin had enough cases in both groups, because the
established-untargeted cell retained 2 identifiable cases. The estimated
control there answers a narrower question — targeting among recent-onset cases
— rather than controlling exposure across the range.

**3. The combination that matters most was never produced.** A regime where
exposure control is genuinely needed *and* the estimator declines often did not
arise in this grid. Where control was needed (spurious, 1.5 SD) the estimator
declined 0% of the time; where it declined often (0.5 SD) no masking existed to
correct.

---

## The structural caveat

**The estimator's model is the simulator's model.** Stages 2–4 validate an
exponential-approach onset estimator against data generated by an
exponential-approach process. Success is therefore close to a consistency
check, not evidence that the estimator works on real dynamics.

Nothing in this sequence tests whether real pre-transition physiological
trajectories are even approximately exponential approaches to a displaced
equilibrium. If they are not, the onset estimates will be wrong in ways these
experiments cannot reveal.

---

## Is real physiological data now justified?

**Yes, but not for the mechanism test.**

The first real-data step should be a **model-adequacy check**: do observed
pre-transition trajectories fit the exponential-approach form at all, with
per-channel rates consistent with baseline autocorrelation? That is a
descriptive question, needs no transition labels, and can be answered on any
multichannel ICU recording.

If the model does not fit, the onset estimator is inapplicable and the
mechanism claim returns to being non-identifiable on real data regardless of
what these synthetic results show. If it does fit, the Stage 4b design
transfers directly, with transition class supplying the exposure imbalance that
had to be constructed here.

Going straight to the mechanism test would assume the model adequacy that has
not been demonstrated.

---

## Bugs found in this sequence

Four, all in the test harness, all producing confident wrong answers. Three
were caught because the result was structurally impossible rather than merely
unwelcome.

| # | Symptom | Cause |
|---|---|---|
| 1 | Stage 1 FALSIFIED, all 108 AUCs inside a 0.008 band | Calibration read max-univariate-z on the deterministic twin, whose baseline SD is zero; force scale collapsed to 4×10⁻¹² |
| 2 | Guard aborted a correct stratum | Guard compared realised severity to a nominal target below the noise floor |
| 3 | Rate recovery reported >100% error | Estimated rates compared against descending-sorted truth while the simulator orders ascending; true error 3% |
| 4 | Masked scenario AUC exactly 0.000 | Naive comparison scored group B as positive, oracle and stratified scored group A |

The checks that caught these were constraints on the *shape* of a result — an
AUC that cannot occur, a variance that cannot be that small, conditions that
cannot be bit-identical — not on its direction. Directional plausibility checks
would have passed all four.

Reproduce: `exposure_stage1_oracle.py`, `onset_estimator.py`,
`stage4_conditional.py`, `stage4b_confounded.py`.

---

© 2026 Davarn Morrison · Transition Dynamics
