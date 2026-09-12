# Tier 2 — predictive attribution: result

**Immutable.** One authorised execution of
[`PROTOCOL_ACQUISITION_DISCRIMINATION.md`](PROTOCOL_ACQUISITION_DISCRIMINATION.md)
as frozen at `33b3195c`, run from `main` at `caf1a418…`. Nothing was tuned,
retried on outcomes, or altered.

**Provenance:** this execution had **one aborted pre-outcome launch** caused by
a missing upstream data-preparation dependency (the frozen runner requires an
`npz_sd/` structural cache it does not itself populate). Zero endpoints, labels,
models or metrics were computed at that point and no artifact was written. The
cache was supplied using the already-frozen `analysis/structural/fetch.py`, and
the **unchanged** runner then completed the same authorised execution. Full
detail: [`PROVENANCE_TIER2_LAUNCH.md`](PROVENANCE_TIER2_LAUNCH.md). **This is
not a second confirmatory attempt.**

---

## H. Binding verdict — frozen rule applied mechanically

# UNRESOLVED

| test | 10 min | 15 min | required |
|---|:--:|:--:|---|
| **T2.1** ΔAUPRC(W) CI includes 0 | **yes** | **no** | both |
| **T2.2** ΔAUPRC(W+inj) > 0, CI excludes 0 | no | no | both |
| **T2.3** paired ΔAUPRC(W+inj − W) > 0, CI excludes 0 | no | no | both |

No branch of the frozen decision table matches, so the rule returns its
fallback: **UNRESOLVED**.

The observed pattern is that **no arm produced a predictive increment at
either horizon**. It does not map to the "no arm shows a significant
increment" branch, because that branch requires every CI to *include* zero,
whereas at 15 min the M and W intervals exclude zero on the **negative** side.
The rule is applied exactly as frozen; the pattern is reported, not
reclassified.

---

## A. Feasibility

| | |
|---|:--:|
| requested (frozen Tier-2 cohort) | 600 |
| structural cache populated | **600/600** |
| **usable after prespecified exclusions** | **236** |
| excluded | 364 |

| horizon | windows | positives | prevalence | event-patients | powered |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 10 min | 29,887 | 1,820 | 0.0609 | **156** | **yes** |
| 15 min | 29,431 | 2,774 | 0.0943 | **159** | **yes** |

All power gates pass: ≥150 usable cases (236), ≥30 event-patients (156/159),
≥1% prevalence (6.1%/9.4%). **The run is not underpowered.**

## B. B\* performance (descriptive absolutes)

| horizon | AUROC | AUPRC | Brier | cal. slope | sens@5% FAR | sens@10% FAR |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 10 min | 0.6926 | 0.1726 | 0.0543 | **0.979** | 0.229 | 0.342 |
| 15 min | 0.6856 | 0.2375 | 0.0799 | **0.967** | 0.229 | 0.328 |

B\* is well calibrated on this cohort (slope ≈ 0.97–0.98).

## C. M arm — descriptive only, in no binding rule

| horizon | ΔAUPRC [CI] | ΔAUROC [CI] |
|:--:|:--:|:--:|
| 10 min | −0.00118 [−0.00556, +0.00325] | +0.00783 [−0.00029, +0.01653] |
| 15 min | **−0.00445 [−0.00793, −0.00139]** | +0.00229 [−0.00211, +0.00682] |

## D. W arm

| horizon | ΔAUPRC [CI] | ΔAUROC [CI] |
|:--:|:--:|:--:|
| 10 min | −0.00081 [−0.00626, +0.00447] | +0.00991 [−0.00003, +0.02033] |
| 15 min | **−0.00434 [−0.00802, −0.00110]** | +0.00267 [−0.00220, +0.00788] |

**T2.1 status:** satisfied at 10 min, **not** at 15 min (the interval excludes
zero, negatively). T2.1 therefore **fails** as a both-horizon condition.

## E. W+inj arm

| horizon | ΔAUPRC [CI] | ΔAUROC [CI] |
|:--:|:--:|:--:|
| 10 min | +0.00008 [−0.00655, +0.00634] | **+0.01400 [+0.00459, +0.02459]** |
| 15 min | −0.00402 [−0.00908, +0.00033] | **+0.00576 [+0.00022, +0.01178]** |

**T2.2 status: FAILS at both horizons.** ΔAUPRC is +0.00008 and −0.00402, and
neither interval excludes zero on the positive side.

## F. Paired W+inj − W — the load-bearing contrast

| horizon | paired ΔAUPRC [CI] |
|:--:|:--:|
| 10 min | +0.00089 [−0.00278, +0.00504] |
| 15 min | +0.00032 [−0.00251, +0.00300] |

**T2.3 status: FAILS at both horizons.** Both intervals comfortably include
zero. **Injecting the acquisition process changed predictive performance by
less than one thousandth of AUPRC.**

## G. Secondary and frozen metrics

| horizon | arm | AUROC | AUPRC | Brier | cal. slope | sens@5% | sens@10% |
|:--:|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 10 min | B\* | 0.6926 | 0.1726 | 0.0543 | 0.979 | 0.229 | 0.342 |
| | M | 0.7005 | 0.1714 | 0.0544 | 0.947 | 0.231 | 0.336 |
| | W | 0.7026 | 0.1718 | 0.0544 | 0.951 | 0.228 | 0.328 |
| | W+inj | 0.7067 | 0.1727 | 0.0543 | 0.959 | 0.224 | 0.336 |
| 15 min | B\* | 0.6856 | 0.2375 | 0.0799 | 0.967 | 0.229 | 0.328 |
| | M | 0.6879 | 0.2330 | 0.0802 | 0.978 | 0.222 | 0.320 |
| | W | 0.6883 | 0.2332 | 0.0801 | 0.980 | 0.221 | 0.319 |
| | W+inj | 0.6914 | 0.2335 | 0.0801 | 0.986 | 0.219 | 0.322 |

**An AUROC observation, explicitly secondary.** W+inj is the only arm whose
ΔAUROC interval excludes zero, at both horizons (+0.0140 and +0.0058). AUROC is
**not** part of the frozen Tier-2 binding rule (T2.1–T2.3 are AUPRC-based), so
this **cannot and does not** change the verdict. It is recorded because
suppressing it would be selective. Note its direction: the gain belongs to the
**more monitor-like** arm, which is what both $H_{\text{instr}}$ and
$H_{\text{target}}$ would predict — but no frozen rule adjudicates it, and none
is invented now.

Sensitivity at 10% FAR is **not** improved by any arm over B\* at either
horizon. Calibration is essentially unchanged throughout (0.947–0.986).

---

## I. Interpretation boundary

### What this establishes

- **The ABP-only autocorrelation pair carries no predictive increment over
  B\*** at 10 or 15 min, in any of the three arms, on 236 fresh patients with
  adequate power.
- **The injected acquisition process changed predictive performance by
  essentially nothing**: paired contrasts of +0.0009 and +0.0003 AUPRC, both
  intervals spanning zero.
- Because no arm produced an increment, **there was no predictive increment to
  attribute**, and the experiment cannot assign one to acquisition or to
  physiology.

### What this does NOT establish

- **Not** $H_{\text{instr}}$ supported. T2.1–T2.3 are not jointly met.
- **Not** $H_{\text{phys}}$ supported, and not "the signal survived". W showed
  no positive increment to survive anything.
- **Not** a refutation of Tier 1. Tier 1 established, at the measurement level,
  that the acquisition transformation is sufficient to reproduce a substantial
  component of the arterial autocorrelation structure. That stands, and it was
  never a claim about prediction.
- **Nothing about the original H-AC increment.** That was a **six-channel**
  aggregate; this tested a **two-feature ABP-only** block. Its absence here does
  not explain, reproduce, or contradict it. This limitation was declared in the
  frozen protocol before the run.
- **No claim about physiology**, and no mechanistic label — not recovery,
  relaxation, critical slowing down, homeostasis, stiffness, $\Lambda$,
  $\Sigma_0^{-1}$, $S(t)$, $Q_i$, deformation, persistence, consciousness or
  qualia.
- **No generalisation from ABP to the other five channels.** The six-channel
  matched-pair design remains invalid.

$H_{\text{target}}$ remains live and unexamined. **H-AC remains NOT SUPPORTED.**

### Limitations

- The ABP-only block is 2 features against B\*'s 41; the design was always at
  risk of being unable to detect an attributable increment, and that is what
  occurred. Declared in advance, not discovered afterwards.
- 236 arterial-line patients under general anaesthesia; 364 of 600 excluded,
  chiefly for absent arterial lines.
- The verdict is the frozen rule's fallback. A decision table that anticipated
  significantly *negative* arm intervals would have classified this pattern
  more informatively; it did not, and the rule was not amended to fit the
  result.

---

© 2026 Davarn Morrison · Transition Dynamics
