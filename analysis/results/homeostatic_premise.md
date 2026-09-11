## 3. Matched-magnitude, matched-exposure test (the decisive one)

All forced conditions calibrated on the deterministic twin to the same displacement magnitude ‖δ‖ ≈ 3.35, same exposure T = 60. Stationary sampling noise floor for ‖δ‖ is 0.33, so the signal clears it by 10×. 30 seeds. n_eff ≈ 876 (requirement ≥ 10p = 80).


| condition | ‖δ‖ | A | z vs own null | dG | max univariate |
|---|:--:|:--:|:--:|:--:|:--:|
| stationary | 0.39 | 0.348 | -0.08 | 0.79 | 5.6 |
| isotropic | 3.96 | 0.352 | -0.04 | 2.93 | 57.0 |
| targeted-stiff | 3.37 | 2.671 | +7.85 | 4.74 | 207.9 |
| targeted-soft | 3.24 | 0.181 | -1.24 | 2.25 | 50.9 |

A(targeted-stiff) 95% CI [2.651, 2.691] · A(isotropic) 95% CI [0.301, 0.416]


| discrimination at matched magnitude and exposure | AUC |
|---|:--:|
| **A: targeted-stiff vs isotropic** | **1.00** |
| A: targeted-soft vs isotropic | 0.03 |
| dG (covariance drift / DNB): targeted-stiff vs isotropic | 1.00 |
| max univariate z: targeted-stiff vs isotropic | 1.00 |

## 4. Is A's response to TARGETING larger than to EXPOSURE?

If exposure moves A more than targeting does, A cannot be read as a targeting measure in data where exposure is unknown — which is the normal clinical situation.


| isotropic force, exposure T | mean A |
|:--:|:--:|
| 1 | 0.639 |
| 12 | 0.376 |
| 120 | 0.350 |

- A moved by **0.289** across exposure alone (no targeting).
- A moved by **2.318** from targeting at fixed exposure.
- ratio exposure/targeting = **0.12**

AUC separating short-exposure from long-exposure isotropic insults: **0.91** — both with no targeting whatsoever.


## 5. Class-stratified monitoring / sampling control

Physiology identical across classes; only the **observation process** differs, as it does between real event classes. If A separates the classes here, class-specific geometry can be manufactured by monitoring behaviour alone.


| class (observation process) | A | z | n kept |
|---|:--:|:--:|:--:|
| regular | 0.352 | -0.04 | 400 |
| escalating | 0.352 | -0.10 | 249 |

AUC separating the two observation processes on identical physiology: **0.49**


## 6. Sensitivity: baseline window and effective sample size


| baseline window (obs) | n_eff | stationary null median A | A targeted-stiff |
|:--:|:--:|:--:|:--:|
| 1000 | 222 | 0.303 | 0.330 |
| 2000 | 440 | 0.314 | 0.350 |
| 4000 | 876 | 0.318 | 2.671 |

A(targeted) varies by 2.341 across baseline-window choice.


| channels p | 95% null band for A | width |
|:--:|:--:|:--:|
| 4 | [0.27, 2.19] | 1.92 |
| 8 | [0.42, 1.87] | 1.45 |
| 16 | [0.56, 1.61] | 1.05 |
| 32 | [0.67, 1.40] | 0.73 |

## 7. Verdict against the preregistered rules


| criterion | value | threshold |
|---|:--:|:--:|
| AUC targeted vs isotropic (matched) | 1.00 | A ≥ 0.80 / C < 0.65 |
| sampling control AUC | 0.49 | C if ≥ 0.80 |
| exposure span vs targeting span | 0.289 vs 2.318 | C if exposure > targeting |

### Verdict: **A**

