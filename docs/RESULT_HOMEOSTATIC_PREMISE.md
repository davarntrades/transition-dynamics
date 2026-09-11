# Result: the homeostatic premise test

**Status: the premise is NOT resolved. The instrument is valid but not
identifiable without exposure control.**

Verdict against the preregistered rules: **B — unresolved.**

The automated verdict printed by the script was **A**, computed from the
high-signal single-coordinate condition. On adversarial inspection that is
superseded: in the operating regime with distributed targeting, exposure
duration alone produces almost the same separation as targeting. Rule (B)
covers exactly that case, so B stands and A is withdrawn.

---

## What was tested

Whether alignment is a **valid instrument** for inferring homeostatic
targeting, on systems whose ground truth is known by construction.

Clinical data was not reachable from this environment (PhysioNet, UCI, Zenodo
and Figshare all blocked), so the clinical question — do real deteriorating
patients displace along their own low-variance directions — remains untested.
The instrument question is logically prior: if alignment cannot separate
targeted from untargeted displacement where the truth is known, no clinical
result obtained with it could support the premise.

---

## What survived

**1. Alignment is not redundant.** Matched on what conventional monitoring
sees, alignment separates targeted from untargeted displacement where neither
established comparator does.

| displacement | AUC univariate | AUC covariance drift | **AUC alignment** |
|:--:|:--:|:--:|:--:|
| 0.20 SD | 0.49–0.51 | 0.50 | 0.54–0.56 (chance) |
| 0.50 SD | 0.49 | 0.56–0.63 | **0.91–0.92** |
| 2.85 SD | 0.53–0.56 | 0.04–0.20 | **1.00** |

Univariate ≈ 0.50 is true by construction (it is the matching variable) and is
not a finding. Covariance drift is **not** matched on, so its weakness is a
finding: at large displacement it **inverts**, to 0.20 for distributed
targeting and 0.04 for single-coordinate targeting. Concentrating force in one
direction perturbs the covariance structure *less* than spreading it, so a
drift-based detector ranks a sharply targeted insult as more benign than a
diffuse one of the same clinical severity.

This is the first result in this programme where the Transition Dynamics
quantity beats both established comparators on a task neither performs.

**2. The monitoring and sampling confound does not manufacture the geometry.**
With physiology held identical and only the observation process differing
(regular versus escalating sampling, 400 versus 249 retained samples),
AUC = 0.49. Alignment is insensitive to the acquisition-behaviour confound that
threatens most of this field.

**3. Estimation is stable.** Alignment for targeted displacement varied by
0.020 across baseline windows of 1000–4000 samples (n_eff 222–876, requirement
≥ 10p = 80).

---

## What died

**1. The licensing inference.** The premise relies on

> alignment above the stationary null ⟹ homeostatic targeting

That inference is invalid. In the operating regime (0.50 SD displacement),
matched on conventional signal:

| condition | targeting? | AUC vs reference |
|---|:--:|:--:|
| isotropic, recent onset (T=1) | **no** | **0.84** |
| isotropic, T=12 | no | 0.56 |
| isotropic, T=120 | no | 0.47 |
| stiff-subspace targeting, T=60 | **yes** | **0.91** |

A purely kinetic difference — a recent untargeted insult — reaches 0.84 against
0.91 for genuine targeting. Without knowing time-since-onset, an observed
alignment cannot be attributed to targeting.

**2. The class-stratified sign prediction is withdrawn.** The preregistration
predicted positive alignment in sepsis and respiratory classes and null in the
abrupt class. Displacement under a step force is
$\delta_i = (f_i/k_i)(1-e^{-k_i T})$, so recent abrupt insults give **high**
alignment and slowly developing sepsis gives **low** alignment — the opposite
ordering, with no physiology involved. The prediction is confounded with insult
kinetics and is removed rather than re-derived.

**3. A detection floor is established.** At 0.20 baseline SD displacement,
alignment is at chance (AUC 0.54–0.56). The premise's signature is invisible
below roughly 0.2 SD and becomes usable around 0.5 SD.

---

## Two bugs that produced a false falsification

The first run returned **C — falsifies**, at AUC 0.52. It was void.

| Bug | Effect |
|---|---|
| Force onset placed relative to the end of the series while displacement was measured over the pre-transition window | The insult covered 10 of 400 window samples; signal diluted ~40× |
| Target displacement (0.45) set below the stationary sampling noise floor (0.335) | Calibration could not converge; every condition, including the stationary control, returned identical values |
| Long exposures placed force onset inside the baseline window | Contaminated the frozen baseline mean and covariance |

Calibration now runs on a deterministic twin, which is exact because the system
is linear; the target magnitude is set as a multiple of the computed noise
floor; and the simulator raises rather than silently contaminating the
baseline.

**A verdict of C from that run would have killed the premise on an artefact.**

---

## What is now justified, and what is not

**Justified:** alignment carries information that conventional univariate
monitoring and covariance drift do not, above a ~0.5 SD displacement floor, and
is robust to the acquisition-behaviour confound.

**Not justified:** any inference from an observed alignment to a homeostatic
mechanism, in any dataset lacking time-since-onset.

> **SUPERSEDED in part, 2026-09-11.** The exposure confound described below has
> since been addressed. Alignment separates targeting under oracle exposure
> control (within-stratum AUC 0.939), onset is estimable independently
> (median MAE 1.2 time units), and estimated-exposure control removes a
> spurious confounded effect exactly. See
> [`RESULT_EXPOSURE_STAGES.md`](RESULT_EXPOSURE_STAGES.md). The mechanism claim
> is no longer demoted on identifiability grounds, though it remains untested
> on real physiology.

**The next test is not a new construct.** It is whether time-since-onset can be
estimated well enough to separate the two — for example by fitting exposure and
force direction jointly from the displacement trajectory, since
$\delta_i(T) = (f_i/k_i)(1-e^{-k_i T})$ has different curvature per channel and
the per-channel rates are estimable from baseline autocorrelation. Until that
is demonstrated, alignment remains a descriptive quantity, not a mechanistic
one.

---

## Downstream claims demoted

| Claim | Previous status | Now |
|---|---|---|
| Alignment identifies transition mechanism | Load-bearing | **Demoted** — not identifiable without exposure control |
| Class-stratified sign prediction | Preregistered | **Withdrawn** — confounded by insult kinetics, and inverted |
| Alignment adds beyond established methods | Untested | **Supported**, above the 0.5 SD floor |
| Premise itself | Untested | **Still untested** — needs clinical data |

Reproduce: `analysis/experiments/homeostatic_premise.py`,
`analysis/experiments/alignment_identifiability.py`.
Generated tables: [`../analysis/results/homeostatic_premise.md`](../analysis/results/homeostatic_premise.md),
[`../analysis/results/alignment_identifiability.md`](../analysis/results/alignment_identifiability.md).
Derivation: [`DERIVATION_ALIGNMENT.md`](DERIVATION_ALIGNMENT.md).

---

© 2026 Davarn Morrison · Transition Dynamics
