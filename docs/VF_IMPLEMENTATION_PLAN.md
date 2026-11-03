# VF onset programme — implementation plan

> **Status: PLAN ONLY.** No code in this plan has been written or run. Each
> phase needs explicit sign-off before it starts. Nothing here alters
> historical results, frozen protocols, result artefacts or existing analysis
> code. New code goes in `analysis/vf/` and new outputs in `analysis/results/vf_*`.
>
> Protocol: [`VF_PROTOCOL_DRAFT.md`](VF_PROTOCOL_DRAFT.md) ·
> Feasibility: [`VF_DATASET_FEASIBILITY.md`](VF_DATASET_FEASIBILITY.md)

---

## Phase 0 — access and verification (headers and metadata only)

**Blocker.** `physionet.org` must be allowed in the session's network
settings. It is currently refused.

1. Download `sddb` (and `chfdb`, plus `nsrdb` for §9.6) into a fresh data
   directory outside the repository. Verify against PhysioNet `SHA256SUMS`.
2. Parse `.hea` files only: sampling rate, signal count, ADC gain, duration,
   `#vfon` and any rhythm / pacing / demographic comments. List the
   annotation files present (`.ari`, `.atr`).
3. Write `docs/VF_DATASET_VERIFICATION.md`: every row of
   [`VF_DATASET_FEASIBILITY.md`](VF_DATASET_FEASIBILITY.md) §0 marked
   verified or corrected. Corrections amend the feasibility document in a
   separate commit.
4. Apply the §4 eligibility rules. Freeze `analysis/results/vf_eligibility.json`
   with its SHA-256.

**No signal sample is read in Phase 0.**

## Phase 1 — pipeline code (numpy only, matching the rest of the repository)

| Module | Responsibility | Guard |
|---|---|---|
| `analysis/vf/wfdb_io.py` | format-212 / 16 reader, header parser, annotation reader | round-trip test on a synthetic record |
| `analysis/vf/beats.py` | fixed QRS detector, beat classes, NN series | detector parameters as module constants |
| `analysis/vf/panel.py` | per-beat NN, RTa, Tamp, ST | template-correlation SQI |
| `analysis/vf/sqi.py` | the 7 M0-acq features | — |
| `analysis/vf/features.py` | M1, M2 and TD-1…TD-4 per window, reusing `analysis/estimators.py` (`shrunk_covariance`, `delta_G_structure`, `beta1_excess_over_pairwise`, `effective_sample_size`) | **no onset argument**. Test: outputs identical under any onset |
| `analysis/vf/zones.py` | the only reader of `#vfon`. Zones, bins and exclusions | outcome-blind mode truncates at onset − 60 min |
| `analysis/vf/models.py` | fixed-λ ridge logistic, LOPO | no probability pooling (bug 11) |
| `analysis/vf/metrics.py` | within-patient AUROC/AUPRC, alarms, FAR, chance reference | single-feature reproduction test |
| `analysis/vf/controls.py` | pseudo-onsets, block label permutation, shuffled onsets, row-wise channel shuffle (bug 12), order destruction, geometry competitors | each control asserts that its output differs from the real arm |
| `analysis/vf/test_vf.py` | unit and regression tests | — |

## Phase 2 — harness validation (synthetic only, no SDDB signal)

- Synthetic no-precursor arm: chance. Injected-precursor arm: detected.
  Drift-only arm (monotone artefact rising towards the event, no precursor):
  must be **caught by the pseudo-onset control**, which shows that the control
  works.
- Shape checks from [`CANONICAL_STATUS.md`](CANONICAL_STATUS.md) §7: no
  impossible AUROCs; controls never bit-identical to the real arm.

## Phase 3 — outcome-blind calibration on SDDB (truncated loader)

- Load VF records truncated at $t_{\mathrm{VF}}-60$ min; no-VF records are
  loaded whole.
- Compute: the $n_{\mathrm{eff}}$ gate → $W$; baseline SQI thresholds; beat
  yield (eligibility rule 4); pseudo-onset null SD → realised MDE (power
  gate). Write `analysis/results/vf_calibration.json`.
- If the power gate fires, report it and stop H-VF, so the true-onset analysis
  is never read.

## Phase 4 — freeze (review checkpoint)

Resolve protocol §15. Write `docs/PROTOCOL_VF_ONSET.md` with a FROZEN banner,
the parameter hash, the code commit and the eligibility hash. Commit before
execution.

## Phase 5 — single exploratory execution (only on explicit authorisation)

`analysis/vf/run_vf_exploratory.py`: one run with all controls, writing
`analysis/results/vf_exploratory.json`. Development and execution outputs are
never pooled. Any aborted launch is recorded in a provenance note, as in
[`PROVENANCE_TIER2_LAUNCH.md`](PROVENANCE_TIER2_LAUNCH.md).

## Phase 6 — reporting

Write `docs/RESULT_VF_EXPLORATORY.md` with the verdict, the large-effect flag,
every control and the permitted language from protocol §13.5. Any change to
`CANONICAL_STATUS.md` **appends** a new section; existing sections are not
edited.

## Phase 7 — confirmatory path (out of scope here)

Applies only if Phase 5 returns EXPLORATORY SIGNAL. An independent cohort with
≥ ~100 adjudicated VF onsets, a new frozen protocol inheriting this one's
parameters unchanged, and credentialed access
([`CREDENTIALED_ACCESS_CHECKLIST.md`](CREDENTIALED_ACCESS_CHECKLIST.md)).

---

© 2026 Davarn Morrison · Transition Dynamics
