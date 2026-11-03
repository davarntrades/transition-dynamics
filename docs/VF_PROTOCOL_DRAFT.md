# Draft protocol — structural dynamics before ventricular fibrillation onset (H-VF)

> ## Status: DRAFT FOR REVIEW. NOT FROZEN. NOT PREREGISTERED.
>
> - No SDDB signal or annotation file has been accessed. Header snippets seen
>   during design are disclosed in
>   [`VF_DATASET_FEASIBILITY.md`](VF_DATASET_FEASIBILITY.md) §0.
> - This is a **new transition class**: ventricular fibrillation (VF) onset in
>   ambulatory Holter ECG. It is **not** a reinterpretation of, an extension
>   of, or a rescue attempt for any intraoperative-hypotension result. Nothing
>   here changes a verdict in [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md), and
>   no VF outcome may be cited for or against a hypotension verdict.
> - Claim level is **0**. The most positive verdict this protocol can issue is
>   **EXPLORATORY SIGNAL**, capped at Claim Level 2. **No clinical predictive
>   capability is claimed or claimable.**
> - Every numerical threshold below is a proposal for review. Changes are
>   expected **before** freezing. None is permitted after.

---

## 1. Relation to the existing programme

### 1.1 What carries over unchanged

- The five-layer separation (source equation → physical interpretation →
  operationalisation → estimator → test). Every estimator in §7 is labelled as
  an **operationalisation**, not as source mathematics.
- The statements in [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) §0 that
  "must not be softened", and the distinctions there that "must not be
  collapsed", including: representation ≠ mechanism, autocorrelation ≠
  physiology, measurement-level sufficiency ≠ predictive attribution, and
  failure of one representation ≠ failure of all.
- The rules that M0 runs first, that an underpowered null is not a null
  ([`COMPETING_MODELS.md`](COMPETING_MODELS.md) §3), that bootstrapping is by
  patient, the $n_{\mathrm{eff}} \ge 10p$ rule, and the twelve harness-bug
  guards ([`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) §7).

### 1.2 Status of the objects entering this study

Re-testing an object in a new transition class is a **new test**. It is not a
reversal of a demotion, and a demoted object stays demoted unless a test of
that object itself succeeds.

| Object | Current status (unchanged) | Role here |
|---|---|---|
| $S(t)=\lVert\Sigma_0^{-1/2}\delta\rVert$ as a bare whitening statistic | NOT SUPPORTED (hypotension) | TD-1. **No stiffness, resistance or recovery reading.** Must beat diagonal, identity, permuted-off-diagonal and population metrics |
| $\Lambda=\Sigma_0^{-1}$ as stiffness / recovery | DEMOTED (physical interpretation) | **Not used.** No result here can restore it |
| Covariance deformation $\Delta G$ | not novel (DNB / covariance drift) | TD-2, explicitly as a covariance-drift statistic |
| $Q_i=\lVert\Delta G_i\rVert\tau_i$ | DEMOTED (operationalisation) | TD-3, persistence. Must beat an order-destroyed control, or it stays demoted |
| $\lVert\Lambda\Delta G\rVert>T_{\mathrm{critical}}$ | UNOPERATIONALISED | **Not attempted.** A threshold/knee test (ΔAIC > 10, cross-cohort CV) is impossible with about 20 events. TD-1 must not be described as estimating it |
| $C(t)$ / $z_{\beta_1}$ | EXPLORATORY, synthetic only | TD-4, reported descriptively. **No binding role** |
| A(t) alignment / mechanism identification | not a surviving contribution | **Not used.** Needs several transition classes, and SDDB has one |
| Reach / homology, orthogonality law, consciousness / qualia | DEMOTED / out of scope | **Excluded** |

### 1.3 The taxonomy tension, stated in advance

[`TRANSITION_TAXONOMY.md`](TRANSITION_TAXONOMY.md) places "arrhythmic arrest
from a fixed substrate" in **T6**, the negative class where no precursor is
expected and where a positive finding "would be evidence of leakage, not of
sensitivity". SDDB VF cannot be assigned to T6 or excluded from it, because
mechanism is unknown per patient. This protocol therefore:

1. records the prior expectation for TD-specific increments as **M_null**;
2. treats any EXPLORATORY SIGNAL as **suspicious first**, and makes the
   leakage audit in §13.3 mandatory before reporting;
3. leaves the taxonomy itself unchanged. Re-classifying VF is a separate
   decision that is not taken here.

---

## 2. Two estimands that must not be conflated

| | **E-onset (tested)** | **E-risk (not tested)** |
|---|---|---|
| Question | In a patient who will develop VF, does the ECG in the next H minutes before onset differ from that patient's own earlier periods, in a way a model trained on *other* patients recognises? | Does this patient carry a higher risk of VF than other patients? |
| Unit | window within patient | patient |
| Negatives | the same patient's remote pre-onset windows | patients without VF |
| SDDB support | about 12–18 eligible patients | **none**: 3 no-VF records, 2 paced |
| What a positive means | temporal precedence within patients who do develop VF | risk stratification |
| What it does not mean | that the method can identify who will develop VF, or that it alarms usefully in an unselected population | anything about timing |

Rules:

- **E-risk is not estimated.** The SDDB-vs-NSRDB design is prohibited from
  carrying any claim. It appears only as the methodological demonstration in
  §9.6.
- An E-onset result is **conditional on VF occurring**. Its false-alarm rates
  (§12) are measured in pre-VF remote zones and in no-VF recordings. They are
  **not** population alarm rates, and PPV at population prevalence is not
  estimable from this design.

---

## 3. Hypotheses

**H-VF (primary, incremental).** Adding the TD block (TD-1 $S$, TD-2
$\Delta G$, TD-3 $Q_{\mathrm{int}}$; §7.4) to the conventional baseline M1
raises the within-patient, patient-independent discrimination of pre-onset
lead-bin windows from remote pre-onset windows, at lead times beyond the
immediate trigger zone.

**H-VF0 (descriptive, not binding).** M1 alone discriminates lead-bin windows
from remote windows. This checks whether the known conventional precursors
(heart-rate rise, HRV fall, ectopy) are reproduced. It carries no TD claim.

**Not claimed under any outcome.** That VF is predictable; any clinical
alarm capability; any mechanism (stiffness, recovery, homeostasis, critical
slowing down, loss of constraint); that a TD statistic estimates a source
equation; anything about patients without VF.

**Expected outcome, declared before any data access.** NOT SUPPORTED, with
LARGE INCREMENT EXCLUDED likely and H-VF0 likely positive at short lead.

---

## 4. Data and eligibility (rules fixed before headers are read)

- **Source.** SDDB v1.0.0, with checksums verified (Phase 0). External no-VF
  set: `chfdb`, role restricted (§9.5).
- **Primary eligibility for VF records:**
  1. an annotated VF onset (`#vfon`);
  2. no continuous pacing and no atrial fibrillation as the underlying rhythm,
     because NN-based features are undefined;
  3. onset elapsed time ≥ **2 h 15 min**. This equals 15 min settling + 30 min
     baseline + ≥ 30 min remote zone + 60 min (grey zone plus the largest lead
     bin), so every patient contributes all four bins and a remote zone;
  4. ≥ 70% of beats in the baseline period detected with SQI pass (§9.3).
- **Minimum to proceed: 12 eligible VF patients.** Below that, the verdict is
  UNRESOLVED-BY-DESIGN.
- **Sensitivity population.** Records excluded by rule 2 enter an exploratory
  run that uses non-NN features only.
- The eligibility list and its SHA-256 are frozen **before any feature is
  computed**.

---

## 5. Event, time axis and zones

$t_{\mathrm{VF}}$ is the annotated VF onset. For a feature window ending at
$t$, the lead is $\ell = t_{\mathrm{VF}} - t$.

| Zone | Definition | Use |
|---|---|---|
| Settling | first 15 min of the recording | discarded |
| Baseline | the next 30 min | per-patient $\mu_0$, $\Sigma_0$, feature standardisation, SQI thresholds. **Never evaluated** |
| Remote (negative) | from baseline end to $\ell \ge 60$ min | within-patient negatives |
| Grey | $30 < \ell < 60$ min | excluded, so the 30-min bin is not contaminated by neighbouring windows |
| **Lead bins (positives)** | **B5: $2<\ell\le5$ · B10: $5<\ell\le10$ · B15: $10<\ell\le15$ · B30: $15<\ell\le30$ min** | one primary test per bin |
| Lead exclusion | $\ell \le 2$ min | excluded: immediate trigger / onset-marking error |
| Post-onset | $\ell<0$ | excluded, and never read by feature code |

**Why disjoint bins are primary.** Cumulative horizons such as "VF within 30
min" are nested: a 30-min result can be produced entirely by the last 5
minutes. Only disjoint bins show *how far ahead* any information exists.
Cumulative horizons (2, H] for H ∈ {5, 10, 15, 30} are reported as secondary
results, for comparability with the literature.

**Sustained VT.** Any window overlapping annotated or detected sustained VT
(≥ 30 s) is excluded from every analysis. Sensitivity analysis: the event is
redefined as the first sustained VT within 30 min before VF.

Grid: windows end every 60 s; window length $W$ = 5 min (§6.3). Every feature
uses samples at or before $t$ only.

---

## 6. ECG-derived measurement panel

### 6.1 Beat processing

A fixed, open QRS detector is applied to both leads. The provided `.ari`
annotations are used only for beat class (N / V / paced / noise) and for
detector–annotation disagreement, which is an artefact covariate. NN series:
normal beats whose neighbours are both normal, with RR in 0.3–2.0 s.

### 6.2 Per-beat panel ($p=4$, lead 1 primary, lead 2 replication)

| Channel | Measurement |
|---|---|
| NN | normal-to-normal interval |
| RTa | R peak to T-wave apex (more robust than QT end at 250 Hz Holter quality) |
| Tamp | T-wave apex amplitude relative to the PR baseline |
| ST | level at J + 60 ms relative to the PR baseline |

Morphology channels are measured on beats passing a template-correlation SQI.
Their fidelity on analogue Holter tape is a declared limitation
([`VF_DATASET_FEASIBILITY.md`](VF_DATASET_FEASIBILITY.md) §1.2).

### 6.3 Resolution gate (outcome-blind)

In the **baseline zones only**, compute the median $n_{\mathrm{eff}}$ of the
4-channel panel over 5-min windows. If the median is < 40 (= 10p), $W$ becomes
10 min for all features. This is decided and recorded before any label is
attached.

---

## 7. Competing models

All features are standardised against the patient's own baseline zone. Model
inputs are fixed lists, and **no feature selection is performed on SDDB**.

### 7.1 M0-acq — recording and acquisition artefact (gate)

Seven SQI features: noise or unclassifiable annotation fraction;
detector–annotation disagreement fraction; baseline-wander power (< 0.5 Hz);
high-frequency noise power (40–100 Hz); median R amplitude relative to
baseline; clipping or flat-line fraction; inter-lead QRS-detection
disagreement.

### 7.2 M1 — conventional

The 10 features in [`VF_LITERATURE_BASELINES.md`](VF_LITERATURE_BASELINES.md)
§3.1.

### 7.3 M2 — classical early warning

The 6 features in [`VF_LITERATURE_BASELINES.md`](VF_LITERATURE_BASELINES.md)
§3.2.

### 7.4 M3 — Transition Dynamics block (empirical operationalisations only)

| | Estimator | Definition | Layer label |
|---|---|---|---|
| TD-1 | $S(t)$ | $\sqrt{\delta^{\mathsf T}\Sigma_0^{-1}\delta}$, with $\delta=\mu_W(t)-\mu_0$ and $\Sigma_0$ the Ledoit–Wolf estimate from baseline | **bare whitening statistic**. No stiffness reading |
| TD-2 | $\Delta G(t)$ | $\lVert\log(\Sigma_0^{-1/2}\Sigma_W(t)\Sigma_0^{-1/2})\rVert_F$, Ledoit–Wolf (`delta_G_structure` or an affine-invariant variant, decided at freeze) | covariance-drift statistic (DNB family, not novel) |
| TD-3 | $Q_{\mathrm{int}}(t)$ | $\int_{t-30\,\mathrm{min}}^{t}\max(0,\Delta G(s)-\theta)\,ds$, with θ the patient's baseline 95th percentile of $\Delta G$ | persistence operationalisation (integral form, per [`MATHEMATICAL_OBJECTS.md`](MATHEMATICAL_OBJECTS.md) §1) |
| TD-4 | $z_{\beta_1}$ | `beta1_excess_over_pairwise`, θ = 1.5, support 0.10–0.30 | **exploratory, descriptive only** |

### 7.5 Models

- **M1**: 10 features.
- **M4 = M1 ∪ {TD-1, TD-2, TD-3}**: 13 features. **The primary contrast is
  M4 vs M1.**
- Secondary contrasts: M2 vs M1, M1 ∪ M2 vs M1, M3 alone, and each TD
  estimator alone.
- Mandatory geometry competitors for TD-1, each replacing $\Sigma_0$ with:
  the diagonal of $\Sigma_0$; the identity; $\Sigma_0$ with off-diagonals
  permuted; the pooled population covariance of the other patients. Mandatory
  competitors for TD-2: a variance-only change and a correlation-only change.
- Fitting: L2 logistic regression, λ fixed at 1 on standardised features,
  balanced class weights, and no tuning.

---

## 8. Patient-independent evaluation

- **Leave-one-patient-out (LOPO).** Train on the bin and remote windows of
  all other eligible patients, then score the held-out patient. Repeat for
  every patient and every bin.
- **Primary metric: within-patient AUROC** of the held-out patient's scores,
  bin windows vs remote windows, $\mathrm{AUROC}_i$. Probabilities are never
  pooled across folds (harness bug 11). Pooled AUPRC is secondary, computed
  with per-patient rank-normalised scores and reported with its prevalence.
- Per-patient contrast: $\Delta_i = \mathrm{AUROC}_i(M4)-\mathrm{AUROC}_i(M1)$.
- Regression guard: a single-feature "model" must reproduce that feature's
  raw within-patient AUROC.

---

## 9. Controls

All controls are run in the same execution as the primary analysis. None may
be run or re-run after the primary result has been seen.

### 9.1 Pipeline negative controls (gate; any failure → PIPELINE INVALID)

| Control | Requirement |
|---|---|
| Shuffled onsets (each patient given another patient's lead-time geometry, truncated to fit) | mean ΔAUROC 95% CI includes 0, and each model's mean within-patient AUROC is within 0.45–0.55 |
| Within-patient label permutation (bin/remote labels permuted in contiguous blocks) | chance |
| Synthetic no-precursor arm (stationary surrogate series with an abrupt event: the G3 analogue) | no detection: mean ΔAUROC CI includes 0 |
| Synthetic injected-precursor arm (known structural change inserted 15–30 min before a pseudo-event) | detected. Confirms the harness can see a real effect |

### 9.2 Within-patient temporal controls. This is the dominant leakage route

In a within-patient design the label is a function of time: lead-bin windows
are always *later* than remote windows. **Any monotone drift therefore
separates them**, whether it comes from electrode drying, tape degradation,
fatigue, activity or the time of day. An elapsed-time-only model scores
within-patient AUROC = 1 by construction, so a timestamp ratio gate is
meaningless here. It is replaced by:

1. **Pseudo-onset placebo.** For each eligible patient, pseudo-onsets are
   placed at $t_{\mathrm{VF}} - k\cdot 3$ h ($k = 1, 2, \ldots$) wherever the
   full zone geometry of §5 fits using data before the pseudo-onset only.
   No-VF records (SDDB 40, 42, 49 and `chfdb`) also get pseudo-onsets at the
   elapsed times of the real onsets. The identical pipeline is applied to each.
   The null distribution of the mean ΔAUROC comes from 2,000 draws of one
   pseudo-onset per patient. **Requirement:** the observed mean ΔAUROC
   exceeds the 95th percentile of that null in every bin that is claimed.
2. **Detrending.** Each feature is residualised on a per-patient linear trend
   fitted to the remote zone, then the analysis is recomputed. The claimed
   ΔAUROC must keep ≥ 50% of its value and its sign.
3. **Elapsed-time-matched comparison (secondary).** Lead-bin windows are
   compared with windows from other patients at the same elapsed recording
   time.

### 9.3 Recording artefact controls

1. **M0-acq ratio gate**, reusing [`COMPETING_MODELS.md`](COMPETING_MODELS.md)
   §1 thresholds:
   $R = \frac{\overline{\mathrm{AUROC}}(M0\text{-acq}) - 0.5}{\overline{\mathrm{AUROC}}(M3) - 0.5}$.
   R ≥ 0.90 is CRITICAL, ≥ 0.70 SEVERE, ≥ 0.50 MATERIAL.
2. **Conditional increment.** The contrast M4 ∪ M0-acq vs M1 ∪ M0-acq must
   keep the sign and ≥ 50% of the primary ΔAUROC.
3. **Artefact masking.** Windows whose SQI exceeds the patient's baseline
   99th percentile on any SQI feature are excluded and the analysis is rerun.
   The claimed ΔAUROC must keep its sign and ≥ 50% of its value.
4. **Lead replication.** The lead-2 panel must give the same sign in every
   claimed bin (descriptive).
5. **Annotation-algorithm probe.** Rerun with the own-detector beat classes
   only, ignoring `.ari` classes. Same requirement as item 3.

### 9.4 Structure-destroying controls for the TD block

| Control | Destroys | Requirement for any TD-specific claim |
|---|---|---|
| Row-wise channel shuffle (per beat, harness bug 12 fix) | channel identity / covariance structure | real ΔAUROC above the 95th percentile of 200 permutations |
| Within-window beat-order shuffle | temporal order (TD-3, TD-4) | same |
| Order-destroyed $\Delta G$ series (block permutation inside the trailing 30 min) | persistence ordering (TD-3) | TD-3's gain over TD-2 not reproduced. Otherwise $Q$ remains DEMOTED |
| Geometry competitors (§7.5) | patient-specific Σ₀ | TD-1 must beat all four. Otherwise "patient-specific geometry" is not supported in VF either |

### 9.5 External no-VF records

SDDB 40, 42 and 49 plus `chfdb` are used **only** for false-alarm rates
(§12) and pseudo-onset nulls (§9.2). They are never used as negatives in
model training and never used for E-risk.

### 9.6 Between-database demonstration (methodological, not evidence)

An M0-acq-only classifier for SDDB vs NSRDB segments, with patient-level
splits. It is expected to separate the databases. It is reported as a
demonstration that the standard literature design is acquisition-separable.
**It carries no claim about VF.**

---

## 10. Leakage prevention (implemented as code guards)

1. Feature code takes **no onset argument**. Only `zones.py` reads
   `#vfon`, and tests assert that feature outputs are invariant to onset.
2. Feature windows end at or before $t$. Filters are causal, or zero-phase
   within the window only. No record-level normalisation: baselines only.
3. Every evaluated window has $\ell > 2$ min. Post-onset samples are
   truncated **before** feature extraction.
4. Patient-level LOPO, and no hyperparameter or feature selection on SDDB.
   λ, $W$, θ and the bin edges are fixed at freeze, apart from the single
   outcome-blind $W$ gate in §6.3.
5. **Outcome-blind calibration loader.** Before execution, any data access
   uses a loader that truncates each VF record at $t_{\mathrm{VF}} - 60$ min,
   so no lead-bin or grey-zone sample can be read.
6. Frozen manifest: eligibility list, record checksums, code commit and
   parameter hash.
7. Development and execution outputs are never pooled.

---

## 11. Statistics and uncertainty

### 11.1 Primary inference, per bin

- Mean of $\Delta_i$ over eligible patients, with a Student-t interval at
  Bonferroni α = 0.05/4 = 0.0125 (two-sided).
- Patient-cluster bootstrap (2,000 replicates) as a sensitivity analysis.
- Exact one-sided sign test for direction consistency: the number of
  patients with $\Delta_i > 0$ must reach p < 0.025. For n = 20 that means
  ≥ 15; for n = 12, ≥ 10.

### 11.2 Large-effect exclusion

One-sided 95% upper bound of mean $\Delta_i$, per bin, compared with
$\delta_{\mathrm{large}}$ = **0.10 AUROC**.

### 11.3 Outcome-blind power gate

The SD of $\Delta_i$ under the pseudo-onset null (§9.2.1) is computed using
pre-pseudo-onset data only. It gives the realised minimum detectable effect
(MDE: 80% power, α = 0.0125). If **MDE > 0.15 in ≥ 2 bins**, H-VF is
declared UNRESOLVED-BY-DESIGN before the true-onset analysis is read. In that
case only descriptive H-VF0 output is reported.

### 11.4 Reporting

Every interval is reported, including those for failed controls. AUPRC is
always reported with its within-patient prevalence. Calibration (intercept,
slope, Brier) is reported for M1 and M4 on LOPO probabilities within each
patient.

---

## 12. Alarm evaluation and false-alarm rates

- **Alarm.** ≥ 2 consecutive windows above threshold, then a 15-min
  refractory period.
- **Thresholds.** Set in each LOPO training fold at false-alarm-rate (FAR)
  targets of **0.1, 0.5 and 1.0 per hour** in training patients' remote
  zones, then applied unchanged to the held-out patient.
- **Reported.**
  - FAR per hour in held-out remote zones and in no-VF records.
  - Per-patient sensitivity: an alarm inside the bin, or inside the
    cumulative horizon.
  - Lead time from the first alarm to onset.
  - Time-in-alarm fraction.
- **Chance reference.** $1-e^{-\mathrm{FAR}\cdot w}$ for bin width $w$. At
  0.5/h it is 0.025 for B5, 0.041 for B10 and B15, and 0.118 for B30; for the
  cumulative 28-min window it is 0.208. Sensitivities are always reported next
  to this reference and next to M1.
- **Alarm burden statement.** Even 0.1 false alarms per hour is 2.4 per
  patient-day, in a population in which VF is rare. **No FAR achievable on
  this dataset may be described as clinically usable.**

---

## 13. Binding decision rule (proposed)

### 13.1 Gates, evaluated in order. The first that fires is the verdict

1. **PIPELINE INVALID.** Any §9.1 control fails. Stop.
2. **UNRESOLVED-BY-DESIGN.** Fewer than 12 eligible patients, or the §11.3
   power gate fires.
3. **ACQUISITION-EXPLAINED.** M0-acq ratio R ≥ 0.70, or §9.3 items 2–3 fail
   in every bin that would otherwise pass. At R ≥ 0.90 (CRITICAL) no
   physiological reading of any part of the result is permitted.
4. **DRIFT-EXPLAINED.** The pseudo-onset requirement or the detrending
   requirement (§9.2) fails in every bin that would otherwise pass.

### 13.2 Primary verdicts, after the gates

- **EXPLORATORY SIGNAL.** All of the following, in ≥ 2 bins, **at least one
  of which is B15 or B30**:
  1. mean ΔAUROC > 0 with its Bonferroni interval excluding 0;
  2. the sign test is met;
  3. the pseudo-onset and detrending requirements are met;
  4. M0-acq R < 0.50, and the conditional-increment and masking requirements
     are met;
  5. at FAR 0.5/h, M4 sensitivity is ≥ M1 sensitivity and above the chance
     reference.
- **SHORT-LEAD ONLY.** The conditions above are met only in B5 and/or B10.
  Recorded as "**not advance warning**": consistent with trigger-proximal
  change.
- **NOT SUPPORTED.** The harness is valid, the power gate passes, and neither
  of the above holds.
- **HARM** (recorded alongside any verdict). The interval lies entirely below
  0 in ≥ 2 bins.

### 13.3 Binding falsification flag, reported with every verdict past gate 2

- **LARGE INCREMENT EXCLUDED.** The one-sided 95% upper bound is < 0.10 in
  all four bins. This **falsifies the proposition that the TD block provides a
  large (≥ 0.10 AUROC) incremental advance warning of VF in SDDB**. Smaller
  increments remain unresolved, and that must be stated in the same sentence.

**Mandatory before reporting an EXPLORATORY SIGNAL** (the T6 rule, §1.3):

- rerun with an independent second QRS detector;
- a visual audit of 50 random lead-bin windows and 50 remote windows, blinded
  to zone;
- per-patient breakdown, to show whether ≤ 2 patients drive the mean.

### 13.4 TD-specific attribution, secondary and non-binding for the verdict

An EXPLORATORY SIGNAL is attributed to multichannel structure only if the
§9.4 controls pass. Otherwise it is reported as "an increment from features
that do not require multichannel structure", with no TD reading.

### 13.5 What each outcome permits

| Verdict | Maximum language |
|---|---|
| EXPLORATORY SIGNAL | "In this retrospective dataset of ≈ N patients, TD statistics were associated with pre-VF periods at lead times of X min beyond conventional features. This is exploratory and requires an independent cohort." Claim Level ≤ 2. **Never** "predicts VF", "early warning", or any mechanism |
| SHORT-LEAD ONLY | "Changes within X min of onset", and not advance warning |
| NOT SUPPORTED + LARGE EXCLUDED | "No large incremental value. Smaller effects are not excluded" |
| NOT SUPPORTED alone | "Not supported. The data cannot resolve small effects" |
| any verdict | Hypotension verdicts are unaffected. M2 and M_null remain live |

---

## 14. Sample-size assessment (summary)

The full arithmetic is in
[`VF_DATASET_FEASIBILITY.md`](VF_DATASET_FEASIBILITY.md) §3. With about 20
patients and Bonferroni over 4 bins, the detectable mean ΔAUROC is about 0.12
if the between-patient SD is 0.15. About 100 events are needed for 0.05 and
about 280 for 0.03. **This study is exploratory with a binding large-effect
falsification. It is not confirmatory.** A confirmatory test of H-VF requires
an independent cohort, frozen from this protocol's output, with at least
about 100 adjudicated VF onsets and ≥ 60 min of pre-onset multichannel-capable
ECG.

---

## 15. Questions for the reviewer before freezing

1. **Disjoint lead bins as primary** (vs cumulative horizons as primary).
2. **Remote zone at $\ell \ge 60$ min with a 30-min grey zone**, and the
   2 h 15 min eligibility rule. Records 48 and 52 lie just above it; see the
   disclosure.
3. **δ_large = 0.10** and the **12-patient** minimum.
4. **Excluding AF from the primary analysis**, at the cost of up to 4
   patients.
5. **VF onset vs first sustained VT** as the primary event.
6. Whether TD-2 uses `delta_G_structure` as implemented or the
   affine-invariant distance. Only one is permitted.
7. Whether `chfdb` is acceptable as the external no-VF set given its disease
   and era differences.

## 16. Freezing conditions

The protocol is frozen only after: the Phase 0 verification is recorded; §15
is resolved; this file is amended and committed with an explicit FROZEN
banner and a parameter hash; and the user authorises a single execution.
**Until then no analysis code is run on SDDB beyond header/metadata
verification.**

---

© 2026 Davarn Morrison · Transition Dynamics
