# Structural displacement and prediction of deterioration — result

## Verdict

# NOT SUPPORTED

$S(t)=\lVert\Sigma_0^{-1}\delta(t)\rVert$ adds **no** out-of-sample predictive
information about intraoperative hypotension beyond marginal features.

Not FALSIFIED — no confidence interval lies entirely below zero.
Not UNRESOLVED — 103–110 patients contributed an event at each horizon,
prevalence 2.6–8.4%, and the harness carries a passing positive control.

---

## What was tested

> Does a multivariate structural displacement, using $\Sigma_0^{-1}$ purely as
> a whitening / precision metric, predict subsequent deterioration better than
> a marginals-only baseline?

$\Sigma_0^{-1}$ carried **no** stiffness, relaxation, homeostatic or
mechanistic interpretation. Those readings were already dead; this tested only
whether the quantity carries predictive information.

The comparison is **M10 (M9 + $S$) against M9 (marginals only)**, never
"Transition Dynamics against nothing".

---

## 1. Exact endpoint

**Intraoperative hypotension:** `ART_MBP < 65 mmHg` continuously for
`>= 60 s`. Onset is the first sample of that run.

The design is deliberately hostile to trivial prediction. Every evaluation
point whose 5-minute feature window contains *any* sample below 65 mmHg is
dropped, as is every point within 10 minutes after an onset. **All prediction
is therefore from a currently non-hypotensive state.** A 60 s blanking gap
separates the feature window from the prediction horizon, and a point is
labelled negative only if its full horizon is observed — otherwise it is
dropped, not counted as a negative.

This is why absolute AUROC here (0.62–0.69) sits far below the 0.87–0.95
reported by commercial hypotension-prediction indices, which do not exclude
windows that are already deteriorating.

## 2. Frozen patient split

VitalDB, PhysioNet open-access mirror v1.0.0, CC-BY 4.0. Public access only.

| | |
|---|---|
| fresh eligible (disjoint from all 598 previously used cases) | 3,933 |
| calibration | 80 |
| confirmatory | **400** |
| usable after prespecified exclusions | **166** |
| evaluation windows | **21,590** |

Exclusions: 135 coverage (chiefly no arterial line — the endpoint requires
invasive MAP), 99 hypotension inside the baseline window. One case had a
truncated download; it was refetched and found inadmissible for a substantive
reason, so **the analysed cohort is the complete frozen cohort**.

Leakage control: $\mu_0,\Sigma_0$ come only from minutes 30–50, strictly
earlier than every evaluation point; folds are grouped by patient; ridge
strength is chosen by inner CV inside training folds; population covariance and
feature standardisation use training-fold patients only.

## 3. Primary and comparator results

Bonferroni 95% CI over three horizons, 2000 patient-level bootstrap resamples.

| horizon | patients w/ event | AUROC M9 | AUROC M10 | ΔAUROC [CI] | ΔAUPRC [CI] |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 min | 103 | 0.6904 | 0.6938 | +0.0035 [−0.0029, +0.0104] | −0.00047 [−0.0038, +0.0021] |
| 10 min | 109 | 0.6467 | 0.6438 | −0.0029 [−0.0158, +0.0100] | −0.00391 [−0.0120, +0.0034] |
| 15 min | 110 | 0.6165 | 0.6185 | +0.0019 [−0.0107, +0.0153] | +0.00637 [−0.0030, +0.0213] |

**Every interval spans zero, and the sign flips across horizons (+, −, +).**
The largest effect, at 15 min, is a third of the magnitude required.

### The comparator ladder (10 min horizon)

| model | AUROC | AUPRC | Brier | cal. slope |
|---|:--:|:--:|:--:|:--:|
| M9 strong marginals-only | **0.6467** | 0.1312 | 0.0585 | 0.14 |
| M10 = M9 + $S$ | 0.6438 | 0.1272 | 0.0586 | 0.13 |
| M10b = M9 + Mahalanobis | 0.6454 | 0.1278 | 0.0586 | 0.13 |
| M11 = M9 + covariance drift | 0.6391 | 0.1270 | 0.0587 | 0.13 |
| M5 dispersion only ($\sigma_i$, SD) | 0.6289 | **0.1319** | **0.0505** | **0.92** |
| M8 marginal multivariable LR | 0.6215 | 0.1177 | 0.0546 | 0.54 |
| M7 covariance drift / DNB | 0.6016 | 0.0939 | 0.0516 | 0.90 |
| **$S$ alone (literal)** | **0.5371** | 0.0630 | – | – |
| **$S$ alone (Mahalanobis)** | **0.5567** | 0.0693 | – | – |

Alone, $S$ reaches AUROC 0.535–0.545 (literal) and 0.550–0.570 (Mahalanobis).
Both are near chance, and both are beaten by baseline dispersion features that
use no cross-channel information whatever.

**At 5 min, the single best AUPRC of any model belongs to M5 — six numbers
describing per-channel spread (0.0764, against 0.0657 for M9 and 0.0652 for
M10).**

## 4. Ablations — the decisive result

AUROC of M9+$S$ with $\Sigma_0$ replaced, everything else identical:

| horizon | patient-specific | diagonal | identity | **shuffled** | subject-permuted | population |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 min | 0.6938 | 0.6916 | 0.6870 | **0.6905** | 0.6876 | 0.6922 |
| 10 min | 0.6438 | 0.6449 | 0.6369 | **0.6450** | 0.6417 | 0.6469 |
| 15 min | 0.6185 | 0.6173 | 0.6166 | **0.6152** | 0.6168 | 0.6158 |

Replacing the patient's own covariance with **randomly permuted off-diagonals**
changes AUROC by at most 0.003. Replacing it with the **identity matrix** —
discarding the covariance entirely — costs at most 0.007.

Criterion 3 contrasts, paired patient bootstrap:

| horizon | ΔAUROC patient − diagonal | ΔAUROC patient − population |
|:--:|:--:|:--:|
| 5 min | +0.0023 [−0.0036, +0.0083] | +0.0016 [−0.0038, +0.0075] |
| 10 min | −0.0011 [−0.0116, +0.0093] | −0.0031 [−0.0134, +0.0066] |
| 15 min | +0.0012 [−0.0012, +0.0040] | +0.0026 [−0.0079, +0.0135] |

**Patient-specific geometry does not beat diagonal rescaling or a population
covariance at any horizon.** Whatever little $S$ contributes is available from
per-channel variances alone.

## 5. Surrogate / null

Permuting the components of $\delta$ against the same $\Sigma_0$ — preserving
every marginal deviation magnitude exactly, destroying only their pairing with
the covariance — 200 permutations per horizon:

| horizon | real ΔAUPRC | surrogate mean | surrogate p95 |
|:--:|:--:|:--:|:--:|
| 5 min | −0.00044 | −0.00202 | −0.00179 |
| 10 min | −0.00392 | −0.01170 | −0.01116 |
| 15 min | +0.00618 | −0.00065 | −0.00008 |

The frozen criterion 4 ("advantage destroyed by permutation") records *yes* at
all three horizons, **and that pass is vacuous**: there is no advantage to
destroy. It is reported for completeness, not as support.

## 6. Calibration and false-alert burden

| horizon | Brier M9 | Brier M10 | cal. slope M9 | cal. slope M10 | sens@10% FAR M9 → M10 | alerts/h |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 min | 0.0342 | 0.0343 | 0.113 | 0.116 | 0.335 → 0.342 | 6.0 |
| 10 min | 0.0585 | 0.0586 | 0.14 | 0.13 | 0.310 → 0.295 | 6.0 |
| 15 min | 0.0815 | 0.0824 | 0.08 | 0.09 | 0.234 → 0.239 | 6.0 |

Frozen criterion 5 fails at all three horizons — but it fails for **M9 too**,
identically. The large regularised models discriminate while their probabilities
do not transfer across patients (slope ≈ 0.1); the small well-specified models
(M5 slope 0.92–1.03, M7 0.75–0.90) are properly calibrated. **This is a
property of the strong baseline, not a penalty introduced by $S$**, and it is
reported rather than smoothed over.

At a 10% window-level false-alert rate the models detect 23–34% of events at a
burden of ~6 alerts per hour. Nothing here is clinically usable.

## 7. Lead time

Median time from first alert to onset, among detected events, at 10% FAR:
**3.2–3.3 min** (5 min horizon), **5.2–5.4 min** (10 min), **6.9–7.0 min**
(15 min). M10 and M9 are indistinguishable — at most 0.1 min apart at any
horizon. Lead time is set by the horizon, not by the model.

## 7b. Prespecified secondary endpoint — severe hypotension (MAP < 55 mmHg)

The protocol prespecified a secondary endpoint. It was run on the same frozen
split with the same harness and the same models; only the threshold moved. It
is a **better-behaved task**: rarer events, higher discrimination, and — unlike
the primary — well-calibrated baselines.

| horizon | event-patients | prevalence | AUROC M9 | cal. slope M9 | ΔAUROC (M10 − M9) | ΔAUPRC |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 min | 70 | 0.0119 | **0.8319** | 0.99 | −0.0001 [−0.0009, +0.0007] | +0.00015 [−0.0005, +0.0008] |
| 10 min | 83 | 0.0275 | **0.7870** | 0.85 | −0.0001 [−0.0014, +0.0011] | +0.00135 [−0.0011, +0.0044] |
| 15 min | 85 | 0.0449 | **0.7404** | 0.65 | −0.0041 [−0.0084, +0.0002] | **−0.00438 [−0.0088, −0.0010]** |

Two things stand out.

**The nulls are far tighter.** With a well-calibrated baseline at AUROC 0.83,
$S$ moves AUROC by one ten-thousandth. This is not a failure of power — it is a
measurement of zero.

**At 15 min, adding $S$ actively hurts**: the ΔAUPRC interval lies entirely
below zero. One horizon is not enough to trigger the frozen FALSIFIED rule,
which requires two, so the verdict stands at NOT SUPPORTED — but the direction
is recorded.

**The sharpest ablation result in the whole experiment appears here.** At 5 and
10 min, replacing a patient's covariance with **another patient's** gives the
*highest* AUROC of any variant (0.8356 and 0.7896, against 0.8318 and 0.7868
for the patient's own):

| severe, AUROC of M9+S | patient | diagonal | identity | shuffled | **subject-permuted** | population |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 min | 0.8318 | 0.8322 | 0.8321 | 0.8310 | **0.8356** | 0.8322 |
| 10 min | 0.7868 | 0.7865 | 0.7858 | 0.7849 | **0.7896** | 0.7879 |
| 15 min | 0.7363 | **0.7439** | 0.7363 | 0.7391 | 0.7411 | 0.7423 |

A patient's own baseline geometry is not merely weak. It is not preferred over
a stranger's.

---

## 8. What survived

- **The harness.** Its positive control detects a purely geometric displacement
  (AUROC 0.668 vs 0.540 for marginals) and its negative control refuses to
  credit $S$ for a purely marginal one. A null here is therefore informative.
- **The marginals-only baseline.** M9 reaches AUROC 0.690 / 0.647 / 0.617 from a
  non-hypotensive state — a defensible figure for an honestly constructed task.
- **$\Sigma_0^{-1}$ as a well-defined object.** Nothing here says it is
  ill-formed, only that it is not informative for this endpoint.

## 9. What died

**The last empirical claim attached to $\Lambda$.** The stiffness reading was
already demoted. This tested the weakest remaining version — $\Sigma_0^{-1}$ as
a bare whitening metric, no interpretation attached — and it too carries no
incremental predictive value.

Also dead: the hope that cross-channel structure generally would help here.
M7 (covariance drift / DNB-style) reaches AUROC 0.578–0.602 alone and adds
nothing to M9 either. The failure is not specific to the whitening form.

## 10. Does $\Sigma_0^{-1}$ add real predictive value beyond marginals?

**No.**

Three independent lines agree. The incremental intervals all span zero with
signs that flip across horizons. Shuffling the covariance's off-diagonals, or
deleting it outright for the identity, costs at most 0.007 AUROC. And
patient-specific geometry never beats diagonal rescaling.

The honest summary is that at $p=6$ channels in intraoperative anaesthesia,
**almost all of the predictive information is marginal**, and the multivariate
geometry that Transition Dynamics treats as load-bearing is, for this endpoint,
empty.

### Scope of this negative result

It is one endpoint, one setting, six channels, three horizons, 166
arterial-line patients. It does not show that multivariate physiological
structure is never informative. It does show that **this quantity, on this
task, adds nothing** — and that is the claim the framework needed.

## 11. Strongest next falsification experiment

The structural programme has now failed at three successive levels of
weakening: the exponential onset form, the stiffness reading of $\Lambda$, and
now $\Lambda$ as a bare metric. Weakening it a fourth time would test nothing.

The one question left that could still separate this framework from
conventional monitoring is **whether the events it aims at are irreversible at
all** — the threshold object $\lVert\Lambda\Delta G\rVert > T_{\mathrm{critical}}$,
which no experiment in this repository has yet touched:

> **Does the distribution of recovery from physiological excursions show a
> genuine separatrix — a displacement magnitude beyond which return to the
> pre-excursion state effectively never occurs — or is recovery probability a
> smooth, monotone function of excursion size with no threshold?**

It is the right next test for four reasons: it addresses the one source object
never operationalised; it is a claim about the *data*, not about an estimator,
so no onset model, no relaxation timescale and no covariance metric is
required; it is decisively answerable, since a mixture-of-two-regimes model
either beats a smooth monotone one on held-out patients or it does not; and a
negative result would close the programme cleanly rather than invite a fifth
weakening.

Prediction, stated in advance: if recovery probability is smooth and monotone
in excursion magnitude, $T_{\mathrm{critical}}$ is not a physical threshold but
a redescription of "large deviations are worse", and the framework's
distinctive claim is gone.

---

© 2026 Davarn Morrison · Transition Dynamics
