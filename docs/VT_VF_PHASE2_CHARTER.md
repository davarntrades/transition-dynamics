# VT/VF programme: Phase-2 charter (owner decision record and pre-specification draft)

> **Status: CHARTER. Nothing in it has been executed.**
>
> - No real VT/VF hypothesis test, no inspection of pre-event physiology, no
>   protocol freeze, no external enquiry, no change to historical results,
>   no merge.
> - The seven hypotension outcomes and
>   [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) are unchanged.

## 1. Owner decision (2026-11-04)

**Approved activities:**

- **A. Acquisition artefacts as a separate falsification problem.**
  Determine whether additional ECG channels, signal-quality measurements or
  independent acquisition evidence can distinguish physiological structural
  change from artefact.
- **B. An independently specified synthetic holdout.** The next evaluation
  must not reuse the simulator assumptions and configurations that informed
  estimator development.
- **C. Continued dataset-access work.** Obtain verified information about
  longer continuous ECG recordings with documented VT/VF events.

**Not approved:**

- Selecting `pshape_hp` as the primary estimator because it performs better
  than the other candidates.
- Abandoning the heart-rate-coupled hypothesis. Removing heart-rate
  dependence may eliminate confounding, but it may also remove genuine
  physiological information. **These possibilities need separate tests**
  (§5).

**Effect on the Phase-1 report.**
[`VT_VF_PHASE1_REPORT.md`](VT_VF_PHASE1_REPORT.md) framed F3 (the
`pshape_hp` blind spot) as a scope choice for the owner. That framing is
superseded. Both hypotheses stay open and get separate estimands and
separate falsification tests. There is still **no primary estimator**.

## 2. Ordering constraint (to avoid repeating design-stage optimisation)

Activity A will itself develop and tune artefact discriminators. To keep
the holdout a genuine check:

1. The holdout author (B) writes and **seals** the generator, scenario truth
   labels and seeds (a commit hash recorded here) **before** any
   discriminator from A is evaluated on it.
2. A's development uses only the existing simulator (`beatsim2`) and
   real-noise sources (§3.3), never the holdout.
3. Each candidate discriminator, and each estimator × discriminator
   combination, is evaluated on the sealed holdout **once**. All results
   are reported, including failures.

## 3. Activity A: acquisition artefacts as a falsification problem

### 3.1 The problem stated as falsifiable claims

Phase 1 established that a statistic measuring deviation from baseline
structure rises under undetected noise (F1). For each candidate
discriminator D, the claim to test is:

> D separates (i) a physiological structural change from (ii) acquisition
> artefact of matched magnitude and timing, such that a positive verdict
> under (ii) occurs in ≤ 2% of n = 80 studies while power under (i) stays
> ≥ 80% at γ = 0.10.

D is **falsified** if an artefact model that is plausible for the target
acquisition setting defeats it. Every D must also be checked for the
**converse failure**: rejecting real physiology as artefact (for example,
a regional repolarisation change that appears in only some leads).

### 3.2 Candidate discriminators and their predicted signatures

| D | Evidence | Physiology predicts | Artefact predicts | Known way it can fail |
|---|---|---|---|---|
| D1 | **Cross-lead consistency**: compute the statistic on disjoint lead subsets | concordant change, with geometry consistent with a cardiac source (lead-field projection) | electrode-local artefact is discordant | common-mode artefact (whole-body motion, mains) is also concordant; regional physiology can be discordant |
| D2 | **Signal-quality indices** from frequency bands or features *not used by the statistic*: HF power > 40 Hz, baseline power < 0.5 Hz, kurtosis SQI, two-detector QRS agreement (bSQI), saturation and flat-line, beat-to-template correlation | SQIs stable while structure changes | SQIs shift with the structure change | artefact confined to the band the statistic uses; SQI thresholds tuned on the same data |
| D3 | **Independent acquisition evidence**: accelerometer, lead-off and INOP events, impedance, co-recorded ABP/PPG | no motion or lead-off excess; possible haemodynamic correlate | motion and lead-off events cluster with the "structure" change | often unavailable in ICU archives; haemodynamic change can itself be pre-arrhythmic physiology |
| D4 | **Morphology plausibility**: beats remain inside the patient's own template space | yes, with gradual morphology shift | beats fall outside template space | slow artefacts (wander, gain) stay inside template space |
| D5 | **Temporal signature**: burstiness and heavy tails | smoother evolution | bursty | intermittent physiological precursors are bursty too; **weak, not to be used alone** |

A discriminator may be used as a **conditioning or exclusion rule** (for
example, analyse only SQI-clean windows) or as a **competing explanation
test** (an extension of `ACQUISITION_EXPLAINED` using D2 and D3 rather than
only the detected-artefact fraction). Which use is primary must be
pre-specified before evaluation.

### 3.3 Real artefact sources: metadata verified, no signal read

| Source | Verified metadata | Use | Limits |
|---|---|---|---|
| **BUT QDB** (`butqdb/1.0.0`, PhysioNet open mirror) | **[V]** 18 records from 15 subjects (age 21–83). Each: about 24.2 h single-lead ECG at 1,000 Hz, a 3-axis accelerometer at 100 Hz (`_ACC`), and a signal-quality annotation file (`_ANN.csv`; annotator: "signal quality annotations"). Licence CC BY 4.0. | real artefact segments with independent acquisition evidence (accelerometer) for D2 and D3; noise injection into synthetic and clean ECG | single lead (no D1); wearable ambulatory, not ICU monitor; no VT/VF |
| **INCART** (`incartdb/1.0.0`) [V, Phase 0] | 75 records, 12-lead, 30 min | lead-subset consistency (D1) in real multi-lead ECG; common-mode vs local noise | short; arrhythmia annotations exist, so it is used for noise and lead geometry only, **never for VT/VF outcome analysis** |
| **EDB** (`edb/1.0.0`) [V, listing] | 2-lead, about 2 h records with ST/T annotations | two-lead consistency; real ST/T changes as "physiology that should not be called artefact" | ischaemia, not VT/VF; 2 leads only |
| MIT-BIH Noise Stress Test DB (`nstdb`) | **not on the mirror** [V]; physionet.org blocked | standard em/ma/bw noise | unavailable here |

Using these sources reads ECG and quality signals from databases that are
not VT/VF pre-event data. It is **not** an inspection of pre-event outcomes.
It is still data use, so it is listed for owner approval (§7).

### 3.4 Pre-specified evaluation, draft (to be finalised before any run)

- **Artefact models, beyond Phase 1's independent bursts:**
  - common-mode (correlating) noise across all channels;
  - electrode-local noise (one lead);
  - motion artefact segments drawn from BUT QDB quality-class-3 periods;
  - gain or impedance steps;
  - each at undetected fractions of 10%, 30% and 50%, and with near-onset
    rates rising over 15 and 60 min.
- **Physiology that must not be rejected:** global structure change
  (γ = 0.10), regional (lead-subset) change, an HR-coupled change
  (`nncorr`), and an intermittent change.
- **Criteria, kept from Phase 1:** artefact-only any positive ≤ 2%; power
  ≥ 80% at γ = 0.10; regional and HR-coupled physiology reported separately
  (no bound fixed yet; to be set before the run).
- **Stop rule.** If no D, or combination of D, meets the criteria on the
  sealed holdout, the deviation-statistic family is recorded as **not
  identifiable against undetected near-onset artefact with the acquisition
  evidence modelled**. This would be an estimator and acquisition finding,
  not a falsification of the hypothesis. It would also make the evidence
  that a dataset must carry (multi-lead, SQI, motion or lead-off logs) a
  hard dataset requirement (R5).

## 4. Activity B: commissioning an independent synthetic holdout

### 4.1 Independence requirements

The holdout author:

- has **not** seen `beatsim2.py`, `repaired_rule*.py`, `suite.py`, pilot
  outputs, or any Phase-1 results or failure lists;
- receives only this section, the per-patient estimand definition (§4.2),
  and the data interface (§4.3);
- chooses all generative mechanisms and parameter values;
- writes truth labels per scenario (null, conventional-only, artefact,
  physiological; and the expected verdict class) **before** the estimators
  are run;
- commits generator, scenarios and seeds; the commit hash is recorded here
  and the files are not changed afterwards.

**Who.** Preferably a human collaborator outside the estimator design. A
separate Claude session given only this brief offers **partial**
independence only: it shares the model family and its priors. If used,
that must be disclosed in every result.

### 4.2 Estimand given to the author

For each patient: one onset time T and a continuous recording before it.
The pipeline outputs per-bin s_{i,b} = AUROC(bin windows vs remote
windows, lead ≥ 60 min) − ½ for bins (2,5], (5,10], (10,15] and (15,30]
min. The study verdict uses one first event per patient.

### 4.3 Interface

- **Preferred:** raw multi-lead ECG (≥ 2 leads, ≥ 250 Hz) plus optional
  accelerometer and SQI or lead-off event streams, so that beat detection
  and delineation are done by the pipeline, not assumed by the simulator.
  This breaks the main `beatsim2` assumption, which simulates beat features
  directly.
- **Acceptable fallback:** a beat-level table (time, NN, RT, T amplitude,
  ST, per-lead quality flag). It must be disclosed as weaker.

### 4.4 Required scenario coverage (phenomena named; parameters left to the author)

The author must cover:

- nulls, including slow and non-stationary dynamics;
- conventional-only change, including **non-linear and hysteretic RT–RR
  coupling** (restitution) and HR excursions outside the remote range;
- acquisition artefacts of several kinds and detection rates;
- gain and baseline drift;
- missingness;
- heterogeneous patients;
- physiological precursors: structure beyond HR, **HR-coupled**, regional,
  variance-only and intermittent;
- VT vs VF differences, including an effect present in one class only, and
  equal effects in both classes (this measures the false-flag rate, F6);
- at least three adversarial scenarios of the author's own design, aimed at
  producing a spurious positive.

### 4.5 Evaluation rule (corrects Phase-1 F7)

- Pool ≥ 1,600 patients per scenario.
- Admissibility judged by the one-sided 95% binomial upper bound of the
  cell's positive rate against the same bounds as Phase 1 (≤ 2% for
  nulls, conventional-only and artefacts; ≤ 1% EXPLORATORY in nulls).
- Coverage within [0.93, 0.97].
- One run per estimator configuration. Every configuration evaluated is
  reported.

## 5. The two structural hypotheses: separate estimands and tests

| | **H-S: structure beyond HR coupling** | **H-C: change in HR–repolarisation coupling** |
|---|---|---|
| Interpretation | multichannel structure changes after removing the within-window dependence on NN | the coupling itself (slope, lag, non-linearity or hysteresis of RT and T on RR) changes before onset |
| Example estimator (not selected) | `pshape_hp`-type | coupling parameters estimated per window, compared with a patient-specific **coupling map** fitted on remote windows *as a function of HR level* |
| Main confounder | residual HR leakage (F2); artefacts (F1) | the HR/HRV level change itself moves coupling estimates even when the coupling law is unchanged (L2) |
| Separate falsification test | Phase-1 leakage tests, re-run on the independent holdout | **HR-matched test**: pre-onset coupling vs remote coupling *at matched HR* (only within the remote HR support; outside it the verdict is UNRESOLVED, never extrapolated); null scenarios where HR/HRV change under a **fixed** coupling law, including non-linear and hysteretic laws, must give ≤ 2% positives |
| What H-C must also exclude | — | that the "coupling change" is a delineation artefact of shorter RR (T-wave/P-wave overlap at high HR) |

- **Error budget.** H-S and H-C are separate pre-declared families, each
  with its own α. The split or allocation is to be decided by the owner
  before any freeze.
- **Inference rule.** A positive for an unconditioned statistic (for
  example `shape_hp`) together with a null for `pshape_hp` is **not**
  evidence for H-C. Only the H-C-specific test can support H-C.
- No primary estimator is selected for either hypothesis in this phase.

## 6. Activity C: dataset access

| Item | Status | Next action |
|---|---|---|
| `physionet.org`, `pmc.ncbi.nlm.nih.gov`, `proceedings.neurips.cc` | **still refused** by the environment proxy (403, rechecked 2026-11-04) | the owner adds them to the environment's *Allowed domains* (environment settings → Network access) |
| VTaC, Challenge 2015, MIMIC-III/IV waveform metadata | blocked by the above | verify record counts, unique patients, pre-alarm duration, lead sets (metadata only) |
| PhysioNet credentialed access (MIMIC clinical linkage) | not started | the owner completes credentialing ([`CREDENTIALED_ACCESS_CHECKLIST.md`](CREDENTIALED_ACCESS_CHECKLIST.md)) |
| Enquiries U1, T1, I1, A1, V1 | drafted, **not sent** | the owner verifies contacts and decides whether to send |
| New requirement from Activity A | — | add to every enquiry: multi-lead availability, SQI, INOP or lead-off logs, motion or impedance data (candidate requirement **R5**) |

## 7. Decisions still needed from the owner

1. Network allowlist (§6).
2. Who authors the independent holdout: a human collaborator, or a
   separate Claude session with disclosed partial independence (§4.1).
3. Whether BUT QDB, INCART and EDB may be used as real artefact and
   lead-geometry sources (§3.3).
4. Approval to finalise and run the Activity-A pre-specification (§3.4)
   on development data only, before the holdout is sealed.

---

© 2026 Davarn Morrison · Transition Dynamics
