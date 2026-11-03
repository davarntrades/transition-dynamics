# VT/VF programme — Phase-1 dataset verification (CONDITIONAL GO phase)

> **Status: VERIFICATION RECORD.** Metadata and documentation only.
>
> - No ECG sample, RR value or pre-event physiological feature was read.
> - No enquiry was sent.
> - Evidence tags as in [`VT_VF_DATASET_LANDSCAPE.md`](VT_VF_DATASET_LANDSCAPE.md):
>   **[V]** verified from primary files, **[S]** secondary source,
>   **[U]** unresolved.

## 1. Access status (exact blocker)

| Target | Result (2026-11-03) | Consequence |
|---|---|---|
| `https://physionet.org/content/vtac/1.1/`, `.../challenge-2015/1.0.0/RECORDS`, `.../mimic3wdb/1.0/RECORDS` | **refused by the session egress proxy** (`CONNECT` → 403, `connect_rejected`, policy denial) | the primary files of VTaC, Challenge 2015 and the MIMIC waveform DBs cannot be read |
| PhysioNet open-data mirror `physionet-open.s3.amazonaws.com` | reachable. **No `vtac`, `challenge-2015`, `mimic3wdb`, `mimic3wdb-matched` or `mimic4wdb` prefixes** [V] | no alternative primary copy |
| `storage.googleapis.com/mimic3wdb/` | 404 | — |
| PMC, NeurIPS proceedings, Zenodo, THEW, ECRI, Dryad | refused | publication full texts unavailable; search snippets only |

**Required configuration.** Add `physionet.org` (and, for full texts,
`proceedings.neurips.cc`, `pmc.ncbi.nlm.nih.gov`) to the environment's
*Allowed domains*. MIMIC clinical linkage additionally needs PhysioNet
credentialed access
([`CREDENTIALED_ACCESS_CHECKLIST.md`](CREDENTIALED_ACCESS_CHECKLIST.md)).
Until then **nothing below is upgraded from [S] to [V]**.

## 2. Candidates against the four requirements

The four requirements are:

- **R1:** ≥ 80 independent patients (≥ 40 in the smaller of VT/VF).
- **R2:** adjudicated, spontaneous, sustained VT/VF onset times.
- **R3:** multichannel pre-event ECG ≥ 2 h 20 min.
- **R4:** usable within-patient control periods (≥ 30-min remote zone ≥ 60 min
  before onset).

| Candidate | R1 independent patients | R2 adjudicated sustained onsets | R3 multichannel pre-event | R4 control periods | Status |
|---|---|---|---|---|---|
| **VTaC v1.0/1.1** | ≤ 2,376 patient records; 1,441 true VT alarms; per-patient count **[U]** [S] | alarm-level true/false adjudication by ≥ 2 annotators [S]; sustained vs non-sustained **[U]**; onset = **alarm time** | multichannel ECG + PPG/ABP, 250 Hz [S]; pre-alarm length **conflicting (5 vs 10 min)** [S] | **no** (≈ 5 min pre-alarm) | fails R3, R4 for the minute-scale design |
| **Challenge 2015** | 750 public + 500 hidden alarms; per-patient **[U]** [S] | expert true/false alarm labels [S] | 5 min before alarm, ECG + ABP/PPG [S] | **no** | fails R3, R4 |
| **MIMIC-III WDB / matched subset** | thousands of ICU stays [S]; VT/VF count **[U]** (no labels) | **none**: must be built (chartevents codes as a starting point, then waveform adjudication) [S] | 1–3 ECG leads + ABP/PPG, continuous [S] | yes, in principle | **R2 missing**: an adjudication project |
| **MIMIC-IV WDB v0.1.0** | 200 records / 198 patients [S] | none | ECG, PPG, BP [S] | yes, in principle | too small; later releases **[U]** |
| **MIMIC-III-Ext-CA** | 31 patients, 36 cardiac-arrest episodes [S] | manually reviewed arrests (PPG-focused) [S] | from the MIMIC matched subset [S] | **[U]** | too few; arrest ≠ VT/VF onset |
| **MIMIC-III-Ext-PPG** | table lists VT 53, VF 9 "entries" (unit **[U]**) [S] | rhythm labels for PPG segments [S] | PPG-centred | **[U]** | not an onset set |
| **UCSF Alarm Study** | 461 ICU patients; 533 true VT alarms [S] | expert alarm annotation [S]; sustained **[U]** | full-disclosure multi-lead ECG [S] | likely (continuous) | **sharing unconfirmed**: enquiry draft U1 |
| **UVA ICU monitoring archive** | 9,232 ICU admissions (2009–2015) [S]; VT/VF **[U]** | **[U]** | ECG waveforms archived [S]; Dataverse doi:10.18130/V3/MKY17T (a different study) [S] | likely | enquiry draft V1 |
| **ICU short-term-prediction cohort** (J Electrocardiol 2010;43:400–7, PMID 20378124) | 38 events + 30 controls [S] | sustained mono/poly VT and VF, documented [S] | ≥ 12 h multilead [S] | yes | too small for R1; external-replication candidate; enquiry draft I1 |
| **Asan CICU** (Lee et al., Sci Rep 2016) | 52 VT events + 52 controls [S]; patients **[U]** | **[U]** | monitor ECG + respiration [S] | ≥ 1 h [S] | enquiry draft A1 |
| **Mayo ICD electrograms** (Heart Rhythm 2024) | 13,516 patients [S] | device-detected | intracardiac EGM, seconds to minutes [S] | no | wrong modality and horizon |
| **THEW** | > 3,700 Holters (2012) [S]; ICD/VT content **[U]** | **[U]** | Holter, 24 h [S] | yes | enquiry draft T1 |
| *Verified open sets* (SDDB, MVTDB, VFDB, CUDB, VitalDB Arrhythmia, MUSIC) | see the landscape document [V] | — | — | — | none meets R1–R4 [V] |

## 3. Conclusion of Phase-1 verification

- **Strongest *verified* candidate: unchanged.** MVTDB is the largest
  verified VT/VF event set (78 patients, 135 events) [V], but it is RR-only
  and ≈ 10–15 min pre-event, so it fails R3 and R4. SDDB fails R1.
- **Strongest *plausible* candidates (all [S]/[U]):**
  1. the UCSF Alarm Study, which plausibly meets R1, R3 and R4, with R2
     needing confirmation that onsets are sustained and adjudicated;
  2. a MIMIC-III waveform adjudication project, which plausibly meets R1,
     R3 and R4, with R2 to be built and verified;
  3. the UVA archive (unknown).
- **No candidate verified in this phase meets R1–R4.** The verification
  itself is blocked for the open PhysioNet candidates by network policy, not
  by dataset absence.

## Sources (secondary)

- [VTaC paper (NeurIPS 2023)](https://proceedings.neurips.cc/paper_files/paper/2023/file/7a53bf4e02022aad32a4019d41b3b476-Paper-Datasets_and_Benchmarks.pdf) · [VTaC v1.0 on PhysioNet](https://physionet.org/content/vtac/1.0/) · [VT false-alarm algorithm (PMC10685155)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10685155/)
- [Challenge 2015 paper (Clifford et al., CinC 2015)](https://lcp.mit.edu/pdf/CliffordCinC2015.pdf) · [Challenge 2015 data (Zenodo)](https://zenodo.org/record/4634014)
- [MIMIC-III-Ext-CA](https://physionet.org/content/mimic-iii-ext-ca/1.0.0/) · [MIMIC-III-Ext-PPG](https://physionet.org/content/mimic-iii-ext-ppg/1.1.0/) · [MIMIC-IV WDB v0.1.0](https://physionet.org/content/mimic4wdb/0.1.0/waves/p137/p13724605/81178488/) · [MIMIC-IV ECG module](https://mimic.mit.edu/docs/iv/modules/ecg)
- [UVA ICU monitoring cohort (PMC4987175)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4987175) · [UVA continuous-ECG study](https://typeset.io/pdf/cardiorespiratory-dynamics-measured-from-continuous-ecg-2j99bjto7p.pdf)
- [ICU 2010 study record (PMID 20378124)](https://pesquisa.bvsalud.org/ses/resource/pt/mdl-20378124) · [THEW (PMC2989667)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989667)

---

© 2026 Davarn Morrison · Transition Dynamics
