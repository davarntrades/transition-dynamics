# Short-timescale relaxation transfer — result

## Verdict

# NOT SUPPORTED

Baseline relaxation properties do **not** predict short-timescale response
dynamics, even when predictor and response are measured on compatible,
independently identifiable timescales.

Band C returns **UNRESOLVED** (11 subjects, below the 30 minimum) — exactly as
projected from calibration before the confirmatory data was examined.

---

## What was tested, and what kind of claim it is

> **H-ST.** Within a channel, across subjects, a relaxation timescale from a
> quiet baseline predicts the relaxation timescale of that channel's response
> to a naturally occurring perturbation, in the same identifiable band.

| Layer | Status |
|---|---|
| Direct prediction of the source equations | **None.** They say nothing about autocorrelation or recovery times |
| **Derived hypothesis — what was tested** | If $\Lambda=\Sigma_0^{-1}$ is a **stiffness** operator, baseline second-order structure must encode relaxation dynamics |
| New exploratory | the mean-residence-time operationalisation |

A negative result does not falsify the source equations. It removes the
empirical basis for reading $\Lambda$ as a stiffness operator, leaving it a
whitening matrix.

---

## Dataset and split

VitalDB, PhysioNet open-access mirror, CC-BY 4.0, 2-second sampling.
**Entirely fresh subjects**: all 338 used in the previous experiment excluded.
3,924 eligible; 60 calibration, 200 confirmatory, disjoint.

Baseline window is the first 30 min; every analysed perturbation occurs strictly
later. 112 of 200 subjects contributed at least one usable event.

---

## Timescales and identifiability

At $\Delta t=2$ s a relaxation time is recoverable only for
$2\Delta t \le \tau \le W/3$.

| band | τ range | W | subjects | events | median τ_MRT |
|:--:|:--:|:--:|:--:|:--:|:--:|
| A — seconds | 4–20 s | 60 s | **112** | 1771 | 11 s |
| B — tens | 20–90 s | 300 s | **83** | 223 | 47 s |
| C — minutes | 90–400 s | 1200 s | 11 | 13 | **UNRESOLVED** |

---

## Primary result

Within-channel Spearman correlation, baseline $\tau_{\mathrm{int}}$ against
response $\tau_{\mathrm{MRT}}$, Fisher-z pooled, Bonferroni 95% CI over 3 bands.

| band | pooled within-channel ρ | CI | subject-permuted surrogate |
|:--:|:--:|:--:|:--:|
| **A** | **+0.043** | [−0.091, +0.176] | +0.000 [−0.110, +0.119] |
| **B** | **−0.006** | [−0.222, +0.210] | +0.004 [−0.185, +0.180] |

**The observed association is indistinguishable from the surrogate in which
each subject's baseline is paired with another subject's response.** Frozen
threshold was ρ ≥ 0.30 with CI excluding zero.

### Per channel, band A

| channel | n | ρ(τ_int) | ρ(τ_AC1) | ρ(τ_HWHM) | ρ(amplitude) | ρ(SD) |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| ART_MBP | 30 | −0.01 | +0.06 | −0.04 | −0.06 | −0.09 |
| ETCO2 | 112 | +0.22 | +0.29 | +0.31 | +0.16 | +0.22 |
| HR | 94 | −0.01 | +0.02 | +0.00 | −0.21 | −0.07 |
| PLETH_SPO2 | 91 | −0.11 | −0.08 | −0.16 | +0.08 | +0.16 |

Only EtCO₂ shows anything, and for it the trivial predictors (SD +0.22) match
the hypothesised one (+0.22). In band B, HR's amplitude correlation (+0.51)
**exceeds** every baseline predictor.

---

## The decisive control

| predictor | band A ρ |
|---|:--:|
| subject-specific baseline $\tau_{\mathrm{int}}$ | **+0.043** |
| **channel identity alone** | **+0.266** |

**Knowing only which channel you are looking at predicts six times better than
knowing that subject's own baseline.** The only structure present is
channel type, not patient physiology. This is precisely the confound the
within-channel design was built to expose, and it dominates.

---

## Two steelmen, both tested, neither rescues the result

**Range restriction — rejected.** The predictor varies substantially across
subjects: CV 0.56–1.00 for $\tau_{\mathrm{int}}$, 0.27–0.37 for
$\tau_{\mathrm{MRT}}$. There is ample variance to correlate.

**Reliability ceiling — real, but not disqualifying.** Split-half agreement of
$\tau_{\mathrm{MRT}}$ across events within a subject is ρ = 0.213
(Spearman–Brown reliability 0.351), so no predictor could exceed
**ρ = 0.593**. The frozen threshold of 0.30 was therefore achievable.
Disattenuating the observed value gives **+0.073**, CI [−0.154, +0.297] —
still short of 0.30 and still including zero.

Because sufficient subjects contributed, the predictor varied, and the ceiling
exceeded the threshold, this is **NOT SUPPORTED**, not UNRESOLVED.

---

## Did the mismatch close?

Partly, and not enough. Baseline $\tau_{\mathrm{int}}$ sits at 90–186 s
regardless of band, while band-A responses relax in ~11 s — still an order of
magnitude apart at the fastest identifiable timescale. The previous experiment
compared ~1 min against ~107 min; this one compares ~150 s against ~11 s. The
gap narrowed from ~100× to ~15× and the correlation remained zero.

---

## What survived / what died

**Survived:** nothing of the hypothesis.

**Died:** the derived hypothesis that baseline second-order structure encodes
relaxation dynamics — and with it the empirical basis for interpreting
$\Lambda = \Sigma_0^{-1}$ as a **stiffness** operator. That interpretation was
frozen as the primary physical reading. It now has no support at any tested
timescale.

$\Sigma_0^{-1}$ remains well defined as a **whitening metric**. Whether it
retains operational value in that reduced role is untested.

**The original mathematical relationship did not survive at a compatible
timescale.**

---

## Is the result genuinely out-of-sample?

Yes, on four counts: subjects are fresh and disjoint from every prior
experiment; the baseline window is temporally disjoint from and earlier than
every perturbation; perturbation detection uses no baseline quantity; and the
subject-permuted surrogate confirms the pairing carries no information.

---

## Strongest next falsification experiment

Not another rescue of the stiffness reading, which has now failed at two
timescales two orders of magnitude apart.

> **Does $\lVert\Sigma_0^{-1}\delta\rVert$ — with $\Lambda$ explicitly demoted
> to a whitening metric and no stiffness claim attached — predict subsequent
> physiological deterioration better than a marginals-only baseline?**

This is the first experiment that would bear on the **primary hypothesis**
rather than on the estimator machinery, it needs no onset estimate, and it
survives the failures recorded here because a whitening metric requires no
dynamical interpretation. VitalDB carries outcome fields suitable for defining
deterioration endpoints.

---

© 2026 Davarn Morrison · Transition Dynamics
