# VF onset programme — dataset feasibility: PhysioNet Sudden Cardiac Death Holter Database

> **Status: PROPOSAL / DESIGN RECORD (revised with protocol v2). No signal data accessed.**
> This is a new transition-class study (ventricular fibrillation onset). It does
> not reinterpret any of the seven completed intraoperative-hypotension
> experiments. Their verdicts in [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md)
> are unchanged by anything here.
>
> Companion documents: [`VF_PROTOCOL_DRAFT.md`](VF_PROTOCOL_DRAFT.md) ·
> [`VF_LITERATURE_BASELINES.md`](VF_LITERATURE_BASELINES.md) ·
> [`VF_IMPLEMENTATION_PLAN.md`](VF_IMPLEMENTATION_PLAN.md)

---

## 0. Verification status. Read this first

**physionet.org could not be reached from the environment in which this was
written.** Both direct HTTPS and fetch tools were refused by the session's
network policy. Every dataset property below therefore comes from web-search
snippets of the PhysioNet landing page, record header files, and secondary
literature. **None of it has been verified against the files themselves.**
Phase 0 of the implementation plan exists to do that verification. Phase 0
reads headers and annotation metadata only. Any discrepancy found there
**amends this document before any protocol is frozen**.

| Property | Value as found | Source class | Confidence |
|---|---|---|:--:|
| Records | 23 complete Holter recordings | PhysioNet landing page (search snippet) | high |
| Provenance | Collected by Scott Greenwald (MIT). Half-hour excerpts distributed since 1989 as the MIT-BIH Malignant Ventricular Arrhythmia Database | PhysioNet landing page | high |
| Signals | 2 ECG channels per record | secondary (2026 preprint) | medium |
| Sampling rate | 250 Hz | secondary (2026 preprint). **Not seen on PhysioNet's own page** | medium, must verify |
| Duration | roughly 7–25 h. Mean reported as 18.99 ± 8.27 h | secondary. No-VF records listed at 24:53:00, 25:08:10 and 25:01:40 | medium |
| VF onset documented | 20 of 23 records | secondary + landing-page table | medium-high |
| No VF | records **40** (paced, no VF), **42** (no VF), **49** (paced, no VF) | landing-page table (search snippet) | medium-high |
| Onset encoding | header comment `#vfon: hh:mm:ss`, e.g. 38 → 08:01:54, 46 → 03:41:47, 48 → 02:29:40, 52 → 02:32:40 | header files (search snippets) | medium |
| Beat annotations | unaudited `.ari` for all records; audited `.atr` for an **incomplete** subset (reported as 12) | landing page + secondary | medium |
| Underlying rhythm | 18 sinus (some with intermittent pacing), 4 atrial fibrillation, 1 continuously paced | secondary. **PhysioNet's older text words this differently, so the two sources conflict** | low, must verify |
| Clinical outcome | all had sustained ventricular tachyarrhythmia; most had an actual cardiac arrest | landing page / secondary | medium |

> **Disclosure (design contamination).** While searching I saw four VF onset
> times (records 38, 46, 48, 52) in header snippets. No other label and no
> signal sample was seen. The eligibility rules in the protocol were written
> from first principles (§4 of the protocol). Two records (48, 52) have onsets
> close to the minimum-elapsed-time threshold, which the reviewer should check.
> This disclosure is recorded so the reviewer can judge whether those rules
> were shaped by what was seen.

---

## 1. What SDDB can and cannot support

### 1.1 Event annotations

- **Event definition is a single time stamp per patient** (`#vfon`). It marks
  VF onset, not the onset of the preceding ventricular tachyarrhythmia. In
  patients whose VF is preceded by sustained VT, a "5-minute VF prediction"
  window can contain the VT itself. That would be **detection of an ongoing
  arrhythmia**, not prediction. The protocol excludes windows that overlap
  sustained VT and adds a sensitivity analysis whose event is the first
  sustained VT.
- **One event per patient.** Each VF patient contributes exactly one onset, so
  there is no within-patient repeated-event structure. The recording usually
  ends at or shortly after VF, as resuscitation or death ends it.
- **Onset-time precision is unknown.** These are human-marked onsets on
  digitised analogue tape. The protocol's 2-minute lead exclusion absorbs
  plausible marking error, but the error is not quantified.

### 1.2 Sampling resolution

- At 250 Hz the sampling interval is 4 ms (to verify). That is adequate for RR
  intervals and QRS detection. For repolarisation intervals it is coarse:
  published pre-VT QT changes are of order 8 ms, which is two samples.
- **Morphology fidelity is the binding limit, not the sampling rate.** These
  are 1980s ambulatory analogue tapes with unknown frequency response,
  tape-speed variation and electrode motion. T-wave amplitude, ST level and
  microvolt T-wave alternans may be degraded in ways the data cannot reveal.
- **Effective sample size is favourable in this dataset, unlike every earlier
  dataset in the programme.** At beat resolution a 5-minute window holds about
  300–450 beats. With lag-1 autocorrelation of RR at 0.7–0.9,
  $n_{\mathrm{eff}} = n(1-\rho)/(1+\rho) \approx 16$–$50$, against
  $10p = 40$ for a 4-channel panel. That is **borderline**, so the protocol
  checks the $n_{\mathrm{eff}} \ge 10p$ gate on outcome-blind baseline data and
  lengthens the window to 10 minutes if the gate fails. This rule
  ([`DATASET_REQUIREMENTS.md`](DATASET_REQUIREMENTS.md) §2) is inherited
  unchanged.

### 1.3 Patient counts

| Group | Count (to verify) | Usable for |
|---|:--:|---|
| VF onset recorded | 20 | within-patient onset prediction |
| of which AF underlying | up to 4 | excluded from Analysis A (NN features undefined); **included in Analysis B** (NN-free panel, protocol §4.1) |
| of which onset earlier than $T_{\min}$ = 2 h 20 min | unknown until headers are read; records 48 and 52 (disclosed) lie just above it | excluded by the derived geometry rule (protocol §4.2), with sensitivity at 3 h and 4 h |
| **Plausible eligible VF patients** | **≈ 12–18 (A); ≈ 13–19 (B)** | a range, not a verified count |
| No VF | 3 (two paced) | false-alarm estimation only. Far too few for any between-patient comparison |

### 1.4 Data quality

- **Unaudited beat labels.** Most `.ari` annotations come from an automated
  analyser without full human review. PVC-versus-normal labelling errors become
  more likely as ectopy rises, which is exactly the period near onset. A
  labelling algorithm whose behaviour changes with rhythm is this dataset's
  version of the instrumentation rival $R_{\mathrm{instr}}$
  ([`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) §13–§17). The protocol
  therefore runs its own fixed QRS detector, treats detector–annotation
  disagreement as an artefact covariate, and never uses the `.ari` beat class
  as a model input without that covariate.
- **Recording artefacts can rise towards the end of a recording.** Electrode
  drying, patient activity and motion during symptoms can all do this. Any
  such monotone drift is perfectly confounded with "closer to onset" in a
  within-patient comparison. This is the dominant leakage route. See
  protocol §9.2.
- **No clock time, activity, medication timing or treatment events are
  expected.** Header demographics may be present but sparse, so circadian
  confounding cannot be controlled directly.

### 1.5 Limitations that bound every result

1. **Single source, single era, ≈ 20 events.** There is no independent site
   and no independent cohort inside the dataset.
2. **The dataset is heavily mined.** SDDB has been the standard sudden cardiac
   death "prediction" benchmark for over a decade. Any feature set or parameter
   chosen because it worked on SDDB in published work was **selected on these
   same patients**. The protocol forbids SDDB-tuned parameters and uses only
   generic, literature-standard definitions with fixed parameters. Even so,
   **SDDB cannot serve as a confirmatory set in the sense this programme uses**
   (never accessed and not used to design), because the community has already
   designed on it.
3. **No within-database patient-level negatives.** Three no-VF records, two of
   them paced, cannot support patient-level VF risk classification. The common
   workaround of comparing SDDB with the Normal Sinus Rhythm Database (NSRDB)
   confounds disease, age, recording equipment, sampling rate (NSRDB is
   commonly given as 128 Hz, to verify) and era with the label. That design is
   **not used** for any claim here. See protocol §2.
4. **Mechanism heterogeneity is unknown.** Ischaemic, autonomic,
   drug-proarrhythmic and fixed-substrate VF cannot be separated from the
   available data. [`TRANSITION_TAXONOMY.md`](TRANSITION_TAXONOMY.md) places
   "arrhythmic arrest from a fixed substrate" in **T6, the negative class where
   no precursor is expected**. SDDB VF cannot be assigned to T6 or excluded
   from it. That classification is preserved and recorded as prior evidence
   (protocol §1.3); it does not set an expected verdict.

---

## 2. Auxiliary datasets (roles only, all to verify)

| Dataset | Proposed role | Why not primary |
|---|---|---|
| BIDMC Congestive Heart Failure Database (`chfdb`) | **Transportability stress test for false-alarm rates only**, admissible only if the outcome-blind acquisition-comparability check passes (protocol §12.3). Severe structural heart disease, long Holter recordings, reported 250 Hz | Different recorder, digitisation, annotation process and population: its FAR is a property of a different acquisition chain. No VF events. Not a matched control for patient-level risk. **Not** used for pseudo-onset nulls of SDDB drift |
| Long-Term ST Database (`ltstdb`) | Candidate second stress-test set, if verified (ischaemic patients, long Holter) | Unverified; same transportability caveat |
| Spontaneous Ventricular Tachyarrhythmia Database (`mvtdb`) | Possible RR-only replication at the 5 and 10 min lead bins. Reported 135 event/control RR pairs from 78 ICD patients, ≈1,000 RR intervals each | RR-only, so univariate, and [`DATASET_REQUIREMENTS.md`](DATASET_REQUIREMENTS.md) §1 makes univariate evidence non-confirmatory for structural claims. ≈1,000 beats is about 10–15 min, which cannot reach the 15–30 min bins. Whether the controls are within-patient is unverified |
| NSRDB | **Methodological negative demonstration only.** Shows that database identity is separable from acquisition features alone | Confounded by construction. Prohibited from carrying any onset or risk claim |
| MIMIC-III/IV waveform, VTaC and similar ICU monitor datasets (credentialed) | Candidate **independent confirmatory cohort**, conditional on adjudicated VF onsets and ≥ 30 min of pre-onset ECG | Not verified. Needs credentialed access ([`CREDENTIALED_ACCESS_CHECKLIST.md`](CREDENTIALED_ACCESS_CHECKLIST.md)). Event yield unknown |

---

## 3. Sample-size verdict

> **SDDB supports exploratory analysis and the falsification of large effects.
> It does not support confirmatory testing of incremental predictive value at
> the effect sizes this programme has encountered.**

Arithmetic (paired per-patient contrast, two-sided, 80% power; simulated
t-test critical values). $\sigma_\Delta$ is the between-patient SD of the
per-patient ΔAUROC, which is unknown until the outcome-blind calibration
(protocol §11.3):

| eligible VF patients | α | detectable standardised effect | MDE at σ_Δ = 0.10 | 0.15 | 0.20 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 20 | 0.05 | 0.67 | 0.067 | 0.101 | 0.134 |
| 20 | 0.0125 (4 bins, Bonferroni) | 0.82 | 0.082 | **0.123** | 0.164 |
| 15 | 0.0125 | 0.97 | 0.097 | 0.146 | 0.194 |

Events needed to detect a given ΔAUROC at σ_Δ = 0.15 and α = 0.0125:
**0.10 → 26 · 0.05 → 101 · 0.03 → 279 · 0.02 → 628.**

For comparison, every incremental effect this programme has measured on real
data lies between −0.004 and +0.014 AUROC/AUPRC. **An SDDB null therefore
cannot exclude an effect of the size the programme has historically tested
for.** It can only exclude effects of roughly 0.10 AUROC or more. The protocol
therefore makes "large increment excluded" its binding falsification outcome
and caps every positive outcome at **EXPLORATORY SIGNAL**.

---

## Sources (as found by web search, not verified against files)

- [Sudden Cardiac Death Holter Database v1.0.0 (PhysioNet)](https://physionet.org/content/sddb/1.0.0/) · [archive listing](https://archive.physionet.org/physiobank/database/sddb/) · [38.hea](https://physionet.org/content/sddb/1.0.0/38.hea) · [48.hea](https://physionet.org/content/sddb/1.0.0/48.hea) · [52.hea](https://physionet.org/content/sddb/1.0.0/52.hea)
- [Trajectory Analysis of ECG Motif Dynamics in the Run-up to Sudden Cardiac Arrest (arXiv 2609.01543)](https://arxiv.org/pdf/2609.01543) — secondary source for sampling rate, durations, rhythm breakdown and audit status
- [Spontaneous Ventricular Tachyarrhythmia Database (PhysioNet)](https://physionet.org/content/mvtdb/) · [BIDMC CHF Database listing](https://physionet.org/physiobank/database/chfdb/)

---

© 2026 Davarn Morrison · Transition Dynamics
