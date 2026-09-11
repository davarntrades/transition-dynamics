# Real ICU data — Stage A under the frozen protocol

Applies `docs/PROTOCOL_MODEL_ADEQUACY.md` Stage A unchanged. No threshold altered.


**Provenance.** MIMIC-III Clinical Database Demo, open access under ODbL, obtained from the public `MIT-LCP/mimic-workshop` repository. No credentialed data, no access control bypassed.


Stays with 4 channels (HR, SpO₂, RR, MAP) and ≥ 6 h: **11**. Median charting gap **60 min**.


## Baseline-length trade-off


Longer baselines raise effective sample size but are less likely to be stationary. A recording is admissible only if some window satisfies **both**.


| stay | hours | baseline | n | n_eff | need | max shift (SD) | both OK |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 264854 | 367 | 12h | 12 | 11.5 | 40 | 2.17 | no |
| 264854 | 367 | 24h | 24 | 17.7 | 40 | 1.40 | no |
| 264854 | 367 | 48h | 48 | 32.8 | 40 | 0.58 | no |
| 264854 | 367 | 96h | 96 | 47.5 | 40 | 0.90 | no |
| 264854 | 367 | 168h | 168 | 49.2 | 40 | 0.94 | no |
| 271730 | 312 | 12h | 12 | 7.9 | 40 | 1.86 | no |
| 271730 | 312 | 24h | 24 | 11.6 | 40 | 1.94 | no |
| 271730 | 312 | 48h | 48 | 13.1 | 40 | 2.07 | no |
| 271730 | 312 | 96h | 96 | 30.5 | 40 | 1.01 | no |
| 271730 | 312 | 168h | 168 | 41.9 | 40 | 1.05 | no |
| 283260 | 252 | 12h | 12 | 6.8 | 40 | 1.94 | no |
| 283260 | 252 | 24h | 24 | 12.7 | 40 | 0.74 | no |
| 283260 | 252 | 48h | 48 | 16.7 | 40 | 1.54 | no |
| 283260 | 252 | 96h | 96 | 25.6 | 40 | 1.58 | no |
| 283260 | 252 | 168h | 168 | 42.9 | 40 | 1.36 | no |
| 232646 | 160 | 12h | 12 | 11.9 | 40 | 1.42 | no |
| 232646 | 160 | 24h | 24 | 6.2 | 40 | 2.07 | no |
| 232646 | 160 | 48h | 48 | 21.0 | 40 | 1.57 | no |
| 232646 | 160 | 96h | 96 | 33.6 | 40 | 1.47 | no |
| 232646 | 160 | 168h | 155 | 31.8 | 40 | 1.51 | no |
| 252522 | 115 | 12h | 12 | 13.2 | 40 | 0.82 | no |
| 252522 | 115 | 24h | 24 | 14.4 | 40 | 2.05 | no |
| 252522 | 115 | 48h | 48 | 18.6 | 40 | 2.21 | no |
| 252522 | 115 | 96h | 96 | 39.0 | 40 | 1.18 | no |
| 252522 | 115 | 168h | 115 | 36.2 | 40 | 1.30 | no |
| 264630 | 96 | 12h | 12 | 6.4 | 40 | 2.12 | no |
| 264630 | 96 | 24h | 24 | 12.8 | 40 | 0.78 | no |
| 264630 | 96 | 48h | 48 | 21.9 | 40 | 1.51 | no |
| 264630 | 96 | 96h | 96 | 26.3 | 40 | 1.95 | no |
| 264630 | 96 | 168h | 97 | 42.9 | 40 | 1.91 | no |
| 256307 | 93 | 12h | 12 | 9.5 | 40 | 1.19 | no |
| 256307 | 93 | 24h | 24 | 12.7 | 40 | 1.71 | no |
| 256307 | 93 | 48h | 48 | 23.4 | 40 | 1.02 | no |
| 256307 | 93 | 96h | 93 | 28.7 | 40 | 1.46 | no |
| 256307 | 93 | 168h | 93 | 28.7 | 40 | 1.46 | no |
| 269173 | 86 | 12h | 12 | 8.3 | 40 | 1.75 | no |
| 269173 | 86 | 24h | 24 | 14.7 | 40 | 1.11 | no |
| 269173 | 86 | 48h | 48 | 22.8 | 40 | 0.41 | no |
| 269173 | 86 | 96h | 87 | 25.9 | 40 | 1.41 | no |
| 269173 | 86 | 168h | 87 | 25.9 | 40 | 1.41 | no |
| 245649 | 61 | 12h | 12 | 6.0 | 40 | 1.05 | no |
| 245649 | 61 | 24h | 24 | 8.6 | 40 | 0.70 | no |
| 245649 | 61 | 48h | 48 | 21.4 | 40 | 0.76 | no |
| 245649 | 61 | 96h | 58 | 24.4 | 40 | 1.10 | no |
| 245649 | 61 | 168h | 58 | 24.4 | 40 | 1.10 | no |
| 279554 | 55 | 12h | 12 | 7.6 | 40 | 1.50 | no |
| 279554 | 55 | 24h | 24 | 6.8 | 40 | 1.84 | no |
| 279554 | 55 | 48h | 48 | 9.8 | 40 | 1.73 | no |
| 279554 | 55 | 96h | 55 | 12.3 | 40 | 1.92 | no |
| 279554 | 55 | 168h | 55 | 12.3 | 40 | 1.92 | no |
| 285485 | 16 | 12h | 12 | 6.0 | 40 | 2.15 | no |
| 285485 | 16 | 24h | 16 | 9.1 | 40 | 0.78 | no |
| 285485 | 16 | 48h | 16 | 9.1 | 40 | 0.78 | no |
| 285485 | 16 | 96h | 16 | 9.1 | 40 | 0.78 | no |
| 285485 | 16 | 168h | 16 | 9.1 | 40 | 0.78 | no |

## Verdict


- stay × baseline-window combinations evaluated: **55**

- combinations satisfying both rules: **0**

- admissible recordings: **0 / 11** (protocol requires 50)


**Stage B and Stage C are not run.**


The two frozen requirements are jointly unsatisfiable at hourly charting resolution. Short baselines fail the effective-sample-size rule; baselines long enough to pass it are no longer stationary, because real ICU patients drift over multi-day windows.


This does **not** falsify the exponential-approach model. It shows that hourly-charted ICU databases cannot supply the data the test requires. The model remains untested on real physiology.
