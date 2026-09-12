# Frozen confirmatory protocol — window autocorrelation as an incremental predictor

**Status: FROZEN — 2026-09-11. The 600 confirmatory patients have not been
accessed. Nothing in this document may be changed by any later run.**

> ## V2 is a development-selected candidate, not a confirmed survivor
>
> Window autocorrelation was **chosen by a search over nine candidate
> representations on development data**. It is the arm that looked best in that
> search. That is a selection event, not a finding.
>
> Selected-on-development quantities routinely fail on fresh patients. Three
> have already done so in this programme. Until the one-shot confirmatory run
> reports, V2 carries **no evidential status whatever** beyond "survived a
> development screen", and must not be described as a result, a signal, a
> discovery, or evidence for anything.
>
> The development numbers in
> [`RESULT_REPRESENTATION_SEARCH.md`](RESULT_REPRESENTATION_SEARCH.md) are the
> *reason for testing it*. They are not a preliminary confirmation of it, and
> they may not be pooled with, averaged into, or cited alongside the
> confirmatory result.

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

### The binding criterion is STRICT. It is the only criterion that can produce a SURVIVED verdict.

This is the same bar the structural-displacement protocol used. It is
preserved unchanged so that this candidate is judged by a standard set before
it existed, and not by one shaped around it.

**SURVIVED** requires **all** of:

1. $\Delta$AUPRC vs B\* $>0$ with Bonferroni 95% CI ($\alpha=0.05/3$)
   excluding 0 at **both** the 10 and 15 min horizons;
2. $\Delta$AUROC vs B\* $>0.01$ with Bonferroni 95% CI excluding 0 at **both**
   those horizons;
3. all three destructive controls in §4 passed at those horizons;
4. no calibration penalty: Brier $\le$ B\* $+0.005$ and
   $\lvert\text{slope}(A)-\text{slope}(B^*)\rvert\le0.15$;
5. no false-alert penalty: sensitivity at 10% FAR $\ge$ B\*;
6. reproduced on the secondary endpoint (MAP < 55) at $\ge1$ horizon.

### Other binding verdicts

- **FALSIFIED** — $\Delta$AUPRC CI entirely below zero at $\ge2$ horizons.
- **NOT SUPPORTED** — harness valid and adequately powered, criterion 1 or 2
  fails.
- **UNRESOLVED** — < 30 event-patients at a horizon, prevalence < 1%, or a
  harness defect invalidating the run.
- **EXPLORATORY** — passes criteria 1 and 2 at one horizon only, or passes at
  5 min while failing 10 and 15 (contradicting the directional
  prespecification), or passes 1 and 2 while failing any control in §4.

---

### SECONDARY / PROVISIONAL — AUPRC-led interpretation

**This is a labelled secondary reading. It cannot produce SURVIVED, cannot
alter the binding verdict, and carries no advancement authority.**

It is recorded because the development screen selected V2 on AUPRC alone, and
suppressing its confirmatory value would hide the one quantity the candidate
was chosen for.

> **Provisional AUPRC-led observation:** criteria 1 and 3–6 met, criterion 2
> (AUROC) not met.

Where this occurs, the binding verdict is **NOT SUPPORTED**, and the secondary
observation is reported beneath it under that exact label — never as a
qualified pass, a partial survival, a trend, or a near-miss.

**Declared before the run:** on development data the candidate meets the
AUPRC-led reading and **fails the binding STRICT criterion** ($\Delta$AUROC
spans zero at every horizon). The most likely confirmatory outcome under the
binding rule is therefore **NOT SUPPORTED**. Recording that expectation now
removes any interpretive freedom later.

---

## 6. What a SURVIVED verdict would mean

Only that **window autocorrelation adds information to the ranking of
pre-hypotensive windows beyond level, trend, dispersion, elapsed time and mean
recent displacement**, with the gain dependent on temporal order and channel
identity.

It would establish nothing about Transition Dynamics' source equations. No
quantity in this protocol derives from them.

### 6.1 The instrumentation rival hypothesis — carried explicitly

$$R_{\text{instr}}:\ \text{the gain reflects monitor acquisition behaviour — refresh
rate, sample-and-hold, quantisation — not physiology.}$$

$R_{\text{instr}}$ is **not a caveat. It is a live competing explanation of
equal standing**, and the confirmatory design cannot discriminate against it.

The evidence bounding it is weak by construction. The six channels are heavily
held: identical consecutive samples make up 0.962 of PLETH_SPO2, 0.900 of
ETCO2, 0.721 of HR, 0.438 of ART_MBP, 0.376 of ART_DBP, 0.201 of ART_SBP; and
Spearman(lag-1 AC, repeated fraction) reaches $-0.836$ for PLETH_SPO2. The
repeated-sample probe shows only that the *crudest* form of the artefact does
not account for the gain. A subtler acquisition signature would pass that probe
untouched.

### 6.2 Interpretations that are prohibited regardless of outcome

A SURVIVED verdict **does not license**, and no document in this repository may
assert, that window autocorrelation represents:

- physiological recovery or relaxation;
- critical slowing down;
- homeostasis, homeostatic reserve, or loss of regulatory control;
- stiffness, $\Lambda$, $\Sigma_0^{-1}$, $S(t)$, $Q_i$, deformation, or
  persistence in any form;
- any dynamical mechanism whatever.

**A mechanistic reading may be attached only by an experiment whose design can
discriminate that mechanism from $R_{\text{instr}}$ and from the others on this
list.** This experiment cannot. Discriminating would require channels with
genuinely different acquisition characteristics — a high-rate waveform
alongside a held numeric — which this six-channel panel does not contain.
That is the **next** experiment, not a reinterpretation of this one.

---

## 7. If it fails

Then magnitude, persistence, trajectory, coordinated multichannel change,
threshold structure **and** temporal organisation of variability have all
failed to add reproducible information beyond strong marginal baselines. The
stopping rule applies: this branch lacks empirical incremental value and the
recommendation is fundamental reformulation, not further optimisation.

---

## 8. Freeze declaration

Frozen 2026-09-11, before any confirmatory patient was loaded, queried,
summarised or otherwise accessed.

Fixed by this document and **not tunable by any later run**: the estimator
($\rho_i$, $\tau_{\mathrm{AC1},i}$, lag 1, 300 s window, 60 s stride, minimum
20 finite samples, 12 features); the baseline B\* and its 41 features; the
endpoint and secondary endpoint; the three horizons; the baseline window,
feature window and blanking gap; every exclusion and censoring rule;
missingness handling; the patient-level split and 5-fold grouped CV; the three
destructive controls and their 200 permutations; every numerical threshold in
§5; and the directional prespecification that 10 and 15 min pass while 5 min
does not.

No further development-data analysis will be performed on this candidate. The
confirmatory set is evaluated **once**.

---

© 2026 Davarn Morrison · Transition Dynamics
