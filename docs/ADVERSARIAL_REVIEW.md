<div align="center">

# ADVERSARIAL REVIEW

**Attacking the Revised Hypothesis · Ten Questions · One Grade**

![Mode](https://img.shields.io/badge/Mode-Self_Adversarial-b91c1c?style=flat-square)
![Grade](https://img.shields.io/badge/Revised_Grade-B-ca8a04?style=flat-square)
![Objective](https://img.shields.io/badge/Objective-Discover_If_False-1f2937?style=flat-square)

</div>

---

*"Find the smallest version of the claim that reality cannot currently kill. Then publish that, and nothing larger."*

*— Davarn Morrison, 2026*

---

## 1. What is genuinely novel?

**One thing, and it is narrow:**

> z(t) discriminates the **mechanism** that produced a deformation, at matched
> deformation **magnitude**, where covariance drift cannot.

Demonstrated on synthetic systems: at the magnitude-matched point, dG collapses
to AUC 0.56 while z holds at 1.00. The magnitude-invariance is structural — z
is normalised by ‖δ‖² — not a parameter choice.

Two lesser candidates: the **constrained-exponent test** of Q = ‖ΔG‖·τ, and
**β₁-excess against pairwise-matched Gaussian surrogates** as an operational
definition of "higher-order". Neither was located in prior work, but neither is
load-bearing.

**Novelty is claimed weakly.** Absence of located prior work is not evidence of
novelty, and the Dynamical Network Biomarker literature is large and
substantially non-English.

---

## 2. What is already established?

| Result | Owner | Consequence |
|---|---|---|
| Covariance structure deforms before conventional diagnosis | DNB, Chen/Aihara 2012 | C1 is **not novel** |
| Structural dynamics precede clinical signs, with a mortality RCT | HeRO, neonatal sepsis | The core question is already answered affirmatively in one domain |
| Multichannel coupling reconfigures with physiological state | Network Physiology, Bashan/Ivanov | The weak form of C5 |
| Critical slowing down as early warning | Scheffer and colleagues | M2 |
| Recovery rate as a resilience index | multiple, validated | M2's Λ_A |
| Persistent homology on physiological signals | multiple | Method not novel; deferred here by design |
| Deterioration models fail on base rate, not AUROC | Wong 2021, Epic Sepsis Model | The reference floor |

**"Multivariate beats univariate" is established and is not tested here as a
contribution.**

---

## 3. Which predictions are unique to Transition Dynamics?

1. **Sign of z by transition class** — positive in exogenous classes (T2, T3),
   null in abrupt (T6) — **at matched deformation magnitude**.
2. **A hazard knee** in ‖ΛΔG‖ with T_critical transferring across cohorts in χ²
   quantile units. Existing work models risk gradients, not separatrices.
3. **β₁ excess over pairwise-matched surrogates.**

Prediction 1 is the only one whose failure would leave nothing.

---

## 4. Which result would most strongly support it?

Mean z > 0 in T2/T3 with CI excluding zero, z ≈ 0 in T6, **at matched ‖ΔG‖**,
with ΔG failing the same discrimination — replicated by site, with M0 at
ACCEPTABLE leakage and M0 stratified by class.

Two conditions matter more than the effect: **matched magnitude** (otherwise
size masquerades as mechanism) and **class-stratified M0** (otherwise
monitoring differences masquerade as mechanism).

---

## 5. Which single experiment could most efficiently kill it?

> **THE KILL EXPERIMENT**
>
> HiRID. Stratify by transition class. Within strata matched on
> deformation magnitude ‖ΔG‖, compute mean z(t) per class with
> cluster-bootstrap CIs. Run M0 stratified by class first.
> KILLS IT:
> mean z CI includes 0 in all powered classes; OR
> signs do not track class; OR
> z is as large in T6 as in T2/T3; OR
> class-stratified M0 reproduces the class pattern.

One retrospective analysis on existing public data. No new collection. It tests
C6 directly — and C1–C5 can all pass without C6, leaving a replication of 2012
methods.

---

## 6. Which confound is most dangerous?

**Class-correlated acquisition behaviour.**

Sepsis patients are monitored differently from arrest patients — different
channels, different frequencies, different lab cadence. That difference is
correlated with transition class **by construction**. It could manufacture
precisely the class-specific z pattern that would otherwise be the headline
result.

This is more dangerous than plain acquisition leakage because the overall M0
gate can pass while the class-specific pattern is entirely procedural. Hence the
preregistered requirement that **M0 is stratified by class, not merely run once
overall**.

Runner-up: **instrument quantisation masquerading as homeostatic defence.** A
channel may have low baseline variance because it is coarsely measured, not
because it is defended — which would corrupt the Σ₀⁻¹ spectrum that A depends
on entirely.

---

## 7. Which equation is weakest?

**Q = ‖ΔG‖·τ.** τ is defined by a threshold on ‖ΔG‖, so Q is a deterministic
function of ‖ΔG‖ and one tuning constant. The claim required reformulation as a
constrained-exponent test — and **that reformulation is ours, not the
framework's**. The product form is also a rectangle approximation to ∫‖ΔG‖dt,
which is the functional the physical story actually describes.

Weakest *premise*, as distinct from equation: the **homeostatic premise**. A(t)
is geometry; the directional prediction needs the separate empirical claim that
low normal variance indicates active defence. That premise is untested and
carries the whole of C6.

---

## 8. Which equation is strongest?

**‖ΛΔG‖ > T_critical**, under the frozen Λ.

It is coherent as written with no rearrangement; the precision matrix is the
Hessian of the Gaussian potential, so "stiffness" is construction rather than
analogy; the quadratic form is a standard, cheap, well-conditioned Mahalanobis
distance; and the χ² formulation makes T_critical transferable across cohorts
with different channel counts. It also generates the only prediction here that
existing literature does not make — a hazard **knee** rather than a gradient.

---

## 9. What remains analogy rather than demonstrated mechanism?

| Item | Status |
|---|---|
| "Stiffness", "yield", "stress" | **Analogy with a rigorous anchor.** Σ₀⁻¹ genuinely is the Hessian of the Gaussian potential. But physiological systems are not Hookean solids, and nothing establishes that deterioration is a yield process |
| T_critical as a **separatrix** | **Pure analogy until C4 passes.** A fitted knee in a hazard function is not a demonstrated basin boundary |
| "Irreversibility" | **Analogy.** Nothing in the protocol measures irreversibility. It measures association with a subsequent event |
| The homeostatic premise | **Untested hypothesis**, not mechanism |
| Reach, homology, topology of futures | **Not measured at all.** Demoted |
| "Deformation energy" | Dimensionally coherent, but calling a Mahalanobis distance an energy is an interpretive overlay, not a measured quantity |

**The mechanistic vocabulary runs well ahead of the mechanistic evidence.** The
equations are coherent; that they describe the actual physical process is
assumed throughout and demonstrated nowhere.

---

## 10. What is required before discussing clinical deployment?

All of, in order:

```
  1  Claim Ladder Level 5 — replication across datasets and classes
  2  M0 at ACCEPTABLE, stratified by class
  3  Base-rate utility gate at the setting's true prevalence:
       PPV ≥ 0.20, ≤ 1 false alert per patient per horizon,
       median lead ≥ 2 h, calibration slope in [0.8, 1.25]
  4  Prospective validation — Level 6
  5  Demonstrated benefit, not merely demonstrated discrimination
```

Nothing below Level 5 licenses any deployment discussion. The current position
is **Level 0**.

---

## Grade

> B — COHERENT BUT REQUIRES BETTER OPERATIONALISATION

**Unchanged from v1 in letter, substantially improved in substance.**

### Why not A

A requires "coherent, operationalised **and strongly falsifiable**". Three
things block it:

1. **The load-bearing claim rests on an untested premise.** C6 needs the
   homeostatic premise, which is physiological, plausible, and unexamined. The
   equation supplies geometry; the premise supplies the direction.
2. **The primary statistic has a demonstrated blind spot and weak power.** z
   fails on the fold mechanism (AUC 0.30) and its null band is wide at
   realistic channel counts — a cohort discriminator, not a bedside alarm.
3. **No real data has been touched.** Falsifiability has been *designed*; it
   has not been *exercised*. The kill experiment exists on paper.

### Why not C

C would mean major theoretical ambiguity remains. It does not. Λ is frozen with
an argument for why that reading and not the other; the decision rule is fixed
against an empirical null; the directional predictions are stated per class in
advance; and §5 specifies a single retrospective experiment on existing public
data that ends the primary claim. The ambiguity that made v1 arguable —
*which Λ?* — has been removed by commitment rather than by hedging.

### Why not D

D would mean key claims currently fail. Two objects did fail and were demoted;
the rest survive with declared substitutions. The v1 variance prediction failed
and was withdrawn rather than repaired. That is the demotion machinery working,
not the framework collapsing.

### Why not F

Nothing here is internally inconsistent or non-testable **after** the
demotions. The inconsistencies v1 identified — group subtraction, the sign
conflict between the resilience gloss and the multiplicative criterion, the
τ symbol collision — are resolved or quarantined, in writing.

### What would move it to A

```
  1  A real-data test of the homeostatic premise: do deteriorating
     patients displace along low-baseline-variance channels?
  2  Demonstration that z retains power at realistic ICU channel
     counts, or explicit restriction of the claim to cohort level
  3  The kill experiment run, with M0 stratified by class
```

Item 1 alone would settle most of it. It is a small analysis and it is the
next thing that should happen.

---

## The Honest Summary

> **Detection is not the contribution — covariance drift, published**
>
> in 2012, already achieves AUC 1.00 on every mechanism this
> framework can detect.
> What may be new is that the DIRECTION of constrained deformation
> identifies WHICH mechanism produced it, independently of size.
> That claim rests on one untested physiological premise, fails on
> one of the two detectable mechanisms, and has never touched real
> data.
> It is small, it is sharp, and it can be killed by a single
> retrospective analysis of a public dataset.

That is the smallest version of Transition Dynamics that reality has not
already killed.

---

<div align="center">

> **The mechanistic vocabulary runs ahead of the evidence.**
>
> The equations are coherent. That they describe the physical
> process is assumed throughout and demonstrated nowhere.

---

## Related Work

- [`../README.md`](../README.md) · [`LIMITATIONS.md`](LIMITATIONS.md) · [`PREREGISTRATION.md`](PREREGISTRATION.md) · [`FALSIFICATION_CRITERIA.md`](FALSIFICATION_CRITERIA.md)

---

© 2026 Davarn Morrison · Transition Dynamics · Adversarial Review
