# VF onset programme — readiness assessment (post-Phase 0)

> **Status: ASSESSMENT RECORD.** It combines the verified SDDB metadata
> ([`VF_PHASE0_DATASET_VERIFICATION.md`](VF_PHASE0_DATASET_VERIFICATION.md)),
> the independent review of v2
> ([`VF_V2_INDEPENDENT_REVIEW.md`](VF_V2_INDEPENDENT_REVIEW.md)) and
> outcome-blind simulation checks
> ([`analysis/results/vf_phase0_sim_checks.json`](../analysis/results/vf_phase0_sim_checks.json)).
>
> - **No ECG sample was read. No pre-VF feature was computed. No model was
>   trained on outcome windows. The protocol is not frozen, and no VF
>   experiment was run.**
> - The seven hypotension outcomes, `CANONICAL_STATUS.md`, the frozen
>   protocols, the results and the source mathematics are unchanged.
> - Previously demoted mechanisms remain demoted.
> - Retrospective pre-onset association remains distinct from advance
>   prediction, and no clinical capability is claimed.

---

## 1. Provisional decisions applied (planning only, not a freeze)

| Decision | Applied as | Effect found |
|---|---|---|
| D1 | Analysis B (AF-inclusive, NN-free) secondary, reported separately | A is primary with **n = 16** |
| D2 | Large-effect exploratory screen, provisional $\mathrm{MDE}_{\max}$ = 0.25 ΔAUROC | **A fails it** under every simulated assumption set (§3) |
| D5 | $R_{\min}$ = 30 min, mandatory 60-min sensitivity analysis | A: 16 → 14 (48 and 52 drop) |
| D6 | Exploratory analysis permitted without clock time; circadian confounding retained as unresolved | clock time is unavailable for 9/16 and unverified for 7/16. The clock-matched control is non-evaluable |
| D9 | δ = 0.15, excluding only effects ≥ 0.15 | under H0 the flag fires in 50–63% (A) of studies [SIM] |
| D10 | Conservative multi-bin rule retained | power cost documented: stats-only rule MDE 0.29–0.30 on A, higher under the full rule |

**Not resolved here** (left open, per instruction): D3 (guard), D4 (event
definition), D7 (external false-alarm set), D8 (Ledoit–Wolf intensity).

---

## 2. Verified dataset facts that bear on readiness

| Fact | Source |
|---|---|
| 23 records, one per patient. 20 with VF onset; 40, 42 and 49 without | headers, page, `RECORDS` |
| 250 Hz, 2 ECG channels, 12-bit, format 212. Lead identity unrecorded. Records 39 and 47 at 4× coarser gain | headers |
| VF onset is **only** the header comment `#vfon` (elapsed time). **No VF or VT annotation exists in any file** | annotation vocabularies |
| Post-onset corroboration from audited `.atr` is possible for **10 of 20** VF records, **9 of 16** Analysis A patients | P5 check |
| Unaudited `.ari` labels post-onset tachyarrhythmia complexes as normal beats. It has no paced-beat code, and its AF rhythm labels contradict the clinical table | annotation checks |
| Eligible: **A 16 / 14 / 13 / 12** and **B 19 / 17 / 16 / 15** at 2 h 20 / 2 h 50 / 3 h / 4 h | verified onsets |
| Every eligible patient supplies all four bins geometrically: 3 / 5 / 5 / 15 positive windows, ≈ 1 effective observation per bin. Remote zones 40–1,268 min | geometry |
| Pseudo-onset subjects: A 10 VF + 2 no-VF; B 13 + 2 | geometry |
| Checksums: 109/109 files match the mirror's `SHA256SUMS.txt`. physionet.org itself is unreachable | Phase 0 §1 |

---

## 3. Can the dataset support an informative experiment?

### 3.1 Usable observations per horizon

- **Geometrically:** yes. 16 patients × {3, 5, 5, 15} windows.
- **Statistically:** each patient contributes about **one effective
  observation per bin**, so each bin is a 16-observation experiment.
- Sustained-VT exclusions, which cannot be counted until execution, can
  only reduce this.

### 3.2 Detecting large effects

| Set | Mean ΔAUROC needed for 80% power (stats-only rule, reference assumptions) [SIM] |
|---|:--:|
| **A, primary (16)** | **≈ 0.29–0.30** |
| A at 2 h 50 / 3 h / 4 h (14 / 13 / 12) | > 0.30 |
| B, secondary (19) | ≈ 0.25 |

- The full rule (with controls) needs more. The reference assumptions are
  favourable:
  - every patient has a same-direction, step-shaped, bin-aligned precursor;
  - minute-scale autocorrelation;
  - no missingness.
- Under slower autocorrelation, power at Δ ≈ 0.21 falls from 0.525 to 0.285.
  If half the patients lack the precursor, it falls to 0.035. **No
  simulated variant brings the A-set MDE to 0.25.**
- The best case (no heterogeneity) still needs ≈ 0.27–0.29.

**The study can detect only increments of roughly 0.3 AUROC beyond
conventional features.** For calibration:

- every incremental effect this programme has measured on real physiology
  lies between −0.004 and +0.014;
- a 0.3 increment *beyond* heart-rate, HRV and ectopy features would be
  extraordinary for any ECG statistic.

### 3.3 Excluding large effects

- The binding flag (δ = 0.15) fires in **62.5%** (step null) or **50.5%**
  (ramp null) of null studies on A [SIM].
- So **in 38–50% of worlds where there is no effect at all, the study can
  neither find nor exclude one.**
- Raising δ to 0.20 would make the flag fire more often. It would do so by
  excluding only effects that are larger still, which is a weaker claim.

### 3.4 Is the 0.25 informativeness threshold realistic?

No. Two outcomes are possible:

1. Under the simulated assumptions the gate would declare A
   UNRESOLVED-BY-DESIGN.
2. Under the outcome-blind recalibration in v2's plan, the result is
   **knife-edge on unestimable quantities** (heterogeneity and precursor
   shape) (independent review, F3 and Q6).

Raising $\mathrm{MDE}_{\max}$ to ≥ 0.30 so that the gate passes, or promoting
Analysis B (which passes at ≈ 0.25) to primary, would be lowering or
re-routing a threshold to obtain an executable result. **Neither is
recommended, and neither was done.**

### 3.5 Other blockers, independent of sample size

| # | Blocker | Repairable on SDDB? |
|---|---|:--:|
| B1 | v2 binding logic fails on null data: vacuous gates, the R ratio, the pipeline band (review F1–F2) | yes. Specification only |
| B2 | Invalid pseudo-onset test; anti-conservative LOPO intervals (F4–F5) | yes. Refit-based permutation or bootstrap |
| B3 | Annotation dependence: no VT labels, `.ari` mislabels tachyarrhythmia, no paced-beat labels for record 43 | partly. Needs an own beat classifier validated against `.atr` (10 records), which requires reading signal |
| B4 | Event labels uncorroborated for 7 of 16 A patients | only via a pre-specified **Phase 0b** that reads signal at the onset |
| B5 | Onset-locked and clock-locked confounds (F10) | **no**. Clock time is unavailable or unverified |
| B6 | Masking and SQI features absorb physiology (F8, F11) | partly. Needs a redesign |
| B7 | The simulation does not model the protocol's TD estimators (F7) | yes. Beat-level synthetic generator |

### 3.6 Would an alternative dataset or design be scientifically preferable?

**Yes.**

**Why a different dataset.** No repair of B1–B7 changes the binding
constraint: about **16 events from one era and one archive, with labels that
are only partly verifiable**. Rough scaling (MDE ∝ 1/√n from the n = 16
simulation) suggests that:

- about 60 eligible events would be needed for an MDE near 0.15;
- about 130 for 0.10;
- about 500 for 0.05.

**These are extrapolations, not simulated or established figures.** They
must be re-simulated for any candidate dataset.

**Requirements for an informative test of H-VF:**

- ≥ 60–130 adjudicated VF onsets, with documented onset annotation;
- ≥ 3 h of pre-onset multichannel-capable ECG per event;
- recorded clock time;
- an audited beat and rhythm reference;
- event-unconditional monitored time, to estimate false alarms honestly.

**Candidates to verify, none of them verified here:**

- credentialed ICU waveform archives with in-hospital VF (MIMIC-III/IV
  waveform matched subsets, which need adjudication);
- ICU ventricular-tachyarrhythmia alarm datasets on PhysioNet (e.g. VTaC);
  verify pre-event duration;
- ICD or wearable-defibrillator electrogram archives through collaboration.
  Note that the public `mvtdb` is RR-only and ≈ 10–15 min pre-event, so
  it is univariate and cannot reach the 15–30-min bins.

**A preferable role for SDDB:**

- **pipeline and label development** (beat-classifier validation against
  `.atr`, onset verification, measurement-level characterisation of drift
  and artefact, all outcome-blind);
- **plus a purely descriptive, non-inferential report** if one is ever
  wanted.

It is **not** a test of H-VF.

---

## 4. Findings, ranked

| # | Severity | Finding | Reference |
|:--:|:--:|---|---|
| R1 | **CRITICAL** | The primary analysis cannot meet the provisional informativeness threshold. Its MDE is ≈ 0.29–0.30 vs 0.25 under favourable assumptions, and worse otherwise | §3.2; review F3 |
| R2 | **CRITICAL** | The v2 binding logic labels typical null studies PIPELINE INVALID or ACQUISITION-EXPLAINED | review F1–F2 (author-verified: 98% and 88% of null studies) |
| R3 | **CRITICAL** | The event label is an undocumented header comment, uncorroborated for 7 of 16 primary patients. There are no VT/VF annotations | Phase 0 P0-1 |
| R4 | MAJOR | The large-effect falsification is unavailable in 38–50% of null worlds | §3.3 |
| R5 | MAJOR | Unaudited annotations are unusable near onset, and there are no paced-beat labels for record 43 | Phase 0 P0-2, P0-3 |
| R6 | MAJOR | The pseudo-onset test is invalid, and the LOPO intervals are anti-conservative | review F4–F5 |
| R7 | MAJOR | Circadian and onset-locked confounding remain capable of false associations (0.13 and 0.61 under the full rule [SIM]) | review F10; Phase 0 §4.4 |
| R8 | MAJOR | The controls can suppress genuine slow precursors and attribute physiology to acquisition | review F11 |
| R9 | MODERATE | The simulation does not model the protocol's TD estimators, masking or full rule | review F7, F8 |
| R10 | MODERATE | Lead identity is unrecorded, and two records have 4× coarser amplitude quantisation | Phase 0 P0-6 |
| R11 | MINOR | Provenance is checked against the mirror, not physionet.org | Phase 0 §1 |

---

## 5. Unresolved questions

1. Does the user want SDDB repositioned as a development and label-validation
   resource, with H-VF deferred to a larger dataset?
2. If H-VF is ever to be run on SDDB despite §3, who authorises the explicit
   relaxation of $\mathrm{MDE}_{\max}$? Under this programme's rules that
   would be a recorded threshold change, not a technicality.
3. Is a Phase 0b label verification acceptable? It would read ECG only in
   [onset − 2 min, onset + 2 min], with a pre-specified, automated VF/VT
   rhythm classifier, for the 7 uncorroborated A patients. It touches the
   sealed zone minimally, but it does touch it.
4. Which candidate external dataset should be verified first?

## 6. Recommended next actions (each needs approval)

1. **Do not freeze v2. Do not write a frozen v3 for SDDB.** The required
   repairs are listed in
   [`VF_PROTOCOL_V3_AMENDMENTS.md`](VF_PROTOCOL_V3_AMENDMENTS.md) for use
   with whichever dataset is chosen.
2. **Dataset search.** Verify one or two candidate event-rich datasets at the
   metadata level (allowlist the relevant hosts, or attach credentialed
   access), and re-simulate the design on their verified event counts.
3. **Optional SDDB development work, outcome-blind:**
   - validate a beat classifier against `.atr` in baseline and remote zones,
     with the sealed zone excluded;
   - characterise drift and artefact in remote zones only;
   - build the beat-level synthetic generator (review F7).
4. **Optional Phase 0b,** only if explicitly approved (§5 question 3).
5. **Allowlist `physionet.org`** to close the provenance gap.

---

## 7. Readiness classification

**NOT FEASIBLE WITH CURRENT DATA**

**Justification, from verified evidence.**

- **Sample size.** The verified primary set is 16 patients (Phase 0 §4.5).
  On their verified onset times, the design needs a mean ΔAUROC of
  ≈ 0.29–0.30 for 80% power under the most favourable simulated
  assumptions, and more under every less favourable variant. That misses
  the provisional informativeness threshold of 0.25 (D2), so the experiment
  cannot be informative about any plausibly sized increment.
- **Falsification.** The binding large-effect falsification at δ = 0.15
  fails to fire in 38–50% of null studies.
- **Labels.** The event label itself is uncorroborated for 7 of the 16
  primary patients, and the annotations cannot supply the VT, paced-beat or
  rhythm information the design requires.
- **Repairable, but not enough.** The logic defects (R2, R6) are repairable,
  but they do not change the sample-size constraint.
- **Thresholds kept.** Meeting the threshold would require lowering it or
  re-routing the primary analysis, and neither is done.

This classification concerns the **inferential test of H-VF on SDDB**. It is
not a finding about VF physiology or about Transition Dynamics, and it is
not a NOT SUPPORTED verdict: no outcome data were examined.

---

© 2026 Davarn Morrison · Transition Dynamics
