# Derivation: what Λ = Σ₀⁻¹ actually predicts

This document separates, line by line, what is a **mathematical consequence** of
the frozen operator from what is an **additional physiological assumption**.

Nothing here restores the withdrawn falling-variance prediction, and nothing
here redefines Λ.

---

## 1. Setup

Take the standard linear description of a system fluctuating about a set point:

$$dx = -K\,(x - \mu_0)\,dt + \sqrt{2D}\,dW$$

with restoring operator $K$ and noise covariance $D$. For $D = \sigma^2 I$ and
symmetric $K$, the stationary covariance is

$$\Sigma_0 = \sigma^2 K^{-1} \qquad\Longrightarrow\qquad \Lambda = \Sigma_0^{-1} = \sigma^{-2} K$$

**Consequence 1 (mathematical).** Under the frozen operator, *stiffness* and
*low baseline variance* are the same thing. A direction has low baseline
variance exactly when its restoring rate is large. This is not an assumption;
it follows from the stationary solution.

---

## 2. Linear response contradicts the naive reading

A sustained force $f$ moves the equilibrium to

$$\delta = K^{-1} f$$

**Consequence 2 (mathematical).** Stiff directions displace **less** for equal
force, by precisely the factor that makes them stiff. The alignment statistic

$$A = \frac{\delta^{\mathsf T}\Sigma_0^{-1}\delta}{\lVert\delta\rVert^{2}\,\mathrm{tr}(\Sigma_0^{-1})/p}$$

therefore behaves as follows for $k$ spanning 0.05–1.6 over $p = 6$:

| condition | E[A] |
|---|:--:|
| stationary sampling null | 0.39 |
| sustained **isotropic** force, full equilibrium | 0.19 |
| force along the **stiffest** coordinate | 3.05 |
| force along the **softest** coordinate | 0.10 |

An untargeted sustained insult drives A *below* the stationary null, not above
it. Getting A above the null requires force targeted at stiff coordinates
strongly enough to overcome the $1/k$ attenuation.

**This is a stronger requirement than the premise as originally stated.** "Low
variance means defended, and pathology moves defended variables" is not
sufficient: the pathology must push hard enough on those variables to beat the
attenuation that being defended provides.

---

## 3. The exposure-duration confound

A step force acting for duration $T$ gives

$$\delta_i = \frac{f_i}{k_i}\left(1 - e^{-k_i T}\right)$$

- For $T \ll 1/k_i$: $\delta_i \approx f_i T$ — **independent of stiffness**.
- For $T \gg 1/k_i$: $\delta_i \to f_i / k_i$ — **fully attenuated by stiffness**.

**Consequence 3 (mathematical).** A is a monotone function of how long the
insult has acted relative to channel timescales, with **no targeting anywhere**:

| exposure $T$ | E[A], isotropic force | vs stationary null 0.39 |
|:--:|:--:|:--:|
| 0.02 | 1.00 | above |
| 0.10 | 0.96 | above |
| 0.50 | 0.83 | above |
| 2.0 | 0.54 | above |
| 10 | 0.28 | below |
| 50 | 0.20 | below |

### 3.1 Two consequences that damage the premise

**The licensing inference is invalid as stated.** A short-exposure *isotropic*
insult sits above the stationary null. So

> A above the null $\;\not\Rightarrow\;$ displacement along defended directions

unless exposure duration is controlled. The inference the premise depends on
does not hold.

**The preregistered class prediction is inverted.** Under untargeted forcing,
recent abrupt insults (short exposure) give **high** A and slowly developing
sepsis (long exposure) gives **low** A. The preregistration predicted the
opposite ordering — positive alignment in sepsis and respiratory classes, null
in the abrupt class. Any observed class pattern is therefore confounded with
insult kinetics before any physiology is invoked.

---

## 4. What is mathematical and what is assumed

| Statement | Status |
|---|---|
| Stiffness ≡ low baseline variance under $\Lambda = \Sigma_0^{-1}$ | **Mathematical consequence** |
| Stiff directions displace less for equal force | **Mathematical consequence** |
| Untargeted sustained insult gives A below the stationary null | **Mathematical consequence** |
| A decreases monotonically with exposure duration | **Mathematical consequence** |
| Low variance indicates active homeostatic defence | **Physiological assumption** — untested |
| Pathology targets defended coordinates | **Physiological assumption** — untested |
| The targeting is strong enough to beat $1/k$ attenuation | **Physiological assumption** — untested, and stronger than the premise as originally stated |
| Observed class differences reflect mechanism rather than kinetics | **Physiological assumption** — and now known to be confounded |

---

## 5. Competing explanations for low baseline variance

The premise attributes low baseline variance to homeostatic defence. At least
three alternatives produce the same signature and are not homeostatic:

| Alternative | Why it mimics defence |
|---|---|
| **Measurement quantisation** | A channel recorded to one decimal place has low variance because of the instrument, not the physiology |
| **Charting behaviour** | Repeated identical manual entries compress variance without any physiological stability |
| **Iatrogenic clamping** | A variable held at target by an active intervention has low baseline variance, then moves when the intervention fails — producing high alignment for a purely treatment-related reason |

The third is the most dangerous, because it produces exactly the predicted
signature in exactly the patients who deteriorate.

---

## 6. What this derivation does not do

It does not falsify the premise. Whether real insults are targeted strongly
enough, and whether observed alignment survives exposure matching, are
empirical questions requiring clinical data.

It does establish that **any** test of the premise must control exposure
duration and must exclude quantisation-limited and intervention-clamped
channels, and that a bare comparison of alignment against a stationary null
carries no mechanistic content.

---

© 2026 Davarn Morrison · Transition Dynamics
