# VF onset programme — independent review of the v2 statistical design

> **Status: REVIEW RECORD.**
>
> - Subject: [`VF_PROTOCOL_DRAFT.md`](VF_PROTOCOL_DRAFT.md) v2 (commit
>   `e52b116`), its design simulation
>   [`analysis/vf/design_sim.py`](../analysis/vf/design_sim.py), and
>   [`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md).
> - **Not frozen. No VF experiment run. No ECG sample read.** Every number
>   here is from **synthetic** simulation, or from verified **metadata**
>   ([`VF_PHASE0_DATASET_VERIFICATION.md`](VF_PHASE0_DATASET_VERIFICATION.md)).
> - The hypotension record and `CANONICAL_STATUS.md` are unchanged.

## How the review was done

1. **Unanchored pass.** A separate reviewer agent received only the
   protocol, the simulation code, its JSON output and the ten audit
   questions. It was given none of the author's conclusions. It ran small
   numerical checks (< 120 replicates each) and modified no file.
2. **Author pass.** Logic read-through of §3, §11 and §13, plus new
   simulation checks
   ([`analysis/vf/phase0_sim_checks.py`](../analysis/vf/phase0_sim_checks.py),
   output [`analysis/results/vf_phase0_sim_checks.json`](../analysis/results/vf_phase0_sim_checks.json)):
   - the power curve on the **verified** onset times;
   - an assumption-sensitivity grid;
   - an independent seed;
   - an exact same-seed reproduction.
3. **Verification of the reviewer's CRITICAL claims.** These were rerun
   independently by the author on 60 fresh pure-null studies before being
   accepted (§2, F1–F2).

**Labelling.** Throughout, **[SIM]** marks behaviour demonstrated in
simulation, which says nothing about SDDB. **[ASSUMPTION]** marks a premise
about real physiology or recordings that no part of this work has tested.
**[LOGIC]** marks a property of the protocol text itself.

---

## 1. Findings, ranked

| # | Severity | Finding | Evidence | Source |
|:--:|:--:|---|---|:--:|
| F1 | **CRITICAL** | **Gates 3–4 fire on null results.** "Fails in every bin that would otherwise pass" is vacuously true when no bin passes. Gate 3 also fires on R ≥ 0.70 alone, and R = (AUROC(M0) − 0.5)/(AUROC(M3) − 0.5) has a near-zero, sign-changing denominator under H0. **A typical null study would be labelled ACQUISITION-EXPLAINED, not NOT SUPPORTED** | [LOGIC] §13.1 items 3–4. [SIM] reviewer: R ≥ 0.70 in ≥ 1 bin in 74% of null studies. **Author reproduction (60 pure-null studies): 88%; R < 0 in 44%** | both |
| F2 | **CRITICAL** | **The pipeline gate rejects valid pipelines.** "Each model's mean AUROC within 0.45–0.55" under shuffled onsets is far narrower than the null sampling spread of a ~20-patient cohort mean | [SIM] author reproduction: cohort-mean AUROC SD 0.06–0.09 under a pure null. **The band fails in 98% of valid null studies** (reviewer: 97.5%) | both |
| F3 | **MAJOR** | **The verified eligible set makes the primary analysis uninformative at the provisional threshold.** On the 16 verified Analysis-A onset times, the rule needs mean ΔAUROC ≈ **0.29–0.30** for 80% power, above $\mathrm{MDE}_{\max}$ = 0.25 | [SIM] §3.1 below | author |
| F4 | **MAJOR** | **The pseudo-onset test is invalid.** Its null resamples only *which* offset each subject contributes (most have 1–2), so it ignores the sampling variance of the observed mean. Under a pure null it passes 15–30% of the time (nominal 5%) | [LOGIC/SIM] `design_sim.py` pseudo block; protocol §9.2.1. Reviewer measurement, mechanism confirmed by the author's code reading | reviewer |
| F5 | **MAJOR** | **Patient-level intervals are anti-conservative under LOPO.** Folds share n − 2 of n − 1 training patients, so the Δᵢ are positively correlated. SD(mean Δ)/mean SE is 1.12–1.49; 95% coverage is 84–92% | [SIM] reviewer. Author: per-bin false-pass rate under null 43/4,800 = **0.90%** against a nominal ≤ 0.625% (Poisson z = 2.4) | both |
| F6 | **MAJOR** | **"MDE ≈ 0.23 per bin" is mislabelled.** It is the stats-only *decision-rule* 80% point at n = 20. The per-bin 80% MDE is ≈ 0.24–0.25. Under the simulated full rule power falls to 0.70 at that effect, so the full-rule MDE is ≈ 0.25–0.27 | [SIM] JSON `power_step30.n20_b2.0`, `rules.P1` | reviewer |
| F7 | **MAJOR** | **The simulated TD features are not the protocol's TD features.** The simulation uses linear 5-min mean shifts; the protocol uses non-negative distances (S, ΔG), 256-beat windows and a thresholded 30-min integral (TD-3). Linear channel drift becomes non-linear in those features, which is exactly where detrending fails | [LOGIC] §7.4 vs `design_sim.py` `make_patient` | reviewer |
| F8 | **MAJOR** | **Artefact masking is degenerate.** A 99th-percentile threshold from a 30-min baseline of slowly wandering features masks ≈ 88% of post-baseline windows under a stationary null | [SIM] reviewer (not in `design_sim.py`) | reviewer |
| F9 | **MAJOR** | **Annotation dependence is not implementable.** Verified: no VT/VF rhythm annotations exist, and `.ari` labels tachyarrhythmia complexes as normal. The v2 NN series, ectopy features, sustained-VT exclusion and NSVT sensitivity relied on annotation labels | Phase 0 §4.2–4.3 | author |
| F10 | **MAJOR** | **Uncontrolled false-positive routes remain under the full rule.** Onset-locked artefact barely visible in SQI: 0.61. Clock-locked surge: 0.13. Verified clock time is unavailable (9/16) or unverified (7/16) | [SIM] `rules.S4`, `rules.S5`; Phase 0 §4.4 | both |
| F11 | **MAJOR** | **The controls can suppress genuine precursors.** Remote-zone detrending absorbs an hours-long precursor; pseudo-onsets at −3 h contain the same precursor; SQI features respond to physiological ectopy, ischaemia and agitation, which can push a real effect into ACQUISITION-EXPLAINED | [LOGIC]. [SIM] P1 0.80 → 0.70; P2 (with drift) 1.00 → 0.54 | both |
| F12 | MODERATE | **Verdict branches are missing or contradictory.** One passing B15/B30 bin has no verdict. TRIGGER-PROXIMAL needs one bin but EXPLORATORY two. HARM can co-occur with EXPLORATORY. Condition 5 (alarms) is undefined per bin. One bin with < 6 patients voids the whole study | [LOGIC] §13.1–13.2, §5.1 | reviewer |
| F13 | MODERATE | **"More conservative verdict governs" has no defined ordering**, and covers only 2 h 20 vs 3 h | [LOGIC] §4.2, §13.4 | reviewer |
| F14 | MODERATE | **H0 / H1 are not complements, and H0 is mis-centred.** Uninformative TD features give E[Δ] ≈ −0.01 to −0.02 (overfitting cost). The directional tests should be stated one-sided. The sign test is unadjusted while the t-test is Bonferroni-adjusted | [LOGIC] §3, §11.1. [SIM] every b = 0 cell | reviewer |
| F15 | MODERATE | **δ = 0.15 is a valid intersection-union test, but chosen for informativeness, not substance.** Its H0 firing rate is helped by the negative bias in F14 and the anti-conservative SE in F5. It excludes only the mean Δ of this fixed-λ LOPO model, not subgroup effects | [LOGIC/SIM] §3.2 below | both |
| F16 | MODERATE | **Elapsed-time matching tests the raw TD composite, not the increment.** A conventional precursor passes it through the TD–M1 correlation | [LOGIC] §9.2.3 | reviewer |
| F17 | MODERATE | **The guard result assumes onset-aligned integer leads.** On a 60-s grid not aligned to $T_{\mathrm{VF}}$, a B5 window can end at lead 2 + ε. "g = 2 removes contamination" holds only for marking error < 2 min | [LOGIC] §5.1; simulation §5 | reviewer |
| F18 | MINOR | **Simulation-document errors.** "≤ 19 offsets" is wrong (≤ 5 are used; `N_PSEUDO_DRAWS` is unused). The < 60-min remote-zone SD row rests on ≈ 2.7% of patients, i.e. Monte Carlo noise, and cannot inform D5. The protocol's pseudo-onset floor is 8 but the code uses 6. Undefined R counts as a pass in the code | [LOGIC] code vs docs | reviewer |
| F19 | MINOR | **The λ = 1 scale (sum vs mean loss) is undefined** in the protocol. With summed loss over thousands of windows it is effectively unpenalised | [LOGIC] §7.5 | reviewer |

**No coding error was found that changes a reported number.** `t_quantile`
matches scipy within 0.003 for df ≥ 5. `binom_sf`, `auroc` and the ridge
back-transform are correct. The reporting errors are F6 and F18.

---

## 2. Verification of the CRITICAL findings

Author rerun (script kept in the session scratchpad, not committed):

- 60 fresh pure-null studies: n = 20, no conventional precursor, no TD
  increment, LOPO over M1, M4, M3 and SQI.
- R ≥ 0.70 in at least one bin: **88%** of studies. Per bin: 37.9%.
  R < 0: 44%.
- Cohort-mean AUROC SD: 0.06–0.09. The 0.45–0.55 band fails for at least
  one of M1/M4 × 4 bins in **98%** of studies.

Both CRITICAL findings are therefore confirmed. **As written, v2 would
usually end a valid null study at PIPELINE INVALID or ACQUISITION-EXPLAINED.
Its binding logic cannot be frozen.**

---

## 3. Answers to the ten audit questions

**Q1. Are null, alternative, tests and verdict logic consistent? No (CRITICAL).**

- See F1, F2, F12, F13 and F14.
- The t-interval (two-sided 0.0125, i.e. one-sided 0.00625) and the sign
  test (one-sided 0.025, unadjusted) are compatible only because they are
  combined with AND.
- The large-effect flag (§13.3) is internally sound as an
  intersection-union test.

**Q2. Is patient-level uncertainty correct? Partly (MAJOR).**

- Inference is correctly at the patient level, and window-level inference is
  correctly prohibited. [SIM] Hanley–McNeil is ×3.2 too narrow.
- But leave-one-patient-out dependence makes the t-interval anti-conservative
  by ×1.1–1.5 (F5).
- **Repair:**
  - a patient bootstrap that **refits the full LOPO** in every replicate, or
  - a patient-level permutation test with refitting, calibrated on the
    pseudo-onset structure.

**Q3. Does the simulation represent the protocol? Not adequately for its
controls (MAJOR).**

| Element | Simulation | Protocol |
|---|---|---|
| M1 features | 4 | 10 |
| TD features | linear 5-min means | baseline distances, 256-beat windows, TD-3 integral |
| M0 for R | 1 SQI feature | 8 |
| Pseudo-onset floor / draws | 6 / 999 | 8 / 9,999 |
| Lead grid | integer, onset-aligned | 60-s grid, not aligned |
| Verdict categories | TRIGGER-PROXIMAL and single-bin collapsed | separate |

**Not simulated:** masking, lead replication, condition 5, gates 1–2,
eligibility governance, VT exclusion, missingness, beat-level estimation,
M2, comparators, Analysis B.

The simulation is adequate for **overlap, effective-sample-size and
power-scaling** questions. It is **not** adequate for the behaviour of the
TD estimators or the full rule.

**Q4. Is the 0.23 MDE reproducible? Yes, as a rule-level figure under its
own assumptions; mislabelled as per-bin (F6).**

| Check | Result |
|---|---|
| Independent seed (7), n = 20, step30 | rule power 0.56 / **0.835** / 0.92 at mean Δ ≈ 0.18 / **0.24** / 0.27. Committed: 0.55 / 0.815 / 0.95 at ≈ 0.18 / 0.23 / 0.29 |
| Exact same-seed rerun of the committed `power` stage | **bit-identical** to the committed JSON (max abs difference 0.0; `reproduction` in `vf_phase0_sim_checks.json`) |

On the verified eligible sets it is not 0.23 (§3.1).

**Q5. Is δ = 0.15 statistically justified? As a test, yes. As a substantive
threshold, no (F15).**

- "Upper bound < δ in all four bins" is a valid intersection-union test at
  one-sided 0.05.
- It falsely excludes a true Δ ≈ 0.18 in ≤ 0.5% of studies [SIM].
- Under H0 on the verified sets it fires in only **50–75%** of studies
  (§3.2), so the falsification is still **unavailable in roughly a quarter
  to a half of null worlds**.
- It is asymmetric with the confirmation burden (0.05 per bin vs 0.00625 +
  sign test + two bins). Asymmetry in favour of falsification is acceptable
  here, but must be declared.

**Q6. Do the assumptions matter? Yes, strongly.**

[SIM] sensitivity grid on the verified A set (n = 16), step30, latent b = 2:

| assumption varied | mean ΔAUROC (B5–B30) | rule power |
|---|:--:|:--:|
| reference (φ 0.9, heterogeneity 0.5, ρ 0.5, all responders) | 0.21–0.23 | 0.525 |
| no heterogeneity | 0.24–0.29 | 0.80 |
| heterogeneity SD 1.0 | 0.16–0.17 | 0.235 |
| slower autocorrelation φ 0.97 | 0.20–0.22 | **0.285** |
| TD–M1 correlation ρ 0.2 / 0.8 | 0.22–0.25 / 0.20–0.23 | 0.53 / 0.495 |
| only 50% of patients have the precursor | 0.09–0.11 | **0.035** |

- **Effect heterogeneity and the physiological autocorrelation timescale
  dominate.** Neither is estimable outcome-blind.
- **[ASSUMPTION]** Every power figure assumes all patients share a
  same-direction precursor with a step shape aligned to the bins. Real
  pre-VF change, if any, is unlikely to be that homogeneous.

**Q7. Are overlap, heterogeneity and multiplicity handled correctly?**

- **Overlap:** correct at the patient level.
- **Multiplicity:** Bonferroni over four bins is conservative because the
  bins share data. The two-bin requirement adds little independent evidence,
  because TD-3 makes bins nearly identical.
- **Heterogeneity:** not handled. A few-patient effect is invisible to the
  mean and sign test, and "≤ 2 patients drive the mean" has no criterion.
- The §13.5 comparator tests have no α.

**Q8. Do the temporal controls constrain drift? Partly, and less than v2
claims.**

| Confound | [SIM] result | But |
|---|---|---|
| Linear elapsed-time drift | removed by detrending | F7: linear channel drift is non-linear in S, ΔG and TD-3 |
| Accelerating drift | removed by elapsed-time matching | only because the simulated drift slope is **shared** across patients (4 ± 1). Patient-specific drift escapes |
| Any drift | pseudo-onsets partly help | the pseudo-onset test is invalid (F4) |
| Drift tied to recording end or behaviour | escapes all three | — |

**Q9. Can event-related artefacts and circadian effects still generate false
associations? Yes.**

- [SIM] Full-rule false-positive rate is 0.61 for an onset-locked artefact
  barely visible in SQI, and 0.13 for a clock-locked surge.
- [ASSUMPTION] Whether such artefacts exist in SDDB is unknown.
- [Phase 0] Clock time cannot be recovered for most patients.

**Q10. Could the controls suppress genuine changes? Yes (F11).**

- Slowly developing precursors are absorbed by detrending, and contaminate
  the pseudo-onset null.
- Physiological changes leak into SQI features: ectopy raises detector
  disagreement, ischaemia shifts R amplitude, agitation raises noise power.
  They can then be attributed to acquisition.
- The grey zone, the guard and the VT/NSVT sensitivities remove
  trigger-proximal and intermediate signal by design.
- [SIM] True long-lead precursor: 0.80 → 0.70. With co-existing drift:
  1.00 → 0.54.

### 3.1 Power on the verified eligible sets [SIM; verified onset labels only]

Step30 (sustained long-lead precursor). Reference assumptions, 200
replicates each.

| set (n) | mean ΔAUROC ≈ 0.23 | ≈ 0.27–0.28 | ≈ 0.30 | 80% rule MDE (stats-only rule) |
|---|:--:|:--:|:--:|:--:|
| A, 2 h 20 (16) | 0.54 | 0.695 | 0.835 | **≈ 0.29–0.30** |
| B, 2 h 20 (19) | 0.685 | 0.87 | — | ≈ 0.25 |
| A, 2 h 50 (14) | 0.485 | 0.635 | — | > 0.30 |
| A, 3 h (13) | 0.41 | 0.585 | — | > 0.30 |
| A, 4 h (12) | 0.42 | 0.575 | — | > 0.30 |

- For a trigger-weighted precursor (ramp30) on A (16), rule power is 0.415
  even when B5 Δ ≈ 0.29.
- **The full-rule MDE is higher than all of these** (F6 and F8: power loss
  from the controls).

### 3.2 Large-effect flag under H0 on the verified sets [SIM]

P(upper bound < δ in all four bins | H0):

| set | δ 0.10 | **δ 0.15** | δ 0.20 |
|---|:--:|:--:|:--:|
| A 2 h 20 (step null / ramp null) | 0.375 / 0.315 | **0.625 / 0.505** | 0.815 / 0.725 |
| B 2 h 20 | 0.51 | 0.745 | 0.915 |
| A 2 h 50 / 3 h / 4 h | 0.44 / 0.415 / 0.28 | 0.655 / 0.645 / 0.495 | 0.805 / 0.795 / 0.65 |

---

## 4. Demonstrated vs assumed

| Demonstrated in simulation (properties of the statistical machinery) | Assumed about real data (untested) |
|---|---|
| Window overlap gives ≈ 1 effective observation per patient per bin; patient-level inference handles it | that real feature autocorrelation is minute-scale (φ ≈ 0.9). Slower dynamics halve power |
| Window-level SEs are ×3.2 too narrow | that any precursor is homogeneous, same-direction and step-shaped |
| The LOPO t-interval is ×1.1–1.5 too narrow | the size and form of drift and artefacts in SDDB |
| AIRM falls ≈ 9% for +10% beats with no structural change | that `#vfon` marks true onset to within ≈ 2 min (verified only post-onset, for 9 of 16 A patients) |
| Which control catches which *simulated* confound | that SQI features capture recording artefacts without capturing physiology |
| The v2 gate and pipeline logic fails under null data | — |

---

## 5. Unresolved questions

1. **Can any statistic be pre-specified for the informativeness gate**,
   given that the MDE depends on precursor heterogeneity and shape, which are
   not estimable outcome-blind? (F3, Q6)
2. **What valid pseudo-onset test is possible** with 10–13 subjects having
   pseudo-onsets? Candidate: paired per-patient true-minus-pseudo Δ with a
   patient-level test. (F4)
3. **How can acquisition be separated from physiology** when the SQI
   features respond to both? (F8, F11)
4. **Is label verification (Phase 0b) acceptable** under the sealed-zone
   policy? See the readiness assessment.

---

© 2026 Davarn Morrison · Transition Dynamics
