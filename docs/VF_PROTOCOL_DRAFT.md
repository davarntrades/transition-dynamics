# Draft protocol v2 — structural dynamics before ventricular fibrillation onset (H-VF)

> ## Status: DRAFT v2 FOR INDEPENDENT REVIEW. NOT FROZEN. NOT PREREGISTERED.
>
> - **No SDDB, chfdb or NSRDB signal or annotation file has been accessed.**
>   Header snippets seen during design are disclosed in
>   [`VF_DATASET_FEASIBILITY.md`](VF_DATASET_FEASIBILITY.md) §0.
> - **v2 revises v1** in response to the methodological review in
>   [`VF_METHODOLOGICAL_REVIEW.md`](VF_METHODOLOGICAL_REVIEW.md). Every change
>   is listed, with its reason, in Appendix A. Design numbers come from the
>   synthetic simulation in
>   [`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md), not from approximate
>   formulas.
> - This is a **new transition class**: VF onset in ambulatory Holter ECG. It
>   is **not** a reinterpretation of, extension of, or rescue attempt for any of
>   the seven intraoperative-hypotension results. Their verdicts in
>   [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) are unchanged, and no VF
>   outcome may be cited for or against them.
> - Claim level is **0**. The most positive verdict this protocol can issue is
>   **EXPLORATORY ASSOCIATION**, which is retrospective and capped at Claim
>   Level 2. **Retrospective discrimination is not advance prediction and not
>   clinical early warning** (§15). No such capability is claimed or claimable
>   from this study.
> - **Not to be executed until this revision has been independently reviewed**,
>   the open decisions in §16 are resolved, and a separate FROZEN document
>   exists.

---

## 1. Relation to the existing programme

### 1.1 What carries over unchanged

- The five-layer separation (source equation → physical interpretation →
  operationalisation → estimator → test). Every estimator in §7 is labelled as
  an **operationalisation**, never as source mathematics.
- The statements in [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) §0 that must
  not be softened, and its distinctions that must not be collapsed.
- Running M0 first, "an underpowered null is not a null", patient-level
  uncertainty, $n_{\mathrm{eff}} \ge 10p$, and the twelve harness-bug guards
  ([`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) §7).

### 1.2 Status of the objects entering this study

Re-testing an object in a new transition class is a **new test**. It is not a
reversal of a demotion.

| Object | Current status (unchanged) | Role here |
|---|---|---|
| $S(t)$ as a bare whitening statistic | NOT SUPPORTED (hypotension) | TD-1. No stiffness, resistance or recovery reading. Mandatory geometry competitors |
| $\Lambda=\Sigma_0^{-1}$ as stiffness / recovery | DEMOTED (physical interpretation) | **Not used.** No result here can restore it |
| Covariance deformation $\Delta G$ | not novel (DNB / covariance drift) | TD-2, exact estimator in §7.4. Must beat the simpler covariance statistics for any structure-specific claim |
| $Q_i=\lVert\Delta G_i\rVert\tau_i$ | DEMOTED (operationalisation) | TD-3. Stays demoted unless it beats the order-destroyed control |
| $\lVert\Lambda\Delta G\rVert>T_{\mathrm{critical}}$ | UNOPERATIONALISED | **Not attempted** (threshold identification is impossible with ≈ 20 events) |
| $C(t)$ / $z_{\beta_1}$ | EXPLORATORY, synthetic only | TD-4, descriptive only |
| A(t) alignment, reach / homology, orthogonality, consciousness / qualia | not surviving / DEMOTED / out of scope | **Excluded** |

### 1.3 Prior evidence, recorded without a declared expected outcome

v1 declared NOT SUPPORTED as the expected result. **That declaration is
withdrawn.** It prejudged the outcome and served no inferential purpose. The
prior evidence is recorded instead, in both directions, and none of it enters
the decision rule:

- **Against a TD-specific increment:**
  - every incremental TD test in this programme so far has been NOT SUPPORTED
    (hypotension; [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) §10–§14);
  - [`TRANSITION_TAXONOMY.md`](TRANSITION_TAXONOMY.md) classes arrhythmic
    arrest from a fixed substrate as T6, a no-precursor class;
  - early-warning signals are bifurcation-specific, and none were found
    before human seizures ([`LITERATURE.md`](LITERATURE.md) §0).
- **For some pre-onset change (conventional features):** Holter and ICD
  studies report heart-rate rise, HRV decline and T-wave alternans upsurge
  before spontaneous ventricular tachyarrhythmia
  ([`VF_LITERATURE_BASELINES.md`](VF_LITERATURE_BASELINES.md) §1).
- **The T6 classification is kept, not overridden.** SDDB VF cannot be
  assigned to T6 or excluded from it, because mechanism is unknown per
  patient. v1 applied extra scrutiny to positive results only. v2 replaces
  this with a **symmetric** audit (§13.4) that runs whatever the verdict, so
  that scrutiny is not itself a function of the outcome.

---

## 2. Estimands that must not be conflated

| | **E-onset (tested)** | **E-risk (not tested)** | **E-advance (not estimable here)** |
|---|---|---|---|
| Question | In patients who **do** develop VF, do pre-onset periods differ from the same patients' remote periods, as recognised by a model trained on other patients? | Is this patient at higher VF risk than others? | Given continuous monitoring of an unselected population, does an alarm precede VF with useful lead time and an acceptable false-alarm burden? |
| Conditioning | on VF occurring | none | none: event-unconditional |
| SDDB support | about 13–19 patients (Analyses A and B, §4) | none (3 no-VF records) | none |
| A positive result means | a retrospective, within-patient association | — | — |

E-risk is not estimated. The SDDB-vs-NSRDB design appears only as the
methodological demonstration in §9.7. E-advance is discussed in §15.

---

## 3. Hypotheses

- **H0-VF (null; binding falsification target).** In every lead bin, adding
  the TD block (TD-1, TD-2, TD-3) to M1 does not change mean within-patient
  AUROC: $\mathbb{E}[\Delta_i]=0$.
- **H1-VF (alternative).** $\mathbb{E}[\Delta_i]>0$ in at least two lead bins,
  at least one of which is B15 or B30.
- **H-VF0 (descriptive, not binding).** M1 alone discriminates lead-bin
  windows from remote windows.
- **Not claimed under any outcome.**
  - That VF is predictable.
  - Any alarm or clinical capability.
  - Any mechanism (stiffness, recovery, homeostasis, critical slowing down,
    loss of constraint).
  - That a TD statistic estimates a source equation.
  - Anything about patients without VF.

**No expected outcome is declared** (§1.3).

---

## 4. Data and eligibility

### 4.1 Two separately reported analyses (no pooling)

| | **Analysis A (primary)** | **Analysis B (rhythm-inclusive, separate)** |
|---|---|---|
| Records | VF records in sinus rhythm, including intermittent pacing (paced beats removed) | **All** VF records except continuous pacing, **including AF** |
| Panel | NN, RTa, Tamp, ST | RTa, Tamp, ST, R amplitude: **no NN-derived channel** |
| M1 | 10 features ([`VF_LITERATURE_BASELINES.md`](VF_LITERATURE_BASELINES.md) §3.1) | M1-B: mean ventricular rate, Δ mean rate vs baseline, PVC₅, PVC₃₀, couplets₃₀, NSVT₃₀ |
| M2 | 6 features | M2-B: AC1(RT), var(RT), TWA |
| Decision rule | §13, at α = 0.05/4 | §13, at its own α = 0.05/4. Reported in a separate table, never combined with A |

Analysis B exists because excluding AF is a **selection on rhythm**. AF
patients are older, more often in heart failure, and may differ in
arrhythmic mechanism. B tells the reader whether any A result depends on
that selection. The rhythm composition of each analysis is reported, along
with any available header demographics for included vs excluded patients.
Known limitation of B: PVC detection in AF is less reliable (aberrancy), so
M1-B's ectopy features are noisier.

Whether B is co-primary with an α split, or secondary, is an open decision
(§16, D1). The current proposal makes it secondary but binding-reported: its
verdict is stated, but it cannot alone yield an EXPLORATORY ASSOCIATION for
the programme.

### 4.2 Eligibility: derived geometry, not an arbitrary sum

A VF record is eligible if, first, its onset elapsed time satisfies
$T_{\mathrm{VF}} \ge T_{\min} = $ settling 15 + baseline 30 + window 5 +
$R_{\min}$ + 60 min, with $R_{\min}$ = 30 min. **This gives $T_{\min}$ =
140 min (2 h 20 min).** It must also satisfy two signal conditions:

- ≥ 600 complete panel beats in the baseline (for $\Sigma_0$, §7.4);
- baseline beat-level $n_{\mathrm{eff}} \ge 10p$.

**Justification of each term.**

| Term | Value | Why |
|---|---|---|
| Settling | 15 min | electrode settling. **Choice**, sensitivity analysis at 0 and 30 min |
| Baseline | 30 min | the minimum that gives ≥ 600 beats for a 4×4 shrunk covariance at any heart rate ≥ 20 bpm. **Choice** |
| Window | 5 min | first window entirely after the baseline |
| $R_{\min}$ | 30 min | in simulation, per-patient Δ precision is limited by the ≈ 1 effective positive per bin (§8.2). The SD of $\Delta_i$ is flat for remote zones ≥ 60 min (0.19–0.25) and modestly inflated below 60 min, in B15/B30 only (0.31/0.24) ([`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) §3.4). 30 min keeps short recordings at a small precision cost. **Choice informed by simulation; open decision D5** (60 min would give $T_{\min}$ = 2 h 50 and exclude records 48 and 52) |
| 60 min | grey zone 30 + largest bin 30 | fixed by the horizons |

**The v1 rule (2 h 15 min) was an unjustified sum, and it sat just below two
disclosed onsets** (records 48 at 02:29:40 and 52 at 02:32:40). v2 handles
this as follows:

1. Two things are true at once. Onset times reveal nothing about whether a
   record's ECG shows a precursor, so selection bias from knowing them is
   limited. A threshold placed near known values still invites the suspicion
   of being tuned.
2. **Pre-specified eligibility sensitivity analysis:** $T_{\min}$ ∈
   {2 h 20 (primary), 3 h, 4 h}. The verdict is reported at each. Records 48
   and 52 are included at 2 h 20 and excluded at 3 h. If the verdict differs
   between 2 h 20 and 3 h, that is reported as **eligibility-sensitive**, and
   the more conservative verdict (the one further from EXPLORATORY
   ASSOCIATION) governs.
3. The eligibility list is frozen, with its hash, before any feature is
   computed.

### 4.3 The 12-patient minimum is withdrawn

The 12-patient minimum was not derived from anything. It is replaced by:

- **A capability floor.** n ≥ 6 patients contributing to a bin. This is the
  smallest n at which the one-sided sign test can reach p < 0.025 (6/6 gives
  p = 0.016).
- **An outcome-blind informativeness gate** (§11.3). The design simulation is
  rerun with parameters estimated from outcome-blind data (truncated loader)
  and the realised n and $T_{\mathrm{VF}}$ distribution. If the MDE (80%
  power) exceeds **$\mathrm{MDE}_{\max}$** in B15 and in B30, H-VF is
  UNRESOLVED-BY-DESIGN, and
  the true-onset analysis is not read.
- **$\mathrm{MDE}_{\max}$ is open decision D2.** Under the simulated
  assumptions the MDE at n = 20 is about **0.23** ΔAUROC per bin for a
  sustained long-lead precursor, and above 0.30 at n = 12
  ([`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) §2). The v1 value
  of 0.20 would therefore probably declare the study uninformative before it
  is run. The proposal is **0.25**: the study is then explicitly a
  *large-effect screen*. This value was chosen after seeing the
  **design** simulation (no outcome data exist), and the reviewer should
  treat it as a substantive choice, not a technicality.

---

## 5. Event, time axis and zones

$T_{\mathrm{VF}}$ is the annotated VF onset. For a window ending at $t$, the
lead is $\ell = T_{\mathrm{VF}} - t$.

| Zone | Definition |
|---|---|
| Settling | first 15 min, discarded |
| Baseline | the next 30 min: $\mu_0$, $\Sigma_0$, standardisation, SQI thresholds. Never evaluated |
| Remote (negative) | windows ending after baseline end + 5 min, with $\ell \ge 60$ min |
| Grey | $30 < \ell < 60$, excluded |
| **Lead bins** | **B5: $g<\ell\le5$ · B10: $5<\ell\le10$ · B15: $10<\ell\le15$ · B30: $15<\ell\le30$**, with guard $g$ = 2 min (primary) |
| Post-onset | never read by feature code |

Bins are disjoint in **alarm time** $t$. Their data overlap, because a B10
window spans 5–15 min before onset and so shares data with B5 and B15.
Information "at lead 10 min" therefore means *an alarm raised 5–10 min before
onset using only data up to that time*, which is the correct definition for
prediction. Bins are not statistically independent, so Bonferroni over four
bins is conservative.

### 5.1 VT, the guard interval, and the risk of removing the precursor

A window that overlaps a **sustained** VT episode (≥ 30 s) is excluded:
during such a window the patient is already in a ventricular
tachyarrhythmia. **Non-sustained VT, couplets and PVCs are retained**, and
enter M1 as features. A precursor made of ectopy is therefore attributed to
M1 rather than removed, and the TD increment is tested beyond it.

The guard $g$ protects against onset-marking error. If the true arrhythmia
starts before the annotated onset, windows within the error contain the
arrhythmia itself. Design simulation, with marking error up to 3 min
([`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) §5):

- Contamination inflates the **conventional** B5 AUROC from 0.57 to 0.64
  with no guard. It does not inflate the TD increment.
- $g$ = 2 removes the contamination, at a cost of about 13 points of B5 power
  for a trigger-weighted precursor.
- A precursor confined to the last ≈ 5 min is undetectable at **any** guard
  (power ≤ 0.08). The limit is sample size, not the guard, so a null result
  says nothing about trigger-proximal change.

**Pre-specified sensitivity analyses** (reported; non-binding unless stated):

| # | Variant | Purpose |
|---|---|---|
| S-g1 | $g$ = 1 min | recovers trigger-proximal signal; reports contamination risk |
| S-g5 | $g$ = 5 min (B5 becomes empty, B10 starts at 5) | removes any residual onset-marking contamination |
| S-VT1 | event = first sustained VT within 60 min before VF (where present) | the event is the start of the tachyarrhythmia, not VF |
| S-VT2 | windows overlapping sustained VT **kept** | labelled "detection-contaminated"; bounds what was removed |
| S-VT3 | windows containing NSVT **also** excluded | tests whether a TD increment is carried by ectopy |
| S-ect | windows with > 10% ventricular beats excluded | same purpose, at the beat level |

**Precursor-removal audit, reported for every analysis.** For each patient
and bin it reports:

- windows available;
- windows excluded by each rule, and the share of all windows each removed;
- the time from the last sustained VT to $T_{\mathrm{VF}}$.

If **> 25% of patients lose a bin** to the VT rule, that bin is reported as
non-evaluable rather than tested.

---

## 6. ECG-derived measurement panel

### 6.1 Beat processing

A fixed, open QRS detector runs on both leads. `.ari` annotations supply beat
class only, and detector–annotation disagreement is an SQI covariate. NN beats
are normal beats whose neighbours are both normal, with RR in 0.3–2.0 s
(Analysis A).

### 6.2 Per-beat panel ($p$ = 4, lead 1 primary, lead 2 replication)

Analysis A: NN, RTa (R to T apex), Tamp (T apex vs PR baseline), ST (J + 60 ms
vs PR baseline).

Analysis B: RTa, Tamp, ST and R amplitude.

Morphology is measured on beats that pass a template-correlation SQI.

### 6.3 Window definitions

- **First-order features** (M1, M2, SQI): 5-min windows ending at $t$, on a
  60-s grid.
- **Covariance-based features** (TD-1, TD-2, TD-4): the **most recent
  $N_b$ = 256 complete panel beats** ending at or before $t$. The window is
  missing if those beats span more than 10 min.

**Why fixed beat count.** In fixed-duration windows the number of beats rises
with heart rate. The small-sample bias of the covariance distance falls as
the beat count rises, so ΔG would drop *mechanically* whenever heart rate
rose. Heart-rate rise is the main conventional precursor. Simulation: under
no structural change, mean AIRM falls from 0.474 at 300 beats to 0.430 at 330
beats, which corresponds to a 10% HR rise (§7.4).

**$n_{\mathrm{eff}}$ gate (outcome-blind).** If the median baseline
$n_{\mathrm{eff}}$ of 256-beat windows is < 40 (= 10p), $N_b$ becomes 512.

---

## 7. Competing models

All inputs are standardised against the patient's own baseline. Lists are
fixed, and **no feature selection is performed on SDDB**.

### 7.1 M0-acq — acquisition and artefact (gate)

Seven SQI features:

- noise or unclassifiable annotation fraction;
- detector–annotation disagreement;
- baseline-wander power (< 0.5 Hz);
- high-frequency power (40–100 Hz);
- median R amplitude vs baseline;
- clipping or flat-line fraction;
- inter-lead QRS disagreement.

Beat-exclusion (missingness) rate per window is added as an eighth.

### 7.2 M1 and 7.3 M2

As listed in [`VF_LITERATURE_BASELINES.md`](VF_LITERATURE_BASELINES.md) §3,
with the Analysis B variants in §4.1.

### 7.4 M3 — TD block: exact estimators (to be frozen as written)

**Pre-processing (shared).** Each beat $k$ gives $x_k\in\mathbb{R}^4$. A
channel value outside the baseline median ± 6·MAD·1.4826 marks the beat
incomplete. Channels are standardised by the baseline median and
MAD·1.4826, so every channel enters on a unitless, outlier-robust scale
before shrinkage.

**Covariance estimator, identical for $\Sigma_0$ and $\Sigma_W$.**
Ledoit–Wolf shrinkage toward $\bar\sigma^2 I$, with analytic intensity, as in
`analysis/estimators.py::shrunk_covariance`. This is followed by the SPD
guard (relative eigenvalue floor $10^{-6}$, `_spd_guard`).

- $\Sigma_0$ uses all complete baseline beats (≥ 600).
- $\Sigma_W(t)$ uses the last $N_b$ complete beats.
- The condition number of $\Sigma_0$ is recorded; above $10^4$ the patient's
  TD features are flagged and a sensitivity analysis excludes them.

Ledoit–Wolf intensity formulas assume independent samples. Beats are
autocorrelated, so the analytic intensity is biased low. **Sensitivity:**
fixed intensities α ∈ {0.1, 0.3}.

**TD-2, covariance deformation (AIRM).**
Let $L$ be the Cholesky factor of $\Sigma_0$ and $\lambda_1..\lambda_4$ the
eigenvalues of $L^{-1}\Sigma_W L^{-\mathsf T}$, floored at $10^{-12}$. Then

$$\Delta G(t)=\Big(\sum_{k}\log^2\lambda_k\Big)^{1/2}
=\Big(\underbrace{p\,\overline{\log\lambda}^{\,2}}_{\text{scale}}+\underbrace{\textstyle\sum_k(\log\lambda_k-\overline{\log\lambda})^2}_{\text{shape}}\Big)^{1/2}.$$

This is mathematically identical to `delta_G_structure`; Cholesky is used
for numerical stability. The scale and shape components are reported
separately.

**Mandatory simpler covariance comparators**, on the same beats, the same
standardisation and the same estimator:

| | Statistic | Captures |
|---|---|---|
| C-a | $\big(\sum_i \log^2(s^2_{W,i}/s^2_{0,i})\big)^{1/2}$ | variance change only (diagonal AIRM) |
| C-b | AIRM between correlation matrices $R_0$, $R_W$ | correlation change only |
| C-c | $\lVert R_W-R_0\rVert_F$ | DNB-style correlation drift |
| C-d | $\lvert\log\det\Sigma_W-\log\det\Sigma_0\rvert$ | generalised variance |
| C-e | mean $\lvert r_{ij}\rvert$ in the window × mean SD | DNB composite |

**Known mechanical couplings, declared.**

1. ΔG's sampling dispersion grows when beat autocorrelation grows, because
   $n_{\mathrm{eff}}$ falls. So ΔG partly re-expresses AC1, an M2 quantity.
2. ΔG's scale component overlaps SDNN and var(RT).

TD-specific attribution therefore requires the M1 ∪ M2 contrast and the
comparator contrasts (§13.5).

**TD-1, displacement.** $\delta(t)$ is the mean of the last $N_b$
standardised beats minus the baseline mean, and
$S(t)=\sqrt{\delta^{\mathsf T}\Sigma_0^{-1}\delta}$. Its competitors replace
$\Sigma_0$ with: its diagonal; the identity; $\Sigma_0$ with off-diagonals
permuted; the pooled covariance of the other patients.

**TD-3, persistence.**
$Q_{\mathrm{int}}(t)=\sum_{s=t-29}^{t}\max(0,\Delta G(s)-\theta)$ over the
1-min grid. θ is the 95th percentile of ΔG computed over baseline sub-windows,
and it is noisy: about 3 independent baseline sub-windows exist.
**Sensitivity:** θ from the first 30 min of the remote zone. The
order-destroyed control is a block permutation of ΔG within the trailing
30 min.

**TD-4.** `beta1_excess_over_pairwise`, descriptive only.

### 7.5 Models

- M1 (Analysis A: 10 features).
- **M4 = M1 ∪ {TD-1, TD-2, TD-3}. The primary contrast is M4 vs M1.**
- **Mandatory for TD attribution** (§13.5): M1 ∪ M2 ∪ M3 vs M1 ∪ M2;
  M1 ∪ {ΔG} vs M1 ∪ {C-x} for each comparator; and the geometry competitors.
- Fitting: L2 logistic regression, λ = 1 on standardised features, balanced
  class weights, no tuning.

---

## 8. Patient-independent evaluation and what the overlapping grid does

### 8.1 Leave-one-patient-out (LOPO)

Train on all other patients' bin and remote windows, then score the held-out
patient. The primary metric is the within-patient AUROC (bin vs remote) of
the held-out patient, $\Delta_i=\mathrm{AUROC}_i(M4)-\mathrm{AUROC}_i(M1)$.
No probabilities are pooled across folds (bug 11). A single-feature model
must reproduce its raw AUROC (regression guard).

### 8.2 Overlap: effective sample size, uncertainty and false alarms

Results are from the design simulation; see
[`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) §3.

- **Window correlation.** Consecutive 5-min windows on a 60-s grid share 80%
  of their data. Simulated lag-1 correlation of window features is 0.985.
  Correlation is 0.55 at 10 min, 0.41 at 15 min and ≈ 0 at 30 min, so the
  correlation length is about 15–20 min.
- **Effective positives per bin.** B5 has 3 windows, B10 and B15 have 5, and
  B30 has 15. These amount to about **1, 1, 1 and 1–2 effective independent
  observations**. Each patient's $\mathrm{AUROC}_i$ is therefore close to the
  percentile of one or two independent observations within that patient's
  remote distribution. That is why $\Delta_i$ is so dispersed across patients.
- **Stride does not create information.** At a 5-min stride
  (non-overlapping), the null SD of $\Delta_i$ is of the same order. The 60-s
  grid gives alarm-time resolution, not extra information. It does not bias
  the patient-level inference, because inference treats the patient as the
  unit.
- **Window-level uncertainty is invalid.** A Hanley–McNeil SE that treats
  windows as independent underestimates the true within-patient AUROC
  variability by a factor of about 3. **Every CI in this protocol is
  patient-level**, and no window-level SE or p-value may be reported.
- **False alarms.** Overlap makes "≥ 2 consecutive windows above threshold"
  almost no filter. Even a 3-minute persistence rule removes only 17–26% of
  single-window alarms in simulation. The
  alarm rule is therefore defined as a **persistence-in-time requirement**
  (§12). FAR is reported per monitored hour and does not depend on the
  stride.

### 8.3 Power and MDE

Summarised in §14 from the simulation. Approximate analytic AUROC power
formulas are not used anywhere for design decisions.

### 8.4 Guard-interval trade-off

See §5.1 and the simulation document §5.

---

## 9. Controls

### 9.1 Pipeline negative and positive controls (gate)

| Control | Requirement |
|---|---|
| Shuffled onsets | mean Δ CI includes 0; mean AUROC of each model within 0.45–0.55 |
| Within-patient block label permutation | chance |
| Synthetic no-precursor arm | no detection |
| Synthetic injected precursor (known change 15–30 min before a pseudo-event, inserted into real outcome-blind remote data) | detected. Shows the harness can see a real effect, so a null is not a pipeline failure |

### 9.2 Temporal controls, and exactly what each can and cannot catch

Lead-bin windows are always later than remote windows. The design
simulation (§4 of that document) audited each control against artefacts
calibrated so that, alone, each gives the same raw within-patient separation
as a strong precursor.

| Confound | Pseudo-onsets | Detrending | Elapsed-time matching | SQI gate | Blinded audit |
|---|:--:|:--:|:--:|:--:|:--:|
| Linear drift in elapsed time | partly (0.85 → 0.46) | **catches** (→ 0.01) | **catches** | only if visible in SQI | partly |
| Accelerating (convex) drift in elapsed time | partly (0.69 → 0.49; offsets are earlier, where drift is slower) | partly (→ 0.21) | **catches** if shared across patients (all three → 0.02) | only if visible | partly |
| Onset-locked non-physiological change (symptom-related motion, electrode, end of tape) | **cannot** (0.82–0.91 unchanged) | **cannot** | **cannot** (→ 0.71–0.76) | **catches only if visible** (κ 0.8 → 0.00; κ 0.2 → **0.61**) | partly |
| Clock-locked change (wake-up surge) with VF clustering in the morning | **cannot** (0.22 → 0.20) | **cannot** | **cannot** (clock ≠ elapsed time) | **cannot** (full rule 0.13) | **cannot** |

Figures in brackets are the simulated false-EXPLORATORY-ASSOCIATION rates,
before → after the control, at n = 20. Under a true long-lead precursor the
controls cost power: 0.80 → 0.70, and 1.00 → 0.54 when drift co-exists.

The simulated rates behind this table are in
[`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) §4.

**Consequence, binding on reporting.** Any positive result must state, in
the same sentence, that **onset-locked non-physiological change is excluded
only to the extent that the SQI features see it**, and that **circadian
confounding is not excluded** unless clock time is available (Phase 0 checks
the headers for start times).

**Specification.**

1. **Pseudo-onsets.**
   - Offsets $k\cdot$3 h before $T_{\mathrm{VF}}$, wherever the §5 geometry
     fits. No-VF records (SDDB 40, 42, 49) are added at elapsed times drawn
     from the real onsets.
   - One LOPO per offset. The null of the cohort mean comes from 9,999 draws
     of one available offset per subject.
   - Pass: $p=(1+\#\{\text{null}\ge\text{obs}\})/(1+9999)\le0.05$.
   - If fewer than 8 subjects contribute, the pseudo-onset control is
     **non-evaluable**, and the bin cannot pass. This is conservative by
     design. About 83% of patients have a pseudo-onset in the simulated
     "mixed" duration scenario, and fewer if recordings are short.
2. **Detrending.** Per patient and per feature, a linear trend is fitted on
   the remote zone and removed everywhere. Pass: retained Δ ≥ 50% of the
   observed value, same sign.
3. **Elapsed-time matching** (promoted from secondary to required).
   - Statistic: the fixed, unfitted TD composite (mean of the
     baseline-standardised TD-1, TD-2 and TD-3).
   - For each patient, compare its bin windows with other patients'
     remote-zone windows within ±15 min of the same elapsed time.
   - Pass: mean matched AUROC > 0.5, with its Bonferroni interval excluding
     0.5.
   - LOPO model scores are **not** used here. Other patients' windows are
     training data for those models, so their scores would be in-sample.
4. **Clock-time matching**, only if start times exist: the same, with clock
   time instead of elapsed time. Otherwise the circadian limitation is
   declared.

### 9.3 Recording-artefact controls

1. **M0-acq ratio gate:**
   $R=\frac{\overline{\mathrm{AUROC}}(M0)-0.5}{\overline{\mathrm{AUROC}}(M3)-0.5}$.
   R ≥ 0.90 is CRITICAL, ≥ 0.70 SEVERE, ≥ 0.50 MATERIAL.
2. **Conditional increment:** M4 ∪ M0 vs M1 ∪ M0 keeps ≥ 50% of Δ, with the
   same sign.
3. **Artefact masking:** exclude windows above the patient's baseline 99th
   percentile on any SQI feature, then require ≥ 50% retained, same sign.
4. **Lead replication:** same sign on lead 2.
5. **Annotation-algorithm probe:** own-detector beat classes only.

### 9.4 Structure-destroying controls (TD attribution)

Row-wise channel shuffle (bug 12), within-window beat-order shuffle, and the
order-destroyed ΔG series. Each uses 200 permutations, and the real value
must exceed the 95th percentile.

### 9.5 No-VF records

See §12.3 for their restricted role.

### 9.6 Symmetric integrity audit

Runs for every verdict past gate 2:

- an independent second QRS detector;
- a visual audit, blinded to zone, of 50 random bin windows and 50 remote
  windows;
- a per-patient breakdown, including whether ≤ 2 patients drive the mean.

### 9.7 Between-database demonstration (methodological only)

M0-acq-only classification of SDDB vs NSRDB segments, with patient-level
splits. Its result is reported **whatever it is**, and carries no claim about
VF.

---

## 10. Leakage prevention (code guards)

1. Feature code takes **no onset argument**. Only `zones.py` reads `#vfon`.
   Tests assert that feature outputs are invariant to the onset.
2. Every feature uses samples at or before $t$ only. Filters are causal or
   window-local. Standardisation uses the baseline only.
3. Evaluated windows have $\ell>g$, and post-onset samples are truncated
   before feature extraction.
4. LOPO with no SDDB-based selection. Parameters are fixed at freeze, apart
   from the two outcome-blind gates ($N_b$, informativeness).
5. Outcome-blind loader: truncation at $T_{\mathrm{VF}}-60$ min for all
   calibration.
6. A frozen manifest: eligibility list, checksums, code commit and parameter
   hash.
7. Outputs from development and execution are never pooled.

---

## 11. Statistics and uncertainty

1. **Primary, per bin.** Mean $\Delta_i$; Student-t interval at α = 0.0125;
   patient-cluster bootstrap (2,000 replicates) as sensitivity; exact
   one-sided sign test at p < 0.025.
2. **Large-effect exclusion.** The one-sided 95% upper bound of mean
   $\Delta_i$ is below $\delta_{\mathrm{large}}$ = **0.15** (proposal;
   decision D9). In simulation at n = 20, δ = 0.10 fires in only 38–53% of
   null studies, so the binding falsification would usually be
   uninformative. δ = 0.15 fires in 66–81% of null studies and in ≤ 0.5% of
   studies whose true effect is ≥ 0.18
   ([`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) §2.4).
3. **Outcome-blind informativeness gate.** As in §4.3, using the simulation
   recalibrated on truncated-loader data.
4. **Reporting.**
   - Per-patient $\Delta_i$ for every bin, shown as a dot plot.
   - Within-patient prevalence beside every AUPRC.
   - Calibration (intercept, slope, Brier) within patient.
   - **No window-level inference.**

---

## 12. Alarm evaluation and false-alarm rates

### 12.1 Alarm rule (exact)

An alarm is raised at $t$ if the score has been above threshold in every
window ending in $[t-2, t]$ (3 consecutive minutes), and no alarm has been
raised in the preceding 15 min. Thresholds are set in the LOPO training fold
for nominal FAR targets of 0.1, 0.5 and 1.0 per hour.

### 12.2 What is reported

- **Realised held-out FAR**, which is the quantity reported. The nominal
  target is not. In simulation, a nominal 0.5/h gave a realised mean of
  0.61/h, a median of 0.36/h and a 10th–90th percentile range of 0–1.75/h.
  At a nominal 0.1/h, 58% of patients had no alarm at all.
- The per-patient FAR distribution: median, 10th–90th percentiles, and the
  fraction of patients with zero alarms.
- The pooled FAR with a patient-bootstrap CI.
- Per-patient sensitivity, lead time from the first alarm, and time in alarm.
- The chance reference $1-e^{-\mathrm{FAR}\cdot w}$, and the M1 comparison.

### 12.3 Which records may estimate FAR

| Set | Status | Reason |
|---|---|---|
| SDDB remote zones (same equipment, same patients) | **primary**, labelled "**pre-VF-conditional FAR**" | same acquisition and population. But these are hours before VF in patients who go on to have it, **not** VF-free time |
| SDDB no-VF records 40, 42, 49 | descriptive only (n = 3; two paced) | same acquisition. Far too few for any rate claim |
| `chfdb` (and the Long-Term ST Database, if verified) | **transportability stress test**, admissible only if an acquisition comparability check passes; see below | different recorder, digitisation, annotation process and population. Its FAR measures a different acquisition chain |
| NSRDB | **never used for FAR** | different sampling rate (reported 128 Hz), healthy population |

**Acquisition comparability check, outcome-blind.** For each SQI feature,
compare the distribution in external records with that in SDDB remote zones.
The check fails if any feature's two-sample KS distance exceeds 0.3, or if
the ECG power spectra differ by more than 3 dB in the 0.5–40 Hz band. If it
fails, external FAR is reported as **non-interpretable** and not tabulated as
a rate.

### 12.4 Burden statement

Even 0.1 false alarms per hour is 2.4 per patient-day. **No FAR from this
study may be described as clinically usable.**

---

## 13. Binding decision rule

### 13.1 Gates, in order

1. **PIPELINE INVALID.** A §9.1 control fails.
2. **UNRESOLVED-BY-DESIGN.** A bin has < 6 contributing patients, or the
   outcome-blind informativeness gate fires.
3. **ACQUISITION-EXPLAINED.** R ≥ 0.70, or the conditional-increment or
   masking requirement fails in every bin that would otherwise pass.
4. **DRIFT-EXPLAINED.** Pseudo-onset, detrending or elapsed-time matching
   fails (or is non-evaluable) in every bin that would otherwise pass.

### 13.2 Primary verdicts

- **EXPLORATORY ASSOCIATION** (renamed from EXPLORATORY SIGNAL). In ≥ 2
  bins, at least one of which is B15 or B30, all of the following hold:
  1. the primary interval excludes 0;
  2. the sign test is met;
  3. all three temporal controls pass;
  4. R < 0.50, and the conditional-increment and masking requirements are
     met;
  5. at nominal FAR 0.5/h, realised sensitivity is ≥ M1 and above chance.
- **TRIGGER-PROXIMAL ASSOCIATION ONLY.** The same conditions hold, but only
  in B5 and/or B10.
- **NOT SUPPORTED.** The harness is valid and the informativeness gate is
  passed, and neither of the above holds.
- **HARM** (alongside any verdict). The interval lies entirely below 0 in
  ≥ 2 bins.

### 13.3 Binding falsification flag

**LARGE INCREMENT EXCLUDED:** the one-sided 95% upper bound is
< $\delta_{\mathrm{large}}$ (0.15, proposed) in all four bins. This
falsifies a large (≥ $\delta_{\mathrm{large}}$ AUROC) incremental association in
SDDB. Smaller increments remain unresolved, and that must be stated in the
same sentence.

### 13.4 Eligibility and sensitivity governance

- The verdict is reported at each $T_{\min}$ (§4.2) and each guard (§5.1).
- A verdict that changes between the primary and the 3-h eligibility rule is
  reported as eligibility-sensitive, and the more conservative verdict
  governs.
- Sensitivity variants never upgrade a verdict.

### 13.5 TD-specific attribution (secondary; required before any TD wording)

An EXPLORATORY ASSOCIATION may be described as involving **multivariate
structure** only if all of the following hold:

- M1 ∪ M2 ∪ M3 beats M1 ∪ M2;
- ΔG beats each of comparators C-a to C-e, with a positive point estimate
  and the sign test met;
- the §9.4 controls pass.

Otherwise it is reported as "an increment from features that do not require
multichannel structure", with no TD reading.

### 13.6 Permitted language

| Verdict | Maximum language |
|---|---|
| EXPLORATORY ASSOCIATION | "In a retrospective dataset of N patients who developed VF, adding TD statistics to conventional features was associated with better within-patient separation of pre-onset periods at alarm lead times of X min. Onset-locked artefact is excluded only insofar as the SQI features detect it, and circadian confounding is not excluded. This is exploratory and requires independent, event-unconditional validation." **Never** "predicts VF", "early warning", "advance warning", "forecast", or any mechanism |
| TRIGGER-PROXIMAL ONLY | "Changes within X min of onset." Not advance warning |
| NOT SUPPORTED + LARGE EXCLUDED | "No incremental association of ≥ 0.15 AUROC. Smaller effects, including every effect size this programme has previously measured, are not excluded" |
| NOT SUPPORTED alone | "Not supported. The data cannot resolve small effects" |
| any verdict | Hypotension verdicts are unaffected. M2 and M_null remain live |

---

## 14. Sample size and minimum detectable effect (from simulation)

See [`VF_DESIGN_SIMULATION.md`](VF_DESIGN_SIMULATION.md) for the
assumptions, the scenarios and the full tables. The headline figures are
summarised there and in
[`VF_DATASET_FEASIBILITY.md`](VF_DATASET_FEASIBILITY.md) §3. They are
**design-stage numbers under stated generative assumptions**, not
established properties of SDDB. They are recalibrated by the outcome-blind
gate.

| Quantity (n = 20, sustained long-lead precursor unless stated) | Simulated value |
|---|:--:|
| Null SD of per-patient Δ | 0.16–0.21 (v1 assumed 0.15) |
| 80%-power MDE per bin, mean ΔAUROC | **≈ 0.23** (v1 analytic: 0.12) |
| MDE at n = 12 | > 0.30 |
| Type-I rate of the decision rule under H0 | 0.000–0.005 (very conservative) |
| P(rule met), trigger-weighted precursor with B5 Δ ≈ 0.22 | 0.24 |
| P(LARGE INCREMENT EXCLUDED) under H0 at δ = 0.10 / 0.15 / 0.20 | 0.38–0.53 / 0.66–0.81 / 0.82–0.94 |
| Power for the effect sizes this programme has measured before (≤ 0.014) | ≈ α |

**Conclusion.** Under these assumptions, SDDB supports at most a
**large-effect screen**:

- an EXPLORATORY ASSOCIATION is reachable only if the true per-bin
  increment is about 0.2 AUROC or more;
- the binding falsification can, with δ = 0.15, exclude increments of
  ≥ 0.15 in most null worlds.

It does not support confirmatory testing of increments of the size this
programme has historically measured. **Whether a large-effect screen is
worth running is open decision D2.**

---

## 15. Retrospective discovery is not advance prediction

| Requirement for genuine advance prediction | Met here? |
|---|:--:|
| Model frozen **before** it is evaluated on independent patients | partly (LOPO within one dataset; community-mined dataset) |
| Evaluation over **all** monitored time, event-unconditional, including people who never develop VF | **no** |
| Calibrated absolute risk at realistic prevalence; PPV | **no**: not estimable from VF-conditional data |
| False-alarm burden measured in the target population and acquisition chain | **no**: pre-VF-conditional FAR only |
| Actionable lead time, shown prospectively or in a temporally external cohort | **no** |
| Independent site / era / equipment | **no** |

**This study can at most discover a candidate retrospective association.**
Even a strong EXPLORATORY ASSOCIATION would leave every row above except the
first unmet. It would justify only a confirmatory study designed to meet
them, never a statement about early-warning capability.

---

## 16. Open research decisions (must be resolved before freezing)

| # | Decision | Options | Current proposal |
|---|---|---|---|
| D1 | Status of Analysis B (AF-inclusive, NN-free) | co-primary with α split (0.05/8) / secondary but binding-reported | secondary, binding-reported |
| D2 | Is the design worth executing, given a simulated MDE of ≈ 0.23 at n = 20? And $\mathrm{MDE}_{\max}$ for the informativeness gate | run as a large-effect screen ($\mathrm{MDE}_{\max}$ 0.25) / keep 0.20 (probably UNRESOLVED-BY-DESIGN) / defer until a larger, event-unconditional cohort exists | large-effect screen at 0.25; **the reviewer decides** |
| D3 | Guard $g$ | 1 / 2 / 5 min | 2 min, with 1 and 5 as sensitivities |
| D4 | Primary event | VF onset / first sustained VT | VF onset |
| D5 | $R_{\min}$ and therefore $T_{\min}$ | 30 min (2 h 20) / 60 min (2 h 50) | 30 min, with eligibility sensitivity. The simulated precision cost of short remote zones is modest and confined to B15/B30 |
| D6 | Circadian confound, if headers lack clock time | accept as a declared limitation / do not run | declared limitation |
| D7 | External FAR set | chfdb / LTSTDB / none | chfdb, conditional on the comparability check |
| D8 | ΔG Ledoit–Wolf intensity | analytic / fixed 0.1 / fixed 0.3 | analytic primary, fixed as sensitivity |
| D9 | δ_large | 0.10 / 0.15 / 0.20 | **0.15**. At n = 20 it fires in 66–81% of null studies, vs 38–53% for 0.10 |
| D10 | Keep the conservative conjunctive rule (Bonferroni × sign test × two bins; simulated type I 0–0.5%) | keep / replace with a single omnibus test over bins | **keep**. Changing binding criteria after a design simulation is a move this programme avoids; the cost is a larger MDE |

## 17. Freezing conditions

The protocol is frozen only after all of the following:

- Phase 0 verification is recorded;
- an independent review of v2 is complete;
- the §16 decisions are resolved;
- a separate `PROTOCOL_VF_ONSET.md` exists with a FROZEN banner and hashes;
- the user authorises a single execution.

Until then nothing is run on SDDB beyond header and metadata verification.

---

## Appendix A — change log v1 → v2

| # | v1 | v2 | Reason (review item) |
|---|---|---|---|
| A1 | "Expected outcome: NOT SUPPORTED …" | **removed**. Prior evidence recorded in both directions, none in the rule | review C3 / issue 1 |
| A2 | Positive results "treated as suspicious first" | symmetric integrity audit for every verdict (§9.6) | outcome-dependent scrutiny prejudges the result (issue 1) |
| A3 | Explicit H0 absent | H0-VF stated as the binding falsification target (§3) | issue 1 |
| A4 | Analytic MDE (σ = 0.15 assumed) | simulation-based MDE, clustering, overlap, 4 bins, LOPO (§14) | review C2 / issue 2 |
| A5 | Pseudo-onsets and detrending required; elapsed-time matching secondary | all three required, with a capability table; onset-locked and circadian limits declared in reporting language (§9.2) | review C1 / issue 3 |
| A6 | Overlap not analysed; "≥ 2 consecutive windows" alarm rule | effective-positive analysis, patient-level-only inference, persistence-in-time alarm rule, realised FAR reported (§8.2, §12) | review M1 / issue 4 |
| A7 | Guard 2 min; VT exclusion with one sensitivity | guard justified by the simulated trade-off; NSVT retained in M1; six sensitivity variants; precursor-removal audit (§5.1) | review M2 / issue 5 |
| A8 | $T_{\min}$ = 2 h 15 (arbitrary sum); minimum 12 patients | derived $T_{\min}$ = 2 h 20 with each term justified; eligibility sensitivity at 3 h and 4 h with a conservative governing rule; 12 replaced by a capability floor of 6 and an outcome-blind informativeness gate (§4.2–4.3) | review M3 / issue 6 |
| A9 | AF excluded; non-NN analysis exploratory | Analysis B, rhythm-inclusive and NN-free, separately reported (§4.1) | review M4 / issue 7 |
| A10 | ΔG "decided at freeze" | exact AIRM, Ledoit–Wolf, SPD floor, Cholesky, fixed beat count, robust standardisation, five simpler comparators, M1 ∪ M2 attribution (§7.4) | review M5 / issue 8 |
| A11 | chfdb as the external FAR set | FAR source hierarchy; outcome-blind comparability check; NSRDB excluded (§12.3) | review M6 / issue 9 |
| A12 | "EXPLORATORY SIGNAL"; "advance warning" wording | "EXPLORATORY ASSOCIATION"; §15 requirements table; forbidden-terms list | review M7 / issue 10 |
| A13 | Pseudo-onset null with no availability rule | non-evaluable when < 8 subjects, which fails the bin | review moderate item |
| A14 | Between-database demo "expected to separate" | reported whatever it shows | issue 1 |
| A15 | δ_large = 0.10 | 0.15 proposed (D9) | simulation: 0.10 fires in < half of null studies, so the binding falsification would usually be uninformative |
| A16 | informativeness gate MDE > 0.15 (v1) / 0.20 | $\mathrm{MDE}_{\max}$ = 0.25 proposed, explicitly a large-effect-screen framing, open (D2) | the simulated MDE is ≈ 0.23 at n = 20 |
| A17 | covariance windows of fixed duration | fixed beat count ($N_b$ = 256) | simulation: a 10% HR rise lowers AIRM by about 9% with no structural change |
| A18 | "≥ 2 consecutive windows" alarm | 3-minute persistence, realised FAR reported | simulation: overlap makes window-count rules nearly ineffective |

---

© 2026 Davarn Morrison · Transition Dynamics
