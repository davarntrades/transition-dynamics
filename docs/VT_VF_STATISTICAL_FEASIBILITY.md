# VT/VF programme — statistical feasibility

> **Status: FEASIBILITY RECORD.**
>
> - Power, false-positive rates and coverage come from the **synthetic**
>   beat-level calibration of the *repaired* rule
>   ([`VT_VF_PROTOCOL_REPAIR_PLAN.md`](VT_VF_PROTOCOL_REPAIR_PLAN.md);
>   [`analysis/results/vtvf_repair_calibration.json`](../analysis/results/vtvf_repair_calibration.json)).
> - Dataset counts are from verified metadata
>   ([`VT_VF_DATASET_LANDSCAPE.md`](VT_VF_DATASET_LANDSCAPE.md)).
> - No real outcome data were examined.
> - **These are design-stage numbers under stated assumptions, not
>   properties of any real dataset.**

## 1. Assumptions (disclosed)

| Element | Assumption | Effect on conclusions |
|---|---|---|
| Panel | 4 channels per beat (NN, RTa, Tamp, ST); 70 bpm; beat AR φ = 0.8; minute-scale slow component φ = 0.95 | slower physiological dynamics reduced power by about half in the v2 simulation |
| TD-specific precursor | step change in two inter-channel correlations (+γ) over the last 30 min, marginals unchanged; per-patient amplitude multiplier N(1, 0.5²) | sustained, bin-aligned and homogeneous. **Optimistic** |
| Effect-size scale | per-patient $s_{i,b}$ = residual within-patient AUROC − 0.5. Null SD ≈ **0.26–0.29** per bin | the scale on which every threshold below is stated |
| Pre-onset duration | uniform 140–1,440 min | real distributions are dataset-specific |
| Not modelled | missing data; clock-locked effects; VT vs VF heterogeneity (except via responders); annotation error beyond the guard | each would *reduce* power or *add* false positives |

## 2. Effective independent sample size

| Source of apparent n | Counts as independent? | Rule |
|---|---|---|
| Patients | **yes** | the unit of inference |
| Repeated episodes per patient | **no** | first qualifying event is primary. Later events are averaged within patient. Under $\operatorname{var}(\bar s_i) = \sigma^2/m + \tau^2$, extra episodes cannot reduce variance below the between-patient heterogeneity τ² |
| Overlapping 1-min windows | **no** | ≈ 1 effective observation per patient per bin (v2 simulation §3) |
| Four horizons | **no** | the bins share data. Bonferroni is conservative |
| LOPO folds | — | removed from the primary analysis. The per-patient statistic needs no cross-patient training, so the s_i are independent and **95% coverage is 0.92–0.955** |
| Unreliable / missing annotations | **reduce n** | patients whose onset cannot be corroborated are excluded or sensitivity-tested (Phase 0: 7 of 16 SDDB primary patients) |

MVTDB illustrates the gap: **135 events but 78 independent patients**, and
35 of them contribute 92 events [V].

## 3. Power and exclusion of the repaired rule (shape statistic) [synthetic]

| Scenario (per-patient mean s, B5 / B10 / B15 / B30) | n = 16 | 20 | 40 | 80 | 150 |
|---|:--:|:--:|:--:|:--:|:--:|
| **Null**: EXPLORATORY ASSOCIATION | 0.0% | 0.0% | 0.1% | 0.1% | 0.0% |
| **Null**: P(LARGE INCREMENT EXCLUDED at δ = 0.10) | 0.14 | 0.19 | 0.48 | **0.82** | 0.97 |
| γ = 0.10 (0.26 / 0.24 / 0.21 / 0.11): EXPLORATORY | 0.13 | 0.31 | 0.63 | **0.96** | 0.995 |
| γ = 0.05 (0.12 / 0.11 / 0.09 / 0.05): EXPLORATORY | 0.016 | 0.029 | 0.067 | 0.19 | **0.49** |
| γ = 0.10, only 50% of patients respond: EXPLORATORY | 0.027 | 0.072 | 0.15 | 0.45 | 0.85 |
| γ = 0.05, trigger-weighted ramp: EXPLORATORY | 0.001 | 0.003 | 0.006 | 0.008 | 0.005 |
| Conventional-only precursor: any positive verdict (residual leakage) | 2.1% | 2.4% | 3.2% | 6.3% | **13.1%** |

**Reading.**

- **About 80 independent patients** are needed both to detect a moderate,
  sustained TD-specific effect (γ = 0.10) and to exclude s ≥ 0.10 with
  probability ≥ 0.8 under H0.
- **About 300 patients** (extrapolated: power 0.49 at n = 150) are needed to
  detect effects at the proposed smallest effect of interest (§4).
- Trigger-weighted precursors remain undetectable at any feasible n.
- **Leakage grows with n.** At n ≥ 80 the conventional-only false-positive
  route exceeds 5%, so repair RP2 is required *before* a large study, not
  after.

## 4. Thresholds reassessed (the old 0.25 / 0.15 are not reused)

The v2 thresholds were stated on the **LOPO model-increment ΔAUROC** scale,
which the repaired design no longer uses for primary inference.

| Quantity | Proposal | Basis | Status |
|---|---|---|---|
| Smallest effect of interest (SESOI) | **s = 0.10 per bin** (within-patient residual AUROC 0.60) | the weakest within-patient separation that could plausibly matter for any alarm-oriented follow-up; about one third of the per-patient null SD | **research decision D-VT2**. Not derived from VT/VF data (none examined) |
| Exclusion threshold | **δ = SESOI = 0.10** (intersection-union, one-sided 95%) | one threshold for detection and exclusion. Under H0 the flag fires ≥ 0.8 at n ≥ 80 | proposal |
| Informativeness requirement | P(exclusion \| H0) ≥ 0.8 **and** power ≥ 0.8 for the γ = 0.10 profile, both computed on the chosen dataset's verified n and onset distribution | prevents running a study that can neither find nor exclude | proposal |

These numbers are a **design target**, not a tuning knob. If a dataset falls
short, the study is not run as a hypothesis test. The thresholds are not
moved.

## 5. Feasibility by dataset

| Dataset | Endpoint | Independent patients usable for the multivariate TD test with all four horizons | Feasible horizons | Informative under §4? |
|---|---|:--:|---|:--:|
| SDDB | A | **16** [V] | all four | **No.** Power 0.13 (γ = 0.10); exclusion 0.14 |
| MVTDB | C (device-labelled) | **0**: TD not computable (RR only). 78 for univariate work [V] | ≤ 10–15 min; onset position unannotated | **No** (TD test impossible; univariate non-confirmatory) |
| VFDB / CUDB | A, B, C, D | **0**: no ≥ 60-min remote zone (35- and 8.5-min excerpts) [V] | ≤ B15 (VFDB) / ≤ B5 (CUDB) | **No** |
| VitalDB Arrhythmia | B / C | **1** sustained VT [V]. NSVT (E): 88 patients, 16 with first VT label ≥ 2 h 20 (first not guaranteed) | — | **No** for A–D. E development only |
| VTaC / Challenge 2015 | B (alarm) | unknown. ≤ 2,376 patient records [S] | ≈ 5 min pre-alarm, so B5 only and no remote zone | **No** for this design |
| MUSIC | E-risk | 992 [V], but events are months to years later | — | **Not an onset dataset** |
| MIMIC-III/IV waveform + adjudication | C | **unknown** [U] (needs an adjudicated event count) | long pre-onset [S] | **Possibly**, if ≥ 80 eligible first events (≥ 300 for SESOI-level effects) |
| Full-disclosure ICU alarm archive (UCSF class) | B / C | **unknown**: ≤ 461 patients, 533 true VT alarms [S] | continuous [S] | **Possibly**, if ≥ 80 patients have a first sustained VT/VF with ≥ 2 h 20 of pre-onset ECG |

**Endpoint C subgroups** (endpoint assessment C2–C4). Estimating VT and VF
separately with a CI half-width ≈ 0.09 needs ≈ 40 patients **per subgroup**
(σ ≈ 0.28). A pooled C study therefore needs ≈ 80 patients, **with ≥ 40 in
the smaller class**.

## 6. Bias sources that power calculations do not absorb

| Source | Direction | Mitigation |
|---|---|---|
| Selection (event-rich archives, excerpts chosen around events) | unknown, usually toward detectability | patient-level inclusion rules frozen before any signal is read |
| Acquisition (monitor vendor, lead set, artefact detection sensitivity) | false positives if detection < 100% for marginal statistics | beat-level exclusion; correlation-only primary statistic; **measure** detection sensitivity |
| Treatment (antiarrhythmics, ICD therapy, ICU interventions) | either | record and stratify; exclude windows after intervention where timestamps exist |
| Community mining of open datasets | optimistic literature baselines | use only as development data |

---

© 2026 Davarn Morrison · Transition Dynamics
