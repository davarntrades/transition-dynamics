# VitalDB confirmatory model-adequacy result

Frozen protocol plus the 2026-09-11 amendment. Nothing tuned.


| | |
|---|:--:|
| cases screened | 298 |
| admissible | **56** |
| required | 50 |

## Exclusions

| reason | n |
|---|:--:|
| baseline non-stationary | 196 |
| fewer than 4 channels | 17 |
| baseline n_eff 37 < 40 | 5 |
| baseline n_eff 39 < 40 | 4 |
| too short after removing incomplete rows | 3 |
| baseline n_eff 30 < 40 | 2 |
| baseline n_eff 22 < 40 | 2 |
| baseline n_eff 38 < 40 | 2 |
| baseline n_eff 35 < 40 | 2 |
| baseline n_eff 36 < 40 | 2 |
| baseline n_eff 21 < 40 | 1 |
| baseline n_eff 25 < 40 | 1 |
| baseline n_eff 27 < 40 | 1 |
| baseline n_eff 31 < 40 | 1 |
| baseline n_eff 32 < 40 | 1 |
| baseline n_eff 18 < 40 | 1 |
| baseline n_eff 26 < 40 | 1 |

## Stage B — model selection


| quantity | value | 95% CI |
|---|:--:|:--:|
| **M-exp selection rate** | **62%** | [50%, 75%] |
| surrogate selection rate | 56% | [50%, 61%] |
| **difference** | **+7%** | [-6%, +19%] |
| M-exp beats free-rate variant | 89% | – |

### Held-out error by model (lower is better)


| model | median MSE | mean rank | won in |
|---|:--:|:--:|:--:|
| M-null | 104.6 | 4.64 | 2% |
| M-const | 78.62 | 3.00 | 7% |
| M-lin | 81.9 | 3.05 | 27% |
| M-exp | 75.02 | 1.61 | 62% |
| M-exp-free | 86.33 | 3.25 | 2% |
| M-spline | 304.3 | 6.34 | 0% |
| M-rw | 307.3 | 6.11 | 0% |

## Stage C — baseline rates vs trajectory curvature


| quantity | value | 95% CI |
|---|:--:|:--:|
| median rank correlation | **0.00** | [-0.15, 0.15] |
| fraction with corr >= 0.5 | 25% | – |

## Per-subject distribution


- cases where M-exp won: 35 of 56

- n_eff across cases: median 106, range 40–740

- worst 3 cases for M-exp: 5550 (MSE 681), 2700 (MSE 328), 3625 (MSE 279)

## Verdict


### **NOT SUPPORTED — exponential form not preferred, or no advantage over surrogates**
