# VF onset programme — published prediction methods and reproducible baselines

> **Status: PROPOSAL / DESIGN RECORD.** Citations marked *unverified* were
> identified from memory or search snippets and must be checked against the
> primary paper before the protocol is frozen. No performance figure below is
> adopted as a benchmark. Section 2 explains why.

---

## 1. What the literature contains, by estimand

Studies of "VF / SCD prediction" from ECG answer at least three different
questions, and they are routinely conflated:

| Estimand | Question | Typical design | Example |
|---|---|---|---|
| **E-risk** (patient-level, long horizon) | Will this person die suddenly within months or years? | cohort survival analysis, one recording per person | ultra-short-term HR fluctuations and SCD (JACC EP 2024); ARIC ECG biomarkers in a survival framework |
| **E-between** (database-level segment classification) | Is this segment from an SDDB patient or from a normal subject? | SDDB vs NSRDB, segments N minutes "before SCD" vs normal segments | the bulk of the SDDB literature: Ebrahimzadeh et al. 2014 (PLoS One, *unverified details*), Acharya et al. 2015 (*unverified*), Murukesan et al. 2014 (*unverified*), CNN on HRV 2023 (average accuracy 99.30% reported) |
| **E-onset** (within-patient, short horizon) | Within a patient who will have VF, is the next H minutes different from earlier periods? | each patient as their own control | Holter: heart rate up about 8%, LF and HF power down and T-wave alternans rising in the 30 min before spontaneous VT in 59 patients (Circulation, *details to verify*). ICD electrograms: TWA/V 62.9 ± 3.1 µV before VT/VF vs 12.8 ± 1.8 µV at baseline (Circulation 2011) |

**This programme's VF question is E-onset.** E-between results are not
evidence for E-onset. Section 2 gives the reasons.

## 2. Why published SDDB accuracies are not baselines

Reported SDDB-vs-NSRDB accuracies run from roughly 85% to over 99%, with
"warning times" from 1–6 minutes up to 70 minutes. None of these is a
reproducible baseline for advance warning:

1. **The label is the database.** Positive segments come from SDDB and
   negative segments from NSRDB, so any difference between the databases is a
   label: disease, age, drugs, recorder, sampling rate, era, digitisation and
   annotation software. A segment taken "30 minutes before SCD" is separable
   from NSRDB for the same reasons as one taken 3 hours before, so the
   "horizon" is not tested at all. A public critique (Halim, *preprint and
   code, unreviewed*) argues exactly this and proposes within-patient tests.
   It is recorded here as a critique found by search, not as established
   consensus.
2. **Segment-level splits.** Many studies split segments, not patients, into
   train and test sets, so the same patient appears on both sides.
3. **Tiny n with flexible pipelines.** About 20 positive patients, together
   with feature selection, classifier selection and window choice, produce
   optimistic accuracies by selection alone.
4. **Community reuse.** The same 20 patients have informed dozens of
   pipelines (see [`VF_DATASET_FEASIBILITY.md`](VF_DATASET_FEASIBILITY.md)
   §1.5).

**Consequence.** Published methods are reimplemented as **feature sets with
fixed, literature-standard definitions**, evaluated inside this protocol's
within-patient, patient-independent design. Published accuracies are never
compared numerically with this protocol's outputs.

## 3. Reproducible baselines adopted

All parameters below are fixed by the cited standards, not by SDDB.

### 3.1 M1 — conventional (primary comparator)

| Feature | Definition | Standard |
|---|---|---|
| meanNN, ΔmeanNN | mean normal-to-normal interval in the window, and its difference from the patient's baseline mean | Task Force HRV standards (Circulation 1996) |
| SDNN, RMSSD | standard time-domain HRV | Task Force 1996 |
| log LF, log HF | Lomb–Scargle power, 0.04–0.15 Hz and 0.15–0.40 Hz, on the NN series | Task Force 1996 bands |
| PVC₅, PVC₃₀ | ventricular ectopic count in the window and in the trailing 30 min | conventional Holter ectopy burden |
| couplets₃₀, NSVT₃₀ | ≥ 2 and ≥ 3 consecutive ventricular beats (< 30 s), trailing 30 min | conventional Holter definitions |

These 10 features carry the documented within-patient precursors: heart-rate
rise, HRV decline and ectopy.

### 3.2 M2 — classical early-warning / critical slowing down

| Feature | Definition | Reference |
|---|---|---|
| AC1(NN), AC1(RT) | lag-1 autocorrelation of the NN and RT-apex series within the window | Scheffer et al. early-warning review (in [`LITERATURE.md`](LITERATURE.md) §1.1) |
| var(RT) | repolarisation variance | as above |
| DFA α₁ | detrended fluctuation, box sizes 4–16 beats | Peng et al., Chaos 1995 |
| SampEn(NN) | m = 2, r = 0.2·SD | Richman & Moorman, AJP Heart 2000 |
| TWA (MMA) | modified moving average alternans amplitude, ST-T segment | Nearing & Verrier, J Appl Physiol 2002 (*verify*). Alternans as a period-doubling precursor: Quail, Shrier & Glass, PNAS 2015 (*verify*) |

The bifurcation-specificity threat in [`LITERATURE.md`](LITERATURE.md) §0
(threat 3) applies with full force. If VF onset is noise-induced (a PVC
landing on a fixed re-entrant substrate), **no** critical-slowing-down signal
is expected. Wilkat et al. 2019 found none before human seizures.

### 3.3 Prediction models

L2-penalised logistic regression with a **fixed** penalty, as used elsewhere
in the programme, and no gradient boosting or deep models. With about 20
patients, any tuned or flexible model would turn its remaining degrees of
freedom into selection bias.

## Sources (search results; details marked *unverified* above must be checked)

- [Upsurge in T-Wave Alternans and Nonalternating Repolarization Instability Precedes Spontaneous Initiation of Ventricular Tachyarrhythmias in Humans (Circulation)](https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.105.607895)
- [Intracardiac Electrogram T-Wave Alternans/Variability Increases Before Spontaneous Ventricular Tachyarrhythmias in ICD Patients (Circulation)](https://www.ahajournals.org/doi/full/10.1161/circulationaha.110.986364) · [PubMed 21357826](https://pubmed.ncbi.nlm.nih.gov/21357826/)
- [High Amplitude T-wave Alternans Precedes Spontaneous VT or VF in ICD Electrograms (Heart Rhythm)](https://www.sciencedirect.com/science/article/abs/pii/S1547527108001422)
- [Accurate Prediction of SCD Based on HRV Analysis Using CNN (PMC10456609)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10456609/)
- [ECG-based Detection and Prediction Models of SCD: review](https://www.researchgate.net/publication/338000649_ECG-based_Detection_and_Prediction_Models_of_Sudden_Cardiac_Death_Current_Performances_and_New_Perspectives_on_Signal_Processing_Techniques)
- [sddb-warning-time-tests (Halim; within-patient and power tests on SDDB)](https://github.com/agustinohalim/sddb-warning-time-tests)
- [Prediction of SCD With Ultra-Short-Term Heart Rate Fluctuations (JACC EP 2024)](https://www.jacc.org/doi/10.1016/j.jacep.2024.04.018)
- [Dynamic Predictive Accuracy of ECG Biomarkers of SCD (ARIC, bioRxiv)](https://www.biorxiv.org/content/10.1101/514380.full.pdf)
- [Prediction of VT by a neural network (CinC 2010, mvtdb)](https://www.cinc.org/archives/2010/pdf/0585.pdf)

---

© 2026 Davarn Morrison · Transition Dynamics
