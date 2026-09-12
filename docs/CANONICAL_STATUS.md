# Canonical status

The authoritative record of what this programme has and has not established.
Where any other document disagrees with this one, this one governs.

Phase closed: **synthetic exposure and onset control (Stages 1–4).**
Nothing in this programme has been tested on human physiology.

---

## 1. Established in the simulator

| # | Claim | Evidence |
|---|---|---|
| S1 | Alignment separates targeted from untargeted displacement **under true exposure control** | Within-stratum AUC median 0.939 over 108 strata; 0.998 in the detectable regime |
| S2 | **Controlling exposure improved discrimination rather than destroying it** | Unconditional 0.783 → within-stratum 0.939 |
| S3 | Alignment beats the established comparator under identical control | Covariance drift 0.746 vs alignment 0.998, detectable regime |
| S4 | Onset is **independently recoverable** over much of the simulated parameter space | Median absolute error 1.2 time units; identifiable in 81% of cases; rates from baseline only |
| S5 | The estimator declines on stationary trajectories, as required | 80–95% declined |
| S6 | **Estimated** exposure control removes a deliberately manufactured spurious targeting effect | Naive bias 0.119 → 0.008, matching oracle control to three decimals |
| S7 | Exposure imbalance can create a false positive but **cannot mask** genuine targeting | Targeting effect AUC 0.95–1.00 vs exposure effect 0.62. Not predicted in advance |

---

## 2. Known limits of the above

| # | Limit |
|---|---|
| L1 | **Non-identifiable regime**: low displacement combined with long exposure. Near equilibrium the trajectory has lost the curvature onset is inferred from. The estimator mostly declines there, and when it does fire it errs by roughly half the true exposure |
| L2 | **Differential decline — UNRESOLVED.** The estimator declines at group-dependent rates (2/14 identifiable for untargeted-established vs 13/45 for targeted-established), so the identifiable subset is not a random sample and stratified estimates are conditioned on a group-dependent filter. Not quantified |
| L3 | **Thin support.** Where decline is frequent, stratification collapses to a single bin and answers a narrower question rather than controlling exposure across the range |
| L4 | **The combination that matters most never arose.** No regime in the grid required exposure control *and* had frequent decline |
| L5 | **Detection floor.** Below roughly 0.2 baseline SD of displacement nothing separates, for any statistic including covariance drift |

---

## 3. The structural caveat that bounds Stages 2–4

> The onset estimator assumes displacement of the form
> $\delta_i(t) = b_i(1-e^{-k_i(t-t_0)})$, and it was tested on data generated
> by exactly that family.
>
> **Stages 2–4 are therefore primarily an internal consistency and
> identifiability result, not evidence that human physiology follows that
> model.**

Nothing in this programme tests whether real pre-transition trajectories take
that form. If they do not, the onset estimates will be wrong in ways these
experiments cannot reveal, and the mechanism claim returns to being
non-identifiable on real data regardless of the synthetic results.

---

## 4. Preregistered verdicts, recorded as issued

| Stage | Verdict | Held |
|---|---|---|
| Homeostatic premise (instrument test) | **B — unresolved** | The script printed A; overridden because the automated check computed the exposure comparison in the wrong regime |
| Stage 1 oracle control | **UNRESOLVED** | Median 0.939 clears the 0.75 bar; 67% of strata exceed 0.65 against a 70% bar |

**The Stage 1 verdict stands at UNRESOLVED.** All 36 sub-threshold strata are
exactly the lowest severity, which lies below the noise floor of the matching
variable itself. A rule written after seeing that structure would have excluded
those strata and returned SURVIVES. That rule was not preregistered and is
**not** adopted retrospectively.

---

## 5. Withdrawn and demoted claims

| Claim | Status | Reason |
|---|---|---|
| "Exposure duration destroys targeting discriminability" | **WITHDRAWN** | Stage 1: controlling exposure *improves* separation. Exposure shifts alignment's absolute level, not its discriminative content |
| Per-class alignment sign predictions (positive in sepsis/respiratory, null in abrupt) | **WITHDRAWN, remain withdrawn** | Confounded by insult kinetics, and the kinetic ordering is inverted relative to the prediction |
| "Stiffness predicts falling pre-transition variance" | **WITHDRAWN** | Does not follow from a baseline-frozen operator, which is a fixed metric rather than a state variable |
| "Transition Dynamics competes with critical slowing down; one must lose" | **WITHDRAWN** | They are complementary; each detects the mechanism the other misses |
| "The contribution is detection" | **NARROWED** | Covariance drift already detects at least as well |
| Homological truth condition | **DEMOTED** | Not operationalised; reachable set not observable from one trajectory |
| Literal orthogonality law | **DEMOTED** | Universal zero-effect claim, already refuted |
| Stage 4 as a test of the confound | **VOID** | Both groups drawn from the same exposure grid, so no confound existed to remove. Retained with the limitation recorded |

---

## 6. The mechanism claim

**Status: identifiable in principle, operationally identifiable in the
simulated regime tested, and NOT validated in real physiology.**

It may not be described as validated, as clinically useful, or as a
demonstrated property of human deterioration. The next step is a model-adequacy
study, not a mechanism or prediction study.

---

## 7. Harness bugs in this programme

Seven in total across the whole programme; four in the exposure sequence. All
produced confident wrong answers.

| # | Symptom | Cause | Guard added |
|---|---|---|---|
| 1 | Instrument test reported falsification at AUC 0.52 | Force onset placed relative to the series end while displacement was measured over the pre-transition window; signal diluted ~40× | Deterministic-twin calibration |
| 2 | Same run: conditions identical | Target displacement set below the sampling noise floor, so calibration could not converge | Target set as a multiple of the computed noise floor |
| 3 | Long exposures contaminated the baseline | Force onset fell inside the baseline window | Simulator raises rather than proceeding |
| 4 | Stage 1 reported FALSIFIED, all 108 AUCs inside a 0.008 band | Calibration read max-univariate-z on the deterministic twin, whose baseline SD is exactly zero; force scale collapsed to 4×10⁻¹² | Analytic stationary SD; per-stratum assertion that conditions differ and are equally observable |
| 5 | Guard aborted a correct stratum | Guard compared realised severity to a nominal target lying below the noise floor | Guard now checks cross-condition agreement, which is the assumption the analysis rests on |
| 6 | Rate recovery reported >100% error | Estimated rates compared against descending-sorted truth while the simulator orders ascending | Corrected; true per-channel error 3% |
| 7 | Masked scenario returned AUC exactly 0.000 | Naive comparison scored group B as positive while oracle and stratified scored group A | Orientation unified |
| 8 | Onset estimator never declined, including on stationary data | Interleaved cross-fitting does not control overfitting at lag-1 autocorrelation 0.76 | Null-calibrated threshold from stationary trajectories; declines 80–95% |
| 9 | Stage C appeared to validate the onset model | Baseline rates recomputed from the first half of the very segment being tested — circular | `k_base` made a required argument |
| 10 | Stage C correlations undefined | Rate grid capped at 1/h while real rates are ~1000/h, so every fit pinned to the boundary; and rates faster than the sampling interval are unidentifiable | Grid spans 10⁻²–10⁴; baseline estimated at matched resolution; identifiability band enforced |
| 12 | Channel-shuffle control returned numbers bit-identical to the uncontrolled arm | The control permuted feature **columns** globally, which is a no-op for a ridge model — reordering columns leaves the fit identical | Permute channel assignment **independently per row**, preserving each row's multiset of values while destroying channel identity |
| 11 | Every fitted model sat at AUROC 0.48–0.52 while unfitted raw scores reached 0.60–0.63 | Out-of-fold **probabilities** pooled across folds. One fold had test prevalence 0.014 against 0.129 in training, so its intercept and standardisation placed its predictions on a different scale and the pooled ranking inverted — despite every fold ranking correctly on its own | Discrimination, false-alert rate and lead time use within-fold rank-normalised scores; calibration keeps untransformed probabilities. Regression test: a single-feature model must reproduce its own feature's AUROC |

**Why they were dangerous.** Each produced a confident, plausible-looking
answer. Bugs 1, 4, 7 and 11 produced *falsifications* — the flattering
direction would have been to accept them, since a null result looks rigorous.
Bugs 8 and 9 pointed the other way and would have produced a false positive.

**What caught them.** Constraints on the *shape* of a result, not its
direction: an AUC that cannot occur, a variance too small to be real,
conditions bit-identical to machine precision, a single-feature model whose
AUROC is neither its feature's nor its complement. Directional plausibility
checks would have passed all eleven.

---

## 8. Discarded runs

Retained as record, not as evidence. Result files from runs 1, 4 and 7 above
were deleted rather than kept, because each contained values that cannot occur.
The reasoning that produced and then rejected them is preserved in the result
documents and in the commit history.

---

## 9. Real-data transfer — attempted, blocked by resolution

Two real datasets were obtained through legitimate open channels and both were
rejected by the frozen Stage A rules. **Stage B and Stage C have never been
run on real data.**

| Dataset | Admissible |
|---|:--:|
| MIMIC-III demo, 11 ICU stays, up to 367 h | **0 / 11** |
| NeuroKit human ECG/RSP/EDA, 100 Hz | **0 / 2** |

At hourly charting resolution the effective-sample-size rule and the
stationarity screen are **jointly unsatisfiable**: 0 of 55 stay × baseline-window
combinations satisfied both. Short baselines fail on sample size; baselines long
enough to pass are no longer stationary because real ICU patients drift.

**This does not falsify the exponential-approach model.** It establishes that
hourly-charted ICU databases cannot supply the data the test needs. The model
remains untested on real physiology, and no mechanism or early-detection claim
may proceed. See [`REAL_DATA_ACQUISITION.md`](REAL_DATA_ACQUISITION.md).

The 0.5 SD stationarity screen rejected 100% of real ICU baselines. That may
mean the screen is too strict rather than the data unusable, but it is **not
changed**, because altering a preregistered threshold after seeing the result
is the move this programme forbids.

---

## 10. Real-physiology transfer — NOT SUPPORTED (2026-09-11)

First valid real-data test. VitalDB, CC-BY 4.0, 2-second sampling, **56
admissible recordings** against a required 50 — a scientific determination,
not an admissibility failure.

| gate | required | observed | |
|---|:--:|:--:|:--:|
| advantage over surrogates | CI excludes 0 | +7% [−6%, +19%] | **FAIL** |
| baseline-rate vs curvature correlation | ≥ 0.50 | **0.00** [−0.15, 0.15] | **FAIL** |
| M-exp selection rate | ≥ 60% | 62% | pass |
| M-exp beats free-rate variant | > 50% | 89% | pass |

The exponential form contributes nothing: baseline rates imply sub-minute
relaxation, so over multi-hour segments the model is fully saturated in 100% of
cases and differs from an explicit step by 0.28% in held-out error, with the
step winning 57% of the time.

Baseline autocorrelation measures fast fluctuation decay (~1 min); trajectory
curvature reflects slow regulation (~107 min). No baseline resolution bridges
them. **The onset estimator is not transferable to real physiology as
specified**, and no mechanism or early-detection claim may proceed on its
basis. See [`RESULT_VITALDB_ADEQUACY.md`](RESULT_VITALDB_ADEQUACY.md).

---

## 11. Short-timescale transfer — NOT SUPPORTED (2026-09-11)

Baseline relaxation does not predict response relaxation even on compatible,
identifiable timescales. Fresh subjects, disjoint from all prior work.

| band | subjects | within-channel ρ | CI | surrogate |
|:--:|:--:|:--:|:--:|:--:|
| seconds | 112 | +0.043 | [−0.09, +0.18] | +0.000 |
| tens of seconds | 83 | −0.006 | [−0.22, +0.21] | +0.004 |
| short minutes | 11 | — | — | **UNRESOLVED** |

Channel identity alone predicts **+0.266**, six times better than a subject's
own baseline. Range restriction rejected (predictor CV 0.56–1.00); reliability
ceiling is 0.593, above the 0.30 threshold, so the test was capable of
detecting the effect. Disattenuated estimate +0.073 [−0.15, +0.30].

**Consequence: the stiffness interpretation of $\Lambda=\Sigma_0^{-1}$ has no
empirical support at any tested timescale.** It is demoted to a whitening
metric, whose operational value is untested. The source equations are not
falsified by this; the physical reading frozen for them is.
See [`RESULT_SHORT_TIMESCALE.md`](RESULT_SHORT_TIMESCALE.md).

---

## 12. Structural displacement prediction — NOT SUPPORTED (2026-09-11)

$S(t)=\lVert\Sigma_0^{-1}\delta(t)\rVert$, with $\Sigma_0^{-1}$ treated as a
bare whitening metric and no interpretation attached, adds **no** out-of-sample
predictive information about intraoperative hypotension beyond marginal
features. 166 fresh arterial-line patients, 21,590 windows, 103–110
event-patients per horizon, prediction only from currently non-hypotensive
states.

| horizon | AUROC M9 (marginals) | ΔAUROC (M10 − M9) | ΔAUPRC |
|:--:|:--:|:--:|:--:|
| 5 min | 0.6904 | +0.0035 [−0.0029, +0.0104] | −0.0005 [−0.0038, +0.0021] |
| 10 min | 0.6467 | −0.0029 [−0.0158, +0.0100] | −0.0039 [−0.0120, +0.0034] |
| 15 min | 0.6165 | +0.0019 [−0.0107, +0.0153] | +0.0064 [−0.0030, +0.0213] |

Every interval spans zero and the sign flips across horizons. Replacing the
patient's covariance with **randomly permuted off-diagonals** changes AUROC by
at most 0.003; replacing it with the **identity** costs at most 0.007.
Patient-specific geometry never beats diagonal rescaling or a population
covariance. $S$ alone reaches 0.535–0.570.

The prespecified **secondary endpoint** (MAP < 55 mmHg) reproduces this on a
better-behaved, well-calibrated task: M9 reaches AUROC 0.832 / 0.787 / 0.740
with calibration slope 0.99 / 0.85 / 0.65, and $S$ moves AUROC by ≤ 0.0001 at
5 and 10 min. At 15 min it **hurts** — ΔAUPRC −0.0044 [−0.0088, −0.0010], the
interval entirely below zero. One harmful horizon is short of the two the
frozen FALSIFIED rule requires, so the verdict stands at NOT SUPPORTED.
At 5 and 10 min another patient's covariance outperforms the patient's own.

**Consequence: the last empirical claim attached to $\Lambda$ is gone.** The
stiffness reading was already demoted; the bare metric now has no incremental
predictive value either. Cross-channel structure generally fails here — the
covariance-drift/DNB comparator adds nothing to the marginal baseline.
See [`RESULT_STRUCTURAL_PREDICTION.md`](RESULT_STRUCTURAL_PREDICTION.md).

---

## 13. Representation search — persistence demoted, autocorrelation survives development (2026-09-11)

Strategy changed after three real-data failures: no longer rescuing the
covariance/stiffness representation. Search over temporal representations of
**marginal variability**, which is the actual empirical survivor — the
dispersion block dominates every other feature block by an order of magnitude
on leave-one-out.

Nine candidates on 166 development patients, each paired with a destructive
control preserving marginals and destroying temporal order.

| candidate | verdict |
|---|---|
| run-length of abnormal variability (the $Q_i=\lVert\Delta G_i\rVert\tau_i$ family) | **NOT SUPPORTED** — gain fully reproduced by the order-destroyed control |
| dV/dt, accumulated excess, change-point, hazard/first-passage | **NOT SUPPORTED** |
| spectral / entropy, all-temporal combined | **EXPLORATORY** |
| **window autocorrelation** | **SURVIVED on development, AUPRC-only, narrow** |

Window autocorrelation: ΔAUPRC +0.0011 / **+0.0127 [+0.0055, +0.0211]** /
**+0.0189 [+0.0099, +0.0298]** at 5/10/15 min, surviving Bonferroni over all 27
search comparisons. **ΔAUROC spans zero at every horizon.** Gain destroyed by
both the within-window shuffle and a row-wise channel shuffle, and not
explained by the repeated-sample fraction — though these signals are heavily
quantised (SpO₂ 96% identical consecutive samples) and an instrumentation
origin is not excluded.

$Q_i$ is **demoted for this application**; its protocol was withdrawn before
freezing.

**V2 is a development-selected candidate, not a confirmed survivor.** It was
chosen by a search over nine representations on development data — a selection
event, not a finding. It carries no evidential status until the one-shot
confirmatory run reports, and its development numbers may not be pooled with or
cited alongside that result.

The successor protocol is **FROZEN** with the pre-existing **STRICT** criterion
binding: SURVIVED requires **both** ΔAUPRC and ΔAUROC significant at 10 and
15 min. The AUPRC-led reading is recorded only as a labelled
secondary/provisional observation with no advancement authority. Declared
before the run: development meets the AUPRC-led reading and **fails STRICT**,
so the most likely binding verdict is NOT SUPPORTED.

The instrumentation/quantisation explanation is carried as a **live rival
hypothesis of equal standing**, which this design cannot discriminate against.
No mechanistic reading — recovery, relaxation, critical slowing down,
homeostasis, or any revival of Λ, Σ₀⁻¹, S(t) or Q_i — may be attached to any
outcome of this experiment.

See [`RESULT_REPRESENTATION_SEARCH.md`](RESULT_REPRESENTATION_SEARCH.md)
and [`PROTOCOL_AUTOCORR.md`](PROTOCOL_AUTOCORR.md).

---

## 14. H-AC confirmatory — NOT SUPPORTED (2026-09-12)

One-shot preregistered run of the protocol frozen at `9efe10c`, on 600 fresh
patients never previously accessed. 228 usable, 28,219 windows, 130–155
event-patients per horizon.

**Binding STRICT criterion fails on ΔAUROC at both required horizons.**

| horizon | ΔAUROC [CI] | ΔAUPRC [CI] |
|:--:|:--:|:--:|
| 5 min | +0.0057 [−0.0145, +0.0259] | +0.0043 [−0.0051, +0.0140] |
| 10 min | **+0.0022 [−0.0126, +0.0171]** | +0.0132 [+0.0024, +0.0237] |
| 15 min | **−0.0014 [−0.0156, +0.0135]** | +0.0145 [+0.0034, +0.0259] |

Five of six STRICT criteria met; criterion 2 (ΔAUROC > 0.01 with CI excluding
0) fails at both 10 and 15 min, one point estimate being negative. All three
destructive controls passed at all three horizons, calibration improved, the
false-alert criterion was met, and the MAP < 55 secondary endpoint reproduced
the AUPRC increment. The directional prespecification held on ΔAUPRC: 10 and
15 min exclude zero, 5 min does not.

**Secondary/provisional AUPRC-led observation** (no advancement authority):
criteria 1 and 3–6 met, criterion 2 not met. This is the outcome the frozen
protocol declared most likely before the run.

$R_{\mathrm{instr}}$ — monitor refresh, sample-and-hold and quantisation —
**remains a live competing explanation of equal standing**; the design could
not discriminate against it, since acquisition behaviour also depends on
temporal order and channel identity. No physiological, recovery, relaxation,
critical-slowing-down, homeostatic, Λ, Σ₀⁻¹, S(t) or Q_i reading is attached to
any part of this result.

Development and confirmatory results are kept separate and are not pooled.
See [`RESULT_HAC_CONFIRMATORY.md`](RESULT_HAC_CONFIRMATORY.md).

---

## Related records

- [`RESULT_EXPOSURE_STAGES.md`](RESULT_EXPOSURE_STAGES.md) — four-stage detail
- [`RESULT_STAGE1_ORACLE.md`](RESULT_STAGE1_ORACLE.md) — oracle control
- [`RESULT_HOMEOSTATIC_PREMISE.md`](RESULT_HOMEOSTATIC_PREMISE.md) — instrument test
- [`DERIVATION_ALIGNMENT.md`](DERIVATION_ALIGNMENT.md) — consequence versus assumption
- [`LIMITATIONS.md`](LIMITATIONS.md) · [`CLAIM_LADDER.md`](CLAIM_LADDER.md)

---

© 2026 Davarn Morrison · Transition Dynamics
