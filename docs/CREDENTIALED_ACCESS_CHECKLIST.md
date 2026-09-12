# Credentialed-access checklist — MIMIC-IV Gate 1

For a user who has obtained PhysioNet credentialed access. Follow in order.
**Credentialing does not make the experiment feasible. It only makes Gate 1
checkable.** Gate 1 may still fail.

Nothing in this checklist freezes a protocol, runs an experiment, or inspects a
deterioration outcome.

---

## 0. Data-handling rule — read before anything else

This repository is **public**. MIMIC-IV is governed by a data use agreement
that prohibits redistribution.

> **Do not commit any MIMIC-IV or MIMIC-IV Waveform content to this repository.**
> Not raw files, not record-level values, not `subject_id`s, not timestamps,
> not extracts, not plots containing record-level data.

Only the following may be committed: aggregate counts, pass/fail flags, the
software versions used, and prose describing what was checked. Anything
record-level stays on the credentialed machine.

---

## 1. Access required

| item | requirement |
|---|---|
| PhysioNet account | credentialed status |
| Training | CITI "Data or Specimens Only Research" (or the equivalent PhysioNet accepts at the time) |
| DUA | signed for **each** project separately |
| Project A | **MIMIC-IV** (clinical) |
| Project B | **MIMIC-IV Waveform** |

Both are required. Neither alone is sufficient: the clinical database supplies
intervention times and magnitudes, the waveform database supplies the response.

> **Note on naming.** Exact project names, version numbers, table names and
> column names in this checklist **must be read from the authoritative schema
> documentation you now have access to**, not taken from this document. They
> were not verifiable from the environment that wrote it. Where this file names
> a field, treat it as *the thing to locate*, not as a verified identifier.

---

## 2. Files and tables to obtain

**Clinical (MIMIC-IV)**

| purpose | table |
|---|---|
| patient and stay spine | `patients`, `admissions`, `icustays` |
| interventions with time and amount | `inputevents` |
| procedures with time | `procedureevents` |
| ventilator settings, charted physiology | `chartevents` |
| item dictionary (to resolve item ids) | `d_items` |

**Waveform (MIMIC-IV Waveform)**

| purpose | file |
|---|---|
| record inventory | `RECORDS` (or the project's equivalent index) |
| per-record metadata: start time, duration, sampling frequency, channel list | record header (`.hea`) files |
| any provided patient↔record mapping | whatever linkage file the project ships |

---

## 3. Identifiers to join

1. `subject_id` — the patient spine. Confirm the waveform project uses the same
   `subject_id` space as the clinical project.
2. `hadm_id` and `stay_id` — confirm whether waveform records are linked at
   admission level, stay level, or neither.
3. Determine whether the mapping is **provided by the project** or must be
   **constructed** from `subject_id` plus record start time. Record which.

**If the linkage is admission-level only, Gate 1 fails** — admission-level
matching cannot support a perturbation-response experiment, regardless of
dataset size.

---

## 4. Timestamp fields to compare

| side | field to locate | what to establish |
|---|---|---|
| waveform | record header base date and time | what clock, what frame, what resolution |
| clinical | `inputevents.starttime`, `inputevents.endtime` | same questions |
| clinical | `icustays.intime`, `icustays.outtime` | used as the bracketing sanity check |

Establish, from documentation:

1. whether both sides are expressed in the **same per-patient date-shifted
   frame**;
2. whether the shift is **identical within a patient across both projects** —
   if it is not, alignment is impossible in principle and Gate 1 fails
   immediately;
3. the **stated precision** of the linkage.

---

## 5. Gate-1 verdict rules

Gate 1 is decided on checks 1–5 of
[`DATASET_REQUIREMENTS_MATCHED_STATE.md`](DATASET_REQUIREMENTS_MATCHED_STATE.md) §4a.

**PASS — all of:**
- documentation establishes the clock and frame on both sides;
- the date shift is documented as identical within a patient across both
  projects;
- the identifier mapping resolves to stay level or finer;
- on the manually inspected records (§6), waveform spans bracket recorded
  intervention times, and the implied offsets are **mutually consistent across
  records** — not a different apparent offset for every patient;
- check 6 (physiological timing) produces **no** systematic
  response-before-intervention pattern.

**FAIL — any of:**
- the date shift is not preserved across projects;
- linkage is admission-level only;
- inspected records show waveform spans that do not bracket intervention times;
- implied offsets are inconsistent across records;
- responses systematically **precede** the recorded intervention.

**UNRESOLVED — any of:**
- documentation is silent or ambiguous on the frame or the shift;
- too few records satisfy §6 to judge;
- results are mixed across records with no identifiable rule.

**UNRESOLVED is not a soft pass. Gate 2 does not begin on UNRESOLVED.**

### Interpretation of check 6, restated

- Response systematically **before** the intervention → **falsifies** alignment.
- Response **after** the intervention → **does not establish** alignment.
  Delays, absent responses, noise, concurrent care and imperfect charting all
  make a plausible lag compatible with a wrong alignment.

Check 6 can only take Gate 1 away. It can never grant it.

---

## 6. Minimum manual inspection before automating

Inspect **by hand, one at a time**:

- **≥ 20 distinct patients**, and
- **≥ 20 intervention events** drawn from at least **3 different intervention
  types**, and
- at least **5 patients with more than one waveform record**, to test whether
  the mapping holds across record boundaries.

Rationale: fewer than this cannot distinguish a consistent global offset from
per-record chaos, and automation applied to a misaligned join produces
confident, uniformly wrong results — a failure this programme has already
recorded twelve times in other forms.

Do not write extraction code until the manual pass is complete.

---

## 7. Evidence to save to this repository

A single file, `analysis/results/mimic_gate1_verification.json`, containing
**aggregates only**:

```
{
  "date": "...",
  "projects": {"clinical": "<name and version>", "waveform": "<name and version>"},
  "documentation_frame_clinical": "...",
  "documentation_frame_waveform": "...",
  "shift_identical_within_patient_across_projects": true | false | "undocumented",
  "linkage_granularity": "admission" | "stay" | "record" | "constructed",
  "n_patients_inspected": 0,
  "n_events_inspected": 0,
  "n_intervention_types": 0,
  "n_events_waveform_brackets_intervention": 0,
  "offset_consistency": "consistent" | "inconsistent" | "undetermined",
  "check6_response_before_intervention": true | false | "undetermined",
  "gate1_verdict": "PASS" | "FAIL" | "UNRESOLVED",
  "notes": "..."
}
```

Plus a short prose note in `docs/` recording what the documentation said, in
your own words, with a citation to the section you read.

**No `subject_id`s. No timestamps. No record identifiers. No waveform values.**

---

## 8. Conditions under which Gate 2 may begin

All four must hold:

1. `gate1_verdict == "PASS"`;
2. the evidence file in §7 is committed;
3. the prose note citing the documentation is committed;
4. the manual-inspection minimums in §6 were met **before** any extraction code
   was written.

Gate 2 then measures **temporal coverage**: how many intervention events have
≥ 10 min of continuous pre-perturbation and ≥ 30 min of continuous
post-perturbation waveform on the required channels. Gate 2 has its own failure
mode — a patient may have a waveform record without having waveform *at the
times that matter* — and must be measured, not assumed.

Gate 3, event yield after isolation rules, begins only if Gate 2 passes.

**No deterioration outcome may be inspected during Gates 1–3.**

---

## Related

- [`DATASET_REQUIREMENTS_MATCHED_STATE.md`](DATASET_REQUIREMENTS_MATCHED_STATE.md) — requirements and the standing conclusion **C**
- [`STATE_COMPLETENESS_TEST.md`](STATE_COMPLETENESS_TEST.md) — the design that challenges any observed history effect
- [`CANDIDATE_VENTILATOR_EXPERIMENT.md`](CANDIDATE_VENTILATOR_EXPERIMENT.md) — feasible secondary experiment, not frozen

---

© 2026 Davarn Morrison · Transition Dynamics
