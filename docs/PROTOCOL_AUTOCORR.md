# Frozen confirmatory protocol — window autocorrelation as an incremental predictor

**Status: PROPOSED, awaiting approval. The 600 confirmatory patients have not
been accessed.**

---

## 1. The narrowest hypothesis the development data justifies

> **H-AC.** Adding per-channel window autocorrelation to the frozen marginal
> baseline B\* improves the **ranking of positive windows (AUPRC)** for
> intraoperative hypotension at horizons of **10 and 15 minutes**, but not at
> 5 minutes. The improvement requires both the temporal ordering of samples
> within the window and the identity of the channel, and is not attributable
> to monitor quantisation.

What H-AC deliberately does **not** claim:

- no AUROC improvement (development ΔAUROC spans zero at every horizon);
- no improvement at the 5 min horizon;
- no relaxation, recovery-time, stiffness, homeostatic or mechanistic reading;
- no revival of $\Lambda$, $\Sigma_0^{-1}$, $S(t)$, or $Q_i$ in any form;
- no claim that the signal is physiological rather than instrumental.

**Directional prespecification.** The protocol commits in advance to *which*
horizons should pass: 10 and 15 min yes, 5 min no. A pattern that passes only
at 5 min, or at all three equally, contradicts the development finding and is
recorded as such rather than counted as support.

---

## 2. Exact estimator

On a continuous 60 s grid over the analysable interval, for each channel $i$,
using the 5 min window ending at $t$ and **only** samples at or before $t$:

$$\rho_i(t)=\frac{\sum_{k}\tilde x_i(t_k)\,\tilde x_i(t_{k+1})}{\sum_k \tilde x_i(t_k)^2},
\qquad \tilde x = x - \bar x_{\text{window}}$$

$$\tau_{\mathrm{AC1},i}(t)=\begin{cases}-\Delta t/\ln\rho_i(t) & \rho_i(t)>0\\ 0 & \text{otherwise}\end{cases}$$

Feature block (12): $\rho_i$ and $\log(1+\tau_{\mathrm{AC1},i})$ for
$i=1\ldots6$. Non-finite values → 0. Windows with fewer than 20 finite samples
in a channel → that channel's pair set to 0.

Fixed parameters, no tuning permitted: $\Delta t=2$ s, window 300 s, grid
stride 60 s, minimum 20 finite samples, lag 1.

**Model:** `A = B* + autocorr`, $p=53$. L2-penalised logistic regression,
$\lambda$ by inner grouped CV over $10^{-2}\ldots10^{3}$, standardisation from
training folds only. Identical in every respect to B\* except the 12 columns.

---

## 3. Data

| set | n | status |
|---|:--:|---|
| development | 166 usable | burned; every choice above made here |
| **confirmatory** | **600 fresh cases** | **never accessed**; disjoint from all 1,078 previously used |

Endpoint, horizons, baseline window, feature window, blanking gap, exclusions,
censoring, missingness and patient-level 5-fold grouped CV are **unchanged**
from the structural protocol. Secondary endpoint MAP < 55 mmHg.

Projected yield at the observed 41.5%: ≈250 usable patients.

---

## 4. Required controls, run on the confirmatory set

| control | destroys | requirement |
|---|---|---|
| within-window shuffle | temporal ordering; marginals preserved exactly | real ΔAUPRC above the **95th percentile** of the 200-permutation control distribution |
| row-wise channel shuffle | channel identity; per-row multiset preserved | same |
| repeated-sample-fraction arm | — (artefact probe) | that arm alone must not reach half the real ΔAUPRC, **and** `A + repfrac` must not exceed `A` by more than its own CI width |

All three are required at every horizon that passes the primary criterion.

---

## 5. FROZEN DECISION RULE

Reported under **both** rules. Neither is chosen after seeing the result.

### PRIMARY rule (AUPRC-led — matches where the development signal is)

**SURVIVED** requires all of:

1. ΔAUPRC vs B\* $>0$ with Bonferroni 95% CI ($\alpha=0.05/3$) excluding 0 at
   **both** the 10 and 15 min horizons;
2. all three controls in §4 passed at those horizons;
3. no calibration penalty: Brier $\le$ B\* $+0.005$ and
   $\lvert\text{slope}(A)-\text{slope}(B^*)\rvert\le0.15$;
4. no false-alert penalty: sensitivity at 10% FAR $\ge$ B\*;
5. reproduced on the secondary endpoint (MAP < 55) at $\ge1$ horizon.

### STRICT rule (both metrics — the bar the structural protocol used)

As above, **plus** ΔAUROC $>0.01$ with CI excluding 0 at both horizons.

> On development data the candidate **passes the primary rule and fails the
> strict rule.** That is declared here, before the confirmatory run. If it
> passes strict on fresh patients, that is a stronger result than development
> predicted and will be reported as such.

### Other verdicts

- **FALSIFIED** — ΔAUPRC CI entirely below zero at ≥ 2 horizons.
- **NOT SUPPORTED** — valid and powered, criterion 1 fails.
- **UNRESOLVED** — < 30 event-patients at a horizon, prevalence < 1%, or a
  harness defect.
- **EXPLORATORY** — passes at one horizon only, or passes at 5 min while
  failing 10 and 15 (contradicting the directional prespecification), or
  passes the primary criterion while failing any control in §4.

---

## 6. What a SURVIVED verdict would mean

Only that **window autocorrelation adds information to the ranking of
pre-hypotensive windows beyond level, trend, dispersion, elapsed time and mean
recent displacement**, with the gain dependent on temporal order and channel
identity.

It would remain open whether the source is physiological or a subtler
instrumentation signature than the repeated-sample probe detects. Resolving
that is the **next** experiment, not this one, and would require channels with
genuinely different acquisition characteristics — not a reinterpretation of
this result.

It would establish nothing about Transition Dynamics' source equations. No
quantity in this protocol derives from them.

---

## 7. If it fails

Then magnitude, persistence, trajectory, coordinated multichannel change,
threshold structure **and** temporal organisation of variability have all
failed to add reproducible information beyond strong marginal baselines. The
stopping rule applies: this branch lacks empirical incremental value and the
recommendation is fundamental reformulation, not further optimisation.

---

© 2026 Davarn Morrison · Transition Dynamics
