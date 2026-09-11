# Preregistered protocol — short-timescale relaxation transfer

**Frozen before any confirmatory case is examined.**

---

## 0. Provenance of the question, stated honestly

The previous experiment failed because baseline autocorrelation reflects
dynamics of ~1 minute while the target curvature evolved over ~107 minutes.
This protocol removes that mismatch by measuring predictor and response on
**compatible** timescales.

**What kind of claim is this?**

| Layer | Statement |
|---|---|
| **Direct prediction of the source equations** | **None.** $Q=\lVert\Delta G\rVert\tau$, $Q_G=\Lambda Q$, $\lVert\Lambda\Delta G\rVert>T_c$ and $C(t)$ say nothing about autocorrelation or recovery times |
| **Derived hypothesis** | If $\Lambda=\Sigma_0^{-1}$ is a **stiffness** operator — the frozen physical interpretation — then baseline second-order structure must encode relaxation dynamics. Otherwise $\Sigma_0^{-1}$ is merely a whitening matrix and the stiffness reading has no empirical content |
| **New exploratory** | The specific mean-residence-time operationalisation below |

This experiment tests the **derived hypothesis**. A negative result does not
falsify the source equations; it removes the empirical basis for interpreting
$\Lambda$ as stiffness. A positive result does not confirm them either.

---

## 1. Hypothesis

> **H-ST.** Within a physiological channel, across subjects, a relaxation
> timescale estimated from a quiet baseline window predicts the relaxation
> timescale measured from that channel's response to a naturally occurring
> perturbation, when both are measured in the same identifiable timescale band.

Null: no within-channel association.

---

## 2. Identifiability limits — fixed by sampling, not by preference

At $\Delta t = 2$ s, a relaxation time $\tau$ is recoverable from a response
window $W$ only if

$$2\Delta t \;\le\; \tau \;\le\; W/3$$

Faster decays are complete between samples; slower ones have not bent within
the window.

| Band | τ range | response window W |
|:--:|:--:|:--:|
| **A — seconds** | 4–20 s | 60 s |
| **B — tens of seconds** | 20–90 s | 300 s |
| **C — short minutes** | 90–400 s | 1200 s |

All three bands are tested. **The band is not chosen after seeing results**;
multiplicity is handled by Bonferroni at α = 0.05/3 = 0.0167.

---

## 3. Response measure — model-free by construction

$$\tau_{\mathrm{MRT}} \;=\; \frac{\int_{t_p}^{t_p+W} \delta(t)\,dt}{\delta(t_p)}$$

with $\delta(t)$ the deviation from the pre-perturbation level and $t_p$ the
excursion peak. This is a **mean residence time**. It assumes no functional
form. For a pure exponential decay it equals $1/k$ exactly, so it reduces to
the exponential rate if the exponential model happens to be right, without
presupposing it.

---

## 4. Perturbation detection — uses no baseline rate

For each channel independently, on the analysis segment:

1. rolling median $m(t)$ and MAD $s(t)$ over $10W$;
2. candidate: a local extremum with $|x-m| > 4\,\mathrm{MAD}$;
3. **quiet pre-window**: the preceding $W/2$ must satisfy $|x-m| < 1.5\,\mathrm{MAD}$ throughout;
4. **decay requirement**: at $t_p+W$, $|x-m| < 0.5\,|x_{t_p}-m|$, else the
   excursion has not resolved and $\tau_{\mathrm{MRT}}$ is unbounded;
5. non-overlapping: successive perturbations separated by $\ge W$.

Nothing in this uses baseline autocorrelation, so detection cannot be
circular with the predictor.

---

## 5. Baseline predictors — from a separate, earlier window

Baseline window: the first 30 min of the recording, **disjoint** from and
strictly earlier than every analysed perturbation.

| Predictor | Definition | Note |
|---|---|---|
| $\tau_{\mathrm{AC1}}$ | $-\Delta t/\ln\rho_1$ | the quantity that failed at hour scale |
| $\tau_{\mathrm{int}}$ | $\Delta t\,(1+2\sum_{k\ge1}\rho_k)$ | integrated autocorrelation time — an **integral** timescale, conceptually matched to MRT. **Primary predictor** |
| $\tau_{\mathrm{HWHM}}$ | lag where $\rho$ first falls to 0.5 | robust, model-free |

---

## 6. Primary analysis — WITHIN channel

Spearman correlation between baseline $\tau_{\mathrm{int}}$ and response
$\tau_{\mathrm{MRT}}$, computed **within each channel across subjects**, then
pooled across channels by Fisher z.

> **Pooling channels is prohibited as the primary analysis.** Different
> channels have different characteristic timescales, so a pooled correlation
> would arise from channel identity alone and would say nothing about
> subject-specific physiology. The pooled figure is reported only as a
> deliberately inflated comparator.

---

## 7. Comparators and controls, all prespecified

| # | Comparator | Purpose |
|:--:|---|---|
| C1 | Null — no relationship | reference |
| C2 | $\tau_{\mathrm{AC1}}$, $\tau_{\mathrm{HWHM}}$ | does the predictor choice matter? |
| C3 | Free-rate exponential fit to the response | does a constrained form beat a fitted one? |
| C4 | Stretched exponential and power-law response | is the decay even exponential? |
| C5 | **Channel identity alone** | does knowing only the channel predict as well as subject-specific baseline? |
| C6 | **Subject-permuted surrogate** — baseline τ shuffled across subjects within channel | destroys the subject pairing, preserves all marginals |
| C7 | Trivial predictors — channel SD, sample count, perturbation amplitude | is any association just amplitude or sampling? |

---

## 8. Frozen decision rule

Let $\rho_w$ be the pooled within-channel Spearman correlation in a band.

| Outcome | Condition |
|---|---|
| **SUPPORTED (narrow)** | $\rho_w \ge 0.30$ with Bonferroni-corrected 95% CI excluding 0, in **≥ 2 of 3** bands; **and** surrogate C6 CI includes 0; **and** the association survives with channel identity as a covariate (C5) |
| **RESTRICTED** | the above holds in exactly **1** band — claim narrowed explicitly to that band |
| **NOT SUPPORTED** | CI includes 0 in all three bands, **or** C5/C6 removes it |
| **UNRESOLVED** | fewer than 30 subjects contribute a usable perturbation in a band, or fewer than 50 subjects overall |

---

## 9. Cohort and split

Fresh subjects only. Cases used in the previous VitalDB experiment (338) are
**excluded entirely**.

| Set | Definition |
|---|---|
| eligible | recording ≥ 2 h, caseid not among the previous 338 → 3,924 cases |
| **calibration** | first 60 eligible by caseid — detection parameters, identifiability checks |
| **confirmatory** | next 200 eligible by caseid — examined only after freezing |

Disjoint by construction.

---

## 10. Prohibited

- Choosing the band after seeing results.
- Reporting the channel-pooled correlation as the primary result.
- Adjusting detection thresholds after examining confirmatory outcomes.
- Describing any outcome here as evidence of clinical utility or early
  detection.
- Introducing a new construct if this fails.

---

© 2026 Davarn Morrison · Transition Dynamics

---

## 11. Calibration yield — recorded before the confirmatory run

Measured on the 60 calibration subjects only:

| band | W | subjects contributing | events | median τ_MRT |
|:--:|:--:|:--:|:--:|:--:|
| A — seconds | 60 s | 46 / 60 | 709 | 8.6 s |
| B — tens of seconds | 300 s | 39 / 60 | 114 | 46.0 s |
| **C — short minutes** | 1200 s | **7 / 60** | 12 | 182 s |

Bands A and B are well powered. **Band C is expected to fail the 30-subject
minimum** — 7/60 projects to roughly 23 of 200 confirmatory subjects — and is
therefore expected to return **UNRESOLVED** rather than a determination.

This is recorded now so that a Band C null cannot later be presented as
evidence against the hypothesis, nor its exclusion as a convenience.

The measured τ_MRT medians (8.6 s, 46 s, 182 s) fall inside their respective
prespecified bands, confirming the bands were placed on identifiable
timescales rather than chosen to fit.
