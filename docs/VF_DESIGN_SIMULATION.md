# VF onset programme — design simulation (synthetic only)

> **Status: DESIGN-STAGE EVIDENCE ABOUT THE PROTOCOL, NOT ABOUT VF.**
> Every number below comes from synthetic data generated under the
> assumptions in §1. **No SDDB, chfdb or NSRDB record was read.** These
> numbers describe how the draft v2 protocol behaves *if* the assumptions
> hold. They are not established properties of SDDB, and they are
> recalibrated on outcome-blind real data before freezing (protocol §4.3).
>
> Code: [`analysis/vf/design_sim.py`](../analysis/vf/design_sim.py) ·
> Results: [`analysis/results/vf_design_sim.json`](../analysis/results/vf_design_sim.json)
> (seed 20261103) · Reproduce:
> `python3 analysis/vf/design_sim.py --only rules,guard,overlap,power,airm`

---

## 1. What is simulated, and what is assumed

| Element | Implementation | Faithful to the protocol? |
|---|---|---|
| Patients | one VF event each. Pre-onset duration $T$ ~ U(140, 1200) min ("mixed"). 3 no-VF records of 24 h | yes (the duration distribution is an assumption) |
| Features | minute-level AR(1), φ = 0.9 (φ = 0.97 as sensitivity). 4 M1 channels and 3 TD channels with corr(TD, M1₀) = 0.5 and a shared TD factor; 1 SQI channel | **assumed** structure |
| Windows | 5-min rolling windows on a 1-min grid (overlapping); baseline standardisation | yes |
| Zones | settling 15, baseline 30, remote lead ≥ 60, grey zone, bins (2,5], (5,10], (10,15], (15,30] | yes |
| Model | leave-one-patient-out (LOPO), balanced ridge logistic, λ = 1, M1 vs M4 = M1 + TD | yes |
| Statistic | per-patient within-patient ΔAUROC; t-interval at α = 0.0125; one-sided sign test p < 0.025 | yes |
| Decision rule | ≥ 2 bins including B15 or B30 | yes |
| Precursors | *step30*: sustained shift over the last 30 min (long lead). *ramp30*: linear rise into onset (trigger-weighted). *late5*: last 5 min only. Patient heterogeneity: amplitude × N(1, 0.5²) | **assumed** shapes |
| Not simulated | M2, the comparator contrasts, Analysis B, real beat-level covariance estimation (except §6), AF, missingness | — |

The TD increment $b$ is in latent-SD units. Each table also reports the
resulting **expected mean ΔAUROC at the design n**, which is the
interpretable scale. The mapping from $b$ to ΔAUROC depends on the assumed
structure.

**Approximations, declared.**

1. The pseudo-onset null runs one LOPO per offset and then draws one offset
   per subject. Its subject composition differs from the real cohort, since
   only long recordings and no-VF records contribute.
2. The rules stage uses 19 offsets at most and 999 draws, where the protocol
   specifies 9,999.
3. Elapsed-time matching uses the fixed unfitted TD composite, as in the
   protocol.
4. The alarm rule is 3 consecutive 1-min windows with a 15-min refractory
   period, as in the protocol.

---

## 2. Power and minimum detectable effect (n = 20 unless stated; 200 replicates)

### 2.1 Sustained long-lead precursor (*step30*)

| latent b | expected mean ΔAUROC per bin | power per bin (B5/B10/B15/B30) | P(rule met) |
|:--:|:--:|:--:|:--:|
| 0 | −0.012 to −0.016 | ≤ 0.01 | **0.000** |
| 0.5 | 0.023–0.025 | ≤ 0.03 | 0.005 |
| 1.0 | 0.10–0.12 | 0.14–0.22 | 0.13 |
| 1.5 | 0.17–0.19 | 0.48–0.53 | 0.55 |
| 2.0 | 0.22–0.24 | 0.74–0.78 | **0.82** |
| 3.0 | 0.27–0.30 | 0.91–0.95 | 0.95 |

At **n = 12**, ΔAUROC ≈ 0.22–0.24 gives rule power 0.48. ΔAUROC ≈ 0.28–0.31
gives 0.70.

### 2.2 Trigger-weighted precursor (*ramp30*)

| n | latent b | mean ΔAUROC (B5 / B15 / B30) | power (B5 / B15 / B30) | P(rule met) |
|:--:|:--:|:--:|:--:|:--:|
| 20 | 2.0 | 0.215 / 0.142 / 0.036 | 0.54 / 0.24 / 0.06 | 0.24 |
| 20 | 3.0 | 0.295 / 0.224 / 0.055 | 0.87 / 0.63 / 0.08 | 0.62 |
| 12 | 3.0 | 0.287 / 0.216 / 0.062 | 0.49 / 0.31 / 0.07 | 0.28 |
| 8 | 3.0 | 0.285 / 0.209 / 0.042 | 0.19 / 0.13 / 0.03 | 0.10 |

### 2.3 What this establishes about the design

- **The 80%-power minimum detectable effect is about 0.23 ΔAUROC per bin at
  n = 20**, and above 0.30 at n = 12. This is roughly **twice** the 0.12 that
  v1 derived analytically from an assumed σ = 0.15.
- **The null SD of per-patient Δ is 0.16–0.21.** It grows to 0.25–0.31 under
  a heterogeneous effect, so the analytic shortcut understated both.
- **The decision rule is very conservative.** Under H0 it fired in 0–0.5% of
  studies, against a nominal 5%. The causes are Bonferroni over four bins that
  share data, the conjunction with the sign test, and the two-bin
  requirement. Conservativeness is part of why the MDE is large.
- **The rule detects long-lead precursors only.** A trigger-weighted precursor
  of the same size is mostly reported as TRIGGER-PROXIMAL (B5/B10 only), and
  B30 power stays ≤ 0.13 for every ramp30 effect simulated. This is intended
  (protocol §13.2), but readers must not interpret a null as "no pre-onset
  change".
- **Every incremental effect this programme has measured on real data lies
  between −0.004 and +0.014.** Effects of that size are undetectable here
  (power ≈ α).

### 2.4 The binding large-effect falsification flag

Rate at which "one-sided 95% upper bound < δ in all four bins" fires:

| true state | δ = 0.10 | δ = 0.15 | δ = 0.20 |
|---|:--:|:--:|:--:|
| H0, n = 20 (ramp / step null) | 0.38 / 0.53 | **0.66 / 0.81** | 0.82 / 0.94 |
| H0, n = 12 | 0.25 / 0.32 | 0.44 / 0.59 | 0.64 / 0.73 |
| step30, ΔAUROC ≈ 0.11, n = 20 | 0.005 | 0.09 | 0.22 |
| step30, ΔAUROC ≈ 0.18, n = 20 | 0.000 | 0.005 | 0.045 |
| step30, ΔAUROC ≈ 0.23, n = 20 | 0.000 | 0.000 | 0.005 |

With **δ = 0.10, the binding falsification fires in fewer than half of
null studies**, so the experiment would usually end without either verdict.
δ = 0.15 fires in about two-thirds to four-fifths of null studies at n = 20.
It almost never fires wrongly, i.e. when the true effect is ≥ δ: 0.5% at a
true 0.18. The protocol's δ is a research decision (D9). The simulation
favours **0.15**.

---

## 3. Overlapping windows

### 3.1 Correlation and effective sample size

Correlation of the window feature (φ = 0.9) by lag in minutes:

| lag (min) | 1 | 2 | 3 | 5 | 10 | 15 | 30 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| corr | 0.985 | 0.949 | 0.898 | 0.779 | 0.546 | 0.406 | 0.028 |

The correlation length is about 15–20 min, and the lag-1 correlation is 0.99
at φ = 0.97. The bins contain 3, 5, 5 and 15 windows, which amount to about
**1, 1, 1 and 1–2 effective independent observations per patient**.

### 3.2 Does the 60-s stride add information? No

Null SD of per-patient Δ (n = 20, 100 replicates):

| | B5 | B10 | B15 | B30 |
|---|:--:|:--:|:--:|:--:|
| φ 0.9, stride 1 min | 0.193 | 0.197 | 0.212 | 0.174 |
| φ 0.9, stride 5 min (non-overlapping) | 0.206 | 0.200 | 0.220 | 0.176 |
| φ 0.97, stride 1 min | 0.214 | 0.212 | 0.217 | 0.225 |
| φ 0.97, stride 5 min | 0.226 | 0.220 | 0.218 | 0.203 |

Overlap neither helps nor biases the patient-level inference. The 60-s grid
buys alarm-time resolution only.

### 3.3 Window-level uncertainty is invalid

Within-patient AUROC (B30 vs remote, single feature, no effect): the
empirical SD across noise realisations is **0.241**. The Hanley–McNeil SE,
which treats windows as independent, gives **0.076**: a **3.2-fold
underestimate**. Any window-level CI or p-value would be grossly
anti-conservative.

### 3.4 Remote-zone length

SD of per-patient Δ by remote-zone length is essentially flat:

| remote length (min) | B5 | B10 | B15 | B30 |
|---|:--:|:--:|:--:|:--:|
| < 60 | 0.21 | 0.22 | 0.31 | 0.24 |
| 60–180 | 0.23 | 0.24 | 0.25 | 0.22 |
| 180–360 | 0.22 | 0.22 | 0.22 | 0.19 |
| 360–720 | 0.21 | 0.22 | 0.23 | 0.20 |
| > 720 | 0.21 | 0.22 | 0.21 | 0.19 |

The limiting quantity is the ≈ 1 effective positive per bin. Remote length
beyond about 60 min hardly matters. Short remote zones (< 60 min) inflate the
SD modestly in B15 and B30 only. This informs decision D5 (protocol §16).

### 3.5 False alarms (held-out patients, threshold set on the other 19)

| nominal FAR /h | realised mean | median | 10th–90th pct | patients with 0 alarms | alarms kept by the 3-min persistence rule |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 0.1 | 0.15 | 0.00 | 0.00–0.41 | 58% | 74% |
| 0.5 | 0.61 | 0.36 | 0.00–1.75 | 27% | 75% |
| 1.0 | 1.17 | 0.94 | 0.00–2.65 | 11% | 83% |

- The realised FAR is biased upward and scattered widely around the nominal
  target. The protocol therefore reports the **realised** FAR distribution,
  never the target.
- Because windows overlap, the persistence rule removes only 17–26% of
  single-window alarms.
- At 0.1/h, most patients have no false alarm at all, so per-patient FAR
  carries almost no information. Only the pooled FAR with a patient-bootstrap
  CI is interpretable.

---

## 4. Temporal-confounding audit (n = 20, 100 replicates per scenario)

Each artefact was scaled so that, **on its own**, it gives a raw
within-patient TD-composite separation comparable to the positive-control
precursor (raw AUROC ≈ 0.7–0.85). Every artefact loads on the TD features
only, which is the worst case for a TD claim.

Rate at which the study returns EXPLORATORY ASSOCIATION under progressively
fuller rules:

| scenario | primary test only | + pseudo-onsets | + detrending only | pseudo + detrend | + elapsed-time matching | **full rule** (+ SQI gate, conditional) |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| S0 null | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | **0.00** |
| S1 linear elapsed-time drift | 0.85 | 0.46 | 0.01 | 0.00 | 0.00 | **0.00** |
| S2 convex (accelerating) drift | 0.69 | 0.49 | 0.21 | 0.17 | 0.02 | **0.02** |
| S3 onset-locked artefact, visible in SQI (κ = 0.8) | 0.91 | 0.91 | 0.86 | 0.86 | 0.76 | **0.00** |
| S4 onset-locked artefact, barely visible in SQI (κ = 0.2) | 0.82 | 0.82 | 0.79 | 0.79 | 0.71 | **0.61** |
| S5 clock-locked wake-up surge, morning VF | 0.22 | 0.20 | 0.18 | 0.16 | 0.14 | **0.13** |
| P1 true long-lead precursor (step30, b = 2) | 0.80 | 0.79 | 0.76 | 0.76 | 0.71 | **0.70** |
| P2 P1 + linear drift | 1.00 | 0.85 | 0.83 | 0.70 | 0.54 | **0.54** |
| P3 true trigger-weighted precursor (ramp30, b = 2) | 0.28 | 0.28 | 0.25 | 0.25 | 0.17 | **0.17** |

In the mixed-duration scenario, about 83% of patients contribute a
pseudo-onset.

### 4.1 Conclusions

1. **Elapsed-time drift is controllable.** Detrending removes linear drift
   almost entirely. Elapsed-time matching is what removes accelerating drift
   (0.17 → 0.02). Pseudo-onsets alone remove only about half of either,
   because they sit earlier in the recording than the true onset. **None of
   the three is sufficient alone. All three are required** (protocol §9.2).
2. **Onset-locked non-physiological change is not identifiable from
   timing.** No temporal control can separate it from a precursor, because
   it *is* a pre-onset change. Only the SQI gate removes it, and only when
   the artefact is visible to the SQI features (0.00 at κ = 0.8, **0.61 at
   κ = 0.2**). This is a permanent blind spot of the retrospective design.
   The protocol states it in every positive report.
3. **Clock-locked confounding passes every control.** In this scenario
   (morning surge, morning-clustered VF) it starts at a lower rate (0.22),
   but the controls remove only about 40% of it. Without clock time it cannot
   be addressed (decision D6).
4. **The controls cost power.**
   - True long-lead precursor: 0.80 → 0.70.
   - The same precursor with co-existing drift: 1.00 → 0.54. Detrending and
     pseudo-onsets absorb part of a real effect when drift is present.
   - A trigger-weighted precursor ends at 0.17.

---

## 5. Guard interval, onset-marking error and trigger-proximal precursors (n = 20, 150 replicates)

Onset-marking error ε ~ U(0, 3) min: the arrhythmia starts up to 3 min
before the annotated onset.

| scenario | guard 0 | guard 1 | guard 2 |
|---|:--:|:--:|:--:|
| null + marking error: mean M1 AUROC in B5 (H-VF0) | **0.642** | 0.593 | 0.571 |
| null + marking error: mean Δ (TD increment) | −0.015 | −0.016 | −0.014 |
| precursor in last 5 min only (late5, b = 3): mean Δ / power | 0.054 / 0.08 | 0.016 / 0.02 | 0.008 / 0.03 |
| ramp30 precursor (b = 2): power in B5 | 0.76 | 0.69 | 0.63 |

- Marking error mostly contaminates the **conventional descriptive** result
  (H-VF0): with no guard, M1 "discriminates" B5 at 0.64 AUROC from captured
  arrhythmia alone. It does not create a TD increment, because both models
  see the contamination.
- The 2-min guard (with marking error < 3 min) removes this contamination
  completely. Its cost is about 13 points of B5 power for a ramp precursor.
- **A precursor confined to the final few minutes cannot be detected by
  this design at any guard.** Power is ≤ 0.08 even without a guard. The
  guard is not what hides it; the sample size is. Sensitivity analyses at
  $g$ = 1 and 5 min (protocol §5.1) bound the effect.

---

## 6. Covariance-distance bias tied to heart rate

Mean AIRM (`delta_G_structure`) between a baseline estimate (1,800 beats)
and a window estimate, under **no change**. Beats follow AR(1) with
φ = 0.8 and p = 4; 100 replicates per row.

| beats in window | 200 | 256 | 300 | 330 | 400 |
|---|:--:|:--:|:--:|:--:|:--:|
| Ledoit–Wolf | 0.559 | 0.491 | **0.474** | **0.430** | 0.386 |
| no shrinkage | 0.716 | 0.625 | 0.589 | 0.546 | 0.488 |

In a 5-min window, a 10% heart-rate rise (300 → 330 beats) lowers ΔG by
about 9% **with no structural change at all**. The protocol therefore
computes covariance features on a **fixed beat count** (protocol §6.3).

---

## 7. Limitations of this simulation

- The generative model is linear-Gaussian with assumed correlations. Real
  features are non-Gaussian, heteroscedastic and may be bimodal. Real MDEs
  can be larger or smaller.
- Artefact magnitudes were chosen to stress the controls, not estimated.
  The *rates* in §4 depend on them. The *qualitative pattern* (which
  control catches which confound) does not.
- Not simulated: M2, Analysis B, comparator contrasts, missingness, and
  sustained-VT exclusion.
- **Phase 3 of the implementation plan recalibrates this simulation** on
  outcome-blind real data: truncated loader, real feature autocorrelation,
  real between-patient spread, and the realised n and $T_{\mathrm{VF}}$.

---

© 2026 Davarn Morrison · Transition Dynamics
