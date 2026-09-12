# H-AC — one-shot confirmatory result

**Immutable.** Produced by a single preregistered execution of
[`PROTOCOL_AUTOCORR.md`](PROTOCOL_AUTOCORR.md) as frozen at commit
`9efe10c3c8cc31fd25c871c9ed80b2af89c89b15`. Nothing was tuned, retried,
substituted, reinterpreted or altered on the basis of anything observed in the
confirmatory cohort.

---

## Binding verdict

# NOT SUPPORTED

The binding STRICT criterion fails on **criterion 2 (ΔAUROC)** at both required
horizons. STRICT is the only rule capable of producing SURVIVED.

Not FALSIFIED — no ΔAUPRC interval lies below zero.
Not UNRESOLVED — 130–155 event-patients per horizon, prevalence 2.6–8.9%, no
harness defect.

---

## 1. Freeze verification

| check | result |
|---|---|
| working tree clean | 0 uncommitted files |
| HEAD == frozen commit | `9efe10c…` **match** |
| all 10 frozen files vs `rs_freeze_manifest.json` | **10/10 SHA-256 identical** |

Verified **before** any confirmatory patient was accessed. The runner
(`run_hac_confirmatory.py`, commit `7d24a38`) was written and committed after
verification and before the cohort was fetched.

## 2. Confirmatory cohort accounting

| | |
|---|:--:|
| requested (frozen split) | 600 |
| fetched | **600/600** |
| **usable after prespecified exclusions** | **228** |
| evaluation windows | **28,219** |

Exclusions: coverage 215 (chiefly no arterial line), hypotension in baseline
155, analysable span 2.

| horizon | windows | positives | prevalence | patients | event-patients |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 min | 28,012 | 719 | 0.0257 | 228 | **130** |
| 10 min | 27,692 | 1,577 | 0.0569 | 228 | **152** |
| 15 min | 27,259 | 2,418 | 0.0887 | 228 | **155** |

All horizons exceed the frozen power floors (≥ 30 event-patients, ≥ 1%
prevalence).

## 3. Complete preregistered results

Bonferroni 95% CI (α = 0.05/3), 2000 patient-level bootstrap resamples.

| horizon | AUROC B\* → A | ΔAUROC [CI] | AUPRC B\* → A | ΔAUPRC [CI] |
|:--:|:--:|:--:|:--:|:--:|
| 5 min | 0.7163 → 0.7219 | +0.0057 [−0.0145, +0.0259] | 0.0945 → 0.0988 | +0.00433 [−0.00509, +0.01397] |
| **10 min** | 0.6929 → 0.6950 | **+0.0022 [−0.0126, +0.0171]** | 0.1785 → 0.1917 | **+0.01316 [+0.00241, +0.02366]** |
| **15 min** | 0.6788 → 0.6773 | **−0.0014 [−0.0156, +0.0135]** | 0.2174 → 0.2319 | **+0.01451 [+0.00343, +0.02594]** |

### Calibration and false-alert burden

| horizon | Brier B\* → A (limit) | cal. slope B\* → A (\|Δ\|) | sens@10% FAR B\* → A |
|:--:|:--:|:--:|:--:|
| 5 min | 0.0246 → 0.0244 (0.0296) | 0.899 → 0.942 (0.043) | 0.3700 → 0.3505 |
| 10 min | 0.0513 → 0.0507 (0.0563) | 0.916 → 0.947 (0.031) | 0.3386 → **0.3583** |
| 15 min | 0.0769 → 0.0764 (0.0819) | 0.913 → 0.948 (0.035) | 0.3019 → **0.3267** |

### Secondary endpoint — MAP < 55 mmHg

| horizon | event-patients | prevalence | AUPRC B\* → A | ΔAUPRC [CI] | ΔAUROC [CI] |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 min | 83 | 0.0102 | 0.1454 → 0.1584 | +0.0133 [−0.0007, +0.0282] | +0.0004 [−0.0120, +0.0120] |
| 10 min | 112 | 0.0271 | 0.2368 → 0.2731 | **+0.0367 [+0.0167, +0.0602]** | +0.0042 [−0.0151, +0.0230] |
| 15 min | 115 | 0.0455 | 0.2675 → 0.3055 | **+0.0382 [+0.0184, +0.0583]** | +0.0119 [−0.0030, +0.0270] |

## 4. STRICT criterion, item by item

| # | criterion | 10 min | 15 min | result |
|:--:|---|:--:|:--:|:--:|
| 1 | ΔAUPRC > 0, Bonferroni CI excludes 0 | +0.0132 [+0.0024, +0.0237] ✓ | +0.0145 [+0.0034, +0.0259] ✓ | **PASS** |
| 2 | **ΔAUROC > 0.01, Bonferroni CI excludes 0** | **+0.0022, CI spans 0** ✗ | **−0.0014, CI spans 0** ✗ | **FAIL** |
| 3 | all three destructive controls | PASS | PASS | **PASS** |
| 4 | Brier ≤ B\*+0.005 and \|Δslope\| ≤ 0.15 | 0.0507 ≤ 0.0563; 0.031 | 0.0764 ≤ 0.0819; 0.035 | **PASS** |
| 5 | sens@10% FAR ≥ B\* | 0.3583 ≥ 0.3386 | 0.3267 ≥ 0.3019 | **PASS** |
| 6 | reproduced on MAP < 55 at ≥ 1 horizon | +0.0367 CI excludes 0 | +0.0382 CI excludes 0 | **PASS** |

**Five of six met. Criterion 2 fails at both required horizons. STRICT is not
met. The binding verdict is NOT SUPPORTED.**

### Directional prespecification — held

The protocol predicted success at 10 and 15 min and not at 5 min. On ΔAUPRC
this is exactly the observed pattern: the 5 min interval includes zero
(+0.0043 [−0.0051, +0.0140]) while 10 and 15 min exclude it. The horizon
pattern is not reinterpreted; it is recorded as predicted, and it does not
alter the verdict.

## 5. SECONDARY / PROVISIONAL — AUPRC-led observation

**Labelled per the frozen protocol. No advancement authority. It does not
alter the binding verdict of NOT SUPPORTED, and is not a qualified pass, a
partial survival, a trend, or a near-miss.**

> **Provisional AUPRC-led observation:** criteria 1 and 3–6 met, criterion 2
> (AUROC) not met.

This is the outcome declared as most likely in the frozen protocol before the
run. The confirmatory cohort reproduced the development pattern — including its
failure mode.

## 6. Destructive controls — all three passed at all three horizons

200 permutations each. Real ΔAUPRC must exceed the 95th percentile.

| horizon | control 1 within-window (real vs p95) | control 2 channel row-wise (real vs p95) | control 3 repfrac |
|:--:|:--:|:--:|:--:|
| 5 min | +0.00427 vs +0.00047 | +0.00427 vs +0.00070 | alone +0.00038 < +0.00214 |
| 10 min | +0.01319 vs +0.00220 | +0.01319 vs +0.00148 | alone −0.00015 < +0.00660 |
| 15 min | +0.01454 vs +0.00049 | +0.01454 vs −0.00005 | alone +0.00268 < +0.00727 |

Control distribution means are ≈ 0 (−0.0008 to +0.0011). Destroying temporal
ordering within the window, or destroying which channel is autocorrelated,
removes the AUPRC increment in both cases. Adding the repeated-sample fraction
to the model changes it by −0.0018 to +0.0011, far inside the CI width.

## 7. Status of $R_{\mathrm{instr}}$

$$R_{\text{instr}}:\ \text{the AUPRC increment reflects monitor acquisition
behaviour — refresh rate, sample-and-hold, quantisation — not physiology.}$$

**$R_{\mathrm{instr}}$ remains a live competing explanation of equal standing.
This experiment did not and could not discriminate against it.**

The destructive controls constrain *what kind* of information the increment
depends on — temporal order within the window, and channel identity — but
monitor acquisition behaviour has both properties. Different channels are held
and refreshed differently, and shuffling samples destroys hold structure
exactly as it destroys physiological structure. The repeated-sample probe
excludes only the crudest form of the artefact.

Accordingly, and regardless of the AUPRC result, nothing here is evidence
specifically for physiological recovery, relaxation, critical slowing down,
homeostasis, $\Lambda$, $\Sigma_0^{-1}$, $S(t)$, $Q_i$, deformation,
persistence, consciousness, or qualia. No such reading is attached.

## 8. Limitations

- **The binding criterion failed.** ΔAUROC is +0.0022 and −0.0014 at the two
  required horizons — one of them negative. Whatever the AUPRC increment
  reflects, it does not improve global discrimination.
- $R_{\mathrm{instr}}$ is unresolved and unresolvable by this design, which
  needs channels with genuinely different acquisition characteristics.
- One endpoint pair, one setting, six channels, three horizons, 228
  arterial-line patients under general anaesthesia.
- Absolute performance is not a clinical estimate: vasopressor treatment
  removes events that would otherwise have occurred. This affects both arms
  identically, so the A-versus-B\* contrast stands.
- 38% of requested cases were usable; the arterial-line requirement restricts
  the cohort to higher-acuity surgery.

### Data-quality and harness issues encountered

- One of 600 downloads (case 1616) was truncated by a connection reset. It was
  refetched and succeeded; the manifest is complete at 600/600. No case was
  dropped for a network reason.
- No harness defect occurred during the run.
- `fast_ac.py`, the reduced fast path used by the 200-permutation controls, was
  verified **bit-identical** to the frozen `variability.grids()` in both modes
  on 8 development cases before use.
- The controls reuse the median λ from the real run's inner CV — the convention
  the structural protocol's surrogate already used. No threshold is affected.

## 9. Separation from development

Development and confirmatory results are **not pooled, averaged,
meta-analysed, or combined**, and the development numbers are not restated
here. They are in
[`RESULT_REPRESENTATION_SEARCH.md`](RESULT_REPRESENTATION_SEARCH.md) and were
the reason for testing this candidate, not evidence about it.

For the record, B\* behaves differently on this cohort than on development —
higher AUROC and AUPRC, and far better calibrated (slope ≈ 0.91 against 0.25
at 5 min). This is a different and larger set of patients. It is noted, not
reconciled.

---

© 2026 Davarn Morrison · Transition Dynamics
