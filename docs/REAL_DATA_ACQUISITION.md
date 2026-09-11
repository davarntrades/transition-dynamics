# Real-data acquisition specification

## Summary

Real human physiology **was obtained and tested**, not assumed unavailable.
Two independent real datasets were acquired through legitimate open channels
and both were rejected by the frozen protocol's Stage A rules.

| Dataset | Real? | Obtained | Admissible |
|---|:--:|:--:|:--:|
| MIMIC-III Clinical Database Demo (ODbL, open access) | yes | yes, 11 ICU stays, 4 channels, up to 367 h | **0 / 11** |
| NeuroKit human ECG/RSP/EDA, 100 Hz | yes | yes, 2 recordings | **0 / 2** |

**Stage B and Stage C were not run.** No threshold was altered.

---

## The finding

At **hourly charting resolution** — the resolution of MIMIC-III, MIMIC-IV and
eICU — the protocol's two Stage A requirements are **jointly unsatisfiable**:

- a short baseline fails the effective-sample-size rule ($n_\text{eff} \ge 10p$);
- a baseline long enough to pass it is no longer stationary, because real ICU
  patients drift over multi-day windows.

Across 11 real ICU stays × 6 candidate baseline lengths (4 h to 168 h),
**0 of 55 combinations satisfied both rules.** The single combination reaching
$n_\text{eff} \ge 40$ (stay 264854, 96 h baseline, $n_\text{eff}=47.5$) showed a
0.90 SD baseline shift against a 0.5 SD limit.

> This does **not** falsify the exponential-approach model. It shows that
> hourly-charted ICU databases cannot supply the data the test requires. The
> model remains **untested** on real physiology.

This confirms by measurement what `DATASET_REQUIREMENTS.md` predicted by
calculation: the test needs ~2-minute sampling, not hourly.

### A threshold worth revisiting — but not now

The 0.5 SD stationarity screen rejects **100%** of real ICU baselines examined.
That may mean the screen is too strict for real physiology rather than that
real physiology is unusable.

**It is not changed here.** Altering a preregistered threshold after seeing the
real-data result is precisely the move this programme forbids. If it is to be
revised, that must be a dated amendment written *before* the next real-data
analysis, with the justification stated in advance.

---

## What is accessible from this environment

| Source | Status |
|---|:--:|
| github.com — `git clone` of any public repo | **reachable** |
| raw.githubusercontent.com | reachable |
| pypi.org, files.pythonhosted.org | reachable |
| physionet.org, archive.physionet.org | **403 — organisation policy denial** |
| archive.ics.uci.edu, zenodo.org, figshare.com | **403 — policy denial** |
| datadryad.org, osf.io, dataverse.harvard.edu | **403 — policy denial** |
| kaggle.com, huggingface.co | **403 — policy denial** |
| vitaldb.net, api.vitaldb.net | **403 — policy denial** |

These are organisation policy denials reported by the egress proxy. Per the
proxy documentation they are to be reported, not retried or worked around. No
authentication, licence or access control was bypassed.

---

## Dataset required

### Primary: HiRID

High Time Resolution ICU Dataset, Bern University Hospital. Chosen because its
sampling density is the only public ICU option that can satisfy
$n_\text{eff} \ge 10p$ with a clinically plausible baseline length.

| Property | Requirement |
|---|---|
| Sampling | ~2 min for monitored vitals |
| Channels | ≥ 4 simultaneous; ≥ 3 homeostatically defended |
| Baseline | ≥ 4 h treatment-quiet per subject |
| Subjects | ≥ 50 admissible |
| Labels | **not required** for Stages B and C |

**Why 2-minute sampling fixes the problem.** At 2 min, a 4 h baseline gives 120
samples instead of 4. With a lag-1 autocorrelation of 0.6 that is
$n_\text{eff}\approx 30$; an 8 h baseline gives $n_\text{eff}\approx 60$,
clearing the bar **while remaining short enough to stay stationary**. The
joint constraint becomes satisfiable.

### Files and variables

From HiRID's `observation_tables` (or equivalent), per patient:

| Channel | Typical HiRID variable | Defended |
|---|---|:--:|
| Heart rate | monitor HR | moderate |
| Respiratory rate | monitor RR | moderate |
| SpO₂ | pulse oximetry | **high** |
| Mean arterial pressure | invasive ABP mean or NIBP mean | **high** |
| Core temperature | continuous temperature | **high** |

Plus, for exclusion accounting only, timestamps from `pharma_records` for
vasopressor, sedation, fluid-bolus and transfusion changes, to enforce the
treatment-quiet rule.

### Credentials

HiRID is distributed via PhysioNet and requires a free PhysioNet account,
completion of the CITI "Data or Specimens Only Research" training, and
acceptance of the dataset's data use agreement. **That process must be
completed by you.** The data must not be committed to this repository.

### Acceptable alternatives

| Dataset | Sampling | Note |
|---|---|---|
| **VitalDB** | 1–500 Hz | Open access, no credentialing for the public set; ~6,000 surgical cases, hours each. Would satisfy the protocol comfortably. Host is policy-blocked here |
| AmsterdamUMCdb | ~1 min | Credentialed; high resolution |
| MIMIC-IV waveform subset | high | Small matched cohort only |
| MIMIC-IV / eICU chartevents | ~hourly | **Shown here to be inadequate.** A null on these is evidence about sampling rate, not about the model |

---

## What you would need to provide

Any **one** of these unblocks Stages B and C:

1. **A HiRID or VitalDB extract**: ≥ 50 subjects, ≥ 6 h each, ≥ 4 channels, at
   native resolution. One file per subject, a `time` column plus one column per
   channel, CSV or Parquet.
2. **Network access** to physionet.org or api.vitaldb.net from this
   environment.
3. **Any equivalent recording** of ≥ 6 h per subject with ≥ 4 simultaneous
   channels sampled at ≤ 5 min. It need not be ICU data and needs **no
   transition labels** for the first pass.

### Directory structure expected

```
data/real/
  <dataset>/
    subject_0001.csv      # time, HR, RR, SPO2, MAP, TEMP, ...
    subject_0002.csv
    ...
```

Then run:

```
python3 analysis/adequacy/run_real.py           # Stage A on CSV recordings
python3 analysis/adequacy/run_mimic_stage_a.py  # Stage A on a MIMIC-style SQLite
python3 analysis/adequacy/adequacy.py           # Stage B and C harness self-test
```

Loaders already in the repository:

| File | Purpose |
|---|---|
| `analysis/adequacy/mimic_loader.py` | MIMIC-style SQLite → regular-grid multichannel arrays. Runs unchanged on a full MIMIC-IV extract |
| `analysis/adequacy/real_loader.py` | Raw waveforms → vital-sign-like channels |
| `analysis/adequacy/adequacy.py` | Stage A admissibility, Stage B comparison, Stage C rate consistency, surrogates |

---

## Falsification and advancement, unchanged

**Falsifies transfer:** M-exp selected < 30%; or beaten by the null or random
walk; or no advantage over phase-randomised surrogates; or the free-rate
exponential substantially outperforms the baseline-rate-constrained form; or
rate rank-correlation < 0.5; or decline > 50%.

**Justifies proceeding to early-detection testing:** all of — ≥ 60% selection
and more often than surrogates with a bootstrap CI excluding zero; better
held-out prediction than linear and natural-spline comparators; rate
correlation ≥ 0.5; decline ≤ 50%; ≥ 50 admissible recordings.

Passing that gate would **not** demonstrate early detection. It would establish
only that the dynamical assumptions look transferable enough to justify testing
whether they provide useful pre-transition warning.

---

© 2026 Davarn Morrison · Transition Dynamics
