"""
stationarity_calibration.py — is the 0.5 SD stationarity screen statistically
appropriate for continuously sampled human physiology?

WHY THIS EXISTS
---------------
The screen rejected 100% of hourly ICU baselines. That could mean the data are
unusable, or that the screen is mis-specified. Loosening it after seeing that
result would be the forbidden move, so the question is settled here using
(a) simulation, where the truth is known by construction, and (b) the
CALIBRATION subset only. The confirmatory cohort is not touched.

THE STATISTICAL POINT
---------------------
The screen compares the mean of the first third of a window against the last
third, in units of the window's own SD:

    shift = |mean(first third) - mean(last third)| / SD

Under a STATIONARY but autocorrelated process this quantity is NOT small. The
difference of two third-window means has standard deviation

    SD * sqrt(2 / n_eff_third)

so the expected shift grows as the effective sample size falls. A fixed 0.5
threshold therefore does not test stationarity: it tests effective sample size,
and rejects short or strongly autocorrelated windows regardless of whether
anything is drifting.

A threshold that does test stationarity must scale with n_eff, which is what
this module measures and what any amendment must justify.

Distinguished throughout:
  genuine nonstationarity  a real change in the generating mean
  ordinary variability     stationary fluctuation about a fixed mean
  autocorrelation          inflates the apparent shift without any drift
  measurement noise        deflates SD-standardised shift
  intervention effects     genuine, but exogenous
  slow drift               genuine nonstationarity at long timescales
  missingness / artifact   distorts both mean and SD

Run:  python3 analysis/adequacy/stationarity_calibration.py
"""
from __future__ import annotations
import os, sys
import numpy as np

_HERE = os.path.dirname(__file__)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, ".."))
from adequacy import n_eff                                   # noqa: E402


def shift_stat(X):
    """The preregistered screen statistic, per channel, max over channels."""
    X = np.asarray(X, float)
    third = max(2, len(X) // 3)
    return float(np.max(np.abs(X[:third].mean(0) - X[-third:].mean(0))
                        / (X.std(0) + 1e-12)))


def ou(n, rho, seed, p=4):
    """Stationary AR(1): no drift whatsoever, by construction."""
    rng = np.random.default_rng(seed)
    e = rng.normal(0, 1, (n, p))
    X = np.empty((n, p))
    X[0] = e[0]
    for t in range(1, n):
        X[t] = rho * X[t - 1] + np.sqrt(1 - rho ** 2) * e[t]
    return X


def ou_drift(n, rho, seed, drift_sd, p=4):
    """Same process plus a genuine linear drift of `drift_sd` SD end-to-end."""
    X = ou(n, rho, seed, p)
    t = np.linspace(0, 1, n)[:, None]
    return X + drift_sd * t


def main() -> str:
    out, w = [], lambda s: out.append(s)
    w("# Is the 0.5 SD stationarity screen appropriate?\n")
    w("Decided on simulation and the calibration subset. The confirmatory "
      "cohort is not examined.\n")

    w("\n## 1. The screen on data that is stationary BY CONSTRUCTION\n")
    w("\nAR(1) with no drift at all. Any rejection here is a false positive.\n")
    w("\n| n | lag-1 ρ | n_eff | median shift | 95th pct | rejected at 0.5 |")
    w("|:--:|:--:|:--:|:--:|:--:|:--:|")
    rows = []
    for n, rho in ((48, 0.85), (96, 0.85), (168, 0.85),
                   (500, 0.95), (2000, 0.98), (10800, 0.995)):
        s = np.array([shift_stat(ou(n, rho, i)) for i in range(200)])
        ne = np.mean([n_eff(ou(n, rho, i)) for i in range(30)])
        rows.append((n, rho, ne, np.median(s), np.quantile(s, .95),
                     (s > 0.5).mean()))
        w(f"| {n} | {rho} | {ne:.0f} | {np.median(s):.2f} | "
          f"{np.quantile(s,.95):.2f} | **{(s>0.5).mean():.0%}** |")
    w("\nThe false-positive rate is driven by effective sample size, not by "
      "drift. A fixed threshold rejects stationary data whenever n_eff is "
      "small, which is exactly the regime hourly ICU baselines sit in.\n")

    w("\n## 2. The screen's null scales as 1/sqrt(n_eff)\n")
    w("\nThe difference of two third-window means has SD "
      "`SD*sqrt(2/n_eff_third)`, so the expected shift under stationarity "
      "falls with n_eff. Observed against predicted:\n")
    w("\n| n_eff | observed median shift | predicted ~2/sqrt(n_eff/3) |")
    w("|:--:|:--:|:--:|")
    for n, rho, ne, med, q95, rej in rows:
        w(f"| {ne:.0f} | {med:.2f} | {2/np.sqrt(max(ne,1)/3):.2f} |")

    w("\n## 3. Can it detect genuine drift?\n")
    w("\nSame process plus a real linear drift. A useful screen should "
      "separate these from the stationary case.\n")
    w("\n| n | ρ | drift (SD) | median shift | flagged at 0.5 |")
    w("|:--:|:--:|:--:|:--:|:--:|")
    for n, rho in ((2000, 0.98),):
        for dsd in (0.0, 0.5, 1.0, 2.0, 4.0):
            s = np.array([shift_stat(ou_drift(n, rho, i, dsd))
                          for i in range(150)])
            w(f"| {n} | {rho} | {dsd} | {np.median(s):.2f} | "
              f"{(s>0.5).mean():.0%} |")

    w("\n## 4. A threshold that actually tests stationarity\n")
    w("\nStandardising the shift by its own null scale gives a quantity whose "
      "distribution does not depend on n_eff:\n")
    w("\n```\nz_shift = shift / (2 / sqrt(n_eff/3))\n```\n")
    w("\n| n | ρ | drift (SD) | median z_shift | flagged at z>2 |")
    w("|:--:|:--:|:--:|:--:|:--:|")
    for n, rho in ((96, 0.85), (2000, 0.98)):
        for dsd in (0.0, 1.0, 4.0):
            zs = []
            for i in range(120):
                X = ou_drift(n, rho, i, dsd)
                ne = max(n_eff(X), 3.0)
                zs.append(shift_stat(X) / (2 / np.sqrt(ne / 3)))
            zs = np.array(zs)
            w(f"| {n} | {rho} | {dsd} | {np.median(zs):.2f} | "
              f"{(zs>2).mean():.0%} |")
    return "\n".join(out)


if __name__ == "__main__":
    txt = main()
    with open(os.path.join(_HERE, "..", "results",
                           "stationarity_calibration.md"), "w") as fh:
        fh.write(txt)
    print(txt)


# ---------------------------------------------------------------------------
# KPSS test for level stationarity, implemented directly (no new dependency).
#
#   e_t = y_t - mean(y);  S_t = cumsum(e)
#   LM  = sum(S_t^2) / (n^2 * s2_l)
#   s2_l = Newey-West long-run variance with Bartlett weights at lag l
#
# Null hypothesis: the series IS level-stationary. Large LM rejects.
# Asymptotic critical values (Kwiatkowski et al. 1992), level stationarity:
#   10% 0.347   5% 0.463   2.5% 0.574   1% 0.739
#
# This is the standard tool for the question the ad-hoc shift screen was trying
# to answer, and unlike that screen its long-run variance estimator accounts
# for autocorrelation explicitly instead of being driven by it.
# ---------------------------------------------------------------------------

KPSS_CV = {0.10: 0.347, 0.05: 0.463, 0.025: 0.574, 0.01: 0.739}


def kpss_stat(y, lags=None):
    y = np.asarray(y, float)
    y = y[np.isfinite(y)]
    n = len(y)
    if n < 20:
        return np.nan
    e = y - y.mean()
    S = np.cumsum(e)
    if lags is None:                     # Schwert rule, standard choice
        lags = int(np.floor(12 * (n / 100.0) ** 0.25))
    lags = max(1, min(lags, n - 2))
    s2 = np.dot(e, e) / n
    for l in range(1, lags + 1):
        w = 1.0 - l / (lags + 1.0)
        s2 += 2.0 * w * np.dot(e[:-l], e[l:]) / n
    if s2 <= 0:
        return np.nan
    return float(np.sum(S ** 2) / (n ** 2 * s2))


def kpss_reject(X, alpha=0.05):
    """True if ANY channel rejects level stationarity at alpha."""
    X = np.asarray(X, float)
    cv = KPSS_CV[alpha]
    for j in range(X.shape[1]):
        s = kpss_stat(X[:, j])
        if s == s and s > cv:
            return True
    return False


# ---------------------------------------------------------------------------
# Block-bootstrap calibration of the ORIGINAL screen statistic.
#
# The statistic is unchanged. What changes is the reference it is compared
# against: instead of a fixed 0.5, it is compared against its own null
# distribution under a circular block bootstrap of the same window.
#
# Block resampling preserves short-range dependence (blocks are contiguous)
# while destroying long-range trend (block order is randomised). The null is
# therefore generated at the same n, the same autocorrelation and the same
# marginal distribution as the observed window, which removes the effective
# -sample-size dependence that made the fixed threshold a test of n_eff.
#
# This is the minimal defensible repair: same statistic, correct reference.
# ---------------------------------------------------------------------------

def _acf_time(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)] - np.mean(x[np.isfinite(x)])
    d = np.dot(x, x)
    if d <= 0 or len(x) < 3:
        return 1.0
    r1 = float(np.dot(x[:-1], x[1:]) / d)
    r1 = min(max(r1, 0.0), 0.999)
    return (1.0 + r1) / (1.0 - r1)


def block_bootstrap_null(X, n_boot=300, seed=0):
    """Null distribution of shift_stat under circular block resampling."""
    rng = np.random.default_rng(seed)
    X = np.asarray(X, float)
    n = len(X)
    tau = max(_acf_time(X[:, 0]), 1.0)
    L = int(min(max(2 * tau, 5), max(5, n // 4)))
    nb = int(np.ceil(n / L))
    out = np.empty(n_boot)
    for b in range(n_boot):
        starts = rng.integers(0, n, nb)
        idx = np.concatenate([(np.arange(s, s + L) % n) for s in starts])[:n]
        out[b] = shift_stat(X[idx])
    return out, L


def stationarity_reject(X, alpha=0.05, n_boot=300, seed=0):
    """True if the window's drift exceeds its own block-bootstrap null."""
    obs = shift_stat(X)
    null, L = block_bootstrap_null(X, n_boot, seed)
    return obs > np.quantile(null, 1 - alpha), obs, float(np.quantile(null, 1 - alpha)), L
