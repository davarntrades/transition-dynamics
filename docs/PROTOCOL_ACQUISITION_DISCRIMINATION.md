# Protocol — discriminating H_phys from H_instr on the arterial pathway

**Status: FROZEN — 2026-09-12.** Tier 1 has not been run. The Tier-2 cohort has
not been accessed. Nothing here may be changed by any later run.

---

## 0. What this experiment is for, and what it is not

The H-AC confirmatory run returned **NOT SUPPORTED** under its binding STRICT
rule. That verdict is final and is not revisited here
([`RESULT_HAC_CONFIRMATORY.md`](RESULT_HAC_CONFIRMATORY.md)).

What remains is narrower: a reproducible **AUPRC-specific** increment at 10–15
min that depends on temporal order and channel identity, of unknown origin.

$$H_{\text{phys}}:\ \text{the temporal structure reflects physiological dynamics.}$$
$$H_{\text{instr}}:\ \text{it reflects acquisition behaviour — refresh timing, sample-and-hold, quantisation, charting cadence, channel-specific measurement processes.}$$

### The six-channel matched-pair design is INVALID and must not be revived

| channel | verdict |
|---|---|
| **PLETH_SPO2** | **NOT IDENTIFIABLE.** SpO₂ requires red (660 nm) / infrared (940 nm) ratio-of-ratios plus a proprietary calibration curve. VitalDB has a **single unitless** `SNUADC/PLETH` waveform and **no** optical absorbance channels. A pleth waveform is not a high-frequency SpO₂ trace. |
| HR | detector-contaminated (R-peak misses cause large HR jumps); monitor's averaging window unknown |
| ETCO2 | plateau-detection structure, and the waveform comes from a **different device** than the numeric |
| ART_SBP / ART_DBP | extreme-value statistics, far more artefact-sensitive than a mean |
| **ART_MBP** | **CLEAN PRIMARY MATCH** |

One valid identification experiment, not six contaminated comparisons.

---

## 1. Arms

| arm | definition | role |
|---|---|---|
| **W** | beat-aligned mean arterial pressure derived from `SNUADC/ART` (500 Hz), binned to 2 s | clean signal |
| **W+inj** | **identical W**, transformed downstream by a frozen acquisition process | intervention |
| M | `Solar8000/ART_MBP` | **descriptive / reference only — appears in NO binding rule** |

**The load-bearing causal contrast is W vs W+inj.** Physiology, patient,
instants and labels are identical; only the known transformation is added.

**Why M is demoted.** Beat alignment did **not** improve agreement with M
(r = 0.783 → 0.783; SD of difference 6.16 → 6.88 mmHg). The residual
disagreement is the monitor's internal smoothing, filtering, artefact rejection
and timing — none of which is reproducible. M therefore cannot carry an
identification claim.

---

## 2. Beat-detector specification (frozen)

Zero-phase moving-average lowpass, $f_c=10$ Hz → upstroke where the first
difference crosses $0.3\times$ the 98th percentile of the derivative →
refractory 0.25 s → beat bound at the diastolic minimum within 0.15 s before
each upstroke.

Per-beat validity: duration $\in[0.25,2.0]$ s; pulse pressure
$\in[10,150]$ mmHg; mean $\in[20,180]$ mmHg; max < 300; min > −20.
Per-beat value = arithmetic mean over the beat. Binned by **beat midpoint**
into 2 s bins. Empty bins are NaN and are **never interpolated**.

**Beat detection is strictly upstream of injection.** W and W+inj share the
same detected beats and the same per-beat means.

## 3. Injection specification (frozen)

Applied downstream of beat binning:

- **quantisation** — round to **1 mmHg**, or off (every Solar8000 channel is integer-quantised);
- **zero-order sample-and-hold** — the value updates every `hold_s` and is held in between;
- `hold_s ∈ {2, 4, 6, 8}` s, where 2 s is the identity level;
- full 2 × 4 factorial;
- missing values are never invented.

**Primary cell = hold 4 s + quant 1 mmHg**, fixed by the rule *"the level whose
implied hold fraction is closest to the monitor's measured hold fraction of
0.560"* (4 s → 0.500, Δ 0.060; 6 s → 0.667, Δ 0.107). Specified from a measured
device characteristic, **never from predictive performance.**

---

## 4. TIER 1 — measurement-level acquisition identification

**Uses no outcome information of any kind.** No labels, no endpoint, no model.
Development cases excluding the 12-case specification subset.

Unit: 5-min autocorrelation window on the 2 s grid, 60 s stride — the same
geometry as the H-AC estimator. All CIs: patient-level bootstrap, 2000
resamples.

### Binding tests

| id | question | statistic | **PASS threshold** |
|:--:|---|---|---|
| **T1.1** | does injection increase AC? | paired within-window median $\Delta$AC $=$ AC(W+inj) − AC(W) | **≥ +0.05 and 95% CI excludes 0** |
| **T1.3** | **saturating** dose-response | (a) AC at 4, 6, 8 s each exceed AC at 2 s by ≥ +0.05 with CI excluding 0; **and** (b) Spearman $\rho$(implied hold fraction, median AC) ≥ +0.60; **and** (c) the 2→4 s increment ≥ 2× the larger of the 4→6 and 6→8 increments | **all three** |

> **Why saturating, not monotonic.** A zero-order hold at step $k$ makes
> $(k-1)/k$ of adjacent pairs identical, so AC must rise and then **saturate**.
> $H_{\text{instr}}$ does **not** predict strict monotonicity across 4/6/8 s.
> The specification pilot confirmed saturation (0.915 / 0.903 / 0.914). A
> monotonicity criterion would have failed $H_{\text{instr}}$ on its own
> correct prediction.

### BINDING VERDICT

**ACQUISITION SUFFICIENT (measurement level) iff T1.1 ∧ T1.3.**
ACQUISITION INSUFFICIENT if T1.1 fails. UNRESOLVED if feasibility fails.

### Characterisation only — cannot overturn the binding verdict

| id | analysis | reported threshold | binding? |
|:--:|---|---|:--:|
| T1.2 | gap closure $G = 1-\lvert \tilde{AC}_{W+inj}-\tilde{AC}_M\rvert/\lvert \tilde{AC}_W-\tilde{AC}_M\rvert$ | $G\ge0.50$, CI excludes 0; NOT EVALUABLE if base gap < 0.05 | **No** |
| T1.4 | interpolated AC at the monitor's measured hold fraction 0.560 | $\lvert$predicted − observed median AC(M)$\rvert \le 0.05$ | **No** |
| T1.5 | quantisation component at matched hold | CONTRIBUTORY if $\lvert\Delta\rvert\ge0.02$ with CI excluding 0 | **No** |

**T1.2 is explicitly non-binding.** M has been demoted because its internal
processing is not reproducible; it must not re-enter the causal decision rule
indirectly through gap closure. **Failure of T1.2 must not overturn a
successful controlled W-vs-W+inj intervention.**

### The only claim a Tier-1 PASS permits — verbatim

> **"The known acquisition transformation is sufficient to reproduce a
> substantial component of the arterial autocorrelation structure."**

Not generalised to the other five channels. Not to the predictive increment.
**Tier 1 must not be described as establishing the origin of the predictive
AUPRC increment.**

---

## 5. TIER 2 — predictive attribution

One shot, on the fresh untouched cohort, only after this protocol is frozen.

Frozen and unchanged: B\* (41 features), endpoint `ART_MBP < 65 mmHg` for
≥ 60 s, horizons **10 and 15 min**, grouped 5-fold patient CV, Bonferroni
$\alpha=0.05/2$, 2000 patient-level bootstrap. Feature block = the **ABP-only
AC pair** ($\rho$, $\log(1+\tau_{\mathrm{AC1}})$), 2 features, added to B\*.
Arms: B\*, B\*+AC(M), B\*+AC(W), B\*+AC(W+inj).

| condition | definition |
|---|---|
| T2.1 | $\Delta$AUPRC(W) CI **includes** 0 at **both** horizons |
| T2.2 | $\Delta$AUPRC(W+inj) > 0, CI **excludes** 0 at **both** |
| T2.3 | paired $\Delta$AUPRC(W+inj) − $\Delta$AUPRC(W) > 0, CI **excludes** 0 at **both** |

| outcome | verdict |
|---|---|
| T2.1 ∧ T2.2 ∧ T2.3 | **H_instr SUPPORTED for the arterial predictive pathway** |
| $\Delta$AUPRC(W) excludes 0 at both **and** T2.3 fails | **H_instr is not sufficient to explain the arterial predictive increment; the signal survives removal of the tested hold/quantisation process** |
| $\Delta$AUPRC(W) excludes 0 **and** T2.3 holds | **UNRESOLVED (additive contributions)** |
| $\Delta$AUPRC(W) excludes 0 **and** paired contrast < 0 with CI excluding 0 | **NEITHER MODEL ADEQUATE** |
| no arm's $\Delta$AUPRC excludes 0 | **PREDICTIVE ATTRIBUTION UNRESOLVED**; Tier 1 reported separately |
| power gate fails | **UNDERPOWERED** |

> **A surviving signal is NOT H_phys SUPPORTED.** "Not explained by the tested
> instrumentation" is not "physiology proven." It would still require a
> separate physiological-mechanism experiment before any mechanistic label.

### H_target — target-construction coupling

A **third instrumentation mechanism**, distinct from H_instr and equally live:

> The Tier-2 endpoint is defined using **monitor `ART_MBP`**. If W+inj becomes
> more monitor-like and therefore produces a larger predictive increment, part
> of that effect may arise because the transformed representation shares
> acquisition characteristics with the very measurement process used to
> **define the endpoint** — not because the hold process tracks physiology.

$H_{\text{target}}$ is an **instrumentation** explanation. A successful Tier-2
W+inj result must **not** be treated as evidence that the hold process reflects
underlying physiology unless target-construction coupling has been separately
excluded. This protocol does **not** exclude it, and says so.

### Three claims that are not equivalent — never to be collapsed

1. **Acquisition creates or changes AC structure.** (Tier 1 can establish this.)
2. **Acquisition improves prediction of a monitor-defined endpoint.** (Tier 2 can establish this; $H_{\text{target}}$ is an alternative route to the same observation.)
3. **Physiology generates predictive temporal structure.** (**Neither tier can establish this.**)

---

## 6. Feasibility thresholds (frozen)

A case is admissible iff `SNUADC/ART` and `Solar8000/ART_MBP` are both present;
waveform finite coverage ≥ **0.80**; beat-detector bin yield ≥ **0.70**;
detected beats per minute ∈ **[30, 200]**; plus every frozen structural
exclusion unchanged.

Tier 1 needs ≥ **100** usable cases and ≥ **500** AC windows.
Tier 2 needs ≥ **150** usable cases, ≥ **30** event-patients at each horizon,
prevalence ≥ **1%**.

If > 30% of otherwise-admissible ABP cases fail the detector gate, that is
recorded as a limitation, not an invalidation.

Specification-pilot values (12 development cases, 8 usable): bin yield median
0.915, min 0.883; 79.3 beats/min. The 0.70 floor is comfortable.

## 7. Cohort

| set | n | use |
|---|:--:|---|
| pilot | 12 | detector and injection specification, effect sizing. Outcome-blind. Spent. |
| **tier1** | 388 | Tier 1. **No outcome information is used**, so burned outcomes do not matter. |
| **tier2** | **600 fresh** | never used by any experiment in this repository |

2,853 fresh cases remain eligible after excluding the 1,678 used previously.

## 8. If Tier 2 is unpowered

Tier 1 remains valid and is reported. The final status must keep the two
conclusions **explicitly separate**, for example:

```
Acquisition effect on arterial autocorrelation : SUPPORTED
Acquisition explanation of predictive AUPRC increment : UNRESOLVED
```

They must never be collapsed into a single verdict.

## 9. Prohibited regardless of outcome

Describing any result as physiological recovery, relaxation, critical slowing
down, homeostasis, stiffness, $\Lambda$, $\Sigma_0^{-1}$, $S(t)$, $Q_i$,
deformation, persistence, consciousness or qualia. Generalising the arterial
result to the six-channel increment. Reviving the six-channel matched-pair
design. Relabelling H-AC's NOT SUPPORTED, or describing five-of-six criteria as
partial survival, near survival, a trend or a qualified pass. Pooling
development and confirmatory results. Treating "not explained by the tested
instrumentation" as "physiology proven".

---

© 2026 Davarn Morrison · Transition Dynamics
