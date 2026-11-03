# VT/VF programme — data-access enquiry drafts

> ## DRAFTS ONLY — NOT SENT
>
> - None of these has been sent, and none may be sent without the programme
>   owner's explicit approval.
> - Names, affiliations and contact routes come from **secondary sources**.
>   They must be verified, and the current corresponding author confirmed,
>   before sending.
> - Sender identity, institution, ethics/IRB references and signature are
>   left as placeholders: `[SENDER]`, `[INSTITUTION]`, `[IRB/ETHICS]`.
> - Every first enquiry asks for **metadata only**. No patient-level data,
>   waveforms or outcomes are requested at this stage.

## Common metadata request (attached to every enquiry)

1. Number of **independent patients** with at least one **spontaneous,
   sustained** VT (≥ 30 s or terminated by therapy) and/or VF, counted
   **separately for VT and VF**, and the number with more than one event.
2. How onset times were **adjudicated**: annotators, blinding, agreement
   statistics, onset definition (first beat vs alarm time).
3. Mono- vs polymorphic VT documentation.
4. **Pre-onset recording duration** per first event (a distribution;
   especially the count with ≥ 2 h 20 min and ≥ 3 h).
5. ECG lead set, sampling frequency, other channels (ABP, PPG,
   respiration), signal-quality annotations.
6. Availability of **clock time** (time of day) for recordings.
7. Medication, pacing, ICD therapy, cardioversion and intervention records,
   with timestamps if available.
8. Access route, data-use agreement terms, ethics requirements, costs, and
   whether external analysis (data never leaving the host) is possible.
9. Prior publications using the data for arrhythmia **prediction**, so that
   community re-use can be accounted for.

**What we offer and commit to:**

- a pre-registered protocol written before any data access;
- synthetic validation of the analysis pipeline;
- outcome-blind verification steps;
- no clinical or predictive claims from retrospective results;
- sharing of code and negative results;
- authorship and acknowledgement per the host's policy;
- compliance with the host's DUA and ethics conditions.

---

## U1 — UCSF ECG Monitoring Research Lab (Alarm Study)

**To:** corresponding investigator of the UCSF Alarm Study (publications list
Drew BJ and Pelter MM; *verify current contact*)
**Subject:** Metadata enquiry — sustained VT/VF onsets in the UCSF Alarm Study full-disclosure ECG

> Dear [Investigator],
>
> I am writing on behalf of [INSTITUTION] about a pre-registered,
> retrospective research question: whether multichannel ECG structure
> changes before spontaneous sustained ventricular tachyarrhythmia,
> *beyond* heart rate, HRV and ectopy. We are not developing an alarm
> product and will make no clinical claims from retrospective data.
>
> Your study's combination of full-disclosure multi-lead ECG and expert
> arrhythmia annotation (461 patients and 533 true VT alarms, as reported)
> appears unusually well suited. Before any data request, could you tell us
> whether the metadata items listed below are available? Our feasibility
> work indicates we need roughly 80 independent patients with a documented
> first sustained VT/VF and at least 2–3 hours of preceding ECG.
>
> [Common metadata request, items 1–9]
>
> We would welcome a short call. Our protocol, synthetic validation and
> analysis code are available on request.
>
> Sincerely, [SENDER], [INSTITUTION], [IRB/ETHICS]

## T1 — THEW (Telemetric and Holter ECG Warehouse, University of Rochester)

**To:** THEW coordinating team / principal investigator (publications list
Couderc J-P; *verify current contact and catalogue*)
**Subject:** THEW catalogue enquiry — Holter or telemetry recordings with spontaneous sustained VT/VF

> Dear THEW team,
>
> We are assessing datasets for a pre-registered retrospective study of
> multichannel ECG structure before spontaneous sustained VT/VF. Could you
> tell us whether any current THEW database contains recordings in which a
> spontaneous sustained VT or VF occurs, with documented onset times and
> several hours of preceding recording? If so, could you share the metadata
> items below and the current data-use procedure (membership,
> not-for-profit terms, steering-committee approval)?
>
> [Common metadata request, items 1–9]
>
> Sincerely, [SENDER], [INSTITUTION]

## I1 — Authors of the ICU short-term-prediction study (J Electrocardiol 2010;43(5):400–7, PMID 20378124)

**To:** corresponding author (*author list not retrieved: verify via
PubMed before sending*)
**Subject:** Possible collaboration — replication cohort of ICU patients with sustained VT/VF and ≥ 12 h pre-event ECG

> Dear Dr [Name],
>
> Your 2010 study of 38 ICU patients with sustained VT/VF (and 30 controls),
> each with ≥ 12 h of continuous multilead ECG, reported no reliable
> short-term predictor. That negative result is directly relevant to our
> pre-registered work. Would the recordings, or a summary of their
> metadata, be available for an **independent replication** under your
> terms? We would treat your published null as a prior result to be
> reproduced, not overturned.
>
> [Common metadata request, items 1–9]
>
> Sincerely, [SENDER]

## A1 — Asan Medical Center cardiovascular ICU group (Lee et al., Sci Rep 2016)

**To:** corresponding author (publication lists Lee H, Joo S and colleagues;
*verify*)
**Subject:** Metadata enquiry — CICU monitor recordings preceding VT

> Dear Dr [Name],
>
> Your study analysed 52 recordings taken one hour before VT events, plus
> controls, from bedside monitors at Asan Medical Center. We would like to
> know whether longer pre-event recordings (≥ 2–3 h), multichannel ECG and
> adjudicated onset times exist for these or later patients, and under what
> terms external researchers might access metadata or collaborate.
>
> [Common metadata request, items 1–9]
>
> Sincerely, [SENDER]

## V1 — University of Virginia continuous monitoring group

**To:** corresponding investigator of the UVA ICU continuous-monitoring
studies (publications list Moorman JR and colleagues; *verify*)
**Subject:** Metadata enquiry — sustained VT/VF events within the UVA ICU waveform archive

> Dear Dr [Name],
>
> Your group's archive of continuous ICU monitoring data (reported as
> 9,232 admissions from 2009–2015) may contain spontaneous sustained VT/VF
> episodes with long preceding recordings. Could you tell us whether such
> episodes are identified or identifiable, how onsets are or could be
> adjudicated, and under what terms collaboration is possible?
>
> [Common metadata request, items 1–9]
>
> Sincerely, [SENDER]

## P1 — PhysioNet / MIMIC (a process, not an enquiry)

- **Action 1:** credentialed access for MIMIC clinical data, per
  [`CREDENTIALED_ACCESS_CHECKLIST.md`](CREDENTIALED_ACCESS_CHECKLIST.md).
- **Action 2:** allowlist `physionet.org` so that VTaC, Challenge 2015 and
  MIMIC waveform metadata can be verified directly.
- **Optional, to the VTaC authors** (publication lists Lehman L-wH and
  colleagues; *verify*): one clarification question only. What is the
  per-record pre-alarm duration, and how many unique patients sit behind the
  1,441 true VT alarms?

---

© 2026 Davarn Morrison · Transition Dynamics
