# Structural displacement and prediction of deterioration — confirmatory_severe result

Endpoint: intraoperative hypotension, `ART_MBP < 65 mmHg` for `>= 60 s`. Every window already containing hypotension is excluded, so this is prediction from a currently non-hypotensive state.

Usable cases **166** of 400 · excluded 234 ({'coverage': 135, 'hypotension in baseline': 99}) · evaluation windows **23961**

## Verdict

# NOT SUPPORTED

## Power

| horizon | windows | positives | prevalence | patients | with an event |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 5min | 23810 | 283 | 0.0119 | 166 | **70** |
| 10min | 23553 | 647 | 0.0275 | 166 | **83** |
| 15min | 23190 | 1042 | 0.0449 | 166 | **85** |

## Primary comparison — M10 (M9 + S) vs M9 (marginals only)

Bonferroni 95% CI over three horizons, patient-level bootstrap, 2000 resamples of caseids.

| horizon | AUROC M9 | AUROC M10 | ΔAUROC [CI] | AUPRC M9 | AUPRC M10 | ΔAUPRC [CI] |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5min | 0.8319 | 0.8318 | **-0.0001** [-0.0010, +0.0009] | 0.1116 | 0.1117 | **+0.00015** [-0.00068, +0.00092] |
| 10min | 0.7870 | 0.7868 | **-0.0001** [-0.0017, +0.0014] | 0.1797 | 0.1811 | **+0.00135** [-0.00156, +0.00517] |
| 15min | 0.7404 | 0.7363 | **-0.0041** [-0.0092, +0.0010] | 0.1730 | 0.1688 | **-0.00438** [-0.00956, -0.00045] |

## All comparators

### 5min

| model | AUROC | AUPRC | sens@5% FAR | sens@10% FAR | lead min | Brier | cal slope |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| ABL_subject | 0.8356 | 0.1131 | 0.481 | 0.569 | 3.4 | 0.0116 | 0.994 |
| ABL_diagonal | 0.8322 | 0.1115 | 0.477 | 0.562 | 3.4 | 0.0116 | 0.987 |
| ABL_population | 0.8322 | 0.1111 | 0.473 | 0.558 | 3.3 | 0.0116 | 0.983 |
| ABL_identity | 0.8321 | 0.1122 | 0.477 | 0.562 | 3.4 | 0.0116 | 0.987 |
| M9_strong_marginal | 0.8319 | 0.1116 | 0.477 | 0.558 | 3.3 | 0.0116 | 0.987 |
| M10b_M9_plus_Mahalanobis | 0.8318 | 0.1119 | 0.477 | 0.558 | 3.3 | 0.0116 | 0.987 |
| M10_M9_plus_S | 0.8318 | 0.1117 | 0.481 | 0.558 | 3.3 | 0.0116 | 0.982 |
| ABL_patient | 0.8318 | 0.1117 | 0.481 | 0.558 | 3.3 | 0.0116 | 0.982 |
| ABL_shuffled | 0.8310 | 0.1116 | 0.484 | 0.551 | 3.3 | 0.0116 | 0.983 |
| M11_marginal_plus_covdrift | 0.8246 | 0.1130 | 0.477 | 0.555 | 3.4 | 0.0115 | 1.028 |
| M8_marginal_LR | 0.8244 | 0.1004 | 0.470 | 0.572 | 3.4 | 0.0115 | 1.049 |
| M5_dispersion | 0.8100 | 0.0971 | 0.431 | 0.558 | 3.4 | 0.0119 | 0.865 |
| M7_cov_drift | 0.7272 | 0.0591 | 0.286 | 0.417 | 3.5 | 0.0116 | 1.142 |
| M1_raw_marginal | 0.6701 | 0.0300 | 0.166 | 0.276 | 3.5 | 0.0141 | 0.352 |
| M6_trend | 0.6471 | 0.0440 | 0.276 | 0.389 | 3.7 | 0.0118 | 0.697 |
| S_only_mahalanobis | 0.6388 | 0.0211 | 0.131 | 0.276 | 3.2 | n/a | n/a |
| M3_max_z | 0.6351 | 0.0203 | 0.124 | 0.237 | 3.4 | n/a | n/a |
| M2_z_marginal | 0.6171 | 0.0217 | 0.106 | 0.216 | 3.4 | 0.0221 | -0.035 |
| S_only_literal | 0.5885 | 0.0158 | 0.071 | 0.170 | 3.2 | n/a | n/a |
| M4_agg_z | 0.4054 | 0.0096 | 0.018 | 0.053 | 3.7 | 0.0223 | -0.400 |

### 10min

| model | AUROC | AUPRC | sens@5% FAR | sens@10% FAR | lead min | Brier | cal slope |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| M10b_M9_plus_Mahalanobis | 0.7913 | 0.1943 | 0.413 | 0.509 | 5.9 | 0.0249 | 0.928 |
| ABL_subject | 0.7896 | 0.1776 | 0.354 | 0.499 | 5.8 | 0.0255 | 0.845 |
| ABL_population | 0.7879 | 0.1800 | 0.362 | 0.484 | 5.8 | 0.0254 | 0.856 |
| M9_strong_marginal | 0.7870 | 0.1797 | 0.365 | 0.491 | 5.8 | 0.0254 | 0.853 |
| M10_M9_plus_S | 0.7868 | 0.1811 | 0.366 | 0.493 | 5.8 | 0.0253 | 0.857 |
| ABL_patient | 0.7868 | 0.1811 | 0.366 | 0.493 | 5.8 | 0.0253 | 0.857 |
| ABL_diagonal | 0.7865 | 0.1748 | 0.351 | 0.488 | 5.8 | 0.0256 | 0.832 |
| ABL_identity | 0.7858 | 0.1736 | 0.355 | 0.493 | 5.9 | 0.0256 | 0.836 |
| ABL_shuffled | 0.7849 | 0.1896 | 0.382 | 0.488 | 5.8 | 0.0252 | 0.894 |
| M11_marginal_plus_covdrift | 0.7816 | 0.1839 | 0.362 | 0.468 | 5.8 | 0.0253 | 0.836 |
| M8_marginal_LR | 0.7710 | 0.1565 | 0.366 | 0.437 | 5.7 | 0.0256 | 1.069 |
| M5_dispersion | 0.7443 | 0.1401 | 0.343 | 0.456 | 5.5 | 0.0263 | 0.863 |
| M7_cov_drift | 0.6760 | 0.0851 | 0.224 | 0.362 | 5.8 | 0.0263 | 1.108 |
| M6_trend | 0.6533 | 0.0847 | 0.249 | 0.360 | 5.9 | 0.0266 | 0.808 |
| M1_raw_marginal | 0.6460 | 0.0580 | 0.155 | 0.264 | 6.4 | 0.0329 | 0.296 |
| S_only_mahalanobis | 0.6221 | 0.0432 | 0.099 | 0.250 | 5.9 | n/a | n/a |
| M3_max_z | 0.6141 | 0.0409 | 0.108 | 0.193 | 5.7 | n/a | n/a |
| M2_z_marginal | 0.5908 | 0.0468 | 0.114 | 0.192 | 5.8 | 0.0373 | -0.067 |
| S_only_literal | 0.5724 | 0.0326 | 0.043 | 0.121 | 4.8 | n/a | n/a |
| M4_agg_z | 0.3924 | 0.0213 | 0.017 | 0.048 | 6.4 | 0.0371 | -1.495 |

### 15min

| model | AUROC | AUPRC | sens@5% FAR | sens@10% FAR | lead min | Brier | cal slope |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| ABL_diagonal | 0.7439 | 0.1693 | 0.263 | 0.383 | 7.1 | 0.0450 | 0.677 |
| ABL_population | 0.7423 | 0.1731 | 0.263 | 0.400 | 7.2 | 0.0448 | 0.651 |
| M10b_M9_plus_Mahalanobis | 0.7416 | 0.1764 | 0.267 | 0.401 | 7.3 | 0.0426 | 0.736 |
| ABL_subject | 0.7411 | 0.1709 | 0.264 | 0.390 | 7.1 | 0.0456 | 0.622 |
| M9_strong_marginal | 0.7404 | 0.1730 | 0.268 | 0.401 | 7.2 | 0.0448 | 0.646 |
| ABL_shuffled | 0.7391 | 0.1739 | 0.262 | 0.401 | 7.2 | 0.0439 | 0.679 |
| M10_M9_plus_S | 0.7363 | 0.1688 | 0.267 | 0.386 | 7.2 | 0.0451 | 0.637 |
| ABL_patient | 0.7363 | 0.1688 | 0.267 | 0.386 | 7.2 | 0.0451 | 0.637 |
| ABL_identity | 0.7363 | 0.1700 | 0.262 | 0.382 | 7.2 | 0.0462 | 0.582 |
| M11_marginal_plus_covdrift | 0.7347 | 0.1692 | 0.262 | 0.379 | 7.1 | 0.0446 | 0.648 |
| M8_marginal_LR | 0.7272 | 0.1488 | 0.257 | 0.359 | 7.1 | 0.0494 | 0.423 |
| M5_dispersion | 0.6907 | 0.1455 | 0.252 | 0.374 | 6.8 | 0.0416 | 0.934 |
| M6_trend | 0.6507 | 0.1139 | 0.208 | 0.314 | 7.8 | 0.0421 | 0.911 |
| M7_cov_drift | 0.6194 | 0.0972 | 0.163 | 0.282 | 6.8 | 0.0425 | 1.016 |
| M1_raw_marginal | 0.6171 | 0.0742 | 0.116 | 0.207 | 7.8 | 0.0480 | 0.292 |
| S_only_mahalanobis | 0.5972 | 0.0618 | 0.072 | 0.199 | 7.4 | n/a | n/a |
| M3_max_z | 0.5879 | 0.0587 | 0.080 | 0.162 | 7.0 | n/a | n/a |
| M2_z_marginal | 0.5650 | 0.0640 | 0.082 | 0.176 | 7.8 | 0.0536 | -0.134 |
| S_only_literal | 0.5546 | 0.0491 | 0.029 | 0.086 | 5.8 | n/a | n/a |
| M4_agg_z | 0.4097 | 0.0360 | 0.021 | 0.050 | 10.4 | 0.0531 | -2.034 |

## Ablations — which covariance is used in S

| horizon | patient | diagonal | identity | shuffled | subject | population |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **AUROC of M9+S** |||||||
| 5min | 0.8318 | 0.8322 | 0.8321 | 0.8310 | 0.8356 | 0.8322 |
| 10min | 0.7868 | 0.7865 | 0.7858 | 0.7849 | 0.7896 | 0.7879 |
| 15min | 0.7363 | 0.7439 | 0.7363 | 0.7391 | 0.7411 | 0.7423 |
| **AUROC of S alone** |||||||
| 5min | 0.5885 | 0.5662 | 0.6041 | 0.5997 | 0.6235 | 0.6524 |
| 10min | 0.5724 | 0.5421 | 0.5969 | 0.5954 | 0.5888 | 0.6053 |
| 15min | 0.5546 | 0.5233 | 0.5768 | 0.5770 | 0.5718 | 0.5770 |

## Surrogate — component permutation of δ against the same Σ₀

| horizon | real ΔAUPRC | surrogate mean | surrogate p95 | real above p95? |
|:--:|:--:|:--:|:--:|:--:|
| 5min | +0.00017 | -0.00116 | -0.00071 | yes |
| 10min | +0.00144 | -0.00140 | +0.00595 | no |
| 15min | -0.00425 | -0.00381 | -0.00307 | no |

## Frozen decision criteria

| # | criterion | 5min | 10min | 15min |
|:--:|---|:--:|:--:|:--:|
| 1 | ΔAUPRC > 0, CI excludes 0 | no | no | no |
| 2 | ΔAUROC > 0.01, CI excludes 0 | no | no | no |
| 3 | patient-specific beats diagonal and population | — | — | — |
| 4 | advantage destroyed by permutation | **yes** | no | no |
| 5 | no calibration penalty | **yes** | **yes** | no |
| 6 | no false-alert penalty | **yes** | **yes** | no |

**Status: NOT SUPPORTED**

© 2026 Davarn Morrison · Transition Dynamics
