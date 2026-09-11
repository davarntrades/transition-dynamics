"""
verify_harness.py -- adversarial checks on the harness, run on the CALIBRATION
set and on synthetic data before the confirmatory set is examined.

The point of tests 6 and 7: establish that the harness CAN detect multivariate
structure when it is present, and does NOT credit S when the signal is purely
marginal. Without both, a null result on real data is uninterpretable.
"""
from __future__ import annotations
import json, os, sys, warnings
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
warnings.filterwarnings("ignore")
import windows as W, features as F, models as M
from cohort import RESULTS, MAP_IDX
from run_calibration import case_rows

FAIL = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)


def main():
    ids = json.load(open(os.path.join(RESULTS, "sd_split.json")))["calibration"]
    cases = []
    for c in ids:
        res, why = case_rows(c)
        if res is not None:
            cases.append(res)
    print(f"\n{len(cases)} usable calibration cases\n")

    # 1 -- anti-triviality: no retained window is already hypotensive
    print("1. no retained window contains hypotension in its feature window")
    worst = np.inf
    for r in cases:
        Xi = r["prep"]["Xi"]
        w = int(W.FEAT_W / W.DT)
        for row in r["rows"]:
            mp = Xi[row["t_idx"] - w:row["t_idx"], MAP_IDX]
            worst = min(worst, np.nanmin(mp))
    check("min MAP over all retained feature windows >= 65",
          worst >= W.MAP_THRESH, f"min = {worst:.1f} mmHg")

    # 2 -- labels agree with the onset times they are derived from
    print("2. labels match onset times")
    bad = 0
    for r in cases:
        for row in r["rows"]:
            nxt = row["next_onset_min"]
            for h in W.HORIZONS:
                if not row["keep"][h]:
                    continue
                want = np.isfinite(nxt) and nxt <= (W.GAP + h) / 60.0
                if bool(row["labels"][h]) != bool(want):
                    bad += 1
    check("every kept label equals (next onset within gap+H)", bad == 0,
          f"{bad} mismatches")

    # 3 -- negatives are never censored
    print("3. censoring")
    bad = 0
    for r in cases:
        for row in r["rows"]:
            for h in W.HORIZONS:
                if row["keep"][h] and row["labels"][h] == 0:
                    if row["t_idx"] + int((W.GAP + h) / W.DT) > r["i1"]:
                        bad += 1
    check("no negative label with an unobserved horizon", bad == 0, f"{bad} bad")

    # 4 -- features do not read forward
    print("4. no forward leakage into features")
    r = cases[0]
    X = np.load(os.path.join(
        os.path.dirname(W.__file__), "..", "..", "data", "real", "vitaldb",
        "npz_sd", f"{r['caseid']:04d}.npz"))["X"].astype(np.float64)
    rows_a, _ = W.build_windows(r["prep"], r["i0"], r["i1"])
    cut = rows_a[len(rows_a) // 2]["t_idx"]
    Xm = X.copy()
    Xm[cut:, :] = Xm[cut:, :] * 3.0 + 17.0        # corrupt everything after t
    prep_m, _ = W.prepare_case(Xm, r["i0"], r["i1"])
    rows_b, _ = W.build_windows(prep_m, r["i0"], r["i1"])
    a = {x["t_idx"]: x for x in rows_a}
    b = {x["t_idx"]: x for x in rows_b}
    same = True
    for t in a:
        if t > cut or t not in b:
            continue
        for k in ("x", "delta", "z", "sd_w", "slope"):
            if not np.allclose(np.nan_to_num(a[t][k]), np.nan_to_num(b[t][k])):
                same = False
    check("features at t unchanged when all samples after t are corrupted", same)
    check("mu0/Sigma0 unchanged when post-baseline data is corrupted",
          np.allclose(r["prep"]["mu0"], prep_m["mu0"]) and
          np.allclose(r["prep"]["Sigma0"], prep_m["Sigma0"]))

    # 5 -- grouped folds never split a patient
    print("5. patient-level folds")
    g = np.concatenate([[r["caseid"]] * len(r["rows"]) for r in cases])
    ok = all(len(set(g[te])) == len(set(g[te]) - set(g[tr]))
             for tr, te in M.grouped_folds(g, 5, 0))
    check("no caseid appears in both train and test of any fold", ok)

    # 6 -- POSITIVE CONTROL: signal only in the covariance geometry
    print("6. positive control -- multivariate-only signal")
    a6 = _synthetic(mode="geometric")
    check("S beats marginals when the signal is purely geometric",
          a6["S"] > a6["marg"] + 0.05,
          f"AUROC S={a6['S']:.3f} vs marginal={a6['marg']:.3f}")

    # 7 -- NEGATIVE CONTROL: signal only in the marginals
    print("7. negative control -- marginal-only signal")
    a7 = _synthetic(mode="marginal")
    check("S does not beat marginals when the signal is purely marginal",
          a7["S"] <= a7["marg"] + 0.02,
          f"AUROC S={a7['S']:.3f} vs marginal={a7['marg']:.3f}")

    print("\n" + ("ALL CHECKS PASSED" if not FAIL else f"FAILURES: {FAIL}"))
    return 1 if FAIL else 0


def _synthetic(mode, n=4000, p=6, seed=0):
    """Two correlated blocks. 'geometric' displaces along a LOW-variance
    direction, leaving each marginal magnitude matched to the negatives.
    'marginal' inflates one channel, which any z-score sees."""
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(p, p)) * 0.3 + np.eye(p)
    Sigma = A @ A.T
    L = np.linalg.cholesky(Sigma)
    evals, evecs = np.linalg.eigh(Sigma)
    low = evecs[:, 0]                       # lowest-variance direction
    y = (rng.random(n) < 0.3).astype(float)
    base = rng.normal(size=(n, p)) @ L.T
    delta = base.copy()
    if mode == "geometric":
        # positives get displaced along the stiff direction; negatives get a
        # displacement of the SAME norm along the compliant direction
        high = evecs[:, -1]
        amp = 1.2 * np.sqrt(evals[0])
        for i in range(n):
            delta[i] += amp * (low if y[i] else high * np.sqrt(evals[0] / evals[-1]))
    else:
        delta[y == 1, 0] += 1.2 * np.sqrt(Sigma[0, 0])
    sig = np.sqrt(np.diag(Sigma))
    Pinv = np.linalg.inv(Sigma)
    S = np.array([F.S_literal(Pinv, d) for d in delta])
    z = np.abs(delta / sig)
    g = np.arange(n) % 50                    # 50 synthetic "patients"
    oof_m, _ = M.cv_predict(z, y, g, k=5)
    return {"S": M.auroc(y, S), "marg": M.auroc(y, oof_m)}


if __name__ == "__main__":
    sys.exit(main())
