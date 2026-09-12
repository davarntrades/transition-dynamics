# Provenance note — Tier-2 execution, aborted first launch

**This note records an aborted pre-outcome launch. It alters no scientific
verdict, no threshold, and no frozen artifact.**

---

## What happened

On 2026-09-12, with authorisation to execute Tier 2, the frozen runner
`analysis/acquisition/run_tier2.py` was invoked from `main` at
`caf1a4187947279ab5841e6576c2d11097975313`. All ten preconditions verified
before launch.

**The launch produced no result.** After 150 of 600 cases the usable count was
still zero.

### Root cause

`run_tier2.py` extracts the arterial **waveform** into `data/real/vitaldb/npz_acq/`,
but never fetches the **eight-channel Solar8000 panel** into
`data/real/vitaldb/npz_sd/`, which the frozen structural harness `case_rows()`
requires in order to build B\*. Every Tier-2 case therefore raised

```
FileNotFoundError: .../npz_sd/<caseid>.npz
```

which the runner's broad `except` recorded as an exclusion. Confirmed by
controlled comparison: with the structural cache present (development case)
`case_rows` follows its normal exclusion path; without it, it raises.

This is a **missing upstream data-preparation dependency**, sitting entirely
upstream of any outcome computation. The runner's analysis logic is correct.

### Exposure at the point of abort — all zero

| quantity | value |
|---|:--:|
| endpoints evaluated | **0** |
| labels computed | **0** |
| models fitted | **0** |
| metrics computed | **0** |
| Tier-2 result artifacts written | **0** |
| outcome summaries inspected | **0** |
| Tier-2 pressure series cached | 175 / 600 |

The cached series include `ART_MBP`, the channel the endpoint is *defined
from*, but no endpoint was applied, no label derived, and nothing was
inspected, summarised or reported. Blinding was intact throughout.

Integrity immediately after the abort: `acq_freeze_manifest.json` 14/14 and
`rs_freeze_manifest.json` 10/10 verifying, working tree clean, HEAD unchanged,
no code modified.

## Resolution

Per explicit instruction, the aborted launch is treated as an **incomplete
execution caused by a missing upstream data-preparation dependency, not as a
completed Tier-2 attempt.**

The remedy changes **no frozen code**: the required `npz_sd/` cache is
populated for the full frozen 600-case Tier-2 cohort using the already-frozen
`analysis/structural/fetch.py`, structurally verified, and the **unchanged**
`run_tier2.py` is then invoked to complete the same authorised execution.

**This is not a second confirmatory attempt.** It is completion of the single
authorised execution after supplying the frozen runner's required upstream
cache. No cohort, endpoint, B\*, horizon, exclusion, feature, detector,
injection parameter, bootstrap setting, threshold, decision rule or line of
runner code was altered.

## Incidental finding, recorded

While confirming no process remained alive, a status check using
`pgrep -f "[r]un_tier2.py"` reported a match. The match was the checking shell
itself: its own command line contained the literal string `run_tier2.py` inside
an `echo` argument. Same self-match class as harness bug 12. A check filtered
to real interpreter processes (`ps` on `^python3 `) correctly returned zero.
No scientific result depends on this; it is recorded because process-status
self-matching has now produced a misleading reading twice in this programme.

---

© 2026 Davarn Morrison · Transition Dynamics
