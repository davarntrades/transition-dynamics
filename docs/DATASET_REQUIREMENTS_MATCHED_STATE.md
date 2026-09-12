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

**MIMIC-IV Waveform matched subset [U] — the most promising candidate, and the
one most likely to fail on a detail.** It is the only widely used resource that
could satisfy R1–R3 and R10 simultaneously. Before any commitment, three things
must be verified against authoritative documentation, **in this order**:
1. **Clock alignment.** Do waveform record timestamps align with `inputevents`
   times, and with what stated accuracy? A matched subset can be "matched" at
   admission level while being useless at minute level.
2. **Coverage overlap.** For how many patients does waveform coverage actually
   span the 10 min pre + 30 min post window around isolated interventions?
3. **Isolation.** After applying R4, how many events survive?
If any of the three fails, the dataset is inadequate regardless of its size.

**HiRID / AmsterdamUMCdb / eICU [U] — fail R1 as stated.** If their resolution
is minute-level numerics with no waveform, they cannot separate response
dynamics from acquisition behaviour, which this programme has already shown is
not a theoretical concern. They could still support a **numerics-only** version
of the matched-state test with acquisition explicitly unresolvable — a weaker
experiment that must be labelled as such.

**CHARIS [V] — inadequate.** 13 subjects, 3 channels, 50 Hz, **no intervention
records at all**. Verified directly from the record headers.

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

More precisely: **C, with a defined path to B.** VitalDB is verified inadequate
for the full question [V]. The credentialed candidates are unverifiable from
this environment [U]; if MIMIC-IV Waveform passes the three checks in §4 —
clock alignment, coverage overlap, post-isolation event count — this would
become **B: partial testing with named limitations**, the limitations being
absent $Z$ variables and residual indication confounding for fluid boluses.

**Nothing should be frozen or executed until that verification is done.**

---

## 8. Related

- [`CANDIDATE_VENTILATOR_EXPERIMENT.md`](CANDIDATE_VENTILATOR_EXPERIMENT.md) —
  the feasible VitalDB secondary experiment, not frozen
- [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) — unchanged by this document
- [`DATASET_REQUIREMENTS.md`](DATASET_REQUIREMENTS.md) — earlier requirements
  analysis for the previous programme

---

© 2026 Davarn Morrison · Transition Dynamics
