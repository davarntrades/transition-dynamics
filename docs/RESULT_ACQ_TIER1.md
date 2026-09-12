# Tier 1 — measurement-level acquisition identification: result

**Immutable.** One execution of
[`PROTOCOL_ACQUISITION_DISCRIMINATION.md`](PROTOCOL_ACQUISITION_DISCRIMINATION.md)
as frozen at commit `33b3195ca002d84092984a3114815f7c5044b8fc`. Nothing was
tuned, retried or altered. **No outcome information of any kind was used.**

---

## Binding verdict

# ACQUISITION SUFFICIENT — measurement level

Determined by **T1.1 ∧ T1.3** only. Both passed.

### The maximum permitted claim, verbatim

> **The known acquisition transformation is sufficient to reproduce a
> substantial component of the arterial autocorrelation structure.**

Nothing beyond this sentence is established. In particular this result does
**not** explain the predictive AUPRC increment, does **not** generalise beyond
the arterial pathway, and makes **no** claim about physiology. H-AC remains
**NOT SUPPORTED**.

---

## Freeze verification (before execution)

| check | result |
|---|---|
| HEAD == `33b3195c…` | **match** |
| working tree | 0 uncommitted |
| all 14 files vs `acq_freeze_manifest.json` | **14/14 SHA-256 identical** |
| 12 pilot cases excluded from Tier 1 | pilot ∩ tier1 = ∅ |
| Tier-1 set == frozen development split minus pilot | **confirmed**, `dev[12:]` |
| Tier-2 cohort | **not accessed** |

## Cohort

| | |
|---|:--:|
| Tier-1 cases attempted | 388 |
| **usable** | **261** |
| AC windows | **51,563** |
| excluded | 127 — missing `SNUADC/ART` or `ART_MBP` 120, waveform coverage 1, beat-gate 6 |

Feasibility floors (≥100 cases, ≥500 windows) exceeded by wide margins.

---

## T1.1 — BINDING — does injection increase AC?

Paired within-window, primary injection cell (hold 4 s, quantisation 1 mmHg).

| quantity | value |
|---|:--:|
| patients / windows | 261 / 51,563 |
| median AC(W) | **0.80336** |
| median AC(W+inj) | **0.90584** |
| **paired median ΔAC** | **+0.08376** |
| 95% patient-bootstrap CI | **[+0.07428, +0.09517]** |
| windows with ΔAC > 0 | 90.68% |
| ΔAC ≥ +0.05? | **yes** |
| CI excludes zero? | **yes** |
| | **PASS** |

## T1.3 — BINDING — saturating dose-response

Median AC by injected hold:

| hold | implied hold fraction | median AC |
|:--:|:--:|:--:|
| 2 s (identity) | 0.000 | 0.79390 |
| 4 s | 0.500 | 0.90584 |
| 6 s | 0.667 | 0.90102 |
| 8 s | 0.750 | 0.91112 |

**(a) contrasts against the 2 s identity level**

| contrast | median Δ | 95% CI | ≥ +0.05 | CI excludes 0 | pass |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 s − 2 s | +0.09280 | [+0.08274, +0.10366] | yes | yes | **PASS** |
| 6 s − 2 s | +0.09682 | [+0.08606, +0.10839] | yes | yes | **PASS** |
| 8 s − 2 s | +0.10786 | [+0.09540, +0.12150] | yes | yes | **PASS** |

**(a) PASS** — all three.

**(b)** Spearman ρ(implied hold fraction, median AC) = **0.8000** ≥ 0.60 → **PASS**

**(c) saturation.** Increments: 2→4 = **+0.11194**, 4→6 = **−0.00483**,
6→8 = **+0.01010**.

$$\text{ratio}=\frac{0.11194}{\max(-0.00483,\;0.01010)}=\frac{0.11194}{0.01010}=\mathbf{11.08}\;\ge\;2.0$$

**(c) PASS.**

**T1.3 overall: PASS.**

---

## Characterisation — non-binding, and it changed nothing

Reported separately per the frozen protocol. None of these could have altered
the verdict, and none did.

**T1.2 gap closure toward M** (explicitly non-binding — M is descriptive only):
median AC(W) 0.80336, AC(M) 0.92564, AC(W+inj) 0.90584; base gap 0.12229;
**G = +0.8381**, CI [+0.8073, +0.8649]. Meets its reported threshold.

**T1.4 dose-response at the monitor's measured hold fraction 0.560:** predicted
AC **0.90411** against observed median AC(M) **0.92564**; |error| **0.02154**
≤ 0.05. Meets its reported threshold.

**T1.5 quantisation component:** **NON-CONTRIBUTORY** at every hold —
−0.00381, −0.00235, −0.00122, −0.00078, all far below the 0.02 magnitude
threshold and all *negative*. **Quantisation is not the mechanism;
sample-and-hold is.**

**W vs M disagreement** (261 cases, 1,568,801 paired bins): Pearson r median
**0.8702** (IQR 0.806–0.915), bias +1.20 mmHg, **SD of difference 6.52 mmHg**.
The two remain materially different measurements — which is why M carries no
identification claim here.

**Detector performance:** bin yield median **0.889** (IQR 0.849–0.916, min
0.704); **61.9** beats/min median; waveform coverage median 1.000, min 0.815.
Detector-gate failure rate among ABP-bearing cases **6/268 = 2.2%**, far inside
the 30% limitation threshold.

---

## What this does and does not license

| claim | status |
|---|---|
| Acquisition changes arterial AC structure | **supported by this result** |
| Acquisition improves prediction of a monitor-defined endpoint | **not addressed** — Tier 2 |
| Physiology generates predictive temporal structure | **not addressed by any tier here** |

These three are not equivalent and are not collapsed.

## Limitations

- **Sufficiency is not necessity.** A hold process reproduces the AC structure;
  this does not prove the monitor's AC arises that way, nor that physiology
  contributes nothing.
- The monitor's *nominal* refresh is 2 s, yet its AC (0.926) matches injected
  holds of 4–8 s. Its measured hold fraction is 0.560. The identification is
  about **a hold process of the observed magnitude**, not about the nominal
  cadence.
- Arterial pathway only. SpO₂ is not reconstructable at all; HR and EtCO₂ are
  detector- and device-contaminated. **The six-channel matched-pair design
  remains invalid.**
- W and M still disagree by 6.52 mmHg SD; the monitor's internal smoothing,
  filtering and artefact rejection are not reproducible.
- 261 development patients under general anaesthesia with arterial lines.
- $H_{\text{target}}$ (the Tier-2 endpoint is itself defined from monitor
  `ART_MBP`) is untouched by Tier 1 and remains live.

---

© 2026 Davarn Morrison · Transition Dynamics
