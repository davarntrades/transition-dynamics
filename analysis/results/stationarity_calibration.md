# Is the 0.5 SD stationarity screen appropriate?

Decided on simulation and the calibration subset. The confirmatory cohort is not examined.


## 1. The screen on data that is stationary BY CONSTRUCTION


AR(1) with no drift at all. Any rejection here is a false positive.


| n | lag-1 ρ | n_eff | median shift | 95th pct | rejected at 0.5 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 48 | 0.85 | 7 | 1.45 | 2.00 | **100%** |
| 96 | 0.85 | 11 | 1.17 | 1.72 | **98%** |
| 168 | 0.85 | 17 | 0.90 | 1.50 | **94%** |
| 500 | 0.95 | 16 | 0.93 | 1.40 | **92%** |
| 2000 | 0.98 | 23 | 0.77 | 1.30 | **85%** |
| 10800 | 0.995 | 54 | 0.64 | 1.07 | **73%** |

The false-positive rate is driven by effective sample size, not by drift. A fixed threshold rejects stationary data whenever n_eff is small, which is exactly the regime hourly ICU baselines sit in.


## 2. The screen's null scales as 1/sqrt(n_eff)


The difference of two third-window means has SD `SD*sqrt(2/n_eff_third)`, so the expected shift under stationarity falls with n_eff. Observed against predicted:


| n_eff | observed median shift | predicted ~2/sqrt(n_eff/3) |
|:--:|:--:|:--:|
| 7 | 1.45 | 1.28 |
| 11 | 1.17 | 1.05 |
| 17 | 0.90 | 0.85 |
| 16 | 0.93 | 0.88 |
| 23 | 0.77 | 0.72 |
| 54 | 0.64 | 0.47 |

## 3. Can it detect genuine drift?


Same process plus a real linear drift. A useful screen should separate these from the stationary case.


| n | ρ | drift (SD) | median shift | flagged at 0.5 |
|:--:|:--:|:--:|:--:|:--:|
| 2000 | 0.98 | 0.0 | 0.76 | 85% |
| 2000 | 0.98 | 0.5 | 0.89 | 92% |
| 2000 | 0.98 | 1.0 | 1.13 | 99% |
| 2000 | 0.98 | 2.0 | 1.52 | 100% |
| 2000 | 0.98 | 4.0 | 1.96 | 100% |

## 4. A threshold that actually tests stationarity


Standardising the shift by its own null scale gives a quantity whose distribution does not depend on n_eff:


```
z_shift = shift / (2 / sqrt(n_eff/3))
```


| n | ρ | drift (SD) | median z_shift | flagged at z>2 |
|:--:|:--:|:--:|:--:|:--:|
| 96 | 0.85 | 0.0 | 1.11 | 0% |
| 96 | 0.85 | 1.0 | 1.27 | 1% |
| 96 | 0.85 | 4.0 | 1.33 | 0% |
| 2000 | 0.98 | 0.0 | 1.06 | 1% |
| 2000 | 0.98 | 1.0 | 1.48 | 7% |
| 2000 | 0.98 | 4.0 | 1.85 | 7% |