# Real data — exactly what is needed, and what is blocking

## Status

Real human physiology **was** obtained and tested against Stage A. It was
**rejected by the protocol's own admissibility rules**. The blocker is not
access to some real physiology; it is that the reachable recordings are
minutes long where the protocol needs hours.

| recording | channels | n at 1 Hz | n_eff | required | admissible |
|---|:--:|:--:|:--:|:--:|:--:|
| NeuroKit resting, 8 min, 100 Hz | 5 | 507 | 29 | 50 | **no** |
| NeuroKit event-related, 100 Hz | 5 | 150 | 15 | 50 | **no** |

Both also failed the baseline stationarity screen. Stage B and Stage C were
**not run**: applying them to inadmissible recordings would manufacture a
confident, meaningless result.

---

## What is accessible from this environment

| Source | Status |
|---|:--:|
| raw.githubusercontent.com | reachable |
| pypi.org | reachable |
| physionet.org | **blocked** |
| archive.ics.uci.edu | **blocked** |
| zenodo.org, datadryad.org | **blocked** |
| kaggle.com, huggingface.co | **blocked** |
| api.github.com | scoped to session repos only — no directory listing |

---

## Dataset required

**Primary: HiRID** (High Time Resolution ICU Dataset, Bern University
Hospital). Chosen because it is the only public ICU dataset whose sampling
density supports baseline dynamics estimation.

| Requirement | Value | Why |
|---|---|---|
| Sampling | ~2 min or finer | n_eff ≥ 10p needs many relaxation times of the slowest channel |
| Channels | ≥ 4 simultaneous, ≥ 3 homeostatically defended | The defended channels carry the alignment signal |
| Baseline | ≥ 4 h treatment-quiet per patient | Stage A1 |
| Recordings | ≥ 50 admissible | Stage A5 |
| Labels | **not needed for the first pass** | Stage D is label-free |

### Minimum viable cohort

**50 patients**, each with ≥ 6 h continuous multichannel recording, of which
≥ 4 h is treatment-quiet baseline. Transition labels are **not** required for
Stages B and C. They are needed only if the protocol passes and the programme
advances to exposure control and lead-time testing.

### Variables

| Channel | HiRID-style item | Defended? |
|---|---|:--:|
| Heart rate | continuous monitor | moderate |
| Respiratory rate | continuous monitor | moderate |
| SpO₂ | continuous monitor | **high** |
| Mean arterial pressure | invasive or NIBP | **high** |
| Core temperature | continuous | **high** |
| Lactate / base excess / pH | intermittent labs | **very high** |

Plus, for exclusion accounting only: timestamps of vasopressor, sedation,
fluid-bolus, transfusion and ventilator changes, to enforce the treatment-quiet
rule and the intervention masking.

### Acceptable alternatives

AmsterdamUMCdb (high resolution), eICU (coarser, for external comparison),
MIMIC-IV (~hourly — adequate only for the slowest channels, and a null there
is evidence about sampling rate rather than about the model).

---

## What you would need to provide

Any **one** of the following unblocks Stage B and Stage C:

1. **A HiRID extract**, 50+ patients, as CSV or Parquet: one file per patient
   with a `time` column and one column per channel, at native resolution.
   Credentialed access and a signed DUA are required on your side; the data
   should not be placed in this repository.
2. **Network access** to physionet.org from this environment.
3. **Any equivalent multichannel recording** of ≥ 6 h per subject with ≥ 4
   simultaneous channels — it does not have to be ICU data, and does not need
   transition labels, for the first pass.

Drop files into `data/real/` and run:

```
python3 analysis/adequacy/run_real.py      # Stage A admissibility
python3 analysis/adequacy/adequacy.py      # Stage B and C harness self-test
```

`analysis/adequacy/real_loader.py` derives vital-sign-like channels from raw
waveforms; for already-tabular vitals it can be bypassed.

---

## What would falsify transfer to real physiology

- M-exp selected in < 30% of admissible recordings, **or** beaten by M-null or
  M-rw, **or** selected no more often than on its own phase-randomised
  surrogates → **onset model not transferable**; no mechanism or early-detection
  claim may proceed.
- M-exp-free ≫ M-exp → the form may hold while baseline rates are
  uninformative, which breaks the estimator's independence → failure of the
  protocol as specified.
- Baseline-versus-curvature rate rank correlation < 0.5 → independence guard
  fails.
- Decline rate > 50% → not operationally usable, regardless of performance on
  the remainder.

## What would justify moving to early-detection testing

All of:

1. M-exp selected in ≥ 60% of admissible recordings, and more often than on
   surrogates with a bootstrap CI on the difference excluding zero;
2. M-exp beats M-lin and M-spline on held-out error, CI excluding zero;
3. rate rank correlation ≥ 0.5 with CI excluding zero;
4. decline rate ≤ 50%;
5. ≥ 50 admissible recordings.

Only then: real-data exposure control, alignment, transition labels, lead-time
and base-rate analysis.

---

© 2026 Davarn Morrison · Transition Dynamics
