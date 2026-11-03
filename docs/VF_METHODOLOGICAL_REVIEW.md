# VF onset programme — methodological review of draft protocol v1

> **Status: REVIEW RECORD.** This document reviews
> [`VF_PROTOCOL_DRAFT.md`](VF_PROTOCOL_DRAFT.md) as committed at `4f9e5a4`
> (v1). The protocol has since been revised to **v2** in the same file. The
> v1 text remains available in git history.
>
> - Nothing was frozen, no VF experiment was run, and no SDDB, chfdb or NSRDB
>   record was read.
> - Quantitative statements come from the **synthetic** design simulation
>   ([`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md)), never from real
>   data.
> - The seven hypotension outcomes and their canonical status
>   ([`CANONICAL_STATUS.md`](CANONICAL_STATUS.md)) are unchanged.
>   `git diff main` touches only `docs/VF_*`, `analysis/vf/` and
>   `analysis/results/vf_design_sim.json`.
> - **v2 must be independently reviewed before any execution.**

Severity scale:

- **CRITICAL**: could produce a false positive or a meaningless verdict as
  written.
- **MAJOR**: materially biases a result, its interpretation or its
  uncertainty.
- **MODERATE**: weakens the design without invalidating it.
- **MINOR**: documentation or presentation.

---

## Summary table

| # | Severity | Finding | Review item | Resolved in v2? |
|:--:|:--:|---|:--:|:--:|
| F1 | **CRITICAL** | Temporal confounding: v1's controls left accelerating drift partly uncaught; onset-locked and clock-locked confounds are uncatchable by timing | 3 | partly. Controls strengthened; residual blind spots declared (R1, R2) |
| F2 | **CRITICAL** | Power and MDE were analytic approximations with an assumed SD. Simulation roughly doubles the MDE | 2 | yes (numbers replaced). Whether to run is open (D2) |
| F3 | **CRITICAL** | The binding falsification flag (δ = 0.10) fires in < half of null studies, so the "binding" outcome was usually unavailable | 2 | proposal δ = 0.15 (D9) |
| F4 | **MAJOR** | A declared "expected outcome", and positive-only scrutiny, prejudged the result | 1 | yes |
| F5 | **MAJOR** | Overlapping windows: about 1 effective positive per bin; window-level SEs 3.2× too small; window-count alarm rule nearly ineffective; nominal FAR not realised | 4 | yes |
| F6 | **MAJOR** | ΔG estimator unspecified, and fixed-duration windows tie it mechanically to heart rate | 8 | yes |
| F7 | **MAJOR** | Discovery vs prediction blurred ("EXPLORATORY SIGNAL", "advance warning") | 10 | yes |
| F8 | **MAJOR** | AF exclusion is a rhythm-based selection, with no structured alternative | 7 | yes (Analysis B). Its status is open (D1) |
| F9 | **MAJOR** | External no-VF FAR set (chfdb) has a different acquisition chain and population | 9 | yes (hierarchy and comparability check). Choice open (D7) |
| F10 | **MAJOR** | Guard / VT exclusion could remove precursors, with no audit or sensitivity grid | 5 | yes. Residual limits declared (R3) |
| F11 | MODERATE | Eligibility (2 h 15) was an unjustified sum placed just below two disclosed onsets; the 12-patient minimum was arbitrary | 6 | yes (derived geometry, sensitivity, capability floor). Open (D5) |
| F12 | MODERATE | Pseudo-onset null had no availability rule or composition caveat | 3 | yes |
| F13 | MODERATE | Elapsed-time matching in v1 would have used in-sample LOPO scores | 3 | yes (unfitted composite) |
| F14 | MODERATE | The decision rule is very conservative (type I ≈ 0–0.5%), which inflates the MDE | 2 | declared, not changed (D10) |
| F15 | MODERATE | ΔG mechanically re-expresses autocorrelation and variance (M2 / M1 content) | 8 | yes (M1 ∪ M2 attribution, comparators) |
| F16 | MINOR | Unverified dataset facts and citations | — | unchanged. Phase 0 |

---

## F1 — CRITICAL — temporal confounding (item 3)

**Problem.** Positive windows are always later than remote windows, so any
change correlated with time separates them. v1 required pseudo-onsets and
detrending, and treated elapsed-time matching as secondary.

**Test.** Simulated artefacts, each scaled to give alone the same raw
within-patient separation as a strong precursor
([`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) §4). Values are
false-EXPLORATORY-ASSOCIATION rates at n = 20:

| confound | primary test | v1 controls (pseudo + detrend) | v2 (+ elapsed-time matching) | v2 full (+ SQI gate) |
|---|:--:|:--:|:--:|:--:|
| linear elapsed-time drift | 0.85 | 0.00 | 0.00 | 0.00 |
| accelerating drift | 0.69 | **0.17** | 0.02 | 0.02 |
| onset-locked artefact, visible in SQI | 0.91 | **0.86** | 0.76 | 0.00 |
| onset-locked artefact, barely visible | 0.82 | **0.79** | 0.71 | **0.61** |
| clock-locked surge, morning VF | 0.22 | 0.16 | 0.14 | **0.13** |

**Findings.**

- **Pseudo-onsets alone remove only about half of linear elapsed-time drift
  (0.85 → 0.46), and less of accelerating drift (0.69 → 0.49).** They sit
  earlier in the recording than the true onset, where accelerating drift is
  slower.
- v1's pair of controls left a 17% false-positive rate under accelerating
  drift. Elapsed-time matching closes this gap.
- **No temporal control can remove onset-locked change**, because it is
  indistinguishable from a precursor by timing alone. Symptom-related motion,
  electrode problems near collapse, or tape effects tied to the event would
  all qualify.
- Clock-locked confounding passes everything unless clock time exists.

**Changes in v2.**

- All three temporal controls are required.
- A capability table and the simulated rates are in protocol §9.2.
- A mandatory reporting clause covers onset-locked and circadian limits.
- Elapsed-time matching is precisely specified (F13).
- Clock-time matching applies if the headers provide start times.

**Residual (R1, R2), not fixable in a retrospective single-database design.**

- R1: onset-locked non-physiological change is excluded only to the extent
  the SQI features see it.
- R2: circadian confounding is not excluded without clock time.

Both are recorded as permanent limits. Neither is "passed".

## F2 — CRITICAL — sample size and MDE (item 2)

**Problem.** v1 used a paired-t formula with an assumed SD of 0.15, which
gave an MDE of about 0.12. It ignored patient clustering with ≈ 1 effective
positive per bin, LOPO fitting noise, effect heterogeneity, and the four-bin
conjunctive rule.

**Test.** Full Monte Carlo of the protocol (§2 of the simulation).

**Findings.**

- The null SD of per-patient Δ is 0.16–0.21, rising to 0.25–0.31 under
  heterogeneous effects.
- The 80%-power MDE is **≈ 0.23** per bin at n = 20 and > 0.30 at n = 12.
- Power for effects of the size this programme has measured (≤ 0.014) is
  ≈ α.

**Changes in v2.** The analytic tables are withdrawn and simulated numbers
are used throughout. The outcome-blind informativeness gate reruns the
simulation on real outcome-blind parameters.

**Open (D2).** Is a large-effect screen worth running? Proposed gate:
$\mathrm{MDE}_{\max}$ = 0.25. At 0.20 the gate would probably fire.

## F3 — CRITICAL — the binding falsification was usually unavailable (item 2)

**Finding.** At n = 20, the v1 flag "upper bound < 0.10 in all four bins"
fires in only 38% (ramp-null) to 53% (step-null) of null studies. In
practice the "binding falsification" would usually not bind.

**Change.** δ = 0.15 is proposed. It fires in 66–81% of null studies, and in
≤ 0.5% of studies whose true effect is ≥ 0.18. The permitted language now
states that smaller effects, including every effect size previously
measured, are not excluded.

**Open (D9).**

## F4 — MAJOR — prejudged outcome (item 1)

**Problem.** v1 §3 declared "Expected outcome … NOT SUPPORTED". v1 §1.3
treated positive results as "suspicious first". The between-database demo
was "expected to separate".

**Changes in v2.**

- The declaration is removed.
- H0-VF is stated explicitly as the binding falsification target.
- Negative prior evidence is recorded alongside the literature on
  conventional pre-onset change. None of it enters the decision rule.
- Outcome-dependent scrutiny is replaced by a **symmetric** integrity audit
  that runs for every verdict.
- The T6 classification and every binding criterion are kept.

## F5 — MAJOR — overlapping windows (item 4)

**Findings** (simulation §3).

- Lag-1 window correlation is 0.985, with a correlation length of about
  15–20 min. The bins hold 3, 5, 5 and 15 windows, which is about 1, 1, 1
  and 1–2 effective observations.
- A 5-min stride gives the same null SD as a 1-min stride. Overlap adds no
  information and does not bias patient-level inference.
- Hanley–McNeil window-level SEs underestimate the true within-patient
  variability by **3.2×**.
- v1's "≥ 2 consecutive windows" rule barely filters. Even a 3-minute
  persistence rule keeps 74–83% of single-window alarms.
- The realised held-out FAR is biased upward and widely scattered. A nominal
  0.5/h gave a mean of 0.61, a median of 0.36 and a 10th–90th percentile
  range of 0–1.75.

**Changes in v2.**

- Patient-level inference only, with window-level inference prohibited.
- A persistence-in-time alarm rule.
- The **realised** FAR distribution is reported, never the target.
- The "60-s grid gives timing resolution, not information" statement.

## F6 — MAJOR — ΔG estimator (item 8)

**Problem.** v1 said the ΔG estimator would be "decided at freeze".

**Finding.** In fixed-duration windows, the beat count is set by heart rate.
Simulated AIRM under no change falls from 0.474 to 0.430 (−9%) when beats go
from 300 to 330, i.e. a 10% HR rise. The main conventional precursor
(heart-rate rise) would therefore move ΔG mechanically.

**Change in v2.** The exact estimator (protocol §7.4):

- robust baseline standardisation;
- Ledoit–Wolf (as in `shrunk_covariance`) with an SPD floor;
- Cholesky AIRM with a scale/shape decomposition;
- a fixed beat count ($N_b$ = 256, or 512 if the $n_{\mathrm{eff}}$ gate
  fails);
- a condition-number flag, with fixed-intensity sensitivity analyses;
- five simpler covariance comparators (variance-only, correlation-only,
  correlation Frobenius, log-det, DNB composite).

## F7 — MAJOR — discovery vs prediction (item 10)

**Problem.** v1 named the top verdict "EXPLORATORY SIGNAL", used "advance
warning" in the bin rationale, and allowed "at lead times of X min" without
a requirements framework.

**Changes in v2.**

- Renamed to **EXPLORATORY ASSOCIATION**, with "TRIGGER-PROXIMAL ASSOCIATION
  ONLY" as the short-lead verdict.
- A third estimand, E-advance (event-unconditional), is declared
  not estimable.
- §15 lists six requirements for genuine advance prediction. This study
  meets at most part of one.
- A forbidden-terms list: "predicts VF", "early warning", "advance warning",
  "forecast".

## F8 — MAJOR — AF exclusion (item 7)

**Problem.** Excluding up to 4 of 20 VF patients by rhythm is a selection on
a characteristic plausibly related to arrhythmic mechanism, age and heart
failure.

**Change in v2.** Analysis B is rhythm-inclusive with an NN-free panel
(RTa, Tamp, ST, R amplitude). M1-B and M2-B are defined, and B gets its own
decision rule and separate reporting, with no pooling. The composition and
demographics of included vs excluded patients are reported.

**Residual.** PVC detection is less reliable in AF.

**Open (D1).** Is B co-primary (α split) or secondary but binding-reported?

## F9 — MAJOR — external no-VF datasets (item 9)

**Problem.** chfdb was the external false-alarm set. Its recorder,
digitisation, annotation process and population differ from SDDB, so its
FAR measures a different acquisition chain. NSRDB additionally differs in
sampling rate (reported 128 Hz).

**Change in v2.** A hierarchy (protocol §12.3):

- SDDB remote zones are primary, labelled "pre-VF-conditional FAR";
- SDDB no-VF records are descriptive only (n = 3);
- chfdb / LTSTDB are a transportability stress test, admissible only after
  an outcome-blind acquisition-comparability check (SQI KS distance < 0.3;
  spectra within 3 dB over 0.5–40 Hz);
- NSRDB is never used.

chfdb is excluded from pseudo-onset nulls of SDDB drift.

**Open (D7).**

## F10 — MAJOR — VF onset definition, VT exclusion, guard (item 5)

**Findings** (simulation §5).

- With onset-marking error up to 3 min, no guard inflates the
  **conventional** B5 AUROC from 0.57 to 0.64 through captured arrhythmia.
  It does not inflate the TD increment.
- A 2-min guard removes the contamination, at a cost of about 13 points of B5
  power for a trigger-weighted precursor.
- **A precursor confined to the last ≈ 5 min is undetectable at any guard**
  (power ≤ 0.08). The limit is sample size, not the guard.
- v1 excluded sustained-VT windows without saying whether NSVT or ectopy
  were kept.

**Changes in v2.**

- NSVT, couplets and PVCs are retained and attributed to M1.
- Six sensitivity variants:
  - guard 1 and 5 min;
  - event = first sustained VT;
  - VT windows kept;
  - NSVT windows excluded;
  - high-ectopy windows excluded.
- A per-patient precursor-removal audit. A bin is non-evaluable if > 25% of
  patients lose it to the VT rule.

**Residual (R3).** Trigger-proximal change is outside what this sample can
resolve, and a null says nothing about it.

**Open (D3, D4).**

## F11 — MODERATE — eligibility and minimum n (item 6)

**Problem.**

- 2 h 15 was a sum of unjustified components. It sat 14–18 min below two
  onset times disclosed during design (records 48 and 52).
- 12 patients was not derived from anything.

**Findings.**

- Onset times carry no information about whether a precursor is present, so
  knowing them creates limited selection bias. The appearance of tuning is
  still a legitimate concern.
- The simulated per-patient precision is flat for remote zones ≥ 60 min and
  modestly worse below 60 min (B15/B30 only).

**Changes in v2.**

- $T_{\min}$ = 2 h 20 is derived term by term, with $R_{\min}$ = 30 min.
- Pre-specified eligibility sensitivity at 3 h and 4 h, where the more
  conservative verdict governs if they differ.
- The 12-patient minimum is replaced by a capability floor (n ≥ 6, the
  smallest at which the sign test can reach p < 0.025) and the outcome-blind
  informativeness gate.

**Open (D5).** $R_{\min}$ = 60 min would exclude records 48 and 52 by rule.

## F12–F15 — MODERATE

- **F12. Pseudo-onset availability.** About 83% of patients contribute in
  the mixed-duration scenario, and fewer if recordings are short. v2 makes
  the control non-evaluable (the bin fails) below 8 contributing subjects,
  and declares the composition difference.
- **F13. In-sample scores.** v1's elapsed-time matching would have compared
  LOPO scores of other patients' windows, which are training data for those
  models. v2 uses the fixed unfitted TD composite.
- **F14. Conservativeness.** Under H0 the rule fires in 0–0.5% of studies.
  Bonferroni over four data-sharing bins, plus the sign test, plus the
  two-bin requirement, is far below the nominal 5%. A less conservative rule
  (e.g. a single omnibus test over bins) would lower the MDE, but it would
  change the binding criteria after seeing the design simulation. **Not
  changed. Recorded as D10.**
- **F15. Mechanical overlap.** ΔG's sampling dispersion rises with beat
  autocorrelation (M2's AC1), and its scale component overlaps SDNN and
  var(RT). v2 requires M1 ∪ M2 ∪ M3 > M1 ∪ M2, and ΔG to beat each simpler
  comparator, before any "multivariate structure" wording.

## F16 — MINOR

Dataset facts and several citations remain unverified, because physionet.org
and arXiv are unreachable from the authoring environment. Phase 0 verifies
them from headers only.

---

## Unresolved issues requiring a research decision

| # | Decision | Why it matters |
|---|---|---|
| D1 | Analysis B co-primary or secondary | multiplicity vs selection-bias protection |
| **D2** | **Run a large-effect screen at all, and $\mathrm{MDE}_{\max}$** | simulated MDE ≈ 0.23. The study can only find very large effects |
| D3 | Guard 1 / 2 / 5 min | contamination vs trigger-proximal power |
| D4 | Primary event: VF onset or first sustained VT | prediction target definition |
| D5 | $R_{\min}$ 30 or 60 min | includes or excludes records 48 and 52 by rule |
| D6 | Proceed without clock time? | circadian confounding is otherwise unaddressable (R2) |
| D7 | External FAR set | transportability vs acquisition mismatch |
| D8 | Ledoit–Wolf intensity: analytic or fixed | the analytic intensity is biased under autocorrelation |
| D9 | δ_large 0.10 / 0.15 / 0.20 | whether the binding falsification can usually bind |
| D10 | Keep the conservative conjunctive rule | MDE vs criteria stability |

## Residual limits that no protocol revision can remove

- **R1.** Onset-locked non-physiological change is excluded only insofar as
  the SQI features see it.
- **R2.** Circadian confounding is not excluded without clock time.
- **R3.** Trigger-proximal precursors are beyond the resolution of about 20
  events.
- **R4.** Retrospective, VF-conditional, single-era and community-mined
  data: no result can establish advance prediction or clinical early
  warning (protocol §15).

---

© 2026 Davarn Morrison · Transition Dynamics
