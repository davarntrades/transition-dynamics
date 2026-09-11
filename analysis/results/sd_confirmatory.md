# Structural displacement and prediction of deterioration — confirmatory result

Endpoint: intraoperative hypotension, `ART_MBP < 65 mmHg` for `>= 60 s`. Every window already containing hypotension is excluded, so this is prediction from a currently non-hypotensive state.

Usable cases **166** of 400 · excluded 234 ({'coverage': 135, 'hypotension in baseline': 98, 'error: FileNotFoundError': 1}) · evaluation windows **21590**

## Verdict

# NOT SUPPORTED

## Power

| horizon | windows | positives | prevalence | patients | with an event |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 5min | 21451 | 565 | 0.0263 | 166 | **103** |
| 10min | 21215 | 1167 | 0.0550 | 166 | **109** |
| 15min | 20880 | 1759 | 0.0842 | 166 | **110** |

## Primary comparison — M10 (M9 + S) vs M9 (marginals only)

Bonferroni 95% CI over three horizons, patient-level bootstrap, 2000 resamples of caseids.

| horizon | AUROC M9 | AUROC M10 | ΔAUROC [CI] | AUPRC M9 | AUPRC M10 | ΔAUPRC [CI] |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5min | 0.6904 | 0.6938 | **+0.0035** [-0.0029, +0.0104] | 0.0657 | 0.0652 | **-0.00047** [-0.00384, +0.00210] |
| 10min | 0.6467 | 0.6438 | **-0.0029** [-0.0158, +0.0100] | 0.1312 | 0.1272 | **-0.00391** [-0.01204, +0.00338] |
| 15min | 0.6165 | 0.6185 | **+0.0019** [-0.0107, +0.0153] | 0.1554 | 0.1615 | **+0.00637** [-0.00301, +0.02126] |

## All comparators

### 5min

| model | AUROC | AUPRC | sens@5% FAR | sens@10% FAR | lead min | Brier | cal slope |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| M10_M9_plus_S | 0.6938 | 0.0652 | 0.200 | 0.342 | 3.3 | 0.0343 | 0.116 |
| ABL_patient | 0.6938 | 0.0652 | 0.200 | 0.342 | 3.3 | 0.0343 | 0.116 |
| M10b_M9_plus_Mahalanobis | 0.6929 | 0.0650 | 0.209 | 0.335 | 3.3 | 0.0342 | 0.118 |
| ABL_population | 0.6922 | 0.0655 | 0.202 | 0.335 | 3.3 | 0.0343 | 0.114 |
| ABL_diagonal | 0.6916 | 0.0657 | 0.207 | 0.340 | 3.3 | 0.0342 | 0.116 |
| ABL_shuffled | 0.6905 | 0.0661 | 0.214 | 0.333 | 3.2 | 0.0342 | 0.117 |
| M9_strong_marginal | 0.6904 | 0.0657 | 0.212 | 0.335 | 3.2 | 0.0342 | 0.113 |
| M11_marginal_plus_covdrift | 0.6883 | 0.0669 | 0.214 | 0.329 | 3.2 | 0.0336 | 0.110 |
| ABL_subject | 0.6876 | 0.0669 | 0.212 | 0.327 | 3.3 | 0.0342 | 0.113 |
| ABL_identity | 0.6870 | 0.0659 | 0.212 | 0.320 | 3.3 | 0.0337 | 0.110 |
| M8_marginal_LR | 0.6745 | 0.0647 | 0.205 | 0.303 | 3.1 | 0.0255 | 0.879 |
| M5_dispersion | 0.6457 | 0.0764 | 0.225 | 0.308 | 3.4 | 0.0252 | 0.994 |
| M1_raw_marginal | 0.6294 | 0.0422 | 0.099 | 0.175 | 3.7 | 0.0285 | 0.302 |
| M7_cov_drift | 0.6008 | 0.0523 | 0.143 | 0.216 | 3.2 | 0.0255 | 0.753 |
| M4_agg_z | 0.5866 | 0.0370 | 0.078 | 0.168 | 3.4 | 0.0307 | 0.077 |
| M6_trend | 0.5828 | 0.0475 | 0.147 | 0.237 | 3.3 | 0.0256 | 0.656 |
| S_only_mahalanobis | 0.5702 | 0.0355 | 0.092 | 0.196 | 3.3 | n/a | n/a |
| M3_max_z | 0.5685 | 0.0340 | 0.085 | 0.147 | 3.0 | n/a | n/a |
| M2_z_marginal | 0.5484 | 0.0319 | 0.081 | 0.159 | 3.3 | 0.0332 | 0.086 |
| S_only_literal | 0.5447 | 0.0324 | 0.081 | 0.170 | 3.4 | n/a | n/a |

### 10min

| model | AUROC | AUPRC | sens@5% FAR | sens@10% FAR | lead min | Brier | cal slope |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| ABL_population | 0.6469 | 0.1307 | 0.200 | 0.309 | 5.4 | 0.0586 | 0.136 |
| M9_strong_marginal | 0.6467 | 0.1312 | 0.199 | 0.310 | 5.3 | 0.0585 | 0.136 |
| M10b_M9_plus_Mahalanobis | 0.6454 | 0.1278 | 0.193 | 0.294 | 5.2 | 0.0586 | 0.132 |
| ABL_shuffled | 0.6450 | 0.1323 | 0.199 | 0.314 | 5.2 | 0.0585 | 0.143 |
| ABL_diagonal | 0.6449 | 0.1306 | 0.199 | 0.314 | 5.3 | 0.0585 | 0.137 |
| M10_M9_plus_S | 0.6438 | 0.1272 | 0.199 | 0.295 | 5.2 | 0.0586 | 0.127 |
| ABL_patient | 0.6438 | 0.1272 | 0.199 | 0.295 | 5.2 | 0.0586 | 0.127 |
| ABL_subject | 0.6417 | 0.1261 | 0.202 | 0.298 | 5.4 | 0.0589 | 0.126 |
| M11_marginal_plus_covdrift | 0.6391 | 0.1270 | 0.203 | 0.301 | 5.4 | 0.0587 | 0.131 |
| ABL_identity | 0.6369 | 0.1208 | 0.203 | 0.275 | 5.1 | 0.0581 | 0.112 |
| M5_dispersion | 0.6289 | 0.1319 | 0.192 | 0.268 | 5.4 | 0.0505 | 0.919 |
| M8_marginal_LR | 0.6215 | 0.1177 | 0.208 | 0.274 | 5.5 | 0.0546 | 0.538 |
| M7_cov_drift | 0.6016 | 0.0939 | 0.130 | 0.213 | 5.8 | 0.0516 | 0.904 |
| M1_raw_marginal | 0.5937 | 0.0783 | 0.104 | 0.172 | 5.7 | 0.0563 | 0.264 |
| M4_agg_z | 0.5654 | 0.0697 | 0.070 | 0.147 | 5.5 | 0.0577 | 0.057 |
| S_only_mahalanobis | 0.5567 | 0.0693 | 0.082 | 0.182 | 5.7 | n/a | n/a |
| M6_trend | 0.5511 | 0.1006 | 0.161 | 0.239 | 6.0 | 0.0517 | 0.805 |
| M3_max_z | 0.5485 | 0.0658 | 0.080 | 0.147 | 5.7 | n/a | n/a |
| S_only_literal | 0.5371 | 0.0630 | 0.070 | 0.145 | 5.1 | n/a | n/a |
| M2_z_marginal | 0.5345 | 0.0612 | 0.060 | 0.123 | 5.5 | 0.0592 | 0.058 |

### 15min

| model | AUROC | AUPRC | sens@5% FAR | sens@10% FAR | lead min | Brier | cal slope |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| M10_M9_plus_S | 0.6185 | 0.1615 | 0.173 | 0.239 | 6.9 | 0.0824 | 0.085 |
| ABL_patient | 0.6185 | 0.1615 | 0.173 | 0.239 | 6.9 | 0.0824 | 0.085 |
| ABL_diagonal | 0.6173 | 0.1616 | 0.177 | 0.240 | 6.9 | 0.0824 | 0.084 |
| M10b_M9_plus_Mahalanobis | 0.6168 | 0.1552 | 0.167 | 0.236 | 7.0 | 0.0815 | 0.090 |
| ABL_subject | 0.6168 | 0.1566 | 0.172 | 0.239 | 7.0 | 0.0815 | 0.084 |
| M11_marginal_plus_covdrift | 0.6167 | 0.1558 | 0.169 | 0.235 | 7.0 | 0.0815 | 0.086 |
| ABL_identity | 0.6166 | 0.1574 | 0.176 | 0.236 | 6.9 | 0.0814 | 0.082 |
| M9_strong_marginal | 0.6165 | 0.1554 | 0.172 | 0.234 | 7.0 | 0.0815 | 0.084 |
| ABL_population | 0.6158 | 0.1548 | 0.172 | 0.234 | 7.0 | 0.0815 | 0.084 |
| ABL_shuffled | 0.6152 | 0.1553 | 0.172 | 0.233 | 7.0 | 0.0815 | 0.088 |
| M8_marginal_LR | 0.6006 | 0.1525 | 0.177 | 0.242 | 7.1 | 0.0812 | 0.299 |
| M5_dispersion | 0.5980 | 0.1541 | 0.151 | 0.224 | 6.7 | 0.0753 | 1.030 |
| M7_cov_drift | 0.5777 | 0.1208 | 0.103 | 0.181 | 7.1 | 0.0767 | 0.883 |
| M1_raw_marginal | 0.5679 | 0.1072 | 0.088 | 0.151 | 7.5 | 0.0809 | 0.263 |
| M6_trend | 0.5574 | 0.1397 | 0.153 | 0.221 | 7.8 | 0.0765 | 0.891 |
| M4_agg_z | 0.5522 | 0.1002 | 0.066 | 0.135 | 7.1 | 0.0818 | 0.103 |
| S_only_mahalanobis | 0.5495 | 0.1014 | 0.074 | 0.161 | 7.0 | n/a | n/a |
| M3_max_z | 0.5402 | 0.0967 | 0.074 | 0.135 | 7.6 | n/a | n/a |
| S_only_literal | 0.5349 | 0.0943 | 0.068 | 0.131 | 7.0 | n/a | n/a |
| M2_z_marginal | 0.5114 | 0.0847 | 0.050 | 0.090 | 7.4 | 0.0838 | 0.058 |

## Ablations — which covariance is used in S

| horizon | patient | diagonal | identity | shuffled | subject | population |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **AUROC of M9+S** |||||||
| 5min | 0.6938 | 0.6916 | 0.6870 | 0.6905 | 0.6876 | 0.6922 |
| 10min | 0.6438 | 0.6449 | 0.6369 | 0.6450 | 0.6417 | 0.6469 |
| 15min | 0.6185 | 0.6173 | 0.6166 | 0.6152 | 0.6168 | 0.6158 |
| **AUROC of S alone** |||||||
| 5min | 0.5447 | 0.5385 | 0.5436 | 0.5558 | 0.5579 | 0.5921 |
| 10min | 0.5371 | 0.5213 | 0.5350 | 0.5446 | 0.5365 | 0.5567 |
| 15min | 0.5349 | 0.5175 | 0.5265 | 0.5353 | 0.5263 | 0.5391 |

### Criterion 3 — patient-specific vs diagonal and population

| horizon | ΔAUROC patient − diagonal | ΔAUROC patient − population |
|:--:|:--:|:--:|
| 5min | +0.00227 [-0.00358, +0.00833] | +0.00164 [-0.00380, +0.00750] |
| 10min | -0.00110 [-0.01158, +0.00930] | -0.00309 [-0.01344, +0.00658] |
| 15min | +0.00120 [-0.00122, +0.00400] | +0.00258 [-0.00792, +0.01348] |

## Surrogate — component permutation of δ against the same Σ₀

| horizon | real ΔAUPRC | surrogate mean | surrogate p95 | real above p95? |
|:--:|:--:|:--:|:--:|:--:|
| 5min | -0.00044 | -0.00202 | -0.00179 | yes |
| 10min | -0.00392 | -0.01170 | -0.01116 | yes |
| 15min | +0.00618 | -0.00065 | -0.00008 | yes |

## Frozen decision criteria

| # | criterion | 5min | 10min | 15min |
|:--:|---|:--:|:--:|:--:|
| 1 | ΔAUPRC > 0, CI excludes 0 | no | no | no |
| 2 | ΔAUROC > 0.01, CI excludes 0 | no | no | no |
| 3 | patient-specific beats diagonal and population | no | no | no |
| 4 | advantage destroyed by permutation | **yes** | **yes** | **yes** |
| 5 | no calibration penalty | no | no | no |
| 6 | no false-alert penalty | **yes** | no | **yes** |

**Status: NOT SUPPORTED**

© 2026 Davarn Morrison · Transition Dynamics
