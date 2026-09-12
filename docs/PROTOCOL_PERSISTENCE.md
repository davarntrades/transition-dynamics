# Protocol — Candidate family 1: deformation persistence

> # WITHDRAWN BEFORE FREEZING — 2026-09-11
>
> This protocol was never frozen and never run on confirmatory data. The
> representation search that preceded freezing tested the run-length of
> abnormal variability — the same persistence family — against a destructive
> control that preserves marginals and destroys temporal order. Its gain was
> **fully reproduced by the control** (temporal gain +0.002 / +0.000 / −0.001
> AUROC at 5/10/15 min). The information is order-free.
>
> $Q_i=\lVert\Delta G_i\rVert\tau_i$ is therefore **demoted for this
> application**, on development data, before any confirmatory patient was
> touched. See [`RESULT_REPRESENTATION_SEARCH.md`](RESULT_REPRESENTATION_SEARCH.md).
>
> The document is retained unaltered below as a record of what was proposed.
> The baseline B\* it establishes in §1 remains in force and is used unchanged
> by the successor protocol.

**Status: WITHDRAWN. Never frozen, never run on confirmatory data.**

---

## 0. What is permanently closed

These are preserved as settled and are **not** revisited, renamed, or
reintroduced in any form:

| claim | status |
|---|---|
| $\Lambda=\Sigma_0^{-1}$ as physiological stiffness | **unsupported / demoted** |
| relaxation-transfer hypotheses | **unsupported** |
| exponential onset transfer | **unsupported** |
| $S(t)=\lVert\Sigma_0^{-1}\delta(t)\rVert$ as incremental predictor | **NOT SUPPORTED** |
| patient-specific covariance geometry | **added essentially nothing** |

No quantity below uses $\Sigma_0$ other than as a per-channel scale
$\sigma_i=\sqrt{(\Sigma_0)_{ii}}$, which is a marginal rescaling already inside
the baseline. **No cross-channel covariance term appears anywhere in this
protocol.**

---

## 1. The frozen baseline B\*

Established on **development patients only** — the 166 usable cases of the
completed structural experiment, which are already burned and are exactly what
representation search is for.

### Which features actually carry the signal

Leave-one-block-out from the old M9, development patients, AUROC drop:

| block | contents | alone (5/10/15 min) | drop if removed |
|---|---|:--:|:--:|
| **`disp`** | baseline $\sigma_i$, within-window $\mathrm{SD}_i$ | **0.646 / 0.629 / 0.598** | **+0.075 / +0.071 / +0.041** |
| `raw` | absolute levels $x_i$, $\mu_{0i}$ | 0.538 / 0.531 / 0.542 | +0.012 / +0.015 / +0.013 |
| `absdelta` | $\lvert\delta_i\rvert$ | 0.629 / 0.594 / 0.568 | +0.012 / +0.019 / +0.007 |
| `slope` | OLS slope per channel | 0.583 / 0.551 / 0.557 | +0.006 / +0.009 / +0.007 |
| `absz`, `signed`, `maxz`, `aggz` | z-scored displacement | 0.51–0.59 | ≈ 0, several **negative** |

> **Variability, not displacement, carries the marginal signal.** `disp`
> dominates every other block by an order of magnitude on leave-one-out, and
> has the best AUPRC of any single block at every horizon. The z-scored
> displacement blocks contribute essentially nothing once dispersion is
> present.

This reframes the persistence test: persistence of *displacement* must beat a
baseline whose strength comes from *dispersion*.

### Baseline selection

Ten candidates were compared on development patients; selection rule was
maximum **AUPRC** (the primary decision metric), with calibration as tiebreak.

| candidate | p | AUROC 5/10/15 | AUPRC 5/10/15 | cal. slope |
|---|:--:|:--:|:--:|:--:|
| M9 (old comparator) | 57 | 0.690 / 0.647 / 0.617 | 0.066 / 0.131 / 0.155 | 0.11 / 0.14 / 0.08 |
| B8 compact + elapsed | 35 | 0.689 / 0.661 / 0.657 | 0.069 / 0.133 / 0.180 | 0.09 / 0.17 / 0.14 |
| **B\* = B8 + mean\|z\|** | **41** | **0.683 / 0.650 / 0.649** | **0.068 / 0.138 / 0.181** | **0.25 / 0.76 / 0.77** |

**B\* is frozen as**
`signed + slope + disp + maxz + aggz + elapsed + mean|z|`, $p=41$,
L2-penalised logistic regression, $\lambda$ by inner grouped CV.

Two deliberate hardening choices, both of which make the persistence test
*harder*, never easier:

1. **Elapsed time is in the baseline.** Every persistence quantity is bounded
   by time since the baseline window closed. Without this, a persistence
   feature could win simply by proxying for "later in the case". It is not a
   hypothetical risk: adding elapsed time moved M9 from AUROC 0.617 to 0.656
   at 15 min. That entire gain would otherwise have been available for
   persistence to claim.
2. **Mean $\lvert z_i\rvert$ over the same 30 min lookback is in the
   baseline.** It is purely marginal — per channel, no run structure — and it
   is the most obvious alternative explanation for any persistence effect
   ("this channel has been displaced a lot lately"). It belongs in the
   comparator, not in a separate control arm. It also repairs calibration
   (slope 0.17 → 0.76 at 10 min; Brier 0.0577 → 0.0512).

B\* beats the old M9 comparator on AUPRC at all three horizons. **The baseline
has been strengthened, not weakened.**

---

## 2. The candidate — $Q_i = \lVert\Delta G_i\rVert\,\tau_i$

Source object, operationalised **strictly** as persistence/duration of
measurable displacement. No consciousness, qualia, stiffness, homeostatic or
mechanistic interpretation is attached, asserted, or tested.

$$\Delta G_i(t)=\delta_i(t)=x_i(t)-\mu_{0i},\qquad
\lVert\Delta G_i(t)\rVert = \lvert z_i(t)\rvert = \lvert\delta_i(t)\rvert/\sigma_i$$

$$\tau_i(t;\theta)=\Delta s\cdot\min\Big(\max\{m:\ \lvert z_i(t-k\Delta s)\rvert>\theta\ \ \forall k<m\},\ L/\Delta s\Big)$$

$$\boxed{\,Q_i(t)=\lvert z_i(t)\rvert\cdot\tau_i(t;\theta)\,}$$

$\tau_i$ is the **current run-length** of displacement beyond $\theta$, ending
at $t$, measured on a 60 s stride ($\Delta s=60$ s) and capped at lookback $L$.

### Parameters, fixed on an outcome-blind distributional criterion

$\theta$ and $L$ were chosen on development data by requiring $\tau$ to be
non-degenerate — neither mostly zero nor mostly saturated. **No outcome was
consulted.**

| $\theta$ | frac $\tau=0$ | frac saturated ($L=30$) | median $\tau\mid\tau>0$ | distinct values |
|:--:|:--:|:--:|:--:|:--:|
| 0.5 | 0.394 | 0.178 | 13.0 min | 31 |
| **1.0** | **0.584** | **0.101** | **10.0 min** | **31** |
| 1.5 | 0.718 | 0.061 | 8.0 min | 31 |
| 2.0 | 0.794 | 0.049 | 8.0 min | 31 |
| 3.0 | 0.885 | 0.023 | 6.0 min | 31 |

**Frozen: $\theta = 1.0$, $L = 30$ min.** $\theta\in\{0.5,2.0\}$ are
prespecified **exploratory sensitivity only** and can never on their own
produce a SURVIVED verdict.

### Two implementation rules that decide whether the test is honest

1. **$\tau$ is computed on a continuous 60 s grid** spanning the whole
   analysable interval, independent of the label-exclusion rules. Computing
   run-lengths only over *retained* evaluation points would break runs wherever
   a window was dropped for being hypotensive or refractory — manufacturing
   structure out of the exclusion rule.
2. **Causality.** $\tau_i(t)$ reads only grid points $\le t$; grid points read
   only samples $\le$ their own timestamp. Verified by the same corruption test
   used in the structural experiment: corrupt everything after $t$, features at
   $t$ must be bit-identical.

---

## 3. Models

| id | model | added features |
|:--:|---|:--:|
| **B\*** | frozen baseline | — |
| **P1-min** | B\* + aggregate persistence | 3: $\log(1{+}\max_i Q_i)$, $\log(1{+}\sum_i Q_i)$, $\log(1{+}\max_i\tau_i)$ |
| **P1-full** | B\* + per-channel persistence | 18: $\log(1{+}\tau_i)$, $\log(1{+}Q_i)$, 3 $\tau$-aggregates, 3 $Q$-aggregates |
| C-shuffle-min / C-shuffle-full | **decisive control** | same, with $\tau$ from order-shuffled $z$ |
| C-tau-only | B\* + $\tau$ without magnitude weighting | 6 |
| C-const-tau | B\* + $\lvert z_i\rvert\times$const | 6 |
| Q-only | unfitted raw score $\max_i Q_i$ | — |

**P1-min and P1-full are co-primary.** Bonferroni $\alpha=0.05/6$
(2 forms × 3 horizons).

### The decisive control

**Order shuffle.** Recompute $\tau$ from the *same* channel's $z$-values with
their order permuted inside the lookback window. The marginal distribution of
$\lvert z\rvert$ over that window is preserved exactly; only the run structure
is destroyed. If the shuffled version predicts as well, what carries the signal
is *how displaced the channel has been on average* — not *for how long
continuously*, which is the entire content of $\tau$.

This is the direct analogue of the covariance shuffle that settled the $S(t)$
experiment. 200 permutations per horizon.

---

## 4. Data — evaluated once

| set | n | status |
|---|:--:|---|
| development | 400 (166 usable) | **burned** — all choices above made here |
| **confirmatory** | **600 fresh cases** | never touched by any experiment in this repository |

3,453 fresh eligible remain after excluding the 1,078 caseids used by all
three previous experiments. At the structural experiment's observed yield
(166/400 = 41.5%), 600 cases project to **≈250 usable patients** — more than
the 166 the baseline was built on, so the confirmatory test is better powered
than the development work behind it.

Endpoint, horizons, windows, exclusions, censoring, missingness and
patient-level CV are **unchanged** from the structural protocol, so results are
directly comparable: MAP < 65 mmHg for ≥ 60 s; horizons 5/10/15 min; baseline
[30, 50] min; 5 min feature window; 60 s blanking gap; every window already
containing hypotension dropped; negatives only when the horizon is fully
observed. Secondary endpoint MAP < 55 mmHg.

---

## 5. FROZEN DECISION RULE

### SURVIVED — requires **all** of:

1. For **at least one** primary form (P1-min or P1-full):
   $\Delta$AUPRC vs B\* $> 0$ with Bonferroni 95% CI excluding 0
   at **≥ 2 of 3 horizons**;
2. $\Delta$AUROC vs B\* $> 0.01$ with CI excluding 0 at those same horizons;
3. real $\Delta$AUPRC exceeds the **95th percentile** of the order-shuffle
   surrogate distribution at those horizons;
4. that form beats **both** C-tau-only and C-const-tau (ΔAUROC CI excluding 0);
5. **no calibration penalty, measured against B\* rather than an absolute band**:
   Brier(P) $\le$ Brier(B\*) $+\,0.005$ **and**
   $\lvert\text{slope}(P)-\text{slope}(B^*)\rvert \le 0.15$;
6. no false-alert penalty: sensitivity at 10% window-level FAR $\ge$ B\*;
7. reproduced on the secondary endpoint (MAP < 55) at ≥ 1 horizon.

### FALSIFIED
$\Delta$AUPRC CI entirely **below** zero at ≥ 2 horizons, for both forms.

### NOT SUPPORTED
Harness valid and adequately powered, but conditions 1–2 fail.

### UNRESOLVED
< 30 patients with an event at a horizon, or window-level prevalence < 1%, or a
harness defect invalidating the run.

### EXPLORATORY
Passes at exactly one horizon, or only under $\theta\in\{0.5,2.0\}$, or only
for one channel or subgroup. Reported as narrow; **never** promoted to
SURVIVED.

---

## 6. What a SURVIVED verdict would and would not mean

It would mean **only** that the duration for which a channel has been displaced
adds predictive information about hypotension beyond instantaneous magnitude,
dispersion, trend, elapsed time and mean recent displacement.

It would **not** establish persistence as a mechanism, revive $\Lambda$ in any
form, or support any broader framework claim. It would trigger the ablation
programme in §3, not a promotion.

If it fails, $Q_i$ is demoted **for this application** and the search moves to
candidate family 2 (trajectory), which is a genuinely different representation,
not a cosmetic transform of this one.

---

© 2026 Davarn Morrison · Transition Dynamics
