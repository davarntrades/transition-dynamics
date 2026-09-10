<div align="center">

# LITERATURE COMPARISON

**What Is Already Known · What Is Adjacent · What May Be New**

![Standard](https://img.shields.io/badge/Standard-Novelty_Claimed_Weakly-1f2937?style=flat-square)
![Rule](https://img.shields.io/badge/Rule-Absence_of_Prior_Work_≠_Novelty-b91c1c?style=flat-square)
![Section](https://img.shields.io/badge/Includes-Adversarial_Findings-4c1d95?style=flat-square)
![Patent](https://img.shields.io/badge/Patent-GB2600765.8-0075ca?style=flat-square)
![Rights](https://img.shields.io/badge/©-Davarn_Morrison-555555?style=flat-square)

</div>

---

*"A field that only reads the papers agreeing with it has not read the literature. It has read a mirror."*

*— Davarn Morrison, 2026*

---

## 0. Read This First — The Three Results That Threaten the Framework

These are placed before the supporting literature deliberately.

╔══════════════════════════════════════════════════════════════════════╗
║  THREAT 1 — THE PROTOTYPICAL TRANSITION SHOWS NO PRECURSOR           ║
╚══════════════════════════════════════════════════════════════════════╝

Wilkat, Rings & Lehnertz, *Chaos* 29:091104 (2019) — "No evidence for critical
slowing down prior to human epileptic seizures." Long-term multichannel
recordings, **28 subjects, 105 seizures**, surrogate-controlled evaluation.
Variance and lag-1 autocorrelation showed **no** pre-seizure signature.

The human epileptic brain is the canonical example of a critical transition in
a person. The canonical early-warning signal is absent from it. If structural
deformation exists there, these standard estimators do not see it.

→ [arXiv:1908.08973](https://arxiv.org/abs/1908.08973) · [Chaos](https://pubs.aip.org/aip/cha/article-abstract/29/9/091104/341751/No-evidence-for-critical-slowing-down-prior-to)

╔══════════════════════════════════════════════════════════════════════╗
║  THREAT 2 — LITTLE SUPPORT IN CLINICAL PSYCHOLOGY                    ║
╚══════════════════════════════════════════════════════════════════════╝

*Nature Reviews Psychology* (2024) — "Slow down and be critical before using
early warning signals in psychopathology." The review finds **little support**
for early warning signals based on critical slowing down in clinical
psychology, and identifies floor effects, measurement error and measurement
non-invariance as undermining the positive findings.

This directly threatens H6's cohort and the psychiatric arm of the protocol.

→ [Nature Reviews Psychology](https://www.nature.com/articles/s44159-024-00369-y)

╔══════════════════════════════════════════════════════════════════════╗
║  THREAT 3 — EARLY WARNING SIGNALS ARE BIFURCATION-SPECIFIC           ║
╚══════════════════════════════════════════════════════════════════════╝

Critical slowing down is a property of **fold (saddle-node) bifurcations**,
which possess a gradient potential. Two other routes produce genuine
transitions with **no precursor whatsoever**:

```
  NOISE-INDUCED TIPPING   a stochastic excursion crosses the separatrix
                          before any bifurcation is reached
  RATE-INDUCED TIPPING    parameters move faster than the system can track
```

If human physiological deterioration is predominantly noise- or rate-induced,
this framework is not false — it is **detecting nothing that exists**.

→ This limitation is reproduced in [`../analysis/estimators.py`](../analysis/estimators.py): the
`noise` arm of the self-test shows ΔG, ‖ΛΔG‖ and ρ(A) all remaining at null
levels through a real transition.

---

## 1. ALREADY ESTABLISHED

Claims the framework makes that **belong to prior work** and may not be
presented as novel.

### 1.1 Critical slowing down as a generic early warning

Rising variance, lag-1 autocorrelation and cross-correlation precede critical
transitions across ecological, climatic and physiological systems (Scheffer and
colleagues). Multiple indices combined outperform any single index.

→ [Scheffer et al., early-warning review](https://pdodds.w3.uvm.edu/files/papers/others/2009/scheffer2009a.pdf) · [multivariate indices in haemodialysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11002238/)

### 1.2 Critical slowing down before mood transitions in humans

van de Leemput et al., *PNAS* 111 (2014) — elevated temporal autocorrelation,
variance, and inter-emotion correlation in auto-recorded emotion time series
relate to the probability of an upcoming shift between depressed and normal
states.

**This is the direct precedent for the alternative Λ_A reading**, and its
direction (variance ↑) is the one the preregistered primary reading contradicts.

→ [PNAS](https://www.pnas.org/doi/full/10.1073/pnas.1312114110)

### 1.3 Dynamical Network Biomarkers — covariance deformation as pre-disease signal

Chen, Liu, Aihara et al. (*Sci Rep* 2:342, 2012 onward). A small set of
strongly correlated variables carries early-warning signals of an impending
critical transition; DNB indicators are derived **from the sample covariance
matrix**, and distinguish a *pre-disease state* from a normal state.

```
════════════════════════════════════════════════════════════════════
  DNB ALREADY COVERS THE COVARIANCE-DEFORMATION CORE OF H1 AND H5.
  Novelty may not be claimed for "covariance structure changes
  before conventional diagnosis." That result is fourteen years old.
════════════════════════════════════════════════════════════════════
```

→ [Sci Rep 2:342](https://www.nature.com/articles/srep00342) · [Theory & applications review](https://pubmed.ncbi.nlm.nih.gov/34626720/) · [DNM selected by covariance](https://www.researchgate.net/publication/337206186_Early-warning_signals_using_dynamical_network_markers_selected_by_covariance)

### 1.4 Multichannel physiological network reconfiguration

Bashan, Bartsch, Kantelhardt, Havlin & Ivanov — *Network Physiology*. Networks
of physiological interactions among cerebral, cardiac, respiratory, ocular and
locomotor systems **reconfigure with physiological state**; distinct states show
distinct network topology. Time Delay Stability introduced as the coupling
estimator.

The weak form of H5 — "multichannel coupling structure carries state
information" — is established here.

→ [Nature Communications / lab summary](https://sites.google.com/site/labnetworkphysiology/research/network-physiology-mapping-interactions-between-physiologic-organ-systems) · [arXiv:1203.0242](https://arxiv.org/pdf/1203.0242) · [brain–body networks](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7890264/)

### 1.5 Structural dynamics precede conventional biomarkers — with a mortality RCT

The **HeRO** heart-rate-characteristics index: reduced heart-rate variability,
decelerations (sample asymmetry) and sample entropy. Changes **wax and wane
before clinical signs of sepsis**. In a randomised trial of **3,003 preterm very
low birth weight infants across 9 NICUs**, displaying the score reduced
sepsis-associated mortality from roughly **20% to 12%**.

```
════════════════════════════════════════════════════════════════════
  THE CORE RESEARCH QUESTION IS ALREADY ANSWERED AFFIRMATIVELY
  IN AT LEAST ONE DOMAIN.  H1 IN ITS GENERIC FORM IS NOT NOVEL.
════════════════════════════════════════════════════════════════════
```

HeRO is also **directional evidence for the primary Λ_B reading**: what precedes
neonatal sepsis is *reduced* variability — rigidification — not the variance
increase that critical slowing down predicts.

→ [Septicemia mortality reduction, *Pediatr Res*](https://www.nature.com/articles/pr2013136) · [ELBW follow-up](https://www.sciencedirect.com/science/article/abs/pii/S0378378221001183) · [complex equation review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11798831/)

### 1.6 Persistent homology on physiological time series

Established as a method for HRV, ECG, EMG and sleep-state classification.
Robust to noise; persistence statistics are usable features.

Using persistent homology on physiological signals is **not novel**. What would
be novel is a preregistered pre-transition prediction with a mechanistic
threshold — which is why topology is deferred in this protocol rather than led
with.

→ [PH for HRV, *PLOS One*](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0253851) · [PH + sleep–wake](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2021.637684/full) · [TDA for multivariate time series](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10669999/)

### 1.7 Deterioration models fail on base rate, not on AUROC

Wong et al., *JAMA Intern Med* (2021) — external validation of the Epic Sepsis
Model on **38,455 hospitalisations**: AUROC 0.63, sensitivity 0.33, specificity
0.83, **PPV 0.12**, while alerting on **18% of all hospitalised patients** and
missing 67% of sepsis cases.

This is the empirical floor. It is why [`../analysis/base_rates.py`](../analysis/base_rates.py)
exists and why AUROC is not the headline metric in this protocol.

→ [PubMed](https://pubmed.ncbi.nlm.nih.gov/34152373/) · [ED external validation](https://academic.oup.com/jamiaopen/article/7/4/ooae133/7900014)

### 1.8 Resilience as recovery rate after perturbation

Dynamic stimulus–response measures of recovery rate quantify resilience in
humans; slower recovery from small perturbations indicates loss of resilience.
Applied in geriatrics, standing balance, Trier Social Stress Test, affect
recovery in daily life, and continuous monitoring in acute COVID-19.

**This is the established operationalisation of Λ_A.** It exists, it is
validated, and it is the framework's competitor — not its confirmation.

→ [speed of affect recovery](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7027206/) · [dynamic resilience indicators in geriatrics](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6593159/) · [continuous monitoring, COVID-19](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11818652/)

### 1.9 Digital phenotyping — passive sensing plus EMA

Multimodal digital phenotyping integrating passive sensor data with active
self-report is established for depression, anxiety and schizophrenia
monitoring. Known field-level problems: heavy dependence on self-report,
non-standardised feature definitions, and conflicting results across studies.

→ [scoping review, self-report vs digital phenotyping](https://mhealth.jmir.org/2026/1/e70840/PDF) · [systematic review](https://dl.acm.org/doi/10.1016/j.artmed.2025.103094)

---

## 2. RELATED BUT NOT EQUIVALENT

| Prior work | What it does | How this framework differs |
|---|---|---|
| TDA of physiological signals | **Classification** of states (sleep stage, patient group) | Preregistered **pre-transition prediction** against a mechanistic threshold |
| Resilience/recovery indices | Λ_A as a standalone predictor | Λ as an **operator inside a yield criterion**, anisotropic, applied to ΔG |
| Attractor-landscape reachability in cell biology | Reachability computed **from models** (Firefront, Avatar, Boolean networks) | Reachability structure **estimated from human recordings** — and this framework concedes it cannot do so (Audit §1.1) |
| DNB | Covariance-derived pre-disease indicator | Adds the **persistence factor τ**, the **anisotropic Λ weighting**, and the **higher-order β₁** claim |
| Recurrence-network geometric EWS | Phase-space geometry as resilience-loss indicator | Closest existing relative to ΔG. Difference is the preregistered threshold and the Λ operator, not the geometry |
| Multivariate EWS index combination | Combined indices outperform single | Establishes that **integration helps**; does not test **higher-order** integration |

→ [Geometric resilience loss, recurrence networks](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9114511/) · [Estimating attractor reachability](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6137237/)

---

## 3. APPARENTLY NOVEL

Claimed **weakly and provisionally**.

| Claim | Why it appears new |
|---|---|
| **Constrained-exponent test of Q = ‖ΔG‖·τ** (H2) | No located work tests the *multiplicative form itself* as a constraint β₁ = β₂ against an unconstrained alternative and against the integral form |
| **Λ as rigidity inside a yield criterion, tested against the CSD direction** (H3, §4.1) | The two directions exist separately in the literature. No located work makes them compete on the same data with the sign preregistered |
| **β₁ of a co-deformation nerve complex as a predictor beyond all pairwise couplings** (H5) | TDA on physiology exists; the nerve-of-channel-deformations construction, tested specifically for higher-order gain over pairwise-complete models, was not located |
| **Preregistered signed structure/report decoupling as an early-warning signal in its own right** (H6) | Digital phenotyping treats self-report as ground truth or as a target. Treating the *divergence* as the signal, with a timing-only negative control, was not located |

```
════════════════════════════════════════════════════════════════════
  NOVELTY DISCIPLINE

  Absence of located prior work is NOT evidence of novelty.

  The DNB literature is large and substantially non-English. The
  covariance components of H1 and H5 are likely covered somewhere
  within it. This section is a hypothesis ABOUT THE LITERATURE and
  is itself subject to falsification by a competent librarian.

  No priority claim is made on the basis of this search.
════════════════════════════════════════════════════════════════════
```

---

## 4. UNKNOWN / REQUIRES TESTING

| Open question | Why it matters |
|---|---|
| **Is T_critical reproducible across individuals?** | The make-or-break unknown. If it transfers, it is genuinely new. If not, it is a per-person fitted parameter and the universality claim collapses to curve-fitting |
| **Does ΔG carry pre-transition signal at ~hourly EHR resolution?** | Determines whether the enormous MIMIC-style literature could ever have detected this, or whether resolution has been the binding constraint all along |
| **Is the Λ_B / Λ_A sign domain-dependent?** | HeRO says rigidification precedes neonatal sepsis. van de Leemput says destabilisation precedes mood transition. Both may be right in their own domain — which would mean **no universal law**, and would be the most interesting negative result available |
| **What fraction of human deterioration is fold- vs noise-induced?** | Determines the ceiling on any early-warning approach, this one included |
| **Does declining self-report compliance explain all measured decoupling?** | Decides whether H6 has any content |

---

## 5. Datasets

| Dataset | Resolution | Endpoint | Use here |
|---|---|---|---|
| **HiRID** | ~2 min, ~34,000 admissions, ~700 variables | Physiology-defined circulatory failure | **Primary cohort, H1–H5** |
| MIMIC-IV | ~hourly, irregular; nurse-charted | Sepsis / deterioration | **External validation only.** See README §8.1 |
| eICU | Coarser, multi-centre | Deterioration | Second external validation |
| MIMIC-IV-ECG / waveform subsets | High-frequency but limited coverage | — | Sensitivity analysis on resolution |
| **CrossCheck** | Daily EMA + passive sensing | Adjudicated psychotic relapse | **Primary for H6** |
| GLOBEM | Multi-year, repeated waves | Depression/anxiety scales | Generalisation testing for H6 |
| StudentLife | 10 weeks, EMA + sensing | Mental health scales | Short horizon limits transition capture |
| RADAR-MDD | Longitudinal, MDD-organised | Depression relapse | Secondary H6 cohort |

→ [HiRID v1.1.1](https://physionet.org/content/hirid/1.1.1/) · [Hyland et al., circulatory failure](https://arxiv.org/pdf/1904.07990) · [HiRID-ICU-Benchmark](https://arxiv.org/pdf/2111.08536) · [cross-dataset generalisation, StudentLife/CrossCheck](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0266516) · [GLOBEM](https://dl.acm.org/doi/10.1145/3569485)

```
════════════════════════════════════════════════════════════════════
  VERIFICATION CAVEAT

  PhysioNet was not directly reachable from the environment in
  which this document was assembled. Dataset specifications above
  are drawn from secondary sources and published descriptions.

  Every figure — record counts, sampling rates, variable coverage,
  endpoint definitions — MUST be re-verified against the dataset
  landing pages before the protocol is executed.
════════════════════════════════════════════════════════════════════
```

---

## 6. Net Position

```
┌──────────────────────────────────────────────────────────────────┐
│  H1 generic form           ALREADY ESTABLISHED (HeRO, DNB)       │
│  H5 weak form              ALREADY ESTABLISHED (Network Phys.)   │
│  H2 product-form test      APPARENTLY NOVEL                      │
│  H3 sign competition       APPARENTLY NOVEL                      │
│  H4 threshold transfer     UNKNOWN — the decisive test           │
│  H5 higher-order form      APPARENTLY NOVEL                      │
│  H6 decoupling             APPARENTLY NOVEL, severely confounded │
└──────────────────────────────────────────────────────────────────┘
```

The framework's defensible contribution is **not** that structure deforms before
biomarkers — that is known and has an RCT behind it. It is the conjunction of:
a preregistered sign for Λ that contradicts the dominant literature, a
threshold that is claimed to transfer between cohorts, and a higher-order
integration term that pairwise models cannot reproduce.

Those three, and only those three, are what this programme is entitled to test
for novelty.

---

<div align="center">

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   HeRO reduced sepsis mortality from 20% to 12% using reduced        ║
║   variability. van de Leemput predicted mood transitions using       ║
║   increased variability. Both are published. Both cannot be the      ║
║   general law.                                                       ║
║                                                                      ║
║                    GB2600765.8                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

**Transition Dynamics** · Morrison Framework™ · *Literature Comparison*

GB2600765.8 · GB2602013.1 · GB2602072.7 · GB26023332.5

© 2026 Davarn Morrison — Intelligence Invariant™ · All Rights Reserved

</div>

---

## Related Work

- [`../README.md`](../README.md) — Preregistration
- [`MATHEMATICAL-AUDIT.md`](MATHEMATICAL-AUDIT.md) — Adversarial audit
- [`PROTOCOL.md`](PROTOCOL.md) — Experimental protocol
- [`FALSIFICATION-MATRIX.md`](FALSIFICATION-MATRIX.md) — Kill conditions
