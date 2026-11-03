# VT/VF programme — research roadmap and recommendation

> **Status: RECOMMENDATION FOR REVIEW.**
>
> - Nothing here authorises execution, freezing or preregistration.
> - The SDDB finding (**NOT FEASIBLE WITH CURRENT DATA**) is preserved.
> - The seven hypotension results, `CANONICAL_STATUS.md`, the frozen
>   protocols and the source mathematics are unchanged.
> - Demoted objects remain demoted.
> - **A dataset limitation is not a falsification of the Transition Dynamics
>   hypothesis.**

## 1. Scientific question and what each stage can establish

> Do measurable changes in multivariate physiological structure precede
> sustained ventricular tachyarrhythmia onset, and do TD estimators add
> information beyond conventional ECG features?

| Stage | Data | What it can establish | What it cannot establish |
|---|---|---|---|
| **0. Access and verification** (next) | candidate archives, metadata only | whether any dataset meets the §4 informativeness rule of the feasibility document | anything about VT/VF |
| **1. Development** | open, mined data (SDDB, VFDB, CUDB, MVTDB, VitalDB Arrhythmia NSVT); outcome-blind portions of the target archive | pipeline correctness; beat-classifier and artefact-detector validation; drift/artefact characterisation; synthetic end-to-end validation | **any** inferential claim |
| **2. Frozen retrospective hypothesis test** | an independent archive meeting the informativeness rule, e.g. **≥ 80 patients with a first sustained VT/VF, ≥ 40 in the smaller class**, ≥ 2 h 20 of pre-onset multichannel ECG, documented onsets, clock time | at most an **EXPLORATORY ASSOCIATION**: retrospective, VF/VT-conditional, within-patient pre-onset discrimination beyond conventional features (Claim Level ≤ 2) | prediction, early warning, mechanism, clinical utility |
| **3. External replication** | a second archive from a different site, vendor and era | replication (toward Level 5 language only if *also* mechanism-qualified) | prospective performance |
| **4. Prospective advance-warning study** | event-unconditional continuous monitoring, model frozen beforehand | genuine **advance prediction**: alarm burden, PPV at real prevalence, lead time | — |

**Retrospective pre-onset discrimination (stages 1–3) is not prospective
event prediction (stage 4).** No retrospective result, however strong, may
be described as advance warning or clinical capability.

## 2. Dataset strategy, chosen on scientific suitability

1. **Primary target for stage 2:** a full-disclosure, multi-lead ICU ECG
   archive with expert-adjudicated sustained VT/VF onsets.
   - Examples: the UCSF Alarm Study class (461 patients, 533 true VT alarms
     [S]), or a MIMIC-III/IV waveform event set built by a frozen, blinded
     adjudication protocol.
   - Either needs collaboration or credentialed access, plus a verified
     eligible-event count ≥ 80.
2. **External replication (stage 3):** a second, independent archive of the
   same class from a different vendor and site. Candidates are the ICU
   cohort of the J Electrocardiol 2010 study (≥ 12 h pre-event, documented
   mono/poly VT) or a hospital telemetry collaboration.
3. **Development (stage 1):** the open, community-mined datasets, used
   **only** for pipeline and detector validation. MVTDB may host a
   univariate, conventional-feature replication, clearly labelled as such.
4. **Not suitable:**
   - VTaC / Challenge 2015 for the minute-scale design (≈ 5 min pre-alarm),
     though they remain useful for seconds-scale or detector work;
   - ICD and wearable-defibrillator archives for 15–30-min horizons;
   - MUSIC, which supports risk, not onset.

## 3. Methodological issues carried forward, ranked

| # | Severity | Issue | Where addressed |
|:--:|:--:|---|---|
| M1 | **CRITICAL** | No verified dataset meets the informativeness rule | landscape §2; feasibility §5 |
| M2 | **CRITICAL** | Conventional-feature leakage into the TD residual: spurious positives ≈ 13% at n = 150 [SIM] | repair plan W1 / RP2 |
| M3 | MAJOR | Undetected artefact contaminates marginal TD statistics, making the correlation-only statistic the recommended primary (D-VT1) | repair plan §2.2 |
| M4 | MAJOR | Circadian / clock-locked confounding needs clock time | repair plan RP4 |
| M5 | MAJOR | VT vs VF heterogeneity: pooled endpoint C requires subgroup machinery | endpoint assessment §3 |
| M6 | MAJOR | Onset annotation reliability (alarm or device onset ≠ arrhythmia onset; SDDB header-only onsets) | endpoint assessment §5 |
| M7 | MODERATE | Label leakage is undetectable on data, so synthetic canaries and code guards are required | repair plan W2 / RP6 |
| M8 | MODERATE | Baseline-proximity bias needs a decorrelation gap | repair plan W3 / RP5 |

## 4. Recommended next steps (each needs approval)

1. **Network and access.**
   - Allowlist `physionet.org` (environment network settings), then verify
     VTaC, Challenge 2015 and MIMIC-III waveform metadata at the level of
     Phase 0.
   - Start credentialed access for MIMIC clinical linkage
     ([`CREDENTIALED_ACCESS_CHECKLIST.md`](CREDENTIALED_ACCESS_CHECKLIST.md)).
2. **Collaboration enquiries.** Approach the UCSF ECG Monitoring Research Lab
   (Alarm Study), THEW (data-use agreement and catalogue query for ICD/VT
   cohorts), and the authors of the J Electrocardiol 2010 ICU study. Each
   enquiry asks only for metadata: event counts, pre-onset durations, lead
   sets, clock time, annotation method.
3. **Repair work (synthetic and outcome-blind only).**
   - RP2: close or bound the conventional leakage, then **re-calibrate**.
   - RP5: decorrelation gap.
   - RP6: leakage canaries.
   - RP7: VT/VF subgroup machinery.
4. **Write a frozen-ready v3 protocol** only after a dataset passes stage 0.
   Use the repaired rule and the shape-primary statistic (if D-VT1 is
   accepted), and re-run the calibration on that dataset's verified n and
   onset distribution.

---

## 5. Final recommendation

1. **Strongest verified dataset candidate.** **None is adequate.**
   - The strongest *verified* VT/VF event set is **MVTDB**: 78 independent
     patients, 135 events (106 VT-labelled, 29 VF-labelled) [V]. But it is
     **RR-interval-only** with ≈ 10–15 min before each event, so the
     multivariate TD test cannot be run on it.
   - The strongest *scientific* candidate is an adjudicated full-disclosure
     ICU ECG archive (UCSF Alarm Study class, or MIMIC waveforms with
     adjudication). It is **unverified** and **not yet accessible**.
2. **Recommended primary endpoint.** **C: first sustained VT or VF, one per
   patient**, valid only with mandatory VT and VF subgroup estimates, a
   heterogeneity test and the "driven by one class" rule. Where those
   conditions cannot be met, test **A (VF) and B (sustained VT) separately**.
   NSVT stays development-only.
3. **Independent patients and events available.**
   - SDDB: 16 eligible primary patients for A [V].
   - MVTDB: 78 patients / 135 events, RR-only [V].
   - VitalDB Arrhythmia: 1 sustained VT [V].
   - VTaC: ≤ 2,376 patient records / 1,441 true VT alarms, ≈ 5 min pre-alarm
     [S].
   - **The eligible count for the target design is unknown for every
     candidate that could support it.**
4. **Can the verified data support a meaningful hypothesis test?** **No.**
   - The informative design needs ≈ 80 independent patients (≈ 300 for
     SESOI-level effects) with multichannel pre-onset ECG [SIM].
   - No verified dataset provides even the minimum.
5. **Minimum additional data and repairs.**
   - ≥ 80 independent patients with a documented first sustained VT/VF
     (≥ 40 in the smaller class), ≥ 2 h 20 (preferably ≥ 3 h) of pre-onset
     multichannel ECG, documented onset method, and clock time.
   - Repairs RP2 (conventional leakage), RP3 (validated real-data pipeline
     with measured artefact-detection sensitivity), RP4–RP7.
   - An informativeness check on the chosen dataset's verified n.
6. **Next research phase: CONDITIONAL GO**, for a **data-access and
   verification phase plus synthetic and outcome-blind repair work only**.
   It is conditional on network allowlisting, credentialed access or
   collaboration approval. **NO-GO for any real VT/VF hypothesis test**
   until a dataset passes the informativeness rule and the repairs are
   re-calibrated.

---

© 2026 Davarn Morrison · Transition Dynamics
