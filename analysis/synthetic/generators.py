"""
generators.py — Synthetic transition mechanisms with KNOWN ground truth.

Why this file exists
--------------------
Real data cannot tell us whether an estimator has power, because we never know
the true mechanism. These generators create transitions whose mechanism is known
by construction, so that an estimator's blind spots are discovered here rather
than mistaken for biology later.

Five mechanisms. Only two of them are supposed to be detectable.

  fold        endogenous soft-mode instability. One restoring rate decays to
              zero. The system escapes along its HIGHEST-variance direction.
              -> critical slowing down SHOULD appear.  A(t) should fall below 1.

  yield       exogenous forcing along a homeostatically DEFENDED direction.
              Restoring rates constant; an external drift pushes a tightly
              regulated (low-variance) coordinate.
              -> no slowing down.  A(t) should rise above 1.

  noise       constant dynamics, a single large shock crosses a separatrix.
              -> NOTHING should be detectable. This is a real transition with
                 no precursor, and any estimator that "predicts" it is leaking.

  rate        parameters move faster than the system can track (rate-induced
              tipping). Classical early-warning theory does not apply.

  null        stationary. No transition. Must produce no signal anywhere.

IMPORTANT HONESTY NOTE
----------------------
The `yield` generator INSTANTIATES the homeostatic premise (that deterioration
displaces defended, low-variance variables). Running it demonstrates that the
A(t) statistic HAS POWER to detect such displacement. It is NOT evidence that
human physiology actually behaves this way. That premise is empirical and is
tested only on real data.

Run:  python3 analysis/synthetic/generators.py
"""

from __future__ import annotations

import numpy as np


def _restoring_rates(p: int) -> np.ndarray:
    """
    Geometric spread of restoring rates. Stationary variance is sigma^2/(2k),
    so small k is a soft, high-variance, weakly-regulated coordinate and large
    k is a stiff, low-variance, tightly-defended one.
    """
    return np.geomspace(0.05, 1.6, p)


def simulate(mechanism: str, T: int = 7000, p: int = 6, seed: int = 0,
             sigma: float = 0.30, dt: float = 0.02, thin: int = 40,
             onset_frac: float = 0.60) -> dict:
    """
    RESOLUTION REQUIREMENT (learned the hard way — see docs/LIMITATIONS.md).
    The integrator step must be fine enough for stability but the OUTPUT must
    be thinned, or consecutive samples are ~99.9% autocorrelated and an
    800-sample window carries an effective sample size of about 4. Covariance
    is then unestimable and every downstream statistic is noise.

    Quantitative requirement, derived rather than guessed: for a covariance
    over p channels to be estimable, the window must satisfy roughly

        n_eff = n(1-rho)/(1+rho)  >=  10p

    With dt=0.02 and thin=40 the slowest mode (k=0.05, relaxation time 20) is
    sampled every 0.8 time units, and a 2500-sample window carries n_eff of
    order 100 for p=6. This is the synthetic analogue of the real constraint
    stated in docs/DATASET_REQUIREMENTS.md: an analysis window must span many
    relaxation times of the SLOWEST channel, not merely contain many samples.

    Returns dict with keys:
      X          (T, p) trajectory
      onset      index at which the driving change begins
      mechanism  echo of the argument
      truth      what an ideal detector could know
    """
    rng = np.random.default_rng(seed)
    k0 = _restoring_rates(p)
    onset = int(onset_frac * T)

    # Random orthonormal basis so no coordinate is privileged by construction.
    Q, _ = np.linalg.qr(rng.normal(0, 1, (p, p)))

    # EXACT Ornstein-Uhlenbeck transition over the observation interval,
    # rather than a fine Euler loop plus thinning. For constant restoring rate
    # k and drift b over an interval h:
    #
    #     y' = e^{-kh} y + (b/k)(1 - e^{-kh}) + N(0, sigma^2 (1-e^{-2kh})/(2k))
    #
    # This is exact, not an approximation. It also removes the discretisation
    # artefact that made the first version of this benchmark unusable, in
    # which consecutive samples were 99.9% autocorrelated and a window of 800
    # samples carried an effective sample size of about 4.
    h = dt * thin
    X = np.zeros((T, p))
    y = np.zeros(p)                      # state in the eigenbasis
    detectable = mechanism in ("fold", "yield")

    for t in range(T):
        k = k0.copy()
        drift = np.zeros(p)
        prog = max(0.0, (t - onset) / max(1, T - onset))

        if mechanism == "fold":
            # Softest coordinate loses its restoring force -> classic fold.
            k[0] = k0[0] * max(1e-3, 1.0 - 0.995 * prog)

        elif mechanism == "yield":
            # Restoring forces intact; an external insult drives the STIFFEST
            # (most tightly defended) coordinate away from setpoint.
            drift[-1] = 2.2 * prog * k0[-1]

        elif mechanism == "rate":
            # All rates swept quickly - faster than the system can track.
            k = k0 * max(1e-3, 1.0 - 0.9 * min(1.0, 6.0 * prog))

        elif mechanism == "noise":
            # Constant dynamics; one large shock, no precursor whatsoever.
            if t == onset:
                y = y + rng.normal(0, 9.0, p)

        decay = np.exp(-k * h)
        sd = sigma * np.sqrt((1.0 - decay ** 2) / (2.0 * k))
        y = decay * y + (drift / k) * (1.0 - decay) + rng.normal(0, 1, p) * sd
        X[t] = Q @ y

    return {
        "X": X,
        "onset": onset,
        "mechanism": mechanism,
        "basis": Q,
        "rates": k0,
        "detectable": detectable,
        "truth": {
            "fold":  "endogenous soft-mode; escape along HIGH-variance direction",
            "yield": "exogenous forcing along DEFENDED low-variance direction",
            "noise": "no precursor exists — detection here is leakage",
            "rate":  "rate-induced; classical early-warning theory inapplicable",
            "null":  "no transition",
        }[mechanism],
    }


MECHANISMS = ("null", "fold", "yield", "noise", "rate")


if __name__ == "__main__":
    print("Synthetic transition mechanisms\n" + "=" * 60)
    for m in MECHANISMS:
        r = simulate(m, seed=0)
        pre = r["X"][r["onset"] - 500:r["onset"]]
        post = r["X"][r["onset"]:r["onset"] + 500]
        print(f"{m:6s} onset={r['onset']:5d}  detectable={str(r['detectable']):5s}  "
              f"|mean shift|={np.linalg.norm(post.mean(0) - pre.mean(0)):.3f}")
        print(f"       {r['truth']}")
