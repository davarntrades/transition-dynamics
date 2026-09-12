# Representation search over temporal variability — development results

**Development patients only (166). The 600 confirmatory patients have not been
touched.**

---

## The question

The empirical survivor is not displacement or covariance. It is that **marginal
dispersion carries substantially more signal than displacement**. The search
asks whether the *temporal organisation* of those fluctuations adds anything
beyond the static dispersion already inside the frozen baseline B\*.

$$H_0:\ \text{predictive information is primarily marginal dispersion}$$
$$H_1:\ \text{temporal organisation of fluctuations adds information}$$

Every candidate is paired with a **destructive control** that preserves the
marginal distribution exactly and destroys temporal ordering. The
candidate-versus-control comparison *is* the test.

---

## Frozen comparator B\*

`signed + slope + disp + maxz + aggz + elapsed + mean|z|`, $p=41$.
AUROC 0.683 / 0.650 / 0.649 and AUPRC 0.068 / 0.138 / 0.181 at 5/10/15 min.
Unchanged throughout. Endpoints, horizons, windows, exclusions, splits and
metrics unchanged from the structural protocol.

---

## All candidates, ranked

$\Delta$ is against B\*. "Temporal gain" is real minus order-destroyed control —
the H₁ quantity.

| candidate | +f | ΔAUPRC 5 / 10 / 15 | temporal gain (AUROC) 5 / 10 / 15 |
|---|:--:|:--:|:--:|
| V8 all temporal | 66 | +0.0057 / +0.0203 / +0.0183 | +0.008 / +0.015 / +0.007 |
| V7 spectral / entropy | 18 | +0.0012 / +0.0093 / +0.0143 | **−0.006** / +0.009 / +0.001 |
| **V2 autocorrelation** | **12** | **+0.0011 / +0.0127 / +0.0189** | **+0.007 / +0.010 / +0.007** |
| V3 dV/dt | 6 | +0.0008 / +0.0011 / +0.0014 | −0.001 / +0.002 / −0.001 |
| V1 run-length of abnormal variability | 6 | +0.0003 / +0.0087 / +0.0069 | +0.002 / +0.000 / **−0.001** |
| V5 change-point | 6 | −0.0000 / +0.0009 / +0.0001 | +0.003 / +0.005 / +0.001 |
| V6 hazard / first passage | 12 | +0.0027 / +0.0050 / **−0.0022** | +0.008 / +0.009 / +0.003 |
| V0 static v-summary (order-free) | 12 | −0.0030 / +0.0051 / +0.0061 | — |
| V4 accumulated excess | 6 | −0.0009 / −0.0026 / −0.0029 | **+0.0000 / +0.0000 / +0.0000** |

**A control validation worth stating.** V4's temporal gain is *exactly* zero at
all three horizons. Accumulated excess is a sum, hence permutation-invariant by
construction, so its order-destroyed control must be identical to it. It is.
The destructive control is doing what it claims.

**Persistence is H₀.** V1, the run-length of abnormal variability — the closest
relative of the $Q_i=\lVert\Delta G_i\rVert\tau_i$ candidate drafted earlier —
has a temporal gain of +0.002 / +0.000 / −0.001. Whatever small gain it shows is
fully reproduced by the order-destroyed control. Its information is order-free.

Only **V2** has a positive temporal gain at all three horizons.

---

## The one candidate with the H₁ signature

Per-channel window autocorrelation: lag-1 $\rho_i$ over the 5 min window, and
the derived $\tau_{\mathrm{AC1},i}=-\Delta t/\ln\rho_i$. 12 features.

> **No relaxation, recovery-time, stiffness or mechanistic interpretation is
> attached.** The short-timescale experiment falsified a *transfer* claim —
> that baseline relaxation predicts response relaxation. Autocorrelation as a
> predictive *feature* is a different question, tested here on its own merits.

### Incremental value, patient-level bootstrap (2000 resamples)

| horizon | ΔAUPRC [95% CI] | ΔAUROC [95% CI] |
|:--:|:--:|:--:|
| 5 min | +0.0011 [−0.0030, +0.0054] | +0.0039 [−0.0095, +0.0182] |
| **10 min** | **+0.0127 [+0.0055, +0.0211]** | +0.0071 [−0.0060, +0.0203] |
| **15 min** | **+0.0189 [+0.0099, +0.0298]** | +0.0056 [−0.0075, +0.0182] |

**The gain is AUPRC-only. ΔAUROC spans zero at every horizon.** This is stated
first because it is the result's principal weakness.

Relative scale: +9.2% and +10.4% of the base AUPRC at 10 and 15 min.
Operationally, sensitivity at a 10% false-alert rate moves 0.304 → 0.326 and
0.273 → 0.301. Calibration improves (slope 0.76 → 0.81, 0.77 → 0.88).

Multiplicity: 9 candidates × 3 horizons = 27 comparisons. Bonferroni threshold
$\alpha=0.0019$. The 10 min result gives $z\approx3.19$ ($p\approx0.0014$) and
15 min $z\approx3.72$ ($p\approx0.0002$). **Both survive correction for the
entire search.**

### Three destructive controls, all passed

| control | what it destroys | 5 / 10 / 15 min ΔAUPRC |
|---|---|:--:|
| real | — | +0.0011 / +0.0127 / +0.0189 |
| **within-window shuffle** | temporal ordering, marginals preserved exactly | control ΔAUROC **negative at all three** |
| **row-wise channel shuffle** | which channel is autocorrelated | **−0.0013 / −0.0023 / −0.0027** |
| **repeated-sample fraction alone** | — (artefact probe) | −0.0003 / −0.0006 / −0.0002 |

The gain requires **both** temporal ordering **and** channel identity.
Destroying either removes it entirely and turns it slightly negative.

### The monitor-quantisation problem, stated plainly

These signals are heavily held and quantised. Fraction of *identical
consecutive samples*:

| channel | repeated fraction | Spearman(AC, repeated fraction) |
|---|:--:|:--:|
| PLETH_SPO2 | **0.962** | **−0.836** |
| ETCO2 | 0.900 | +0.069 |
| HR | 0.721 | +0.083 |
| ART_MBP | 0.438 | +0.234 |
| ART_DBP | 0.376 | +0.316 |
| ART_SBP | 0.201 | +0.430 |

Lag-1 autocorrelation on such series is strongly influenced by monitor refresh
and quantisation, not only physiology. Two facts bound this:

- the repeated-sample fraction **alone adds nothing** (ΔAUPRC ≈ −0.0005);
- adding it alongside V2 does **not** improve V2 (+0.0113 vs +0.0127 at 10 min).

So the gain is not simply the hold artefact. It is **not** established that it
is physiological rather than a subtler instrumentation signature, and the
confirmatory protocol must carry that as the leading alternative explanation.

---

## Verdicts

| candidate | verdict |
|---|---|
| V1 run-length of abnormal variability (incl. the $Q_i$ family) | **NOT SUPPORTED** — gain is order-free |
| V3 dV/dt | **NOT SUPPORTED** |
| V4 accumulated excess | **NOT SUPPORTED** — negative, and order-free by construction |
| V5 change-point | **NOT SUPPORTED** |
| V6 hazard / first passage | **NOT SUPPORTED** — sign flips across horizons |
| V7 spectral / entropy | **EXPLORATORY** — positive ΔAUPRC but temporal gain negative at 5 min |
| V8 all temporal combined | **EXPLORATORY** — 66 features, gain largely V2's; complexity penalty |
| **V2 window autocorrelation** | **SURVIVED (development), AUPRC-only, narrow** |

$Q_i=\lVert\Delta G_i\rVert\tau_i$ is **demoted for this application.** The
persistence protocol drafted earlier is withdrawn before freezing: its own
representation family fails its own destructive control.

---

## Harness bug 12

The first channel-shuffle control permuted feature **columns** globally. Column
permutation is a no-op for a ridge model — the fit is identical — so the
control returned numbers bit-identical to the uncontrolled arm. Caught by that
exact identity, not by a plausibility check. Fixed to permute channel
assignment **independently per row**, which preserves each row's multiset of AC
values and destroys channel identity. The corrected control is the one reported
above, and it is the more informative of the two.

---

© 2026 Davarn Morrison · Transition Dynamics
