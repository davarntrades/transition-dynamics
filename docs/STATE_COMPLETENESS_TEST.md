# The state-incompleteness test

**Design component. Not frozen, not executed, dataset-independent.** Alters no
verdict in [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md).

---

## 1. Three concepts that must never be collapsed

| # | Concept | Symbol | Observable? |
|:--:|---|---|---|
| 1 | **Current observable state** — what the monitor and chart record at $t$ | $Y_t$ | yes |
| 2 | **Underlying physiological state** — the true condition of the system | $X_t$ | **no, never** |
| 3 | **History / path dependence** — whether how the system arrived matters | $H_t$ | partially |

> $Y_A \approx Y_B$ does **not** imply $X_A \approx X_B$.

Therefore:

$$Y_A \approx Y_B \ \wedge\ R_A \ne R_B \quad\not\Rightarrow\quad \text{hysteresis}$$

**This is the falsification boundary for this research branch.** A difference in
response under matched observable state is equally well explained by
$X_A \ne X_B$ — that is, by $Y$ being an incomplete description — as by any path
dependence. The experiment below cannot separate those two. What it *can* do is
progressively harden the observable state description and see whether the
history effect survives.

## 2. The estimand

Let $Z_1,\dots,Z_k$ be **real, pre-perturbation measured** variables. Define a
frozen hierarchy of state descriptions:

$$S_0 = Y_t,\quad S_1 = Y_t \cup Z_1,\quad \dots,\quad S_K = Y_t \cup Z_1 \cup \dots \cup Z_K$$

The conceptual question is whether $I(H_t; R \mid S_k, U_t)$ falls as $k$ grows.

### Estimator: nested predictive comparison, not mutual information

Mutual information conditioned on a growing continuous multivariate set is not
reliably estimable at the sample sizes available. The defensible substitute, and
the one consistent with the machinery already in this repository:

$$\Delta_k \;=\; \mathrm{Perf}\big(R \mid S_k, U, H\big) \;-\; \mathrm{Perf}\big(R \mid S_k, U\big)$$

evaluated out of sample with patient-grouped cross-validation and
patient-level bootstrap intervals. $\Delta_k > 0$ means history carries
information about the response that state level $k$ does not.

**$R$ is the response, not the outcome.** This test requires no deterioration
label and therefore cannot leak outcome information.

## 3. Two ways this test can lie, and the controls for each

### 3.1 $\Delta_k$ is not guaranteed to decrease monotonically

Conditioning on additional variables can **increase** an apparent history
effect — suppression, or collider structure if a $Z$ is influenced by both $H$
and $R$. A frozen criterion demanding monotone decline would therefore be wrong
on its own terms.

**Consequence for the interpretation ladder:** "the history contribution
decreases" must be *reported descriptively*, never used as a gate. The binding
quantity is $\Delta_K$ at the **richest defensible** state level. The trajectory
$\Delta_0,\dots,\Delta_K$ is shown because it is informative, not because it is
required to be monotone.

### 3.2 $\Delta_k$ shrinks with dimension for purely statistical reasons

Every added $Z$ block costs degrees of freedom and inflates variance, so
$\Delta_k$ can fall as $k$ grows even when nothing is being explained away.

**Required control — placebo-$Z$.** At each level, run a parallel arm adding a
block of the **same dimension** containing variables with no physiological
relationship to $R$ (for example: patient identifiers hashed to noise,
irrelevant demographics, or permuted copies of a real $Z$ block). The decline in
$\Delta_k$ attributable to dimension alone is then measured rather than assumed.
A real "explaining away" claim requires

$$\Delta_k^{\text{real-}Z} \;<\; \Delta_k^{\text{placebo-}Z}$$

with a patient-bootstrap interval excluding zero.

Without this control, the state-completeness test is uninterpretable.

## 4. Admissibility rules for every $Z$

A block may enter the hierarchy only if it is:

1. **measured strictly before $U$** — no post-perturbation information;
2. **justified and ordered before confirmatory testing** — the hierarchy is
   frozen, not chosen by what reduces $\Delta$;
3. **adequately covered** — a prespecified minimum non-missing fraction, with
   missingness patterns reported and checked for correlation with $H$ or $R$;
4. **real** — no invented, imputed-from-outcome, or proxy variable standing in
   for something unmeasured;
5. **checked for acquisition artefact** — a $Z$ that is really a device
   behaviour must be labelled as such.

**The purpose is to challenge the history effect by improving state
specification, not to maximise predictive performance.** Richer $S_k$ models
must not become arbitrary high-dimensional predictors; block sizes and model
class are fixed in advance.

## 5. Interpretation ladder, corrected

| Observation | Permitted conclusion |
|---|---|
| $\Delta_0$ interval includes zero | **No evidence for observable history dependence** in this experiment |
| $\Delta_0 > 0$ but $\Delta_K$ interval includes zero, and the real-$Z$ decline exceeds placebo-$Z$ | **State incompleteness is the preferred explanation** |
| $\Delta_K > 0$ but reduced, real-$Z$ decline exceeds placebo-$Z$ | **UNRESOLVED / mixed** — measured state explains part, not all |
| $\Delta_K > 0$ and not materially reduced relative to placebo-$Z$ | **Observable path dependence survives the measured-state-completeness challenge** |

Even in the last row, the strongest permissible conclusion is:

> **"Observable current-state equivalence was insufficient to imply equivalent
> subsequent dynamics, and the difference was not explained by the measured
> state variables tested."**

This is **not** proof of biological memory, hysteresis, irreversibility, or
latent-state structure. An unmeasured $Z$ remains possible and always will;
no observational design can exclude it.

---

© 2026 Davarn Morrison · Transition Dynamics
