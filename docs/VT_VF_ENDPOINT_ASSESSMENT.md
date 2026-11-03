# VT/VF programme — endpoint assessment

> **Status: DESIGN RECORD.** No outcome data were examined. Dataset facts
> follow the evidence tags of
> [`VT_VF_DATASET_LANDSCAPE.md`](VT_VF_DATASET_LANDSCAPE.md):
> **[V]** verified, **[S]** secondary, **[U]** unresolved.

## 1. The four candidate endpoints, kept separate

| | Endpoint | Event definition | Mechanistic note |
|:--:|---|---|---|
| **A** | VF onset | first annotated ventricular fibrillation / flutter | frequently preceded by polymorphic VT, ischaemia or a trigger PVC |
| **B** | First sustained VT onset | first VT lasting ≥ 30 s (or terminated by therapy) | monomorphic VT is usually scar re-entry, a fixed substrate |
| **C** | First sustained ventricular tachyarrhythmia | first of B or A | the pooled endpoint |
| **D** | VT → VF transition | VF following documented VT within the same episode | a *within-arrhythmia* transition. Its pre-transition window is VT itself, so this is a different question |

**Non-sustained VT (NSVT) is not among A–D.** Where a dataset only supports
NSVT (VitalDB Arrhythmia, Icentia11k, MUSIC flags), it is labelled
**endpoint E (development only)** and never pooled with A–D.

## 2. Which datasets support which endpoint

| Dataset | A | B | C | D | E (NSVT) | Event unit |
|---|:--:|:--:|:--:|:--:|:--:|---|
| SDDB | 20 events in 20 patients [V]; primary-eligible 16 | ✗ no VT annotation [V] | ✗ (needs B) | ✗ | ✗ | patient (1 event) |
| MVTDB | 29 device-labelled VF records in 25 patients [V] | 106 VT-labelled records in 59 patients [V]; sustained by **device** criteria, not 30-s ECG criteria [U] | 135 events in **78 patients** [V] | ✗ | ✗ | episode (1–5 per patient) |
| VFDB | 13 VF/VFIB + 98 VFL episodes (≤ 22 records) [V] | 93 VT episodes [V]; sustained status per episode [U] | ✓ (≤ 22 records) | partly (VT→VFL/VF sequences visible in rhythm labels) [V] | — | record (many episodes) |
| CUDB | VF/flutter markers (34 records) [V] | 5 VT [V] | ✓ (≤ 35) | — | — | record |
| VTaC / Challenge 2015 | ✗ / VF-flutter alarms [S] | VT alarms: 1,441 true (VTaC) [S]; sustained vs non-sustained [U] | alarm-level [S] | ✗ | probably included in "true VT" [U] | alarm (≤ 5 per patient record) |
| VitalDB Arrhythmia | ✗ [V] | **1 patient** ≥ 30 s [V] | 1 | ✗ | 88 patients [V] | segment |
| MUSIC | SCD during follow-up only [V] | 3 patients flagged [V] | — | — | 346 flagged, no times [V] | patient |
| UCSF Alarm / ICU 2010 cohort / MIMIC adjudication | [S/U] | [S/U] | [S/U] | possible | possible | patient / episode |

## 3. Is a combined VT/VF primary endpoint (C) defensible?

**Arguments for pooling:**

- It maximises events.
- Clinically, both VT and VF are the life-threatening class.
- Several datasets (MVTDB, VTaC) do not adjudicate the VT/VF boundary
  reliably anyway.

**Arguments against pooling:**

1. **Mechanisms differ.** Monomorphic VT typically arises from a fixed
   re-entrant substrate. VF and polymorphic VT are more often linked to
   ischaemia, autonomic surges or repolarisation instability. The only
   multilead ICU study with ≥ 12 h pre-event ECG found weak pre-event
   trends before polymorphic VT and VF, and **none before monomorphic VT** [S].
2. **The taxonomy already separates them.** [`TRANSITION_TAXONOMY.md`](TRANSITION_TAXONOMY.md)
   places arrhythmic arrest from a fixed substrate in **T6, a no-precursor
   class**. Pooling a possibly-precursor class (polymorphic VT/VF) with a
   possibly-no-precursor class (monomorphic VT) averages opposite
   expectations, which the taxonomy prohibits for mechanistic conclusions.
3. **Prevalence asymmetry.** In MVTDB, VT records outnumber VF records
   3.7 : 1 [V]. A pooled effect would be dominated by VT.

**Recommendation.** C is acceptable as the primary endpoint **only** under
all of the following pre-specified conditions. Otherwise A and B are tested
separately and C is not used.

| # | Condition |
|:--:|---|
| C1 | One event per patient: the **first** qualifying event. Further events are secondary, aggregated within patient, never as independent units |
| C2 | Each subgroup (VT-first, VF-first; and monomorphic vs polymorphic where documented) has **≥ n_min independent patients**, from the statistical-feasibility rule, enough to estimate its own effect with a CI |
| C3 | Separate VT and VF subgroup estimates are reported in every table, with a pre-specified heterogeneity test (difference of subgroup means, patient-level) |
| C4 | **"Driven by one class" rule.** A pooled positive is reported as *class-specific*, not pooled, if:<br>(a) the subgroup point estimates differ in sign; or<br>(b) one subgroup's CI excludes 0 while the other's upper bound is below half the pooled estimate; or<br>(c) the heterogeneity test rejects at 0.05 |
| C5 | The mono/poly distinction, where documented, gets the same treatment. Without it, the "fixed-substrate" reading of a null cannot be examined, and that limitation is stated |
| C6 | Endpoint D (VT → VF) is **exploratory only** and is never pooled. Its "pre-event" window is an ongoing arrhythmia |

## 4. Event independence

- **A dataset of many episodes from few patients does not have the power of
  that many independent patients.** The primary analysis unit is the
  **patient**: the first event, plus pre-specified within-patient
  aggregation of later events as secondary.
- MVTDB's 135 events come from 78 patients, and 35 of those patients
  contribute 92 events [V].
- VTaC's events are clustered by up to 5 per patient record. The number of
  unique patients behind its 1,441 true alarms is [U].

## 5. Onset definition for each endpoint

| Endpoint | Onset | Guard | Notes |
|---|---|---|---|
| A | first VF/VFL annotation, or a documented `#vfon` with post-onset corroboration | 2 min (sensitivity 1 and 5) | Phase 0: SDDB onsets corroborated for 10/20 only [V] |
| B | first beat of the first VT run ≥ 30 s | 2 min | requires adjudicated rhythm labels; device or alarm onsets need re-adjudication |
| C | earlier of the A and B onsets | 2 min | as A and B |
| E | first beat of the first run of ≥ 3 consecutive V beats | 1 min | development only |

**Alarm-anchored data (VTaC, Challenge 2015).** The alarm time lags the
true onset by the detector latency. Onset must be re-adjudicated from the
waveform, which is a label-construction step. With about 5 min of
pre-alarm signal, only B5 is evaluable, and only partly.

## 6. Conclusion

| Question | Answer |
|---|---|
| Recommended primary endpoint | **C (first sustained VT or VF), patient-level**, under C1–C6. Otherwise **A and B separately** |
| Combined endpoint defensible? | **Yes, only with mandatory subgroup estimates and the "driven by one class" rule.** Pooling without them is not defensible, given the mechanistic and prevalence asymmetry |
| Endpoint usable on currently verified data | none for a multivariate TD test: MVTDB supports C only univariately and over ≈ 10–15 min, and SDDB supports A only (and is unsuitable) |

---

© 2026 Davarn Morrison · Transition Dynamics
