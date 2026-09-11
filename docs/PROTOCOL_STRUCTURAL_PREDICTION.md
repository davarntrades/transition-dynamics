# Protocol — structural displacement and prediction of deterioration

**Status: FROZEN.** Written before any signal from the confirmatory set was
read. Nothing below may be changed after the confirmatory data is examined.

---

## 0. Claim layer and provenance

| Layer | Content |
|---|---|
| Source equation | $\lVert\Lambda\Delta G\rVert > T_{\mathrm{critical}}$ |
| Physical interpretation | **None attached.** $\Lambda=\Sigma_0^{-1}$ is treated here purely as a **whitening / precision metric**. No stiffness, relaxation, homeostatic or mechanistic reading is claimed, asserted, or tested |
| Empirical operationalisation | $\delta(t)=x(t)-\mu_0$, with $\mu_0,\Sigma_0$ from a strictly earlier baseline window |
| Estimator | $S(t)=\lVert\Sigma_0^{-1}\delta(t)\rVert_2$ |
| Test | Does $S(t)$ add out-of-sample predictive information about later deterioration **beyond marginal features**? |

Two prior physical readings are dead and are not revisited here: the
exponential onset form (NOT SUPPORTED) and the stiffness reading of
$\Sigma_0^{-1}$ (demoted). This protocol tests only whether the *quantity*
carries predictive information.

### The two norms, both prespecified

The literal candidate quantity is $\lVert\Sigma_0^{-1}\delta\rVert$. This is
**not** the whitened norm: whitening gives $\lVert\Sigma_0^{-1/2}\delta\rVert$,
whose square is the Mahalanobis distance $\delta^\top\Sigma_0^{-1}\delta$. The
literal form carries units of precision squared and over-weights the
lowest-variance directions quadratically.

Both are computed and reported:

| symbol | definition | role |
|---|---|---|
| $S_{\mathrm{lit}}$ | $\lVert\Sigma_0^{-1}\delta\rVert_2$ | **primary** — the quantity as specified |
| $S_{\mathrm{mah}}$ | $\sqrt{\delta^\top\Sigma_0^{-1}\delta}$ | prespecified secondary — the metric-consistent whitened norm |

A result that holds for one and not the other is reported as such, not merged.

---

## 1. Dataset, split, leakage control

VitalDB, PhysioNet open-access mirror v1.0.0, CC-BY 4.0. Public access only.

**Fresh subjects.** All 598 cases used in the two previous confirmatory
experiments are excluded by caseid. 3,933 fresh cases are eligible.

| set | n | purpose |
|---|:--:|---|
| calibration | 80 | channel coverage, event-rate feasibility, harness smoke-test **only** |
| confirmatory | 400 | untouched until this protocol is frozen |

Split is by **patient**, deterministic (ascending caseid), defined in
[`../analysis/structural/cohort.py`](../analysis/structural/cohort.py) from
clinical metadata alone.

**Leakage rules.**
1. $\mu_0,\Sigma_0$ are estimated only from the baseline window, which ends
   strictly before every evaluation point.
2. No window uses any sample at or after its own prediction window.
3. Windows from one patient never split across cross-validation folds; all
   folds are grouped by caseid.
4. Ridge strength is chosen by **inner** cross-validation within the training
   folds only. The outer test fold is never seen during fitting.
5. Population covariance and feature standardisation are computed from
   **training-fold patients only** and applied to the test fold.

---

## 2. Endpoint

**Primary — intraoperative hypotension (IOH).**

> `ART_MBP < 65 mmHg` continuously for `>= 60 s` (>= 30 consecutive samples
> at 2 s). Event onset is the first sample of that run.

This is the standard definition in the intraoperative hypotension literature
and is clinically meaningful: cumulative time below MAP 65 is associated with
myocardial and renal injury.

**Secondary (prespecified, exploratory) — severe IOH:** `ART_MBP < 55 mmHg`
for `>= 60 s`.

---

## 3. Windows and labelling

All times relative to `anestart`.

| element | value |
|---|---|
| baseline window $B$ | [10 min, 30 min] |
| first evaluation point | 35 min |
| evaluation stride | 60 s |
| feature window $W$ | the 5 min ending at $t$ |
| blanking gap $g$ | 60 s |
| horizons $H$ | **5, 10, 15 min** (three co-primary) |
| last evaluation point | `aneend` |

Label at $t$ for horizon $H$ is positive iff an event **onset** falls in
$(t+g,\; t+g+H]$.

### Exclusions — the anti-triviality rules

A case is excluded entirely if:
- any of the eight channels is absent, or has < 80% finite coverage in $B$;
- any hypotension event occurs inside $B$ (the baseline must be event-free);
- $\Sigma_0$ estimated on $B$ has fewer than $10p = 80$ effective samples.

An evaluation point $t$ is dropped if:
- `ART_MBP < 65` at any sample inside the feature window $[t-W,\,t]$
  — **we predict only from currently non-hypotensive states**;
- an event onset occurred in the 10 min preceding $t$ (refractory period);
- after interpolation, any channel has > 20% missing inside $[t-W,\,t]$.

### Censoring

A point is labelled negative only if the full horizon is observed, i.e.
$t+g+H \le$ `aneend`. Otherwise the point is **dropped, not labelled
negative**. Positives are never censored — an onset inside the horizon is
observed by definition.

### Missingness

Per channel, linear interpolation across gaps of $\le 30$ s. Longer gaps stay
missing and count against the coverage rules above. $\mu_0,\Sigma_0$ use
complete-case rows within $B$. No imputation uses any future sample.

---

## 4. The structural quantity

$x(t)$ = per-channel **median over the last 60 s** (robust to monitor spikes).
$\delta(t)=x(t)-\mu_0$.

$\Sigma_0$ is estimated on $B$ with **Ledoit–Wolf shrinkage** towards a scaled
identity, which is required for a well-conditioned inverse at $p=8$ and is
applied identically in every arm that uses a covariance.

$$S_{\mathrm{lit}}(t)=\lVert\Sigma_0^{-1}\delta(t)\rVert_2,\qquad
S_{\mathrm{mah}}(t)=\sqrt{\delta(t)^\top\Sigma_0^{-1}\delta(t)}$$

Both are log1p-transformed before entering any linear model (they are
non-negative and heavy-tailed). This is fixed here, not tuned.

---

## 5. Models and comparators

$p=8$ channels. $z_i=\delta_i/\sigma_i$ where $\sigma_i^2=(\Sigma_0)_{ii}$.

| id | model | features |
|:--:|---|---|
| M1 | raw marginal deviations | $\lvert\delta_i\rvert$ |
| M2 | z-scored marginal deviations | $\lvert z_i\rvert$ |
| M3 | max marginal z | $\max_i\lvert z_i\rvert$ |
| M4 | aggregate marginal z | $\sum_i\lvert z_i\rvert$, $\lVert z\rVert_2$ |
| M5 | baseline + window dispersion | $\sigma_i$, $\mathrm{SD}_i(W)$ |
| M6 | trend | OLS slope of each channel over $W$ |
| M7 | covariance drift / DNB-style | $\lVert\Sigma_W-\Sigma_0\rVert_F/\lVert\Sigma_0\rVert_F$, mean $\lvert\mathrm{corr}\rvert$ in $W$, DNB composite |
| M8 | marginals-only multivariable LR | $z_i$, slope$_i$, $\mathrm{SD}_i$ |
| **M9** | **strong regularised marginals-only baseline** | everything in M1–M6 and M8, plus raw $x_i$ and $\mu_{0,i}$ — **no whitening, no cross-channel term** |
| **M10** | **M9 + $S(t)$** | M9 features $+\ \log(1+S_{\mathrm{lit}})$ |
| M10b | M9 + Mahalanobis | M9 features $+\ \log(1+S_{\mathrm{mah}})$ |
| S-only | univariate | $S_{\mathrm{lit}}$ alone |

M3 and S-only are used as raw scores (no fitting). All others are L2-penalised
logistic regression on standardised features, $\lambda$ by inner 5-fold
grouped CV over $\{10^{-2}\dots10^{3}\}$.

**The question is M10 vs M9.** Not Transition Dynamics versus nothing.

---

## 6. Ablations

$S$ recomputed with $\Sigma_0$ replaced, everything else identical:

| ablation | replacement |
|---|---|
| patient-specific | $\Sigma_0$ of this patient (**primary**) |
| diagonal | $\mathrm{diag}(\Sigma_0)$ |
| identity | $I$ (scaled to matching trace) |
| shuffled | off-diagonals randomly permuted, nearest-PSD projected |
| subject-permuted | another training patient's $\Sigma_0$ |
| population | pooled $\Sigma_0$ over **training-fold** patients only |

If patient-specific does not beat diagonal **and** population, no claim of
subject-specific geometric value may be made.

---

## 7. Surrogate / null

**Component permutation.** Apply a random permutation $P$ to $\delta$ and
compute $\lVert\Sigma_0^{-1}P\delta\rVert$. The marginal deviation magnitudes
are preserved exactly; only their pairing with the covariance geometry is
destroyed. If the advantage survives this, it is not geometric.

Run with 200 permutations; report the surrogate $\Delta$ distribution.

---

## 8. Metrics

Per horizon, patient-level grouped 5-fold CV, out-of-fold predictions pooled.

- AUROC, AUPRC (prevalence reported alongside)
- sensitivity at window-level false-alert rates of 5% and 10%; alerts/hour
- calibration: Brier score, calibration slope and intercept, decile reliability
- lead time: minutes from first alert to event onset, among detected events
- **patient-level bootstrap**, 2000 resamples of caseids, 95% percentile CI
- decision curve / net benefit across threshold probabilities

AUROC alone is not sufficient and is not the decision metric on its own.

---

## 9. Decision rule — FROZEN

**SUPPORTED FOR INCREMENTAL PREDICTIVE VALUE** requires **all** of:

1. $\Delta$AUPRC(M10 − M9) $> 0$, patient-bootstrap 95% CI excluding 0, at
   **>= 2 of the 3 horizons** (Bonferroni-widened CI, $\alpha=0.05/3$);
2. $\Delta$AUROC(M10 − M9) $> 0.01$ with CI excluding 0 at those same horizons;
3. patient-specific $\Sigma_0$ beats **both** diagonal and population
   (ΔAUROC CI excluding 0);
4. the advantage is destroyed by component permutation (real $\Delta$ above the
   95th percentile of the surrogate $\Delta$ distribution);
5. no calibration penalty: Brier(M10) $\le$ Brier(M9) $+0.005$ and calibration
   slope in $[0.8,1.25]$;
6. no false-alert penalty: sensitivity at 10% FAR not below M9.

**FALSIFIED** — M10 significantly *worse* than M9 (ΔAUPRC CI entirely below 0)
at two or more horizons.

**NOT SUPPORTED** — harness valid and adequately powered, but conditions 1–2
fail.

**UNRESOLVED** — fewer than 30 patients with an event at a horizon, or
window-level prevalence < 1%, or a harness defect invalidating the run.

If the effect appears only under one preprocessing choice, one channel, one
subgroup, or one horizon, it is reported as **narrow / exploratory**, never as
supported.

---

## 10. What a positive result would and would not mean

A positive result would mean **only** that a multivariate whitening metric adds
predictive information about hypotension beyond simpler marginal features.

It would **not** establish physiological stiffness, causal mechanism,
relaxation dynamics, onset identifiability, universal early detection, clinical
utility, or any broader framework claim.

## 11. Known confounds, declared in advance

- **Treatment paradox.** Vasopressors are given *because* deterioration is
  anticipated, which removes events that would otherwise have occurred. Every
  arm is affected identically, so the M9-vs-M10 contrast is still
  interpretable; absolute performance is not a clinical estimate.
- **MAP is both a feature and the endpoint channel.** This is deliberate: it
  makes the marginals-only baseline strong, which is the point.
- Intraoperative physiology under general anaesthesia is not ICU deterioration.
  Nothing here transfers to other settings without separate testing.

---

© 2026 Davarn Morrison · Transition Dynamics
