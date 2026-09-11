# Stage 4b — confounded exposure, the test Stage 4 missed

Stage 4 drew both groups from the same exposure grid, so their exposure distributions were identical and there was no confound to remove. Here exposure is deliberately correlated with group, which is the situation the whole exercise was built to address.


Recent exposure T=3, established T=120; 60 cases per group; displacement 1.5 baseline SD.


## SPURIOUS — both groups untargeted


Group A: 80% recent. Group B: 20% recent. Displacement 1.5 baseline SD. Truth: AUC should be 0.50.


| structure | naive (no control) | oracle true T | estimated T | bins | declined |
|---|:--:|:--:|:--:|:--:|:--:|
| wide-rotated | 0.381 | 0.508 | 0.508 | 2 | 0% |
| wide-diagonal | 0.379 | 0.508 | 0.508 | 2 | 0% |
| narrow-rotated | 0.465 | 0.530 | 0.530 | 2 | 0% |

median: naive 0.381 · oracle 0.508 · estimated 0.508

- naive bias from 0.50: **0.119**

- oracle residual bias: 0.008

- estimated-T residual bias: **0.008** (rescues if <= 0.10)


### Verdict: **RESCUES**


## MASKED, strong targeting (1.5 SD)


Group A: 80% recent. Group B: 20% recent. Displacement 1.5 baseline SD. Truth: targeting present.


| structure | naive (no control) | oracle true T | estimated T | bins | declined |
|---|:--:|:--:|:--:|:--:|:--:|
| wide-rotated | 1.000 | 1.000 | 1.000 | 2 | 0% |
| wide-diagonal | 0.998 | 1.000 | 1.000 | 2 | 12% |
| narrow-rotated | 0.995 | 0.998 | 0.998 | 2 | 0% |

median: naive 0.998 · oracle 1.000 · estimated 1.000

- naive comparison: 0.998

- oracle true-T control: 1.000

- estimated-T control: **1.000**

- masking present? no — targeting dominates the exposure contrast


## MASKED, weak targeting (0.5 SD)


Group A: 80% recent. Group B: 20% recent. Displacement 0.5 baseline SD. Truth: targeting present.


| structure | naive (no control) | oracle true T | estimated T | bins | declined |
|---|:--:|:--:|:--:|:--:|:--:|
| wide-rotated | 0.946 | 0.968 | 0.973 | 1 | 37% |
| wide-diagonal | 0.897 | 0.933 | 0.950 | 1 | 38% |
| narrow-rotated | 0.958 | 0.973 | 0.965 | 2 | 33% |

median: naive 0.946 · oracle 0.968 · estimated 0.965

- naive comparison: 0.946

- oracle true-T control: 0.968

- estimated-T control: **0.965**

- masking present? no — targeting dominates the exposure contrast
