# Dataset requirements — matched-state perturbation-response experiment

**Status: feasibility analysis. No experiment frozen, no protocol preregistered,
no confirmatory data accessed.** This document does not alter any verdict in
[`CANONICAL_STATUS.md`](CANONICAL_STATUS.md), which is unchanged.

---

## 0. Verification boundary — read this first

Claims below are marked **[V]** verified directly from this environment, or
**[U]** unverified here and requiring confirmation against authoritative
documentation before any commitment.

Reachability tested 2026-09-12:

| source | result |
|---|---|
| `physionet-open.s3.amazonaws.com` (253 open projects) | **HTTP 200 — reachable** |
| `physionet.org` documentation | HTTP 000 — blocked |
| `amsterdammedicaldatascience.nl` | HTTP 000 — blocked |
| journal / general web | HTTP 000 — blocked |

**Consequence: credentialed datasets cannot be verified from here.** Everything
said about MIMIC-IV Waveform, HiRID, eICU, AmsterdamUMCdb and SICdb below is
**[U]** and is written as *what must be checked*, not as fact. This follows the
existing repository rule that dataset properties are not stated as fact until
verified.

---

## 1. The question, and what it is not

> Given two observations with closely matched current measured physiology
> $Y_A(t)\approx Y_B(t)$ but different preceding histories $H_A \ne H_B$, does
> the response to a comparable identifiable perturbation $U$ reveal differences
> in subsequent response, recovery, or deterioration?

Estimate $P(R\mid Y_t,U_t,H_t)$ and test
$P(R\mid Y_t,U_t,H_A)\ne P(R\mid Y_t,U_t,H_B)$ after strong matching on current
observable state and perturbation characteristics.

**Strongest permitted interpretation:** *observable current-state equivalence
does not imply equivalent subsequent dynamics.* Nothing here observes latent
state, a reachable set, a physiological manifold, or irreversibility.

### The alternative explanation that must stay in front

If history predicts response after matching on $Y_t$, the most economical
explanation is **not** biological memory. It is that **the measured state
vector is incomplete** — some $Z$ differs between A and B and was never
recorded. Depth of anaesthesia, volume status, vasomotor tone, catecholamine
levels and temperature are all plausible $Z$.

A positive result therefore supports only:

> "The measured state vector is not sufficient to predict subsequent dynamics."

It does **not** support hysteresis, biological memory, or path dependence in
any mechanistic sense. Distinguishing "incomplete $Y$" from "genuine path
dependence" requires measuring the candidate $Z$ — which is a design
requirement, not an interpretation choice.

---

## 2. Minimum dataset requirements

### REQUIRED — the experiment is impossible without these

| # | Requirement | Threshold | Why |
|:--:|---|---|---|
| R1 | Continuously sampled multichannel physiology | ≥ 1 Hz numerics; **waveform ≥ 50 Hz for at least one haemodynamic channel** | Below this, response dynamics cannot be separated from acquisition behaviour — the failure mode this programme already measured |
| R2 | **Exact perturbation timestamps** | ≤ 1 min accuracy; ≤ 10 s strongly preferred | Response windows are minutes; minute-level jitter destroys onset alignment |
| R3 | **Perturbation magnitude** | dose, volume, or setting change, numerically recorded | Without it, "comparable perturbation" is unenforceable and response amplitude is uninterpretable |
| R4 | **Isolated onset** | no other recorded intervention within the pre-window and response window | Otherwise $U$ is a bundle, not a perturbation |
| R5 | Pre-perturbation baseline | ≥ 10 min of stable recording before onset | Needed for matching covariates and for $Y_{\text{before}}$ |
| R6 | Post-perturbation response **and recovery** interval | ≥ 30 min, with no further intervention | **This is what VitalDB lacks.** Recovery, incomplete recovery and path dependence all require it |
| R7 | Patient identifiers | stable across records | Grouped splits; no pseudo-replication |
| R8 | Repeated perturbations per patient | ≥ 3 isolated events in a meaningful fraction of patients | Required to separate within-patient history effects from between-patient differences |
| R9 | Enough comparable events for matching | ≥ 2,000 isolated events across ≥ 300 patients (order of magnitude) | Matching discards most events; see §6 |
| R10 | Deterioration endpoint | timestamped, objective | Otherwise only $R$, not $D$, is testable |

### STRONGLY DESIRABLE

| Requirement | Why |
|---|---|
| Acquisition metadata — refresh cadence, quantisation, filtering, device model | H_instr is a live rival in this programme; without it the acquisition control is guesswork |
| Full intervention record, not only the perturbation of interest | Needed for R4 and for post-treatment-bias control |
| Candidate $Z$ variables (depth of anaesthesia/sedation, temperature, cardiac output, lactate, fluid balance) | The only way to separate "incomplete $Y$" from path dependence |
| Ventilator settings and mode | Cardiopulmonary interaction confounds every haemodynamic response |
| Waveform–clinical clock alignment documented and validated | See §4; this is where matched waveform datasets most often fail |

### OPTIONAL

Imaging; genomics; free-text notes; nurse-charted subjective scores; billing
codes. None is needed.

---

## 3. Perturbation candidates, ranked by identifiability

Ranked on exogeneity, timing precision, magnitude observability, recovery
observability, and freedom from clinician-selection confounding.

| Rank | Perturbation | Exogeneity | Timing | Magnitude | Recovery observable | Selection confound | Prevalence | Already established? |
|:--:|---|---|---|---|---|---|---|---|
| **1** | **Passive leg raise** | High — reversible, no drug | seconds, if protocolised | standardised manoeuvre | **yes**, self-reversing | low (done as a test, not a treatment) | rare outside studies | **Yes** — validated preload-responsiveness test |
| **2** | **Fluid bolus** | Moderate | minutes, if infusion times recorded | volume + rate recorded | **yes**, 30–60 min | **high** — given because the patient looks hypovolaemic | common in ICU | partly |
| **3** | **PEEP step** | High — machine-set | seconds, from ventilator log | cmH₂O, exact | yes | moderate | common in ICU | partly |
| **4** | **Vasopressor bolus** | Moderate | minutes | dose recorded | partial — short half-life helps | **very high** — given because BP is low | common in ICU, **rare in VitalDB [V]** | partly |
| **5** | **Vasopressor infusion step** | Low | minutes | rate change | poor — titrated continuously | very high | common in ICU | yes |
| **6** | **Ventilator breath** (periodic probe) | High | exact | TV/PIP recorded | **no — periodic, never unperturbed** | low | ubiquitous **[V]** | **yes — PPV/SVV** |
| 7 | Anaesthetic concentration step | Moderate | exact if TCI logs | CE modelled, not measured | partial | high | **no identifiable steps in VitalDB [V]** | partly |
| 8 | Position change | High | usually unrecorded | unrecorded | yes | low | common, **not timestamped** | partly |

**For the full question — recovery, incomplete recovery, path dependence — only
ranks 1–3 qualify.** Ranks 4–5 fail R6 (continuous titration prevents a clean
recovery interval) and carry severe indication confounding. Rank 6 fails R6 by
construction. Ranks 7–8 fail R2/R3 in practice.

**Recommended primary perturbation: PEEP step or fluid bolus**, because both
have machine- or pump-recorded timing and magnitude, and both permit a genuine
post-perturbation recovery interval. PLR is cleanest scientifically but is
performed as a diagnostic test, so its presence in a record is itself
outcome-correlated — a selection problem that must be handled, not ignored.

---

## 4. Candidate datasets

| Dataset | Waveforms | Intervention timestamps | Magnitude | Outcomes | Size | Access | Verified? |
|---|---|---|---|---|---|---|:--:|
| **VitalDB** | ART/PLETH/ECG 500 Hz, CO₂ 62.5 Hz | Orchestra infusion volume/rate, timestamped | yes for infusions | in-hospital death, ICU days | ~6,388 cases | open, CC-BY | **[V]** |
| **MIMIC-IV Waveform + MIMIC-IV clinical** | ECG/ABP/PPG, high rate | `inputevents` start/end + amount | yes | rich | large | credentialed, DUA, training | **[U]** |
| **HiRID** | none — 2-min numerics | pharma records | yes | rich | ~34k admissions | credentialed | **[U]** |
| **AmsterdamUMCdb** | none — numerics to 1/min | `drugitems` start/stop + dose | yes | rich | ~23k admissions | credentialed, DUA | **[U]** |
| **eICU** | none | infusion records, coarser | partial | rich | ~200k | credentialed | **[U]** |
| **SICdb** | claimed high-frequency | claimed | claimed | yes | ~27k | credentialed | **[U]** |
| **CHARIS** | ABP/ECG/ICP **50 Hz** | **none** | none | outcome string only | **13 subjects** | open | **[V]** |

### What each can and cannot test

**VitalDB [V] — cannot test the full question.** Directly measured on 30
development cases: ventilator present 97–100%; arterial waveform 63%;
phenylephrine infusion **7%**; norepinephrine **10%**; epinephrine, dopamine,
vasopressin, dobutamine **0%**; remifentanil CE present 70% but with **zero**
identifiable step changes (TCI holds a constant target). Clinical intervention
fields (`intraop_eph`, `intraop_phe`, …) are **case totals, not timestamps
[V]**. Hand-given boluses are therefore invisible.
→ Fails R6 (no unperturbed recovery interval), R8/R9 for any non-ventilator
perturbation. Supports the ventilator secondary experiment only.

**MIMIC-IV Waveform matched subset — GATE 1 NOT CLOSED. Pathway stopped.**
See §4a below for the verification attempt and its outcome.

**HiRID / AmsterdamUMCdb / eICU [U] — fail R1 as stated.** If their resolution
is minute-level numerics with no waveform, they cannot separate response
dynamics from acquisition behaviour, which this programme has already shown is
not a theoretical concern. They could still support a **numerics-only** version
of the matched-state test with acquisition explicitly unresolvable — a weaker
experiment that must be labelled as such.

**CHARIS [V] — inadequate.** 13 subjects, 3 channels, 50 Hz, **no intervention
records at all**. Verified directly from the record headers.

### 4a. MIMIC-IV verification attempt — 2026-09-12

Three gates were to be checked in order. **Gate 1 could not be closed from this
environment, so Gates 2 and 3 were not attempted**, per the rule that the MIMIC
pathway stops if reliable alignment cannot be established.

**Gate 1 — clock alignment: UNVERIFIED.** Verified facts:

| check | result |
|---|---|
| MIMIC-IV Waveform present in the open PhysioNet bucket | **absent** — only `mimic-iv-demo-meds` and `mimic-iv-fhir-demo` exist, neither containing waveforms **[V]** |
| Open MIMIC-IV clinical demo (with `inputevents`) in the bucket | **absent** — probed four candidate prefixes, zero keys **[V]** |
| `physionet.org/content/mimiciv/` and `/mimic4wdb/` | **HTTP 000 — blocked [V]** |
| `physionet-restricted.s3.amazonaws.com` | **HTTP 404 [V]** |
| MIMIC-IV access model | *"Access to MIMIC-IV is limited to credentialed users"* — quoted from the open `mimic-iv-demo-meds` README **[V]** |

Neither the waveform data nor its authoritative documentation is reachable.
**No inference about alignment capability is recorded here.** The claim stays
**UNVERIFIED**; it is not downgraded to "probably works" or upgraded on the
basis of recollection.

#### What a credentialed user must check, in this order

**Corrected 2026-09-12.** An earlier draft of this section treated the
physiological-response timing test as confirmation of alignment. That was wrong
and is replaced. The test is **asymmetric** and can only ever falsify.

| # | Check | Kind |
|:--:|---|---|
| 1 | **Authoritative documentation of waveform timestamps** — what clock the record headers carry, and in what frame | documentation |
| 2 | **Authoritative documentation of clinical-event timestamps** — the frame used by intervention records | documentation |
| 3 | **Identifier mapping** — how patient and stay identifiers map between MIMIC-IV and MIMIC-IV Waveform, and whether the mapping is provided or must be constructed | documentation + data |
| 4 | **De-identification / date-shift rules** — and specifically whether the shift is *identical within a patient* across both datasets. If it is not, alignment is impossible in principle | documentation |
| 5 | **Direct timestamp overlap on several credentialed records** — do waveform spans actually bracket recorded intervention times | data |
| 6 | **Physiological-response timing — consistency check only** | data, secondary |

**Interpretation of step 6, stated precisely:**

- A response occurring **systematically before** the recorded intervention
  **falsifies** the assumed alignment.
- A response occurring **after** the intervention **does not** establish correct
  alignment. Responses may be delayed, absent, noisy, confounded by concurrent
  care, or charted imperfectly, and a plausible-looking lag is consistent with
  many wrong alignments.

Step 6 is therefore a **one-directional falsifier**, never evidence of success.
Gate 1 is passed on steps 1–5; step 6 can only take it away.

Until steps 1–5 are passed **on credentialed data and documentation**, MIMIC-IV
must be treated as unverified for this purpose. See
[`CREDENTIALED_ACCESS_CHECKLIST.md`](CREDENTIALED_ACCESS_CHECKLIST.md).

---

## 5. Is the full history / path-dependence question currently testable?

**No — not from any dataset verified available here.**

The blocking requirement is **R6**: an isolated perturbation followed by an
uninterrupted recovery interval. VitalDB has no such perturbation at adequate
prevalence [V]. The datasets that plausibly do are all credentialed and
unverifiable from this environment [U].

The secondary blocker is the $Z$ problem (§1). Even with a perfect dataset, a
positive history effect would establish that the measured state vector is
insufficient — not that the system carries a physiological memory. Separating
those requires deliberately measuring candidate $Z$ variables, which no
retrospective dataset was designed to do.

---

## 6. Ideal prospective design, if no dataset qualifies

Observational only. **No deterioration is induced.** The perturbation is a
clinically indicated or otherwise safe manoeuvre that would occur anyway.

```
Y_pre (>=10 min stable)  ->  U (protocolised, logged to the second)
   ->  dY (response, 0-5 min)  ->  recovery (5-30 min)
   ->  Y_post  ->  subsequent trajectory / outcome
```

- **Perturbation:** PEEP step of a fixed magnitude, or a clinically indicated
  fluid bolus of recorded volume and rate. Both are routine; neither is
  administered for research.
- **Logging:** perturbation onset stamped by the device, not by a human.
- **Channels:** arterial waveform ≥ 100 Hz, ECG, plethysmograph, airway
  pressure and flow, plus cardiac output where already monitored.
- **$Z$ measured deliberately:** depth of anaesthesia/sedation index,
  temperature, cumulative fluid balance, current vasoactive dose.
- **Repeated events:** ≥ 3 isolated perturbations per patient where clinical
  care provides them.
- **Matched pairs:** constructed on pre-perturbation $Y$ (levels, short trends,
  ventilator settings, current drug doses) using a frozen calliper, **with no
  outcome, no post-perturbation data and no future treatment**.
- **History test:** within matched pairs, does $H$ (duration of the case,
  cumulative exposure below thresholds, number of prior excursions, cumulative
  vasoactive dose) predict the response $R$? This needs no outcome and cannot
  leak.
- **Path dependence:** among events where $Y_{\text{post}}\approx Y_{\text{pre}}$
  within a frozen tolerance, does the subsequent trajectory depend on the
  excursion just experienced?
- **Powering:** §2 R9 — order 2,000 isolated events across ≥ 300 patients,
  because matching discards most events.

---

## 7. Conclusion

> **C — no identified existing dataset is verified adequate, and a prospective
> study is required unless verification changes the picture.**

**Reaffirmed 2026-09-12 after the MIMIC-IV verification attempt.** VitalDB is
verified inadequate for the full question [V]. MIMIC-IV Waveform **failed to
close Gate 1 from this environment** — not because alignment was shown to be
impossible, but because neither the data nor its authoritative documentation is
reachable here (§4a). Capability is therefore **not inferred**.

The path to **B** is unchanged and now precisely specified: a credentialed user
executes the six ordered checks in §4a — Gate 1 is passed on checks 1–5, with
check 6 able only to falsify, never to confirm. If Gate 1 passes and Gates 2 and
3 yield adequate events, this becomes
**B — partial testing with named limitations**, the limitations being absent
$Z$ variables, residual indication confounding for fluid boluses, and the
permanent impossibility of excluding unmeasured $Z$
([`STATE_COMPLETENESS_TEST.md`](STATE_COMPLETENESS_TEST.md)).

**Nothing should be frozen or executed until that verification is done.**

---

## 8. Related

- [`STATE_COMPLETENESS_TEST.md`](STATE_COMPLETENESS_TEST.md) — the nested
  state-hierarchy design that challenges any observed history effect
- [`CANDIDATE_VENTILATOR_EXPERIMENT.md`](CANDIDATE_VENTILATOR_EXPERIMENT.md) —
  the feasible VitalDB secondary experiment, not frozen
- [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) — unchanged by this document
- [`DATASET_REQUIREMENTS.md`](DATASET_REQUIREMENTS.md) — earlier requirements
  analysis for the previous programme

---

© 2026 Davarn Morrison · Transition Dynamics
