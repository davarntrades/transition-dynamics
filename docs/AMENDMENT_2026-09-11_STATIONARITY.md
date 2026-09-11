# Preregistration amendment — 2026-09-11

**Written before the confirmatory cohort was examined.** Evidence comes from
simulation and from the 40-case calibration subset only. The 100+ confirmatory
cases have not been loaded.

---

## Why an amendment is needed

The 0.5 SD stationarity screen rejected 100% of hourly ICU baselines. That
could mean the data are unusable or the screen is mis-specified. Loosening it
on that basis alone would be the forbidden move, so the question was settled by
simulation, where the truth is known by construction.

---

## Finding 1 — the screen tests effective sample size, not stationarity

The screen statistic is

$$\text{shift} = \frac{\left|\overline{x}_{\text{first third}} - \overline{x}_{\text{last third}}\right|}{\mathrm{SD}}$$

Under a **stationary** AR(1) with no drift whatsoever, the difference of two
third-window means has standard deviation $\mathrm{SD}\sqrt{2/n_{\text{eff,third}}}$.
The expected shift is therefore $\approx 2/\sqrt{n_{\text{eff}}/3}$ — a function
of effective sample size alone.

Simulation confirms this almost exactly:

| n_eff | observed median shift | predicted 2/√(n_eff/3) |
|:--:|:--:|:--:|
| 7 | 1.45 | 1.28 |
| 11 | 1.17 | 1.05 |
| 17 | 0.90 | 0.85 |
| 23 | 0.77 | 0.72 |
| 54 | 0.64 | 0.47 |

**A fixed threshold of 0.5 rejects stationary data at every effective sample
size tested**, including n_eff = 54. It is a test of n_eff wearing the label of
a stationarity test.

A second defect compounds this: the statistic is standardised by the window's
own SD, which the drift itself inflates, so the ratio does not grow in
proportion to genuine drift.

## Finding 2 — KPSS is also mis-specified here

The standard KPSS level-stationarity test with the usual Schwert lag rule is
badly oversized on strongly autocorrelated physiology: false-positive rate
43% → 95% → 100% as n grows at ρ = 0.85 → 0.98 → 0.995. Its long-run variance
estimator under-corrects when the autocorrelation time far exceeds the chosen
bandwidth. It is not a drop-in replacement.

---

## AMENDED RULE 1 — stationarity screen

**The statistic is unchanged. Its reference changes.**

The observed shift is compared against its own null distribution under a
**circular block bootstrap** of the same window, with block length
$L = 4\tau$, $\tau = (1+\rho_1)/(1-\rho_1)$, and rejection at the 95th
percentile.

Block resampling preserves short-range dependence, because blocks are
contiguous, while destroying long-range trend, because block order is
randomised. The null is generated at the same $n$, the same autocorrelation
and the same marginal distribution as the observed window, which removes the
effective-sample-size dependence at source.

**Measured operating characteristics** (simulation, AR(1), 4 channels):

| condition | fixed 0.5 | KPSS | **block bootstrap** |
|---|:--:|:--:|:--:|
| stationary, n=500, ρ=0.95 | 95% | 83% | **20%** |
| stationary, n=2000, ρ=0.98 | 90% | 95% | **12%** |
| drift 1 SD | 98–100% | 97–100% | 43–57% |
| drift 4 SD | 100% | 100% | **100%** |

The block-bootstrap screen remains **oversized** — actual size 12–20% against a
nominal 5% — and this is recorded rather than hidden. Block length between 2τ
and 16τ does not materially change it. The screen is therefore conservative: it
excludes some acceptable baselines. That direction of error is acceptable here
because the eligible pool is large and admitting a drifting baseline would
corrupt the very quantities the estimator depends on.

## AMENDED RULE 2 — baseline window length

The original rule required a baseline of **≥ 4 h**. That requirement was
written for hourly charting, where 4 h yields 4 samples and length was the only
way to obtain any effective sample size at all.

At 2-second sampling the binding constraint inverts. Measured on the
calibration set:

| baseline | samples | median n_eff | pass n_eff ≥ 40 | **pass both** |
|:--:|:--:|:--:|:--:|:--:|
| 10 min | 300 | 12 | 18% | 0/39 |
| 30 min | 900 | 21 | 31% | 2/39 |
| **60 min** | 1800 | 45 | 54% | **6/39** |
| **120 min** | 3600 | 81 | 95% | **6/39** |
| 240 min | 7200 | 176 | 100% | 4/39 |

Longer windows raise n_eff but guarantee non-stationarity, because real
physiology genuinely drifts over hours. The optimum is flat between 60 and
120 minutes.

**Frozen: baseline window = 120 minutes**, which achieves n_eff ≥ 40 in 95% of
cases while giving the best joint yield. The duration floor is replaced by the
n_eff requirement, which is the quantity the rule was always a proxy for.

## AMENDED RULE 3 — confirmatory pool size

Measured admissible yield on calibration is **≈ 15%**. Reaching the required 50
admissible recordings therefore needs a pool of roughly 330 cases, not 100.

**Frozen: the confirmatory set is all remaining eligible cases** (298), rather
than the first 100. This is a power calculation made on calibration data before
any confirmatory case was loaded. No threshold is altered by it.

---

## What is NOT amended

- The 50-recording minimum.
- The n_eff ≥ 10p requirement.
- Every Stage B and Stage C threshold: selection rate, surrogate comparison,
  held-out comparison against alternatives, rate rank correlation ≥ 0.5,
  decline ≤ 50%.
- The falsification and advancement rules.

---

## A validity limitation recorded in advance

VitalDB is **intraoperative**. A surgical patient is under continuous
intervention — anaesthetic agents, fluids, vasopressors, ventilation changes —
so no window is genuinely "treatment quiet" in the sense the original protocol
intended for ICU baselines.

This is stated now, before the confirmatory result, because it bounds what the
test can establish either way. A positive result would show the dynamical form
transfers to real continuously-monitored human physiology **under
intervention**, not to quiet baselines. A negative result could reflect the
intervention environment rather than the model.

---

© 2026 Davarn Morrison · Transition Dynamics
