"""
exposure_stage1_oracle.py — STAGE 1: oracle falsification of the
mechanism-identification claim.

THE CLAIM UNDER TEST
--------------------
That alignment identifies WHICH mechanism produced a displacement — i.e. that
it distinguishes a targeted insult from an untargeted one.

The previous experiment left this confounded: exposure duration alone moved
alignment nearly as much as targeting did. This stage removes that confound by
fiat, using the simulator's KNOWN true time-since-onset T. No estimator is
built here. If separation collapses once true T is controlled, the claim is
falsified and no estimator may be built to rescue it.

PREREGISTERED DECISION RULE — fixed before this file was run
------------------------------------------------------------
Primary statistic: within-stratum AUC for stiff-targeted versus isotropic
displacement, matched on true T and on conventional observability (max
univariate z), computed separately in every cell of the grid.

  FALSIFIED   median within-stratum AUC < 0.65,
              OR fewer than 50% of strata above 0.65.
              -> mechanism-identification claim dies. Do not build an
                 estimator. Alignment remains descriptive only.

  SURVIVES    median within-stratum AUC >= 0.75
              AND at least 70% of strata above 0.65.
              -> proceed to Stage 2.

  UNRESOLVED  anything between.

A flattering aggregate is explicitly NOT sufficient: the rule is stated on the
distribution across strata, so a result confined to one convenient regime
fails it.

Run:  python3 analysis/experiments/exposure_stage1_oracle.py
"""

from __future__ import annotations

import itertools
import json
import os
import sys
from dataclasses import dataclass

import numpy as np
from scipy.signal import lfilter

_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, ".."))
import estimators as E                                   # noqa: E402


# ---------------------------------------------------------------------------
# Configurable linear system. Exact OU transitions, evaluated with an AR(1)
# filter per channel rather than a Python loop (identical process, ~50x faster).
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    name: str
    p: int = 8
    k_lo: float = 0.30
    k_hi: float = 4.80
    sigma: float = 1.0
    rotate: bool = True          # non-diagonal Sigma_0 (channels != eigenvectors)
    base_n: int = 4000
    pre_n: int = 400
    h: float = 0.30

    @property
    def k(self):
        return np.geomspace(self.k_lo, self.k_hi, self.p)

    def basis(self):
        if not self.rotate:
            return np.eye(self.p)
        Q, _ = np.linalg.qr(np.random.default_rng(12345).normal(0, 1, (self.p, self.p)))
        return Q


def simulate(cfg: Config, force_eig, scale, T, seed, noise=True):
    """
    force_eig : unit vector in the EIGENBASIS (so 'stiff'/'soft' are
                unambiguous), or None. Returned data is in the OBSERVATION
                basis, which for rotate=True is not the eigenbasis.
    T         : true time-since-onset at the END of the series.
    """
    rng = np.random.default_rng(seed)
    p, k, h = cfg.p, cfg.k, cfg.h
    n = cfg.base_n + cfg.pre_n
    on = n - int(round(T / h))
    if force_eig is not None and on < cfg.base_n:
        raise ValueError(f"T={T} puts onset inside the baseline window")

    a = np.exp(-k * h)
    sd = cfg.sigma * np.sqrt((1 - a ** 2) / (2 * k)) if noise else np.zeros(p)
    u = rng.normal(0, 1, (n, p)) * sd
    if force_eig is not None:
        step = np.zeros((n, p))
        step[on:] = (scale * np.asarray(force_eig) / k) * (1 - a)
        u = u + step
    y = np.empty((n, p))
    for j in range(p):                      # AR(1) per channel
        y[:, j] = lfilter([1.0], [1.0, -a[j]], u[:, j])
    return y @ cfg.basis().T


def stationary_cov(cfg: Config):
    """
    Analytic stationary covariance in the OBSERVATION basis.

    For the discrete recursion y_t = a y_{t-1} + eps with
    a = exp(-k h) and var(eps) = sigma^2 (1-a^2)/(2k), the stationary
    variance is sigma^2/(2k) per eigen-coordinate.

    Needed because the deterministic twin has zero baseline variance, so a
    baseline SD cannot be measured from it.
    """
    Q = cfg.basis()
    return Q @ np.diag(cfg.sigma ** 2 / (2 * cfg.k)) @ Q.T


def measure(X, cfg: Config, want_null=False):
    base, pre = X[:cfg.base_n], X[cfg.base_n:]
    S0 = E._spd_guard(E.shrunk_covariance(base))
    mu0, sd0 = base.mean(0), base.std(0) + 1e-12
    Pm = np.linalg.pinv(S0)
    d = pre.mean(0) - mu0
    out = {
        "A": E.stiffness_alignment(d, S0, precision=Pm),
        "uni": float(np.max(np.abs(d) / (sd0 / np.sqrt(len(pre))))),
        "dG": E.delta_G_structure(E.shrunk_covariance(pre), S0),
        "mag": float(np.linalg.norm(d)),
    }
    if want_null:
        out["null"] = E.alignment_empirical_null(base, S0, mu0, win=cfg.pre_n,
                                                 n_sub=200, seed=0)
    return out


# ---------------------------------------------------------------------------
# Force directions, defined in the eigenbasis
# ---------------------------------------------------------------------------

def d_isotropic(cfg, i):
    r = np.random.default_rng(90000 + i).normal(0, 1, cfg.p)
    return r / np.linalg.norm(r)


def d_stiff_sub(cfg, i, m=3):
    v = np.zeros(cfg.p)
    r = np.random.default_rng(91000 + i).normal(0, 1, m)
    v[-m:] = r / np.linalg.norm(r)
    return v


def d_soft_sub(cfg, i, m=3):
    v = np.zeros(cfg.p)
    r = np.random.default_rng(92000 + i).normal(0, 1, m)
    v[:m] = r / np.linalg.norm(r)
    return v


CONDS = {"isotropic": d_isotropic, "stiff-sub": d_stiff_sub,
         "soft-sub": d_soft_sub}


def calibrate(cfg, dirfn, T, target_uni):
    """
    Exact, on the deterministic twin: delta is linear in the force scale.

    BUG FIXED HERE, recorded rather than quietly corrected. An earlier version
    called measure() on the twin and read its max-univariate-z. That statistic
    divides by the BASELINE SD, which on a noise-free twin is exactly zero, so
    the ratio exploded and the returned scale collapsed to about 1e-12. The
    force was then never applied: all three conditions produced bit-identical
    trajectories and every AUC in the grid came out at 0.5, which was reported
    as a falsification. It was an artefact.

    The baseline SD is now taken analytically from the stationary covariance,
    which is well defined whether or not the twin carries noise.
    """
    d = dirfn(cfg, 0)
    X = simulate(cfg, d, 1.0, T, 0, noise=False)
    delta = X[cfg.base_n:].mean(0) - X[:cfg.base_n].mean(0)
    sd0 = np.sqrt(np.diag(stationary_cov(cfg)))
    u = float(np.max(np.abs(delta) / (sd0 / np.sqrt(cfg.pre_n))))
    s = target_uni / u if u > 1e-12 else 0.0

    # Refine against the REALISED (noisy) observable. Max-univariate-z has a
    # noise floor of its own -- the maximum over p channels of a zero-mean
    # fluctuation -- so the deterministic match alone leaves conditions
    # differing by 10-20% in what a clinician would actually see. What the
    # comparison requires is that the conditions match EACH OTHER, so the
    # refinement targets the realised value.
    for _ in range(2):
        got = float(np.mean([measure(simulate(cfg, dirfn(cfg, i), s, T, i),
                                     cfg)["uni"] for i in range(10)]))
        if got <= 1e-9:
            break
        s *= target_uni / got
    return max(s, 0.0)


def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    gt = (pos[:, None] > neg[None, :]).sum()
    eq = (pos[:, None] == neg[None, :]).sum()
    return float((gt + 0.5 * eq) / (len(pos) * len(neg)))


def auc_ci(pos, neg, n=800, seed=0):
    rng = np.random.default_rng(seed)
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    v = [auc(rng.choice(pos, len(pos), True), rng.choice(neg, len(neg), True))
         for _ in range(n)]
    return float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))


# ---------------------------------------------------------------------------
# Preregistered grid
# ---------------------------------------------------------------------------

STRUCTURES = [
    Config("wide-rotated"),
    Config("narrow-rotated", k_lo=0.60, k_hi=2.40),
    Config("wide-diagonal", rotate=False),
    Config("high-noise", sigma=2.0),
    Config("low-noise", sigma=0.5),
    Config("p16-wide", p=16),
]
EXPOSURES = [1.0, 3.0, 10.0, 30.0, 60.0, 120.0]
SEVERITIES = [4.0, 10.0, 30.0]        # max univariate z: 0.2 / 0.5 / 1.5 SD
SEEDS = range(25)


def main() -> str:
    rows = []
    for cfg, T, sev in itertools.product(STRUCTURES, EXPOSURES, SEVERITIES):
        cell = {}
        for cname, dirfn in CONDS.items():
            s = calibrate(cfg, dirfn, T, sev)
            cell[cname] = [measure(simulate(cfg, dirfn(cfg, i), s, T, i), cfg)
                           for i in SEEDS]
        # GUARD. Three separate scaling bugs in this programme have silently
        # produced "no effect" verdicts by never applying the force. A cell is
        # only valid if the realised severity tracks the target and the
        # conditions actually differ. Failing loudly beats reporting a null.
        realised = {c: float(np.mean([x["uni"] for x in cell[c]]))
                    for c in CONDS}
        lo, hi = min(realised.values()), max(realised.values())
        if hi > 1.25 * lo:
            raise AssertionError(
                f"cross-condition severity mismatch in "
                f"{cfg.name}/T={T}/sev={sev}: realised {realised}. The "
                "targeted and untargeted cases are not equally observable, so "
                "any AUC between them is confounded by severity.")
        spread = abs(float(np.mean([x["A"] for x in cell["stiff-sub"]]))
                     - float(np.mean([x["A"] for x in cell["isotropic"]])))
        if spread < 1e-9:
            raise AssertionError(
                f"conditions identical in {cfg.name}/T={T}/sev={sev}: "
                "stiff-targeted and isotropic produced the same alignment to "
                "machine precision.")
        rows.append({"cfg": cfg.name, "T": T, "sev": sev, "cell": cell,
                     "realised": realised})

    def col(r, cond, key):
        return [x[key] for x in r["cell"][cond]]

    out, w = [], lambda s: out.append(s)
    w("# Stage 1 — Oracle exposure control\n")
    w("Generated by `analysis/experiments/exposure_stage1_oracle.py`. "
      "True time-since-onset is taken from the simulator; no onset estimator "
      "is used.\n")
    floors = {c.name: float(np.mean([measure(simulate(c, None, 0.0, 0.0, i), c)["uni"]
                                     for i in range(10)])) for c in STRUCTURES}
    w("\n**Max-univariate-z noise floor** (stationary, no force): "
      + ", ".join(f"{k} {v:.1f}" for k, v in floors.items())
      + ". Severity targets at or below the floor are noise-dominated and are "
        "labelled as such rather than dropped.\n")
    w(f"\nGrid: {len(STRUCTURES)} baseline structures x {len(EXPOSURES)} "
      f"exposures x {len(SEVERITIES)} severities x {len(list(SEEDS))} seeds = "
      f"**{len(rows)} strata**, {len(rows)*len(CONDS)*len(list(SEEDS))} "
      "simulations. Targeted and untargeted cases are matched within every "
      "stratum on true T and on max univariate z.\n")

    # ---- unconditional (pools all T and severities) ----
    allA = {c: [v for r in rows for v in col(r, c, "A")] for c in CONDS}
    alldG = {c: [v for r in rows for v in col(r, c, "dG")] for c in CONDS}
    u_lo, u_hi = auc_ci(allA["stiff-sub"], allA["isotropic"])
    w("\n## 1. Unconditional (exposure NOT controlled)\n")
    w("\n| comparison | AUC | 95% CI |")
    w("|---|:--:|:--:|")
    w(f"| alignment: stiff-targeted vs isotropic | "
      f"{auc(allA['stiff-sub'], allA['isotropic']):.3f} | [{u_lo:.2f}, {u_hi:.2f}] |")
    w(f"| alignment: soft-targeted vs isotropic | "
      f"{auc(allA['soft-sub'], allA['isotropic']):.3f} | – |")
    w(f"| covariance drift: stiff-targeted vs isotropic | "
      f"{auc(alldG['stiff-sub'], alldG['isotropic']):.3f} | – |")

    # ---- within-stratum ----
    w("\n## 2. Within-stratum (true T and severity both controlled)\n")
    per = [auc(col(r, "stiff-sub", "A"), col(r, "isotropic", "A")) for r in rows]
    per = np.array(per)
    w(f"\n- strata: **{len(per)}**")
    w(f"- median AUC: **{np.median(per):.3f}**")
    w(f"- IQR: [{np.quantile(per,0.25):.3f}, {np.quantile(per,0.75):.3f}]")
    w(f"- min / max: {per.min():.3f} / {per.max():.3f}")
    w(f"- fraction above 0.65: **{(per>0.65).mean():.0%}**")
    w(f"- fraction above 0.90: {(per>0.90).mean():.0%}")

    w("\n### By exposure (median across structures and severities)\n")
    w("\n| true T | median AUC | min | fraction > 0.65 |")
    w("|:--:|:--:|:--:|:--:|")
    for T in EXPOSURES:
        v = np.array([auc(col(r, "stiff-sub", "A"), col(r, "isotropic", "A"))
                      for r in rows if r["T"] == T])
        w(f"| {T:g} | {np.median(v):.3f} | {v.min():.3f} | {(v>0.65).mean():.0%} |")

    w("\n### By severity\n")
    w("\n| max univariate z | baseline SD | median AUC | min | fraction > 0.65 |")
    w("|:--:|:--:|:--:|:--:|:--:|")
    for sev in SEVERITIES:
        v = np.array([auc(col(r, "stiff-sub", "A"), col(r, "isotropic", "A"))
                      for r in rows if r["sev"] == sev])
        w(f"| {sev:g} | {sev/20:.2f} | {np.median(v):.3f} | {v.min():.3f} "
          f"| {(v>0.65).mean():.0%} |")

    w("\n### By baseline structure\n")
    w("\n| structure | median AUC | min | fraction > 0.65 |")
    w("|---|:--:|:--:|:--:|")
    for cfg in STRUCTURES:
        v = np.array([auc(col(r, "stiff-sub", "A"), col(r, "isotropic", "A"))
                      for r in rows if r["cfg"] == cfg.name])
        w(f"| {cfg.name} | {np.median(v):.3f} | {v.min():.3f} "
          f"| {(v>0.65).mean():.0%} |")

    w("\n### Comparator: covariance drift, same strata\n")
    pdg = np.array([auc(col(r, "stiff-sub", "dG"), col(r, "isotropic", "dG"))
                    for r in rows])
    w(f"\nmedian {np.median(pdg):.3f}, IQR "
      f"[{np.quantile(pdg,0.25):.3f}, {np.quantile(pdg,0.75):.3f}], "
      f"fraction > 0.65: {(pdg>0.65).mean():.0%}\n")

    # ---- verdict ----
    med, frac = float(np.median(per)), float((per > 0.65).mean())
    verdict = ("FALSIFIED" if (med < 0.65 or frac < 0.50) else
               "SURVIVES" if (med >= 0.75 and frac >= 0.70) else "UNRESOLVED")
    w("\n## 3. Verdict against the preregistered rule\n")
    w("\n| criterion | value | threshold |")
    w("|---|:--:|:--:|")
    w(f"| median within-stratum AUC | {med:.3f} | falsified < 0.65 / survives >= 0.75 |")
    w(f"| fraction of strata > 0.65 | {frac:.0%} | falsified < 50% / survives >= 70% |")
    w(f"\n### Verdict: **{verdict}**\n")

    with open(os.path.join(_HERE, "..", "results",
                           "stage1_strata.json"), "w") as fh:
        json.dump([{"cfg": r["cfg"], "T": r["T"], "sev": r["sev"],
                    "auc_A": auc(col(r, "stiff-sub", "A"),
                                 col(r, "isotropic", "A")),
                    "auc_dG": auc(col(r, "stiff-sub", "dG"),
                                  col(r, "isotropic", "dG")),
                    "A_stiff": float(np.mean(col(r, "stiff-sub", "A"))),
                    "A_iso": float(np.mean(col(r, "isotropic", "A"))),
                    "A_soft": float(np.mean(col(r, "soft-sub", "A"))),
                    "uni_stiff": float(np.mean(col(r, "stiff-sub", "uni"))),
                    "uni_iso": float(np.mean(col(r, "isotropic", "uni")))}
                   for r in rows], fh, indent=1)
    return "\n".join(out)


if __name__ == "__main__":
    txt = main()
    with open(os.path.join(_HERE, "..", "results",
                           "stage1_oracle.md"), "w") as fh:
        fh.write(txt)
    print(txt)
