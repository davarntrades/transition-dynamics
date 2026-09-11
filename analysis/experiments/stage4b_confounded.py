"""
stage4b_confounded.py — STAGE 4b: the test Stage 4 failed to perform.

WHY THIS FILE EXISTS
--------------------
Stage 4 compared targeted against untargeted cases drawn from the SAME
exposure grid, so the two groups had identical exposure distributions. A
confound requires the distributions to DIFFER. With them balanced by
construction there was nothing for exposure control to remove, and the three
conditions came out at 0.982, 0.982 and 0.988. The SURVIVES verdict was real
but empty: it showed that estimated-exposure control does not hurt, not that
it rescues anything.

The confound this whole exercise was built to address is that transition
classes plausibly differ in typical onset timing -- an abrupt event is recent,
a slowly developing one is established -- so exposure becomes correlated with
class. This file constructs exactly that correlation and asks whether
estimated-exposure control removes it.

TWO SCENARIOS
-------------
  SPURIOUS   Both groups are UNTARGETED. One is mostly recent, the other
             mostly established. True targeting difference is zero, so the
             correct answer is AUC 0.5. A naive comparison should report a
             targeting effect that does not exist.

  MASKED     One group is targeted and mostly established, the other
             untargeted and mostly recent, so the two effects oppose. True
             targeting is present; a naive comparison should understate it.

PREREGISTERED READING — fixed before running
--------------------------------------------
  SPURIOUS scenario
    naive |AUC - 0.5| should be large (otherwise no confound was created and
    the scenario is uninformative)
    estimated-T control RESCUES if |AUC - 0.5| <= 0.10
    estimated-T control FAILS   if |AUC - 0.5| > 0.10

  MASKED scenario
    estimated-T control RESCUES if it recovers AUC within 0.10 of the
    same-exposure reference measured in Stage 1

Overlap is required for stratification to be possible at all. If the two
groups share no exposure bin, that is reported as NO COMMON SUPPORT rather
than scored, because comparing groups with no overlap is not a control
failure, it is an impossible comparison.

Run:  python3 analysis/experiments/stage4b_confounded.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(__file__)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, ".."))

from exposure_stage1_oracle import (Config, simulate, calibrate,       # noqa: E402
                                    d_isotropic, d_stiff_sub, auc)
from onset_estimator import estimate_onset, alignment_crossfit         # noqa: E402

SHORT, LONG = 3.0, 120.0
N = 60                       # cases per group
SEV = 30.0                   # 1.5 baseline SD: the regime where onset is identifiable
SEV_WEAK = 10.0              # 0.5 baseline SD: targeting present but not overwhelming
STRUCTS = [Config("wide-rotated"),
           Config("wide-diagonal", rotate=False),
           Config("narrow-rotated", k_lo=0.60, k_hi=2.40)]


def make_group(cfg, dirfn, p_short, seed0, sev=None):
    """A group whose exposure is a mixture: p_short recent, rest established."""
    rng = np.random.default_rng(seed0)
    rows = []
    sev = SEV if sev is None else sev
    scales = {SHORT: calibrate(cfg, dirfn, SHORT, sev),
              LONG: calibrate(cfg, dirfn, LONG, sev)}
    for i in range(N):
        T = SHORT if rng.random() < p_short else LONG
        X = simulate(cfg, dirfn(cfg, seed0 + i), scales[T], T, seed0 + i)
        est = estimate_onset(X, cfg)
        rows.append({"A": alignment_crossfit(X, cfg), "T_true": T,
                     "T_hat": est["T_hat"], "ident": est["identifiable"]})
    return rows


def stratified_auc(gA, gB, edges=(0.0, 20.0, 1e9)):
    """
    AUC after binning both groups by ESTIMATED exposure, pooled across bins
    weighted by the number of comparable pairs. Returns (auc, n_bins, support).

    ORIENTATION. Group B is the positive class, matching the naive comparison.
    An earlier version scored group A as positive here while the naive
    comparison scored group B, so oracle and estimated came back as one minus
    the intended value. In the spurious scenario that is nearly invisible
    because the answer is symmetric about one half; in the masked scenario it
    produced an AUC of exactly zero, which is what exposed it.
    """
    a = [r for r in gA if r["ident"]]
    b = [r for r in gB if r["ident"]]
    num = den = 0.0
    used = 0
    for lo, hi in zip(edges[:-1], edges[1:]):
        xa = [r["A"] for r in a if lo <= r["T_hat"] < hi]
        xb = [r["A"] for r in b if lo <= r["T_hat"] < hi]
        if len(xa) >= 5 and len(xb) >= 5:
            w = len(xa) * len(xb)
            num += auc(xb, xa) * w
            den += w
            used += 1
    if den == 0:
        return float("nan"), used, False
    return num / den, used, True


def oracle_auc(gA, gB):
    num = den = 0.0
    for T in (SHORT, LONG):
        xa = [r["A"] for r in gA if r["T_true"] == T]
        xb = [r["A"] for r in gB if r["T_true"] == T]
        if len(xa) >= 5 and len(xb) >= 5:
            w = len(xa) * len(xb)
            num += auc(xb, xa) * w
            den += w
    return num / den if den else float("nan")


def main() -> str:
    out, w = [], lambda s: out.append(s)
    w("# Stage 4b — confounded exposure, the test Stage 4 missed\n")
    w("Stage 4 drew both groups from the same exposure grid, so their exposure "
      "distributions were identical and there was no confound to remove. Here "
      "exposure is deliberately correlated with group, which is the situation "
      "the whole exercise was built to address.\n")
    w(f"\nRecent exposure T={SHORT:g}, established T={LONG:g}; {N} cases per "
      f"group; displacement {SEV/20:.1f} baseline SD.\n")

    for scen, dirA, pA, dirB, pB, truth, sev in (
        ("SPURIOUS — both groups untargeted",
         d_isotropic, 0.80, d_isotropic, 0.20, "AUC should be 0.50", SEV),
        ("MASKED, strong targeting (1.5 SD)",
         d_isotropic, 0.80, d_stiff_sub, 0.20, "targeting present", SEV),
        ("MASKED, weak targeting (0.5 SD)",
         d_isotropic, 0.80, d_stiff_sub, 0.20, "targeting present", SEV_WEAK),
    ):
        w(f"\n## {scen}\n")
        w(f"\nGroup A: {pA:.0%} recent. Group B: {pB:.0%} recent. "
          f"Displacement {sev/20:.1f} baseline SD. Truth: {truth}.\n")
        w("\n| structure | naive (no control) | oracle true T | estimated T | bins | declined |")
        w("|---|:--:|:--:|:--:|:--:|:--:|")
        rows = []
        for cfg in STRUCTS:
            gA = make_group(cfg, dirA, pA, 200_000, sev)
            gB = make_group(cfg, dirB, pB, 300_000, sev)
            naive = auc([r["A"] for r in gB], [r["A"] for r in gA])
            orc = oracle_auc(gA, gB)
            estv, nb, sup = stratified_auc(gA, gB)
            dec = np.mean([not r["ident"] for r in gA + gB])
            rows.append((naive, orc, estv, sup))
            w(f"| {cfg.name} | {naive:.3f} | {orc:.3f} | "
              f"{'NO COMMON SUPPORT' if not sup else f'{estv:.3f}'} "
              f"| {nb} | {dec:.0%} |")
        nv = np.median([r[0] for r in rows])
        ov = np.median([r[1] for r in rows])
        ev = np.median([r[2] for r in rows if r[3]]) if any(r[3] for r in rows) else float("nan")
        w(f"\nmedian: naive {nv:.3f} · oracle {ov:.3f} · estimated {ev:.3f}")
        if scen.startswith("SPURIOUS"):
            w(f"\n- naive bias from 0.50: **{abs(nv-0.5):.3f}**")
            w(f"\n- oracle residual bias: {abs(ov-0.5):.3f}")
            w(f"\n- estimated-T residual bias: **{abs(ev-0.5):.3f}** "
              f"(rescues if <= 0.10)")
            w(f"\n\n### Verdict: **"
              f"{'RESCUES' if abs(ev-0.5) <= 0.10 else 'FAILS'}**\n")
        else:
            w(f"\n- naive comparison: {nv:.3f}")
            w(f"\n- oracle true-T control: {ov:.3f}")
            w(f"\n- estimated-T control: **{ev:.3f}**")
            w(f"\n- masking present? {'yes' if ov - nv > 0.03 else 'no — targeting dominates the exposure contrast'}\n")
    return "\n".join(out)


if __name__ == "__main__":
    txt = main()
    with open(os.path.join(_HERE, "..", "results",
                           "stage4b_confounded.md"), "w") as fh:
        fh.write(txt)
    print(txt)
