"""
design_sim.py -- design-stage Monte Carlo for the DRAFT VF-onset protocol.

SYNTHETIC ONLY. This script reads no SDDB, chfdb or NSRDB file and computes
nothing on real ECG. It exists to replace hand-waved power arithmetic with a
simulation of the protocol's actual structure:

  * one event per patient, heterogeneous pre-onset durations;
  * 5-min windows on a 60-s stride (overlapping), features with minute-scale
    autocorrelation;
  * four disjoint lead bins (2,5], (5,10], (10,15], (15,30] min vs a remote
    zone (lead >= 60 min), patient-level leave-one-patient-out (LOPO) fitting
    with fixed-lambda ridge logistic regression, within-patient AUROC;
  * the draft decision rule and its temporal controls (pseudo-onsets,
    detrending, elapsed-time matching) and the acquisition gate.

Nothing here is evidence about VF. Every number depends on the generative
assumptions stated in SCENARIOS and in docs/VF_DESIGN_SIMULATION.md.

Run:  python3 analysis/vf/design_sim.py [--quick] [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import math
import time

import numpy as np

# --------------------------------------------------------------------------
# Fixed design geometry (minutes) -- mirrors the draft protocol
# --------------------------------------------------------------------------
W = 5                      # window length
SETTLE, BASE = 15, 30      # settling, baseline
REMOTE_LEAD = 60           # remote zone: lead >= 60
BINS = {"B5": (2, 5), "B10": (5, 10), "B15": (10, 15), "B30": (15, 30)}
ALPHA_BONF = 0.05 / 4
LAMBDA = 1.0
PSEUDO_STEP = 180          # pseudo-onsets every 3 h before the true onset
N_PSEUDO_DRAWS = 19        # p = 1/20 = 0.05 when the observed beats all draws

K1, K3 = 4, 3              # M1 features, TD features


# --------------------------------------------------------------------------
# Small numerical helpers (numpy only, like the rest of the repository)
# --------------------------------------------------------------------------
def t_quantile(p: float, df: int) -> float:
    """Student-t quantile by Cornish-Fisher expansion (adequate for df >= 5)."""
    from statistics import NormalDist
    z = NormalDist().inv_cdf(p)
    g1 = (z ** 3 + z) / 4
    g2 = (5 * z ** 5 + 16 * z ** 3 + 3 * z) / 96
    g3 = (3 * z ** 7 + 19 * z ** 5 + 17 * z ** 3 - 15 * z) / 384
    g4 = (79 * z ** 9 + 776 * z ** 7 + 1482 * z ** 5 - 1920 * z ** 3 - 945 * z) / 92160
    return z + g1 / df + g2 / df ** 2 + g3 / df ** 3 + g4 / df ** 4


def binom_sf(k: int, n: int) -> float:
    """P(X >= k), X ~ Bin(n, 0.5)."""
    return sum(math.comb(n, j) for j in range(k, n + 1)) / 2 ** n


def auroc(pos: np.ndarray, neg: np.ndarray) -> float:
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    s = np.sort(neg)
    lo = np.searchsorted(s, pos, side="left")
    hi = np.searchsorted(s, pos, side="right")
    return float(np.mean(lo + 0.5 * (hi - lo)) / len(neg))


def ar1(rng, T: int, k: int, phi: float) -> np.ndarray:
    """Unit-variance AR(1) at 1-min resolution, shape (T, k)."""
    e = rng.standard_normal((T, k)) * math.sqrt(1 - phi ** 2)
    x = np.empty((T, k))
    x[0] = rng.standard_normal(k)
    for t in range(1, T):
        x[t] = phi * x[t - 1] + e[t]
    return x


def rolling_mean(x: np.ndarray, w: int) -> np.ndarray:
    """Window ending at minute t (inclusive) for t = w-1 .. T-1."""
    c = np.cumsum(np.vstack([np.zeros((1, x.shape[1])), x]), axis=0)
    return (c[w:] - c[:-w]) / w


def fit_ridge_logistic(X: np.ndarray, y: np.ndarray, lam: float = LAMBDA,
                       iters: int = 8) -> np.ndarray:
    """Balanced-weight L2 logistic regression; intercept unpenalised.
    Features are z-scored on the training data only."""
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.hstack([np.ones((len(X), 1)), (X - mu) / sd])
    npos, nneg = y.sum(), len(y) - y.sum()
    w = np.where(y == 1, len(y) / (2 * npos), len(y) / (2 * nneg))
    beta = np.zeros(Z.shape[1])
    pen = lam * np.eye(Z.shape[1])
    pen[0, 0] = 0.0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(Z @ beta, -30, 30)))
        H = (Z * (w * p * (1 - p))[:, None]).T @ Z + pen
        g = Z.T @ (w * (y - p)) - pen @ beta
        beta = beta + np.linalg.solve(H, g)
    return np.concatenate([[beta[0] - np.sum(beta[1:] * mu / sd)], beta[1:] / sd])


def score(X: np.ndarray, coef: np.ndarray) -> np.ndarray:
    return coef[0] + X @ coef[1:]


# --------------------------------------------------------------------------
# Synthetic patients
# --------------------------------------------------------------------------
def shape_fn(kind: str, lead: np.ndarray) -> np.ndarray:
    lead = lead.astype(float)
    if kind == "ramp30":
        return np.clip(1 - lead / 30, 0, 1)
    if kind == "step30":
        return (lead <= 30).astype(float)
    if kind == "late5":
        return np.clip(1 - lead / 5, 0, 1)
    if kind == "none":
        return np.zeros_like(lead)
    raise ValueError(kind)


def make_patient(rng, T: int, sc: dict, vf: bool = True) -> dict:
    """Minute-level latents -> overlapping-window features.

    M1 : 4 channels; channel 0 carries the conventional precursor (amplitude a).
    TD : 3 channels = rho*M1_0 + sqrt(1-rho^2)*(c*v + sqrt(1-c^2)*u_j);
         the increment b is added to the common TD factor v only.
    SQI: 1 channel, loads on the onset-locked artefact with kappa.
    Drift / artefact terms are added to v (TD-only: worst case for TD claims).
    """
    phi, rho, c = sc.get("phi", 0.9), 0.5, 0.7
    m = ar1(rng, T, K1, phi)
    u = ar1(rng, T, K3, phi)
    v = ar1(rng, T, 1, phi)[:, 0]
    q = ar1(rng, T, 1, phi)[:, 0]
    minute = np.arange(T)
    lead = T - minute                      # lead of each minute sample (>= 1)
    if vf:
        h = 1.0 + sc.get("het", 0.5) * rng.standard_normal()
        if rng.random() > sc.get("responders", 1.0):
            h = 0.0
        g = shape_fn(sc.get("shape", "ramp30"), lead)
        m[:, 0] += sc.get("a", 0.5) * h * g
        v += sc.get("b", 0.0) * h * g
        # onset annotation error: arrhythmia actually starts eps min early
        eps = rng.uniform(0, sc.get("mark_err", 0.0))
        if eps > 0:
            hit = lead <= eps
            m[hit] += 4.0
            v[hit] += 4.0
        art = sc.get("onset_art", 0.0)
        if art:
            ga = np.clip(1 - lead / 60, 0, 1) * art
            v += ga
            q += sc.get("kappa", 0.0) * ga / max(art, 1e-9) * 2.0
    d = sc.get("drift", None)
    if d == "lin":
        s = rng.normal(sc.get('lin_mu', 4.0), 1.0)
        v += s * minute / 600
    elif d == "convex":
        s = rng.normal(sc.get('cvx_mu', 2.5), 0.5)
        v += s * (minute / 600) ** 2
    elif d == "circadian":
        clock_on = rng.normal(8 * 60, 120) if vf else rng.uniform(0, 1440)
        clock = clock_on - T + minute if vf else clock_on + minute
        v += sc.get('circ_amp', 4.0) * np.sin(2 * np.pi * (clock - 10 * 60) / 1440)
    td = rho * m[:, :1] + math.sqrt(1 - rho ** 2) * (
        c * v[:, None] + math.sqrt(1 - c ** 2) * u)
    F1 = rolling_mean(m, W)
    F3 = rolling_mean(td, W)
    FQ = rolling_mean(q[:, None], W)
    tend = np.arange(W - 1, T)             # window end minute
    wlead = T - tend                       # window lead (>= 1)
    base = (tend >= SETTLE + W - 1) & (tend <= SETTLE + BASE - 1)
    allf = np.hstack([F1, F3, FQ])
    mu, sd = allf[base].mean(0), allf[base].std(0) + 1e-9
    allf = (allf - mu) / sd                # baseline standardisation
    return {"T": T, "t": tend, "lead": wlead, "X": allf, "vf": vf}


def truncate(p: dict, T_new: int) -> dict:
    """Pseudo-onset at T_new: keep windows ending strictly before T_new."""
    keep = p["t"] < T_new
    return {"T": T_new, "t": p["t"][keep], "lead": T_new - p["t"][keep],
            "X": p["X"][keep], "vf": p["vf"]}


def detrend(p: dict) -> dict:
    """Per-feature linear trend fitted on the remote zone, removed everywhere."""
    r = remote_mask(p)
    X = p["X"].copy()
    if r.sum() < 10:
        return p
    A = np.vstack([np.ones(r.sum()), p["t"][r]]).T
    coef, *_ = np.linalg.lstsq(A, X[r], rcond=None)
    X -= np.vstack([np.ones(len(p["t"])), p["t"]]).T @ coef
    return {**p, "X": X}


def remote_mask(p: dict) -> np.ndarray:
    return (p["lead"] >= REMOTE_LEAD) & (p["t"] >= SETTLE + BASE + W - 1)


def bin_mask(p: dict, lo: int, hi: int) -> np.ndarray:
    return (p["lead"] > lo) & (p["lead"] <= hi)


# --------------------------------------------------------------------------
# LOPO analysis
# --------------------------------------------------------------------------
COLS = {"M1": list(range(K1)), "M3": list(range(K1, K1 + K3)),
        "M4": list(range(K1 + K3)), "SQI": [K1 + K3],
        "M1Q": list(range(K1)) + [K1 + K3],
        "M4Q": list(range(K1 + K3)) + [K1 + K3]}


def lopo(pats: list, models=("M1", "M4"), bins=BINS, guard_lo=None,
         stride: int = 1) -> dict:
    """Returns {bin: {model: array of per-patient within-patient AUROC}}."""
    out = {}
    for b, (lo, hi) in bins.items():
        if guard_lo is not None and b == "B5":
            lo = guard_lo
        P, N = [], []
        for p in pats:
            keep = (p["t"] % stride == 0)
            P.append(bin_mask(p, lo, hi) & keep)
            N.append(remote_mask(p) & keep)
        res = {mname: np.full(len(pats), np.nan) for mname in models}
        # stack once per bin: patients without positives are not used in training
        Xall = np.vstack([np.vstack([p["X"][P[j]], p["X"][N[j]]])
                          for j, p in enumerate(pats)])
        yall = np.concatenate([np.r_[np.ones(P[j].sum()), np.zeros(N[j].sum())]
                               for j in range(len(pats))])
        pid = np.concatenate([np.full(P[j].sum() + N[j].sum(), j)
                              for j in range(len(pats))])
        has_pos = np.array([P[j].sum() > 0 for j in range(len(pats))])
        usable = has_pos[pid]
        for i in range(len(pats)):
            if P[i].sum() == 0 or N[i].sum() == 0:
                continue
            tr = usable & (pid != i)
            te = pid == i
            for mname in models:
                cols = COLS[mname]
                coef = fit_ridge_logistic(Xall[tr][:, cols], yall[tr])
                s = score(Xall[te][:, cols], coef)
                yy = yall[te]
                res[mname][i] = auroc(s[yy == 1], s[yy == 0])
        out[b] = res
    return out


def primary_test(delta: np.ndarray) -> dict:
    d = delta[np.isfinite(delta)]
    n = len(d)
    if n < 3:
        return {"n": n, "mean": float("nan"), "pass": False, "ub95": float("nan")}
    m, se = d.mean(), d.std(ddof=1) / math.sqrt(n)
    tq = t_quantile(1 - ALPHA_BONF / 2, n - 1)
    k = int((d > 0).sum())
    sign_ok = binom_sf(k, n) < 0.025
    return {"n": n, "mean": float(m), "sd": float(d.std(ddof=1)),
            "lo": float(m - tq * se), "hi": float(m + tq * se),
            "ub95": float(m + t_quantile(0.95, n - 1) * se),
            "sign_k": k, "pass": bool(m - tq * se > 0 and sign_ok)}


# --------------------------------------------------------------------------
# One simulated study under a scenario, with the full draft decision rule
# --------------------------------------------------------------------------
def draw_T(rng, n: int, dist: str) -> np.ndarray:
    lo, hi = {"short": (140, 360), "mixed": (140, 1200), "long": (360, 1440)}[dist]
    return rng.integers(lo, hi + 1, size=n)


def run_study(rng, sc: dict, n: int, controls: bool = True,
              stride: int = 1, guard_lo=None) -> dict:
    Ts = draw_T(rng, n, sc.get("Tdist", "mixed"))
    pats = [make_patient(rng, int(T), sc, vf=True) for T in Ts]
    novf = [make_patient(rng, 1440, sc, vf=False) for _ in range(3)]
    want = ("M1", "M4", "M3", "SQI", "M1Q", "M4Q") if controls else ("M1", "M4")
    res = lopo(pats, models=want, stride=stride, guard_lo=guard_lo)
    out = {"bins": {}, "deltas": {}}
    any_pass = False
    for b in BINS:
        dlt = res[b]["M4"] - res[b]["M1"]
        pt = primary_test(dlt)
        pt["auroc_M1"] = float(np.nanmean(res[b]["M1"]))
        out["bins"][b] = pt
        out["deltas"][b] = dlt
        any_pass |= pt["pass"]
    out["Ts"] = Ts
    if not controls:
        return out
    # acquisition gate + conditional increment (always computed: cheap)
    for b in BINS:
        m3 = np.nanmean(res[b]["M3"]) - 0.5
        sq = np.nanmean(res[b]["SQI"]) - 0.5
        R = sq / m3 if m3 > 0.005 else float("nan")
        cond = np.nanmean(res[b]["M4Q"] - res[b]["M1Q"])
        out["bins"][b]["acq_R"] = float(R)
        out["bins"][b]["acq_pass"] = bool((not np.isfinite(R)) or R < 0.5)
        out["bins"][b]["cond_pass"] = bool(cond > 0 and
                                           cond >= 0.5 * out["bins"][b]["mean"])
    if not any_pass:
        for b in BINS:
            out["bins"][b].update(pseudo_pass=False, detr_pass=False, et_pass=False)
        return out
    # detrending
    rd = lopo([detrend(p) for p in pats])
    # elapsed-time matched comparison on the first TD feature (raw)
    et = et_matched(pats)
    # pseudo-onsets: VF patients' earlier segments (offset k * 3 h) + no-VF
    # records at elapsed times matched to the true onsets. One LOPO per offset
    # k; the null of the cohort mean is then built by drawing one available
    # offset per subject (approximation declared in VF_DESIGN_SIMULATION.md).
    kmax = int(max(Ts) // PSEUDO_STEP) + 1
    subj_vals = {b: [[] for _ in range(n + 3)] for b in BINS}
    for k in range(1, kmax + 1):
        cohort, idx = [], []
        for j, p in enumerate(pats):
            if p["T"] - PSEUDO_STEP * k >= 140:
                cohort.append(truncate(p, int(p["T"] - PSEUDO_STEP * k)))
                idx.append(j)
        for j, p in enumerate(novf):
            cohort.append(truncate(p, int(rng.choice(Ts))))
            idx.append(n + j)
        if len(cohort) < 6:
            continue
        rp = lopo(cohort)
        for b in BINS:
            d = rp[b]["M4"] - rp[b]["M1"]
            for jj, s in zip(idx, d):
                if np.isfinite(s):
                    subj_vals[b][jj].append(s)
    for b in BINS:
        obs = out["bins"][b]["mean"]
        avail = [np.array(v) for v in subj_vals[b] if len(v)]
        if len(avail) < 6:
            nm = np.array([])
        else:
            nm = np.array([np.mean([rng.choice(v) for v in avail]) for _ in range(999)])
        out["bins"][b]["pseudo_subjects"] = len(avail)
        out["bins"][b]["pseudo_pass"] = bool(len(nm) > 0 and
                                             (1 + np.sum(nm >= obs)) / (1 + len(nm)) <= 0.05)
        dd = np.nanmean(rd[b]["M4"] - rd[b]["M1"])
        out["bins"][b]["detr_pass"] = bool(dd > 0 and dd >= 0.5 * obs)
        out["bins"][b]["et_pass"] = bool(et[b]["pass"])
    out["pseudo_cohort_frac"] = float(np.mean(
        [p["T"] - PSEUDO_STEP >= 140 for p in pats]))
    return out


def et_matched(pats: list, tol: int = 15) -> dict:
    """For each patient's bin windows, compare the fixed unfitted TD composite
    (mean of the baseline-standardised TD features) with OTHER patients'
    remote-zone windows at the same elapsed time (+/- tol min)."""
    out = {}
    for b, (lo, hi) in BINS.items():
        a = []
        for i, p in enumerate(pats):
            pm = bin_mask(p, lo, hi)
            if pm.sum() == 0:
                continue
            tt = p["t"][pm]
            negs = []
            for j, q in enumerate(pats):
                if j == i:
                    continue
                r = remote_mask(q)
                sel = r & (q["t"] >= tt.min() - tol) & (q["t"] <= tt.max() + tol)
                negs.append(q["X"][sel, K1:K1 + K3].mean(1))
            negs = np.concatenate(negs) if negs else np.array([])
            if len(negs) >= 5:
                a.append(auroc(p["X"][pm, K1:K1 + K3].mean(1), negs))
        a = np.array(a)
        if len(a) < 3:
            out[b] = {"pass": False}
            continue
        m, se = a.mean(), a.std(ddof=1) / math.sqrt(len(a))
        out[b] = {"pass": bool(m - t_quantile(1 - ALPHA_BONF / 2, len(a) - 1) * se > 0.5)}
    return out


def verdict(study: dict, rule: str) -> str:
    sig = []
    for b, r in study["bins"].items():
        ok = r["pass"]
        if rule in ("temporal", "temporal+et", "full"):
            ok = ok and r.get("pseudo_pass", False) and r.get("detr_pass", False)
        if rule in ("temporal+et", "full"):
            ok = ok and r.get("et_pass", False)
        if rule == "full":
            ok = ok and r.get("acq_pass", True) and r.get("cond_pass", True)
        if rule == "pseudo_only":
            ok = ok and r.get("pseudo_pass", False)
        if rule == "detr_only":
            ok = ok and r.get("detr_pass", False)
        if ok:
            sig.append(b)
    if len(sig) >= 2 and ("B15" in sig or "B30" in sig):
        return "EXPLORATORY_SIGNAL"
    if sig:
        return "SHORT_LEAD_OR_SINGLE_BIN"
    return "NO_SIGNAL"



# --------------------------------------------------------------------------
# Parallel replicate runner
# --------------------------------------------------------------------------
POOL = None


def _study_worker(args):
    seed, sc, n, controls, stride, guard_lo = args
    rng = np.random.default_rng(seed)
    return run_study(rng, sc, n, controls=controls, stride=stride, guard_lo=guard_lo)


def many(rng, sc, n, reps, controls=False, stride=1, guard_lo=None):
    seeds = [int(x) for x in rng.integers(0, 2 ** 62, size=reps)]
    args = [(s, sc, n, controls, stride, guard_lo) for s in seeds]
    if POOL is None:
        return [_study_worker(a) for a in args]
    return POOL.map(_study_worker, args, chunksize=1)


# --------------------------------------------------------------------------
# Experiments
# --------------------------------------------------------------------------
SCENARIOS = {
    "S0_null":             {},
    "S1_linear_drift":     {"drift": "lin"},
    "S2_convex_drift":     {"drift": "convex"},
    "S3_onset_artefact_k0.8": {"onset_art": 2.0, "kappa": 0.8},
    "S4_onset_artefact_k0.2": {"onset_art": 2.0, "kappa": 0.2},
    "S5_circadian_aligned": {"drift": "circadian"},
    "P1_increment_b2_step30":  {"b": 2.0, "shape": "step30"},
    "P2_increment_b2_step30_lin_drift": {"b": 2.0, "shape": "step30", "drift": "lin"},
    "P3_increment_b2_ramp30": {"b": 2.0, "shape": "ramp30"},
}
RULES = ["primary", "pseudo_only", "detr_only", "temporal", "temporal+et", "full"]


def exp_rules(rng, reps: int, n: int) -> dict:
    out = {}
    for name, sc in SCENARIOS.items():
        t0 = time.time()
        counts = {r: {} for r in RULES}
        large_excl = 0
        frac = []
        for st in many(rng, sc, n, reps, controls=True):
            for r in RULES:
                v = verdict(st, r)
                counts[r][v] = counts[r].get(v, 0) + 1
            large_excl += all(st["bins"][b]["ub95"] < 0.10 for b in BINS)
            if "pseudo_cohort_frac" in st:
                frac.append(st["pseudo_cohort_frac"])
        out[name] = {
            "reps": reps, "n": n,
            "exploratory_signal_rate": {r: counts[r].get("EXPLORATORY_SIGNAL", 0) / reps
                                        for r in RULES},
            "any_bin_rate": {r: 1 - counts[r].get("NO_SIGNAL", 0) / reps for r in RULES},
            "large_excluded_rate": large_excl / reps,
            "pseudo_cohort_fraction": float(np.mean(frac)) if frac else None,
            "seconds": round(time.time() - t0, 1)}
        print(name, json.dumps(out[name]["exploratory_signal_rate"]),
              "large_excl", out[name]["large_excluded_rate"], flush=True)
    return out


def exp_power(rng, reps: int, ns=(8, 12, 16, 20), bs=(0.0, 0.5, 1.0, 1.5, 2.0, 3.0),
              shape="ramp30") -> dict:
    out = {}
    for n in ns:
        for b in bs:
            sc = {"b": b, "shape": shape}
            pw = {k: 0 for k in BINS}
            rule = 0
            sds = {k: [] for k in BINS}
            means = {k: [] for k in BINS}
            excl = 0
            for st in many(rng, sc, n, reps):
                sig = [k for k in BINS if st["bins"][k]["pass"]]
                for k in BINS:
                    pw[k] += st["bins"][k]["pass"]
                    sds[k].append(st["bins"][k]["sd"])
                    means[k].append(st["bins"][k]["mean"])
                rule += len(sig) >= 2 and ("B15" in sig or "B30" in sig)
                excl += all(st["bins"][k]["ub95"] < 0.10 for k in BINS)
            out[f"n{n}_b{b}"] = {
                "n": n, "b": b, "shape": shape,
                "power_per_bin": {k: pw[k] / reps for k in BINS},
                "rule_rate_stats_only": rule / reps,
                "large_excluded_rate": excl / reps,
                "mean_delta": {k: float(np.nanmean(means[k])) for k in BINS},
                "sd_delta_i": {k: float(np.nanmedian(sds[k])) for k in BINS}}
            print(n, b, out[f"n{n}_b{b}"]["power_per_bin"],
                  "rule", out[f"n{n}_b{b}"]["rule_rate_stats_only"], flush=True)
    return out


def exp_true_effect(rng, bs=(0.5, 1.0, 1.5, 2.0, 3.0), n_big=160, reps=3,
                    shape="ramp30") -> dict:
    """Population mean dAUROC implied by each latent increment b.
    Optional (--only true); O(n^2) and slow. Not part of the default run: the
    power experiment already records the expected mean dAUROC at design n."""
    out = {}
    for b in bs:
        acc = {k: [] for k in BINS}
        for st in many(rng, {"b": b, "shape": shape}, n_big, reps):
            for k in BINS:
                acc[k].append(st["bins"][k]["mean"])
        out[str(b)] = {k: float(np.mean(v)) for k, v in acc.items()}
        print("true", b, out[str(b)], flush=True)
    return out


def exp_overlap(rng, reps: int, n: int = 20) -> dict:
    """Overlap: window correlation, null SD of delta_i at stride 1 vs 5,
    naive vs cluster uncertainty, per-patient precision vs remote length,
    false-alarm calibration."""
    out = {}
    # (a) lag correlation of overlapping window features
    p = make_patient(rng, 1440, {}, vf=False)
    x = p["X"][:, K1]
    out["window_lag_corr"] = {str(k): float(np.corrcoef(x[:-k], x[k:])[0, 1])
                              for k in (1, 2, 3, 5, 10, 15, 30)}
    for phi in (0.9, 0.97):
        pp = make_patient(rng, 1440, {"phi": phi}, vf=False)
        xx = pp["X"][:, K1]
        r1 = float(np.corrcoef(xx[:-1], xx[1:])[0, 1])
        out[f"lag1_phi{phi}"] = r1
    # (b) null SD of delta_i, stride 1 vs stride 5
    for phi in (0.9, 0.97):
        for stride in (1, 5):
            sds = {k: [] for k in BINS}
            dl, Rs = [], []
            for st in many(rng, {"phi": phi}, n, reps, stride=stride):
                for k in BINS:
                    sds[k].append(st["bins"][k]["sd"])
                dl.append(st["deltas"])
                Rs.append(st["Ts"])
            out[f"null_sd_phi{phi}_stride{stride}"] = {
                k: float(np.nanmedian(v)) for k, v in sds.items()}
            if stride == 1 and phi == 0.9:
                # per-patient precision vs remote-zone length
                rem = np.concatenate([T - REMOTE_LEAD - (SETTLE + BASE + W - 1)
                                      for T in Rs])
                for k in BINS:
                    d = np.concatenate([x[k] for x in dl])
                    bands = {}
                    for lo, hi in ((0, 60), (60, 180), (180, 360), (360, 720), (720, 2000)):
                        sel = (rem >= lo) & (rem < hi) & np.isfinite(d)
                        if sel.sum() > 10:
                            bands[f"{lo}-{hi}"] = float(np.std(d[sel]))
                    out.setdefault("sd_delta_i_by_remote_minutes", {})[k] = bands
    # (c) naive window-independent SE vs empirical SD of a patient's AUROC_i
    emp, naive = [], []
    for _ in range(reps):
        T = 600
        # single-feature within-patient AUROC, B30 vs remote, repeated noise draws
        vals = []
        for _r in range(30):
            pt = make_patient(rng, T, {"a": 0.0}, vf=True)
            pm, nm = bin_mask(pt, 15, 30), remote_mask(pt)
            vals.append(auroc(pt["X"][pm, K1], pt["X"][nm, K1]))
        emp.append(np.std(vals))
        n1, n0 = 15, int(remote_mask(pt).sum())
        A = 0.5
        q1, q2 = A / (2 - A), 2 * A * A / (1 + A)
        naive.append(math.sqrt((A * (1 - A) + (n1 - 1) * (q1 - A * A)
                                + (n0 - 1) * (q2 - A * A)) / (n1 * n0)))
        if len(emp) >= 10:
            break
    out["within_patient_auroc_sd_B30"] = {"empirical": float(np.mean(emp)),
                                          "naive_hanley_mcneil": float(np.mean(naive))}
    # (d) false-alarm calibration on a null study
    out["false_alarm"] = far_experiment(rng, n, reps=max(3, reps // 20))
    return out


def alarms(s: np.ndarray, thr: float, consec: int = 3, refractory: int = 15) -> int:
    """Alarm at window t if windows t-consec+1..t are all above threshold and
    no alarm was raised in the previous `refractory` windows (greedy)."""
    above = s > thr
    if consec > 1:
        ok = above.copy()
        for k in range(1, consec):
            ok[k:] &= above[:-k]
            ok[:k] = False
    else:
        ok = above
    cand = np.flatnonzero(ok)
    cnt, last = 0, -10 ** 9
    for t in cand:
        if t - last >= refractory:
            cnt += 1
            last = t
    return cnt


def far_experiment(rng, n: int, reps: int) -> dict:
    res = {}
    for target in (0.1, 0.5, 1.0):
        fars, ratio1 = [], []
        for _ in range(reps):
            pats = [make_patient(rng, int(T), {}, vf=True) for T in draw_T(rng, n, "mixed")]
            for i in range(n):
                tr = [j for j in range(n) if j != i]
                P = [bin_mask(pats[j], 15, 30) for j in tr]
                N = [remote_mask(pats[j]) for j in tr]
                cols = COLS["M4"]
                Xtr = np.vstack([np.vstack([pats[j]["X"][P[k]][:, cols],
                                            pats[j]["X"][N[k]][:, cols]])
                                 for k, j in enumerate(tr)])
                ytr = np.concatenate([np.r_[np.ones(P[k].sum()), np.zeros(N[k].sum())]
                                      for k, j in enumerate(tr)])
                coef = fit_ridge_logistic(Xtr, ytr)
                seqs = [score(pats[j]["X"][N[k]][:, cols], coef) for k, j in enumerate(tr)]
                hours = sum(len(s) for s in seqs) / 60
                lo_t, hi_t = -20.0, 20.0
                for _b in range(30):
                    mid = (lo_t + hi_t) / 2
                    rate = sum(alarms(s, mid) for s in seqs) / hours
                    lo_t, hi_t = (mid, hi_t) if rate > target else (lo_t, mid)
                thr = hi_t
                s_i = score(pats[i]["X"][remote_mask(pats[i])][:, cols], coef)
                h_i = len(s_i) / 60
                if h_i > 0:
                    fars.append(alarms(s_i, thr) / h_i)
                    a1 = alarms(s_i, thr, consec=1)
                    a3 = alarms(s_i, thr, consec=3)
                    if a1 > 0:
                        ratio1.append(a3 / a1)
        f = np.array(fars)
        res[str(target)] = {"heldout_far_mean": float(f.mean()),
                            "heldout_far_median": float(np.median(f)),
                            "heldout_far_p10": float(np.quantile(f, 0.1)),
                            "heldout_far_p90": float(np.quantile(f, 0.9)),
                            "frac_patients_zero_alarms": float(np.mean(f == 0)),
                            "consec3_over_consec1_alarm_ratio":
                                float(np.mean(ratio1)) if ratio1 else None}
        print("FAR", target, res[str(target)], flush=True)
    return res


def exp_guard(rng, reps: int, n: int = 20) -> dict:
    """Guard interval vs onset-marking error and trigger-proximal precursors."""
    out = {}
    for label, sc in {"null_markerr2": {"mark_err": 2.0},
                      "late5_b1.0": {"b": 1.0, "shape": "late5"},
                      "ramp30_b0.75": {"b": 0.75}}.items():
        for g in (1, 2):
            pw, m1, dm = 0, [], []
            for st in many(rng, sc, n, reps, guard_lo=g):
                pw += st["bins"]["B5"]["pass"]
                m1.append(st["bins"]["B5"]["auroc_M1"])
                dm.append(st["bins"]["B5"]["mean"])
            out[f"{label}_guard{g}"] = {"B5_power": pw / reps,
                                        "B5_mean_auroc_M1": float(np.nanmean(m1)),
                                        "B5_mean_delta": float(np.nanmean(dm))}
            print("guard", label, g, out[f"{label}_guard{g}"], flush=True)
    return out


def exp_airm_bias(rng, reps: int = 400) -> dict:
    """Small-sample bias of the AIRM covariance distance under NO change, as a
    function of the number of beats in the window (fixed-duration windows make
    n depend on heart rate)."""
    import sys
    sys.path.insert(0, "analysis")
    from estimators import shrunk_covariance, delta_G_structure
    p, phi_b = 4, 0.8
    out = {}

    def beats(n):
        e = rng.standard_normal((n + 50, p)) * math.sqrt(1 - phi_b ** 2)
        x = np.zeros((n + 50, p))
        for t in range(1, n + 50):
            x[t] = phi_b * x[t - 1] + e[t]
        return x[50:]
    for n in (200, 256, 300, 330, 400):
        dl, dn = [], []
        for _ in range(reps // 4):
            S0 = shrunk_covariance(beats(1800))
            X = beats(n)
            dl.append(delta_G_structure(shrunk_covariance(X), S0))
            dn.append(delta_G_structure(shrunk_covariance(X, alpha=0.0), S0))
        out[str(n)] = {"airm_lw_mean": float(np.mean(dl)), "airm_noshrink_mean": float(np.mean(dn))}
    print("AIRM", out, flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default="analysis/results/vf_design_sim.json")
    ap.add_argument("--only", default="")
    ap.add_argument("--seed", type=int, default=20261103)
    ap.add_argument("--procs", type=int, default=4)
    a = ap.parse_args()
    global POOL
    if a.procs > 1:
        import multiprocessing as mp
        POOL = mp.get_context("fork").Pool(a.procs)
    rng = np.random.default_rng(a.seed)
    q = a.quick
    res = {"meta": {"seed": a.seed, "synthetic_only": True,
                    "note": "Design simulation. No real data. See docs/VF_DESIGN_SIMULATION.md"}}
    todo = a.only.split(",") if a.only else ["airm", "power", "overlap", "guard", "rules"]
    if "airm" in todo:
        res["airm_bias"] = exp_airm_bias(rng, 40 if q else 400)
    if "true" in todo:
        res["true_effect"] = {sh: exp_true_effect(rng, reps=1 if q else 3, n_big=30 if q else 160,
                                                  shape=sh) for sh in ("ramp30", "step30")}
    if "power" in todo:
        res["power"] = exp_power(rng, 10 if q else 200)
        res["power_step30"] = exp_power(rng, 10 if q else 200, ns=(12, 20), shape="step30")
    if "overlap" in todo:
        res["overlap"] = exp_overlap(rng, 5 if q else 100)
    if "guard" in todo:
        res["guard"] = exp_guard(rng, 10 if q else 150)
    if "rules" in todo:
        res["rules"] = exp_rules(rng, 4 if q else 100, 20)
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1, default=float)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
