# Candidate experiment — ventilator breath response in VitalDB

# STATUS: FEASIBLE SECONDARY EXPERIMENT — NOT YET FROZEN

Not preregistered. No protocol frozen, no cohort drawn, no confirmatory data
accessed. This document records a design that survived feasibility so it is not
lost, and records exactly why it does **not** answer the question that motivated
it. It alters no verdict in [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md).

---

## Why it is feasible

Measured directly on 30 development cases:

| signal | availability | note |
|---|:--:|---|
| `Primus/AWP` airway pressure, 62.5 Hz | **97%** | perturbation source |
| `Solar8000/VENT_RR` / `VENT_TV` / `VENT_PIP` | **100%** | magnitude covariates |
| `SNUADC/ART` arterial waveform, 500 Hz | 63% | response channel; the limiting constraint |
| AWP-derived breath rate | **12.7/min** (IQR 11.0–14.7) | ≈ 2,300 perturbations per 3-hour case |

The ventilator is the only abundant, machine-timed, clinician-independent
perturbation in this dataset. Timing is exact, magnitude is recorded, and the
event count per patient is enormous.

## The design, in outline

Two tiers, mirroring the acquisition-discrimination experiment.

**Tier A — no outcome data.** Match windows on pre-perturbation current state
(MAP, HR, SpO₂, EtCO₂, ventilator settings), then test whether pre-perturbation
*history* predicts the breath response
$G=\Delta\text{ART}/\Delta\text{AWP}$. This is the
$P(R\mid Y,U,H_A)\ne P(R\mid Y,U,H_B)$ test. It needs no outcome and cannot leak.

**Tier B — outcome data, fresh cohort.** Does the response add over frozen B\*
for the hypotension endpoint? Primary kill condition: if response information
does not add reproducible out-of-sample information beyond matched current
state plus B\*, the hypothesis is NOT SUPPORTED for this perturbation and
endpoint.

## Why it does not answer the motivating question

1. **Ventilator breaths are periodic probes with no unperturbed interval.** The
   system is never allowed to return to rest between probes.
2. **Therefore recovery time, incomplete recovery, hysteresis and observable
   path dependence cannot be tested** — candidate quantities 3, 5 and 6 of the
   matched-state programme are all out of reach here.
3. **Ventilation-induced arterial variation overlaps substantially with
   established cardiopulmonary-interaction physiology** (pulse-pressure and
   stroke-volume variation), which is a validated preload-responsiveness
   family with its own literature.
4. **B\* may already encode a crude version of the same phenomenon.** Its
   `disp` block contains the within-window SD of ART_SBP and ART_DBP, to which
   respiratory swings contribute directly. An incremental null would therefore
   be ambiguous between "response carries nothing" and "the comparator already
   has it".
5. **A positive result would be primarily replication or refinement** of an
   established phenomenon, not evidence for a distinctive Transition Dynamics
   claim. Any write-up must say so.

## Known threats, recorded now so they cannot be discovered late

- **Partial endogeneity.** Breath *timing* is machine-set, but tidal volume,
  rate and PEEP are chosen by the anaesthetist and sometimes adjusted in
  response to the patient. Ventilator-setting changes would need to be
  exclusions, and TV/PIP would need stratification.
- **Endpoint-correlated missingness.** Beat-detector bin yield is 0.888 at
  MAP < 70 against 0.995 at MAP 70–90 (measured). Missingness rises as the
  endpoint approaches.
- **Established validity limits of the phenomenon** become admissibility
  criteria: spontaneous respiratory effort, arrhythmia, low tidal volume, open
  chest.
- **Vacuous controls are forbidden.** Any permutation leaving a ridge design
  matrix invariant — the column-permutation error recorded as harness bug 12 —
  must not be used. Admissible controls: breath-time permutation against the
  arterial series, per-row channel permutation, acquisition injection, and
  TV/PIP-matched strata.
- **Cohort restriction.** Arterial line in 63% of cases; expect ~35–40% usable
  yield after all exclusions.

## What would have to be decided before freezing

The B\*-overlap problem (threat 4) is the one that most affects
interpretability. A prespecified decomposition isolating the breath-locked
component of arterial variation from total dispersion would be required before
this could be frozen, so that a null is attributable.

---

## Related

- [`DATASET_REQUIREMENTS_MATCHED_STATE.md`](DATASET_REQUIREMENTS_MATCHED_STATE.md) —
  why the full matched-state question needs a different dataset
- [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) — unchanged by this document

---

© 2026 Davarn Morrison · Transition Dynamics
