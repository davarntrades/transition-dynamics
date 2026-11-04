# VT/VF programme: CONDITIONAL GO phase report (Phase 1)

> **Status: REPORT FOR THE PROGRAMME OWNER'S DECISION.**
>
> - No real VT/VF hypothesis test was run. No pre-event physiology was
>   inspected.
> - No protocol is frozen and no external enquiry was sent.
> - No historical result was modified. The branch is not merged.
> - The seven hypotension outcomes and
>   [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) are unchanged.

## Deliverables of this phase

| Scope item | Deliverable |
|---|---|
| 1–2 dataset verification | [`VT_VF_PHASE1_DATASET_VERIFICATION.md`](VT_VF_PHASE1_DATASET_VERIFICATION.md) |
| 3 enquiries (drafts, **not sent**) | [`VT_VF_ACCESS_ENQUIRY_DRAFTS.md`](VT_VF_ACCESS_ENQUIRY_DRAFTS.md) |
| 4 HR-leakage repair + regression tests | [`VT_VF_FALSIFICATION_SUITE.md`](VT_VF_FALSIFICATION_SUITE.md) §2–3; `analysis/vtvf/test_leakage.py` |
| 5 estimator comparison | [`VT_VF_ESTIMATOR_COMPARISON_AND_SESOI.md`](VT_VF_ESTIMATOR_COMPARISON_AND_SESOI.md) §2–3 |
| 6 provisional SESOI | same document, §5 |
| 7 falsification suite | [`VT_VF_FALSIFICATION_SUITE.md`](VT_VF_FALSIFICATION_SUITE.md) §4–6; `analysis/vtvf/suite.py` |
| 8 VT/VF subgroups, patient-independent inference | `repaired_rule2.subgroup_report`; suite §5.2; per-patient estimand (suite §1) |
| selection record and design-stage optimisation | estimator document §4 |

## 1. Strongest verified dataset candidate

- **Verified from primary files:** MVTDB (78 patients, 135 VT/VF events).
  It is RR-only, with about 10–15 min of pre-event recording, so it fails
  the multichannel (R3) and control-period (R4) requirements. **No verified
  dataset meets R1–R4.**
- **Strongest plausible candidates** (secondary sources only):
  1. the UCSF Alarm Study (461 ICU patients, 533 true VT alarms,
     full-disclosure multi-lead ECG; sharing and sustained-VT adjudication
     unconfirmed);
  2. a MIMIC-III waveform adjudication project (onset labels must be built);
  3. the UVA ICU archive (VT/VF content unknown).
- **VTaC and Challenge 2015** hold only about 5–10 min before each alarm
  (secondary sources). They fail R3 and R4 for a 30-min-horizon design
  whatever their patient counts.
- **Blocker.** `physionet.org` is refused by this environment's egress
  proxy, and VTaC, Challenge 2015 and the MIMIC waveform databases are not
  on the open-data S3 mirror. Their primary metadata could not be
  verified. This is a **network-policy** limitation, not evidence that the
  data are unsuitable.

## 2. Unresolved methodological failures

The pre-specified suite selected **no provisional primary estimator**. No
statistic met A1–A4 in either seed set.

| ID | Failure | Severity | Status |
|---|---|---|---|
| F1 | **Undetected near-onset artefact** (30% of bursts missed) yields positive verdicts in 99.2–100% for every deviation-type structure statistic, including the repaired `pshape_hp`. `ACQUISITION_EXPLAINED` only sees *detected* artefacts. | **critical** | unresolved; needs an SQI independent of the statistic, a negative-control requirement, and a test against common-mode noise |
| F2 | Residual conventional leakage of `pshape_hp`: 2.0–3.6% vs the 2% bound in 4 cells; s ≈ +0.01–0.03; likely real under strong RT–RR coupling (4 pools: 0.013, 0.020, 0.030, 0.026); null-artefact 5.6% and coverage 0.925 in the holdout | moderate | unresolved; "HR alone cannot produce a positive verdict" holds only under the tested conditions of the 1,200-patient regression test, not in every pool |
| F3 | `pshape_hp` is blind by construction to HR-coupled structural precursors (`nncorr0.15`: 0%) and to variance and mean precursors | scope | a scientific decision to state in any protocol, not a bug |
| F4 | The original combined estimator `td3` is non-specific: about 99–100% positives under HR or HRV change alone, 8–28% under gain drift | critical for `td3` | `td3` should not be the primary estimator |
| F5 | Covariance competitors respond to variance, gain and HRV | critical for them | not structure-specific |
| F6 | The false-flag rate of the VT/VF "driven by one class" rule when both classes respond is untested (estimated 10–20%) | moderate | to be measured before any freeze |
| F7 | **Suite precision.** Pool 400 → 12.6% of non-gross null cells exceed 2% by fluctuation, so the conjunction criteria are too noisy to separate 2% from 3.6% | moderate (design of the test) | criteria were not changed post hoc; a corrected pre-specification is required before the next run |
| F8 | Provenance. Pilot outputs used for design choices D1–D5 were not all archived. At least 40 configurations were tried on the same generative model. | moderate | recorded; requires a fresh holdout written by someone independent of the estimator design |
| — | Unchanged from Phase 4: no verified dataset; circadian, medication and intervention confounding untestable in synthetic data | — | — |

## 3. Exact synthetic calibration evidence

All figures are synthetic, n = 80 resampled studies (500 per cell),
pool 400 per scenario. They are given as selection / holdout.

**Leakage regression test, run 2** (`pshape_hp`, pool 1,200, 400 studies;
criteria fixed before run 1). **ALL PASS:**

- conventional-only bin means between −0.004 and +0.022;
- any positive 0.000–0.020;
- null 0.010;
- structural γ = 0.10: 0.997;
- the unrepaired `shape_hp` leaks at +0.26 to +0.41, so the test has power.

Run 1 (pool 300) **failed** for HRV −30% (0.065) and is preserved.

**Suite, `pshape_hp`:**

| Scenario family | any positive (sel / hold) |
|---|---|
| nulls (7, plus 1 holdout-only) | 0.000–0.016 / 0.000–**0.056** |
| conventional-only | 0.000–**0.030** / 0.004–**0.036** |
| undetected near-onset artefact | **1.000 / 0.998** |
| near-onset gaps | 0.002 / 0.000 |
| corr γ = 0.10 | 1.000 / 0.998 |
| corr γ = 0.05 (s ≈ SESOI) | 0.172 / 0.312 (EXPLORATORY 0.064 / 0.096) |
| half responders | 0.748 / 0.782 |
| heterogeneity (SD 1.0) | 0.980 / 0.966 |
| missingness | 1.000 / 1.000 |
| gain drift | 1.000 / 0.998 |
| intermittent | 0.998 / 0.956 |
| var0.5 / mean0.5 | 0.000 / 0.034; 0.000 / 0.000 |
| nncorr0.15 (holdout only) | — / 0.000 |
| VF-only effect, 30% VF | 0.030 / 0.460, flagged "one class" in 100% / 93.9% of positives |
| VF-only effect, 60% VF (holdout only) | — / 0.810, flagged in 99.5% |
| null `LARGE_EXCLUDED` at δ = 0.10 | 0.698 / 0.826 |

**Coverage (95% t-interval, n = 40)** was within [0.93, 0.97] in 191 of
192 statistic × scenario × set × bin cells. The exception is `pshape_hp`
holdout corr0.10 B5 at 0.925.

## 4. Recommendation for the following phase

### **CONDITIONAL GO** for a preparatory phase only. **NO-GO** for any real VT/VF hypothesis test, protocol freeze or final estimator selection.

**Conditions (each requires the programme owner's approval):**

1. **Access.**
   - Allowlist `physionet.org` (and `pmc.ncbi.nlm.nih.gov` and
     `proceedings.neurips.cc` for full texts) so that VTaC, Challenge 2015
     and the MIMIC waveform databases can be verified from primary metadata.
   - Start PhysioNet credentialed access.
   - The owner decides whether to send any of the drafted enquiries, after
     verifying the contacts.
2. **Artefact identifiability (F1) before anything else methodological.**
   - Design and test a signal-quality-based repair and a negative-control
     requirement under independent **and** common-mode artefact models, with
     undetected rates of 10–50%.
   - **Stop rule:** if no repair restores A3 while keeping power at γ = 0.10,
     record the deviation-statistic family as non-identifiable against
     undetected near-onset artefact. That is an estimator-level NO-GO, not
     a falsification of the hypothesis.
3. **Pre-specify a corrected suite before running it (F7, F6, F8).**
   - Pool ≥ 1,600; a binomial-bound or family-wise admissibility rule;
     seed base ≥ 3,000,000.
   - A subgroup false-flag scenario.
   - A holdout scenario set authored independently of the estimator design.
4. **Scope decision (F3).** The owner decides whether the primary
   hypothesis is "structure beyond HR coupling" (`pshape_hp`-type) or
   includes HR-coupled structure, which would need a different leakage
   strategy. This must be decided on scientific grounds, not on simulated
   power.

**What would change the recommendation to GO for a real-data feasibility
step (still not a hypothesis test):**

- a verified dataset meeting R1–R4;
- an estimator admissible under the corrected suite in an independent
  holdout;
- outcome-free negative controls specified for the real dataset.

**Interpretation guard.** Neither the dataset limitations nor the synthetic
estimator failures are evidence against the Transition Dynamics hypothesis.
They show only that it cannot yet be tested credibly for VT/VF.

---

© 2026 Davarn Morrison · Transition Dynamics

## Addendum (2026-11-04): owner decision

- The owner approved three activities: artefact falsification, an
  independently specified synthetic holdout, and continued dataset access.
- The owner did **not** approve selecting `pshape_hp` as primary, or
  abandoning the heart-rate-coupled hypothesis.
- Item 4 of §4 (scope decision on F3) is superseded: H-S and H-C remain
  separate hypotheses with separate tests.
- See [`VT_VF_PHASE2_CHARTER.md`](VT_VF_PHASE2_CHARTER.md). The text above
  is otherwise unchanged.
