<div align="center">

# LIMITATIONS

**Negative Findings as First-Class Results**

![Status](https://img.shields.io/badge/Negative_Findings-Preserved-047857?style=flat-square)
![Blind](https://img.shields.io/badge/Blind_To-Noise_Induced_Transitions-b91c1c?style=flat-square)
![Withdrawn](https://img.shields.io/badge/v1_Claims-2_Withdrawn-ca8a04?style=flat-square)

</div>

---

*"Keep the failures where the successes can see them."*

*— Davarn Morrison, 2026*

---

## 1. Withdrawn Claims

Preserved with their reasoning, not deleted.

| Claim | Origin | Status | Why |
|---|:--:|:--:|---|
| "The stiffness reading predicts pre-transition variance **falls**" | v1 §3 | **WITHDRAWN** | Does not follow from Λ = Σ₀⁻¹. Λ is frozen at baseline — a fixed metric, not a state variable. Predicting variance change would require preregistering Σ_t⁻¹, a different object |
| "Transition Dynamics and critical slowing down compete; one must lose" | v1 §4.1 | **WITHDRAWN** | The benchmark shows they are complementary. z detects the exogenous mechanism (AUC 1.00) and fails the endogenous one (0.30); the variance channel does the reverse |
| "The contribution is detection with lead time" | v1 H1 | **NARROWED** | Plain covariance drift scores AUC 1.00 on both detectable mechanisms. Detection adds nothing over methods published in 2012 |
| "A = 1 is the null for stiffness alignment" | v2 draft | **CORRECTED** | True only for isotropic displacement. For stationary data δ is Σ₀-shaped, so the null sits well below 1 — measured at 0.17 against a Cauchy–Schwarz bound of 0.29 |
| "Rate-induced tipping is detected only weakly" | v2 draft | **CORRECTED** | The numbers say otherwise: variance ratio 8.23, dG 5.29. It is detected strongly, but trivially — the sweep inflates variance everywhere |

---

## 2. Structural Blind Spots

These are properties of the mathematics, not gaps to be closed by better
engineering.

### 2.1 Blind to noise-induced transitions

> **──────────────────────────────────────────────────────────────────**
>
> Benchmark result, noise-induced mechanism:
> z  = −0.22   (stationary null −0.23)
> dG =  0.38   (stationary null  0.38)
> variance ratio 1.01
> A real transition occurs. Nothing anticipates it.
> Any estimator that appeared to predict this case would be
> reporting leakage, not dynamics.
> ──────────────────────────────────────────────────────────────────

If human deterioration is predominantly noise- or rate-induced, the framework
is not false — **there is nothing to detect**, and that is a bound on scope
rather than a defect.

### 2.2 A(t) cannot detect the fold mechanism

AUC 0.30 — worse than chance — for fold versus stationary. The failure is
structural: fold escape travels along **high-variance directions**, which is
exactly where stationary sampling noise also lives. Alignment cannot separate
signal from noise when they share a direction.

**A(t) is a detector of exogenous, homeostatically constrained displacement
only.** The endogenous-instability class belongs to the variance channel (M2).

### 2.3 Power limit — a cohort statistic, not a bedside alarm

95% null band for A by channel count:

| p | band | width |
|:--:|:--:|:--:|
| 4 | [0.09, 2.84] | 2.74 |
| 8 | [0.21, 2.49] | 2.27 |
| 20 | [0.41, 1.91] | 1.49 |
| 40 | [0.56, 1.58] | 1.02 |

At realistic ICU channel counts the per-window band is too wide for a
single-window alarm. A(t) supports **cohort-level mechanism discrimination**,
not per-patient real-time alerting, unless many channels are available.

### 2.4 Reach and homology remain unmeasured

Demoted, see [`DEMOTED_OBJECTS.md`](DEMOTED_OBJECTS.md). Every estimator is
metric. **No homological inference is licensed by any result in this
programme**, and the framework's own stated truth condition remains untested.

### 2.5 The resolution tension

Homeostatically defended channels — the ones A(t) weights most — are often the
**slowest** (temperature, lactate, pH). The n_eff ≥ 10p requirement forces long
windows for slow channels, and long windows erode lead time. Fast channels give
lead time but weaker homeostatic contrast. This tension has no clean resolution
and is preregistered as a two-panel design.

---

## 3. The Weakest Link

> **THE HOMEOSTATIC PREMISE IS NOT A CONSEQUENCE OF THE EQUATION.**
>
> A(t) is a geometric statistic. Turning it into a directional
> prediction requires the separate empirical premise that low
> normal variance indicates active homeostatic defence, and that
> pathology displaces defended variables.
> That premise is plausible, physiologically motivated, and
> untested. It is the weakest link in the chain and is stated
> separately so it can be falsified separately.

Counter-cases that would refute it: a low-variance channel that is low-variance
merely because it is **measured coarsely** or **clipped by the instrument**
rather than defended. Preregistered control: exclude channels whose baseline
variance is within measurement quantisation, and report their identity.

---

## 4. Confounds Not Fully Controlled

| Confound | Status | Residual risk |
|---|---|---|
| **Acquisition behaviour** | M0 gate | The most dangerous confound in the programme. The gate is a threshold, not a proof — a MATERIAL verdict still leaves partial contamination |
| **Treatment effects** | intervention masking | Treatments deform covariance directly. Masking reduces power substantially and may leave residual contamination at window edges |
| **Class-correlated monitoring** | M0 stratified by class | Sepsis patients are monitored differently from arrest patients. This could manufacture the class-specific z pattern that would otherwise be the headline result |
| **Immortal time** | landmark analysis | Standard, but sensitive to landmark choice |
| **Case mix and site practice** | validation by site | Cannot be fully removed retrospectively |
| **Instrument artifact** | artifact flagging | Probe disconnection produces large spurious deformation, plausibly correlated with patient agitation and therefore with deterioration |

---

## 5. What a Null Result Would and Would Not Mean

> **A NULL WOULD MEAN**
>
> This operationalisation, in this cohort, at this resolution,
> found no effect.
> A NULL WOULD NOT MEAN
> The mathematics is wrong. The objects may be valid and badly
> proxied — the demoted truth condition is the clearest case.
> A POSITIVE WOULD NOT MEAN
> The mathematics is right. A metric proxy can succeed for
> reasons unrelated to the object it stands in for.

This programme tests **operationalisability**, not truth. It can fail without
the framework being wrong, and succeed without the framework being right.

---

<div align="center">

> **z failed on the fold mechanism. That is recorded here, in the**
>
> same repository, at the same volume as anything that worked.

---

## Related Work

- [`../README.md`](../README.md) · [`PHYSICAL_INTERPRETATION.md`](PHYSICAL_INTERPRETATION.md) · [`DEMOTED_OBJECTS.md`](DEMOTED_OBJECTS.md) · [`ADVERSARIAL_REVIEW.md`](ADVERSARIAL_REVIEW.md)

---

© 2026 Davarn Morrison · Transition Dynamics · Limitations
