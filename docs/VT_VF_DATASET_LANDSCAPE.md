# VT/VF programme — dataset landscape

> **Status: FEASIBILITY RECORD. Metadata only.**
>
> - No ECG sample, RR value or pre-event physiological feature was read or
>   analysed.
> - No VT/VF hypothesis test was run. No protocol is frozen.
> - The earlier finding that **SDDB is unsuitable for the primary hypothesis
>   test**
>   ([`VF_READINESS_ASSESSMENT.md`](VF_READINESS_ASSESSMENT.md): NOT FEASIBLE
>   WITH CURRENT DATA) is preserved unchanged. Widening the endpoint does not
>   rescue it (§3).
> - The seven hypotension results, `CANONICAL_STATUS.md`, the frozen
>   protocols and the source mathematics are unchanged.
>
> Reproduce: `python3 -I analysis/vtvf/landscape_verify.py <workdir> analysis/results/vtvf_dataset_metadata.json`
> (output: [`analysis/results/vtvf_dataset_metadata.json`](../analysis/results/vtvf_dataset_metadata.json)).

## 0. Evidence classes and access path

| Tag | Meaning |
|:--:|---|
| **[V]** | Verified from primary dataset files on PhysioNet's open-data mirror (`https://physionet-open.s3.amazonaws.com/`): file listings, headers, `RECORDS`, documentation tables, rhythm-label annotations |
| **[S]** | Secondary source only: web-search snippets of project pages or publications. **Not verified** |
| **[U]** | Unresolved: not determinable from available evidence |

Access constraints in this session:

- `physionet.org`, PMC, NeurIPS proceedings, Zenodo, THEW, ECRI and Dryad
  are all refused by the egress proxy.
- Only the S3 mirror and GitHub are reachable. Third-party GitHub copies of
  datasets are outside this session's repository scope and were **not**
  read.
- VTaC, PhysioNet Challenge 2015 and the MIMIC waveform databases are **not
  on the open mirror** [V]. Everything below about them is [S].

Read policy, the same as Phase 0: headers, documentation and **event labels
only**.

- For the RR-only `mvtdb`, beat annotations were read only for **pooled**
  per-record counts and spans, never split by event type, because the RR
  series is itself the pre-event physiology.

---

## 1. Comparison table

| Dataset | Access / licence | Independent patients | VT events | VF events | Multiple events per patient | Sustained vs NSVT | Mono vs poly | Spontaneous? | Channels / fs | Pre-onset recording | Onset annotation | Clock time | Key confounders / limits | Prior mining | Verdict for H-VT/VF |
|---|---|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|---|
| **SDDB** (`sddb`) | open, ODC-By [V] | 23 (20 with VF) [V] | not annotated [V] | 20 onsets (header comment only) [V] | no, 1 per patient | not annotated | not documented | yes [V] | 2 ECG, 250 Hz [V] | 1.5–24.6 h; primary-eligible 16 [V] | undocumented `#vfon`; corroborated for 10/20 [V] | absent or placeholder for most [V] | unaudited labels wrong near onset; 1980s analogue tape; digoxin/quinidine [V] | heavy [S] | **unsuitable** (preserved) |
| **MVTDB** (`mvtdb`) | open [V] | **78** [V] | **106** VT-labelled records [V] | **29** VF-labelled records [V] | **yes**: 1–5 per patient (43 single; 35 contribute 92 events) [V] | ICD-detected episodes; not adjudicated by ECG [V/S] | history fields only, not per episode [V] | yes ("spontaneous") [S] | **RR intervals only** (0 signals; ICD QRS times at 1 ms) [V] | 986–1,024 beats; pooled span 9.2–19.6 min (median 12.5) [V] | **onset position not annotated** [V]; at series end per secondary text [S] | episode date/time for 58/78 [V] | 43/57 on antiarrhythmics [V]; device sensing/detection; ICD therapy post-onset | heavy (CinC 2010, HRV papers) [S] | **no** multivariate TD test (univariate; ≤ 10–15 min) |
| **VFDB** (`vfdb`) | open [V] | ≤ 22, **same tapes as SDDB** [V] | 93 `(VT` episodes [V] | 9 `(VF` + 4 `(VFIB` + 98 `(VFL` episodes [V] | yes (many episodes per record) [V] | episodes rhythm-labelled [V] | not documented | yes | 2 ECG, 250 Hz [V] | 35-min excerpts; first ventricular label at median 15.2 min (0.7–30.7); only **1** record ≥ 30 min [V] | reference rhythm annotations [V] | [U] | **not independent of SDDB**; excerpts selected around events | heavy (VF detection; Mandala 2020) [S] | **no** (no remote zone; not independent) |
| **CUDB** (`cudb`) | open [V] | 35 [V] | 5 `(VT` [V] | 2 `(VF`; VF/flutter onset markers in 34 records [V] | few | — | — | yes [S] | **1** ECG, 250 Hz [V] | 8.5-min records; ≤ 8.3 min pre-onset [V] | onset markers [V] | [U] | single lead; excerpted | heavy (VF detectors) [S] | **no** |
| **INCART** (`incartdb`) | open [V] | 32 (75 records) [V] | **no VT/VF rhythm labels** [V] | none [V] | — | — | — | — | 12-lead, 257 Hz [V] | 30 min | — | — | — | moderate | **no** |
| **VitalDB Arrhythmia** (`vitaldb-arrhythmia`) | open [V] | 482 surgical; **88** with a `VT` label [V] | VT runs: median longest **2.7 s**; **1 patient ≥ 30 s** [V] | none labelled [V] | yes (≤ 17 runs) [V] | **essentially all non-sustained** [V] | — | yes (intraoperative) | ECG (beat/rhythm labels); source VitalDB is multichannel [S] | first VT label median 38 min; 16 patients ≥ 2 h 20 [V] | anaesthesiologist-validated, but **only on classifier-screened segments**, so first VT is not guaranteed [V] | VitalDB timestamps [S] | anaesthesia and drugs; **source overlaps the VitalDB hypotension cohorts** | low [S] | NSVT development only |
| **MUSIC SCD** (`music-sudden-cardiac-death`) | open (licence file present) [V] | **992** HF patients [V] | Holter flags: 346 NSVT, **3 sustained VT**, 1 TdP; **no episode times** [V] | SCD **during follow-up** (94; median 1,805 days) [V] | — | flags only | — | — | 3 orthogonal leads (X, Y, Z), 200 Hz, ≈ 23 h [V] | events occur months to years later | none at episode level [V] | Holter start time for 650 [V] | HF drugs, devices (11 ICD) [V] | moderate | **E-risk only, not onset** |
| **Icentia11k** (`icentia11k-continuous-ecg`) | open, CC BY-NC-SA [V: on mirror] | 11,000 [S] | **no VT label**; V beats only [S] | none [S] | — | derivable NSVT runs only | — | yes | 1 lead, 250 Hz [S] | up to 2 weeks [S] | technologist beat/rhythm labels (N, S, V, Q; NSR, AFib, AFL) [S] | [U] | single patch lead | moderate | NSVT development only |
| **AHA database** (ECRI) | **purchase/licence** [S]; 2 sample records on mirror [V] | ≈ 155–160 records [S] | VT class [S] | VF/flutter class (8001–8010 in the dev set) [S] | [U] | [U] | [U] | yes [S] | 2 ECG [S] | 3-h records, **last 30 min annotated** [S] | expert beat annotations in the last 30 min [S] | [U] | era and selection [S] | moderate [S] | possible small external VF set [U] |
| **VTaC** | open on PhysioNet [S]; not on mirror [V] | ≤ 2,376 patient records [S] | **1,441 true VT alarms** among 5,037 adjudicated [S] | none (VT alarms only) [S] | yes (≤ 5 events per record) [S] | alarm-level; includes non-sustained [U] | [U] | yes [S] | ECG leads + PPG/ABP, 250 Hz [S] | **≈ 5 min** before alarm (sources conflict: 5 vs 10-min segments) [S] | **alarm time**, not adjudicated arrhythmia onset [S] | [U] | three vendors; alarm-selected | **heavy** (false-alarm benchmark) [S] | B5 only; onset ≠ alarm |
| **PhysioNet Challenge 2015** | open [S] | [U] | 562 VT alarms (total) [S] | VF/flutter alarms [S] | [U] | alarm-level | [U] | yes | multichannel ECG + ABP/PPG [S] | ≈ 5 min [S] | alarm time [S] | [U] | alarm-selected | heavy [S] | B5 only |
| **MIMIC-III/IV waveform** | open (III waveform) / credentialed (clinical) [S] | thousands [S] | **unlabelled**: needs detection + adjudication [S] | unlabelled [S] | yes | adjudication-defined | adjudication-defined | yes | 1–3 ECG leads + ABP/PPG, 125 Hz [S] | long (continuous stays) [S] | none, must be built | time-of-day preserved under date-shift [S] | treatment, ICU care, gaps | moderate [S] | **candidate after an adjudication project** [U] |
| **UCSF Alarm Study** | **collaboration**, sharing unconfirmed [S] | 461 ICU patients [S] | **533 true VT alarms** (3,860 annotated) [S] | [U] | yes [S] | [U] | [U] | yes | full-disclosure multi-lead ECG [S] | continuous [S] | expert alarm annotation [S] | likely [U] | ICU care | moderate [S] | **strong candidate if accessible** [U] |
| **ICU short-term-prediction study** (J Electrocardiol 2010) | private [S] | 38 with events + 30 controls [S] | mono VT, poly VT, VF [S] | yes [S] | [U] | **documented** [S] | yes | multilead [S] | **≥ 12 h** [S] | [U] | [U] | — | low | collaboration only |
| **Asan CICU** (Lee 2016) | private [S] | [U] | 52 VT events + 52 controls [S] | [U] | [U] | [U] | [U] | yes | monitor ECG + respiration [S] | ≥ 1 h [S] | [U] | [U] | 1/3 test split | — | collaboration only |
| **Mayo ICD electrograms** (Heart Rhythm 2024) | private [S] | 13,516 [S] | VT/VF episodes [S] | yes | yes | device-defined | [U] | yes | intracardiac EGM [S] | device-stored (seconds to minutes) [S] | device-labelled | device clock | ICD therapy | — | collaboration; EGM, not surface ECG |
| **WEARIT-II / ZOLL LifeVest** | private [S] | 2,000 (US) / 892 (EU) [S] | arrhythmia events [S] | yes | [U] | device-defined | [U] | yes | WCD ECG [S] | **≈ 30 s stored pre-event** [S] | device | device | — | — | **no** (pre-onset too short) |
| **THEW** (Rochester) | DUA [S] | > 3,700 Holters from 13 studies [S] | ICD/VT cohort **unverified** [S] | [U] | [U] | [U] | [U] | — | Holter [S] | 24 h [S] | [U] | [U] | — | — | to be queried |
| Leipzig Heart Center (`leipzig-heart-center-ecg`) | open [V] | 39 (29 children, 10 adults) [V] | EP-lab arrhythmias [V] | — | — | — | — | **procedural / induced** [V: README] | 12-lead + intracardiac [V] | procedural | expert [V] | — | catheter manipulation | low | **no** (not spontaneous) |
| SHAREE, TWADB, Fragment DB | open [V] | — | — | — | — | — | — | — | — | — | — | — | vascular events / 2-min TWA records / derived fragments of other DBs | — | **no** |

---

## 2. Findings, ranked

| # | Severity | Finding | Evidence |
|:--:|:--:|---|---|
| L1 | **CRITICAL** | **No verified, accessible dataset combines the four things the test needs:** documented sustained VT/VF onsets, ≥ 30–60 min of multichannel-capable pre-onset ECG, many *independent* patients, and clock time | table §1 |
| L2 | **CRITICAL** | **The largest verified VT/VF event set (MVTDB, 78 patients, 135 events) is RR-only.** The programme's multivariate TD estimators cannot be computed on it, univariate evidence is non-confirmatory by the programme's own rule ([`DATASET_REQUIREMENTS.md`](DATASET_REQUIREMENTS.md) §1), and only ≈ 10–15 min precede each event | [V] 0 signals; 986–1,024 beats |
| L3 | MAJOR | **Event-rich ICU alarm sets (VTaC, Challenge 2015) are alarm-anchored with ≈ 5 min of pre-alarm signal.** Only the 2–5-min bin is even partly covered, and the onset is the monitor alarm, not adjudicated arrhythmia onset | [S] |
| L4 | MAJOR | **Repeated events cluster heavily within patients** (MVTDB: 35 of 78 patients contribute 92 of 135 events). Effective n is the patient count, at most | [V] |
| L5 | MAJOR | **VFDB and SDDB are not independent** (same Greenwald tapes), so VFDB cannot replicate an SDDB result | [V] SDDB page text |
| L6 | MAJOR | **VitalDB Arrhythmia VT is essentially all non-sustained** (1 of 88 patients ≥ 30 s), with labels only on screened segments. Its source overlaps the VitalDB hypotension cohorts | [V] |
| L7 | MAJOR | **The open datasets have been mined extensively** for VF detection and "prediction" (SDDB, VFDB, CUDB, MVTDB, VTaC, Challenge 2015). Any reuse is development-grade, not confirmatory | [S] |
| L8 | MODERATE | **The strongest scientific candidates are all behind collaboration or adjudication barriers**: the UCSF Alarm Study's full-disclosure ICU ECG, an adjudicated MIMIC waveform event set, ICU cohorts with ≥ 12 h pre-event recording | [S] |
| L9 | MODERATE | **ICD and wearable-defibrillator archives store seconds to minutes pre-event** and are electrograms or device ECG. They support seconds-scale questions, not 15–30-min horizons | [S] |

## 3. Why widening the endpoint does not rescue SDDB

SDDB has **no VT rhythm annotations** [V]. Its unaudited beat labels call
tachyarrhythmia complexes normal [V]. A VT or VT/VF endpoint would therefore
need new VT adjudication of the 1980s tapes. The patient count stays at 23,
and the VT-before-VF information sits inside the sealed pre-onset zone. The
Phase 0 classification **NOT FEASIBLE WITH CURRENT DATA** stands.

## 4. Strongest candidates, ranked by scientific suitability (not convenience)

1. **A full-disclosure ICU ECG archive with expert-adjudicated sustained VT/VF**
   (UCSF Alarm Study class).
   - Hundreds of patients, continuous multi-lead ECG, long pre-onset, clock
     time, independent annotations.
   - **Access unconfirmed: a collaboration is required.**
2. **MIMIC-III/IV waveforms plus a pre-registered, blinded adjudication of
   sustained VT/VF onsets.**
   - Open waveforms with long pre-onset and time-of-day.
   - Requires building and validating the event set, and fewer ECG leads.
   - Verifiable only after `physionet.org` is allowlisted.
3. **VTaC**, for a seconds-to-5-minute sub-question only, with multichannel
   ECG + PPG/ABP. The onset must be re-adjudicated from alarm time.
4. **MVTDB**, for a *univariate, conventional-feature* replication only
   (within-patient controls exist). Not a TD test.
5. **AHA database** (licensed), as a small external VF set, if the 2.5 h
   before the annotated half hour is usable.

**No currently verified dataset supports the frozen hypothesis test.**

## 5. Evidence gaps and access routes

| Gap | Route |
|---|---|
| VTaC, Challenge 2015, MIMIC waveform metadata | allowlist `physionet.org` (environment network settings), then verify headers and labels at metadata level; credentialed access for MIMIC clinical data ([`CREDENTIALED_ACCESS_CHECKLIST.md`](CREDENTIALED_ACCESS_CHECKLIST.md)) |
| UCSF Alarm Study sharing terms | contact the UCSF ECG Monitoring Research Lab (Drew, Pelter) with a data-use proposal |
| THEW ICD/VT cohorts | THEW data-use agreement and catalogue query |
| AHA database event positions | ECRI licence; verify that the event lies in the annotated last half hour |
| ICU ≥ 12-h pre-event cohort (J Electrocardiol 2010) | contact the authors |
| Mono vs poly VT documentation | only adjudication-based sources (UCSF / MIMIC adjudication / ICU cohort) can provide it |

## Sources

Search-derived; marked [S] above and not verified against primary files.

- [VTaC on PhysioNet](https://physionet.org/content/vtac/) (Lehman et al., NeurIPS 2023 Datasets & Benchmarks; doi:10.13026/jg2e-tf67)
- [Spontaneous Ventricular Tachyarrhythmia Database](https://physionet.org/content/mvtdb/) · [AHA DB on PhysioNet (excluded sample)](https://physionet.org/content/ahadb/) · [ECRI AHA ECG database](https://www.ecri.org/Products/Pages/AHA_ECG_DVD.aspx)
- [Icentia11k](https://physionet.org/content/icentia11k-continuous-ecg/)
- [Lee et al. 2016, Sci Rep](https://www.nature.com/articles/srep32390) · [Failure in short-term prediction of VT/VF in ICU (J Electrocardiol 2010)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2914842/) · [Mandala et al. 2020, PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0231635)
- [ML on ICD electrograms (Heart Rhythm 2024)](https://www.heartrhythmjournal.com/article/S1547-5271(24)02634-1/abstract) · [VTaC foundation-model study](https://www.sciencedirect.com/science/article/abs/pii/S0883944125003661) · [VT-onset timing study (PMC12794901)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12794901)
- [UCSF Alarm Study summary (eScholarship)](https://escholarship.org/content/qt0qm283mp/qt0qm283mp.pdf?t=rzh2j9) · [WEARIT-II registry](https://lifevest.zoll.com/medical-professionals/clinical-research-results/wearit-ii-registry) · [THEW overview (PMC3483367)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3483367)

---

© 2026 Davarn Morrison · Transition Dynamics
