# VF onset programme — proposed v3 amendments (specification only)

> **Status: PROPOSAL. NOT A PROTOCOL. NOT FROZEN.**
>
> The verified Phase 0 evidence and the independent review require revisions
> to v2 ([`VF_PROTOCOL_DRAFT.md`](VF_PROTOCOL_DRAFT.md)). The readiness
> assessment finds the SDDB test of H-VF **not feasible**
> ([`VF_READINESS_ASSESSMENT.md`](VF_READINESS_ASSESSMENT.md)). For that
> reason, **no full v3 protocol is written for SDDB**. These amendments are
> to be applied to whichever dataset is chosen, and then frozen only after a
> new verification and review.
>
> No threshold is lowered here. Where a fix changes a criterion, the change
> makes it *valid*, not easier.

| # | v2 element | Amendment | Reason |
|:--:|---|---|---|
| V1 | Gate 3 (R ≥ 0.70, or fail "in every bin that would otherwise pass") | Evaluate gates 3–4 **only on bins that pass the primary statistical criteria**. If none pass, gates 3–4 are not evaluated and the verdict proceeds to NOT SUPPORTED. Replace the R ratio with the **conditional increment** (M4 ∪ M0 vs M1 ∪ M0) as the binding acquisition test. R stays descriptive, reported only when AUROC(M3) − 0.5 > 0.05 | review F1: a vacuous gate; R undefined under H0 (author-verified: 88% of null studies) |
| V2 | Pipeline gate "mean AUROC within 0.45–0.55" | Replace it with a **calibrated** criterion: the shuffled-onset mean Δ and mean AUROC must lie within the central 95% of their own permutation distribution, built by refitting the full LOPO on ≥ 200 onset shuffles | F2: the fixed band fails 98% of valid pipelines |
| V3 | Pseudo-onset null (resampling offsets) | A **paired per-patient test**. For each patient with ≥ 1 pseudo-onset, compute $d_i = \Delta_i^{\text{true}} - \overline{\Delta_i^{\text{pseudo}}}$. Then a one-sided t-test and sign test across patients. Non-evaluable below 8 patients | F4: the old test passes 15–30% of null studies |
| V4 | Student-t interval on LOPO Δᵢ | The **primary interval comes from a patient bootstrap that refits the full LOPO in every replicate** (≥ 1,000), or from a refitting patient-permutation test. Keep the t-interval as a descriptive cross-check | F5: ×1.1–1.5 anti-conservative |
| V5 | H0: E[Δ] = 0; two-sided interval; unadjusted sign test | Rewrite the hypotheses. **H0(b): E[Δ_b] ≤ 0 for each bin b**, tested with directional one-sided tests. **Keep v2's effective per-bin level** (one-sided 0.00625, equivalent to v2's two-sided 0.0125) for the interval, and **apply the same 0.00625 level to the sign test**, which was unadjusted at 0.025 in v2. This is strictly more conservative than v2; no level is relaxed. The −0.01 to −0.02 overfitting bias is declared, not corrected away | F14 |
| V6 | Verdict branches | Define them exhaustively: <br>(a) 0 bins pass → NOT SUPPORTED; <br>(b) only B5 and/or B10 pass → TRIGGER-PROXIMAL; <br>(c) exactly one of B15/B30 passes and no other bin → **SINGLE-BIN LONG-LEAD, NOT AN ASSOCIATION**; <br>(d) ≥ 2 bins including B15 or B30 → EXPLORATORY ASSOCIATION. <br>HARM overrides every positive verdict. A bin with < 6 patients is non-evaluable; it does not void the study. Alarm condition 5 is evaluated per claimed bin, descriptively | F12 |
| V7 | "More conservative verdict governs" | A total order: PIPELINE INVALID > UNRESOLVED > ACQUISITION-EXPLAINED = DRIFT-EXPLAINED > NOT SUPPORTED > TRIGGER-PROXIMAL > SINGLE-BIN > EXPLORATORY. "Conservative" means further left. It applies across **all** eligibility variants (including 4 h) and guard variants | F13 |
| V8 | Artefact masking at the baseline 99th percentile | Mask on **absolute, physically defined** artefact criteria (flat line, clipping, detector disagreement above a fixed fraction) set outcome-blind. Report the masked fraction per zone; > 25% masked in a bin means non-evaluable | F8: 88% masked under null |
| V9 | SQI / M0 features | Split them into **pure-acquisition** features (clipping, flat line, saturation, baseline wander < 0.5 Hz) and **physiology-sensitive** features (detector disagreement, R amplitude, HF power). Only pure-acquisition features enter the binding acquisition test. The others are reported descriptively | F11: physiology must not be attributed to acquisition |
| V10 | Elapsed-time matching on the raw TD composite | Match on the **residual of the TD composite after regression on M1 features**, with coefficients fitted in the remote zones of other patients | F16 |
| V11 | Detrending over the full remote zone | Detrend using the **earliest 50%** of the remote zone, and report the extrapolation distance. Declare that slowly developing precursors (> 60 min) are indistinguishable from drift by design | F11 |
| V12 | Annotation-derived NN, ectopy and VT | **No unaudited annotation enters any feature or exclusion.** Use an own beat detector and classifier, validated against `.atr` (or the new dataset's reference) **outside the sealed zone**, with pre-specified acceptance (e.g. V-beat sensitivity and PPV ≥ 0.90). Sustained VT is defined from classifier output | Phase 0 P0-2, P0-3 |
| V13 | Lead "1 primary" | The lead is chosen per patient by an outcome-blind criterion (highest baseline QRS SNR). The other lead is used for replication | Phase 0 P0-6 |
| V14 | Guard on an onset-aligned grid | Align the 60-s grid to $T_{\mathrm{VF}}$ (window ends at $T_{\mathrm{VF}} - k$ min), or state guard validity only for marking error < $g$ | F17 |
| V15 | Informativeness gate on a single MDE | Report the MDE over a **pre-specified grid of heterogeneity × autocorrelation × shape**. The gate passes only if the MDE ≤ $\mathrm{MDE}_{\max}$ in the **median** grid cell. $\mathrm{MDE}_{\max}$ is **not** raised from 0.25 | F3, Q6 |
| V16 | Simulation fidelity | Replace mean-shift TD features with **beat-level synthetic panels** passed through the actual S, ΔG and TD-3 estimators. Simulate the full rule (masking, gates 1–2, condition 5, eligibility governance). Use non-aligned leads | F7, F18 |
| V17 | λ = 1 | Define the loss as the **mean** log-loss over training windows (balanced weights), with λ = 1 on that scale | F19 |
| V18 | Event labels | Require a **documented** onset annotation (annotator and method), or a pre-specified verification step, before eligibility | Phase 0 P0-1 |

**What does not change:**

- the estimand separation (E-onset / E-risk / E-advance);
- the prohibited-language list;
- the status of the TD objects (demoted objects stay demoted);
- δ = 0.15 as the exclusion threshold (D9, provisional);
- the conservative multi-bin requirement (D10).

---

© 2026 Davarn Morrison · Transition Dynamics
