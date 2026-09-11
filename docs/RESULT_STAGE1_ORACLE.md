# Stage 1 result — oracle exposure control

**Preregistered verdict: UNRESOLVED.** Median within-stratum AUC 0.939 clears
the 0.75 bar; the fraction of strata above 0.65 is 67%, short of the 70% bar.

The verdict is recorded as written. It is **not** amended in light of what the
failures turned out to be.

---

## What was tested

Whether alignment distinguishes a targeted insult from an untargeted one once
exposure duration is controlled **by fiat**, using the simulator's known true
time-since-onset. No onset estimator is involved, so this stage could falsify
the mechanism-identification claim before any estimator was built.

108 strata: 6 baseline structures (stiffness spread, channel/eigenvector
rotation, noise level, dimensionality to p=16) × 6 exposures (T = 1…120) ×
3 severities, 25 seeds each. Targeted and untargeted cases matched within every
stratum on true T **and** on max univariate z, with cross-condition agreement
enforced to within 25%.

---

## Result

| | AUC |
|---|:--:|
| Unconditional, exposure **not** controlled | 0.783 |
| Within-stratum, true T and severity controlled — **median** | **0.939** |
| Within-stratum IQR | [0.547, 1.000] |
| Fraction of strata above 0.65 | 67% |

**Controlling exposure improves separation** (0.783 → 0.939). This is the
central finding and it corrects the earlier reading. Exposure duration shifts
the absolute level of alignment, but it does not destroy the discriminability
of targeting at fixed exposure. The confound attacks the *interpretation* of an
alignment value, not the *existence* of the signal.

### By severity

| max univariate z | baseline SD | median AUC | fraction > 0.65 |
|:--:|:--:|:--:|:--:|
| 4 | 0.20 | 0.541 | **0%** |
| 10 | 0.50 | 0.939 | 100% |
| 30 | 1.50 | 1.000 | 100% |

### By exposure

Median AUC is 0.848 at T = 1 and 0.941 at T = 120, rising monotonically. No
exposure regime fails.

### By baseline structure

Median AUC 0.858–0.996 across all six structures, including non-diagonal
covariance and p = 16. No structure fails.

### Comparator

Covariance drift, same strata: within-stratum median 0.566 overall and 0.746
among detectable strata, against 0.939 and 0.998 for alignment.

### Directionality

Among detectable strata, mean alignment is 1.257 stiff-targeted, 0.482
untargeted, 0.334 soft-targeted — the predicted ordering, in the predicted
direction, with soft targeting falling *below* the untargeted case.

---

## Post-hoc observation, labelled as such

All 36 strata below 0.65 are **exactly** the severity-4 strata. The other 72
are 100% above 0.65.

Severity 4 corresponds to 0.20 baseline SD of displacement, which is below the
noise floor of the matching variable itself: max univariate z has a stationary
floor near 6.4 for these configurations, because it is the maximum over
channels of a zero-mean fluctuation. In those strata there is no detectable
displacement for *any* statistic — covariance drift fails there too.

**This observation is post-hoc and does not change the verdict.** The
preregistered rule did not anticipate that a third of the grid would be
noise-dominated by construction, and the honest consequence is that the rule
returned UNRESOLVED. A rule written after seeing this structure would have
excluded sub-floor strata and returned SURVIVES; that rule was not the one
preregistered, and it is not adopted retrospectively.

---

## Consequence for Stage 2

Separation did not collapse under true-T control — it improved. The
falsification branch does not apply, so an onset estimator may be built.

Stage 2 is scoped to the **detectable regime** (displacement ≥ 0.5 baseline
SD). That scope restriction is a stated limitation, not a rescue: below
roughly 0.2 SD nothing in this framework detects anything, and no estimator can
change that.

---

## Bugs found and discarded runs

Two earlier Stage 1 runs were discarded. Neither is evidence.

| Run | Reported | Cause |
|---|---|---|
| 1 | FALSIFIED, all 108 AUCs in [0.490, 0.498] | Calibration targeted max univariate z evaluated on the deterministic twin, whose baseline SD is exactly zero. Force scale collapsed to 4×10⁻¹²; all conditions bit-identical |
| 2 | Aborted by guard | Guard compared realised severity against the nominal target; severity 4 is below the noise floor and unreachable, so a correctly working stratum was flagged |

The first was caught because every AUC across 108 independent strata sat inside
a 0.008-wide band. With 25 versus 25 seeds the null standard error is about
0.08, so that range is impossible under genuine randomness.

This was the third scaling bug in this programme to manufacture an apparent
null by never applying the perturbation. Each stratum now asserts that the
conditions are equally observable and not identical to machine precision, and
raises rather than contributing a spurious 0.5.

Reproduce: `analysis/experiments/exposure_stage1_oracle.py`.
Tables: [`../analysis/results/stage1_oracle.md`](../analysis/results/stage1_oracle.md),
[`../analysis/results/stage1_strata.json`](../analysis/results/stage1_strata.json).

---

© 2026 Davarn Morrison · Transition Dynamics
