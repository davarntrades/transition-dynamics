# Real-data Stage A admissibility

Applies `docs/PROTOCOL_MODEL_ADEQUACY.md` Stage A to the real recordings reachable from this environment.


**Provenance.** Real human ECG/RSP/EDA at 100 Hz from the NeuroKit project, resting and event-related protocols in healthy adults. These contain **no clinical deterioration and no transition events**.


| recording | channels | n (1 Hz) | mean lag-1 AC | n_eff | required | admissible |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| bio_eventrelated_100hz.csv | 5 | 150 | 0.876 | 15 | 50 | **no** |
| bio_resting_8min_100hz.csv | 5 | 507 | 0.899 | 29 | 50 | **no** |

## Exclusion reasons


**bio_eventrelated_100hz.csv** — excluded:

- n_eff 15 < 50 (10 x p)

- baseline not stationary: max shift 0.68 SD


**bio_resting_8min_100hz.csv** — excluded:

- n_eff 29 < 50 (10 x p)

- baseline not stationary: max shift 2.17 SD


## How far short?


| recording | n_eff | needed | shortfall | recording length needed |
|---|:--:|:--:|:--:|:--:|
| bio_eventrelated_100hz.csv | 15 | 50 | 3.2× | ~8 min at this channel set |
| bio_resting_8min_100hz.csv | 29 | 50 | 1.7× | ~15 min at this channel set |

## Verdict


Admissible recordings: **0** of 2. Protocol requires **50** for any adequacy conclusion.


**Stage B and Stage C are not run.** Running them on inadmissible recordings would produce exactly the kind of confident, meaningless result this programme has already generated four times.


The blocker is not access to *some* real physiology — that was obtained. The blocker is that the reachable recordings are minutes long, while the protocol needs hours of multichannel recording per patient with an observed transition. See `docs/DATA_REQUIREMENTS_REAL.md`.
