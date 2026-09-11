"""
run_confirmatory.py -- the confirmatory test.

Fixed in full before the confirmatory set was examined. Nothing in this file
may be edited after its first run on the confirmatory data.
"""
from __future__ import annotations
import json, os, sys, time, warnings
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
warnings.filterwarnings("ignore")
import windows as W, features as F, models as M
from cohort import RESULTS, SHORT
from run_calibration import case_rows

N_BOOT = 2000
N_SURR = 200
FOLDS = 5
SEED = 20260911
FAR_LEVELS = (0.05, 0.10)
COV_KINDS = ("patient", "diagonal", "identity", "shuffled",
             "subject", "population")

# Additive only. None reproduces the primary run exactly; set to MAP_SEVERE to
# run the prespecified secondary endpoint. No primary code path is touched.
THRESH_OVERRIDE = None


# --------------------------------------------------------------------- loading
def load_all(which="confirmatory"):
    ids = json.load(open(os.path.join(RESULTS, "sd_split.json")))[which]
    thresh = W.MAP_THRESH if THRESH_OVERRIDE is None else THRESH_OVERRIDE
    cases, excl = [], {}
    for c in ids:
        try:
            res, why = case_rows(c, thresh)
        except Exception as e:
            excl[c] = f"error: {type(e).__name__}"
            continue
        if res is None:
            excl[c] = why
        elif res["rows"]:
            cases.append(res)
        else:
            excl[c] = "no evaluation points"
    return cases, excl


def assemble(cases):
    """One row per evaluation point, with everything that does not depend on
    a cross-validation fold."""
    blocks, groups, labels, keeps, lead, sig0, delta, Sig = [], [], [], [], [], [], [], {}
    for r in cases:
        prep = r["prep"]
        Sig[r["caseid"]] = prep["Sigma0"]
        for row in r["rows"]:
            blocks.append(F.row_blocks(row, prep))
            groups.append(r["caseid"])
            labels.append(row["labels"])
            keeps.append(row["keep"])
            lead.append(row["next_onset_min"])
            delta.append(row["delta"])
            sig0.append(prep["sigma"])
    return {"blocks": blocks, "groups": np.array(groups),
            "labels": labels, "keeps": keeps, "lead": np.array(lead),
            "delta": np.array(delta), "sigma": np.array(sig0), "Sigma": Sig}


# ------------------------------------------------------------------ S columns
def s_columns(D, rng):
    """S for every covariance variant and both norms. Fold-independent
    variants only; 'subject' and 'population' are built inside the CV loop."""
    out = {}
    per_case_inv = {}
    for kind in ("patient", "diagonal", "identity", "shuffled"):
        inv = {c: F.metric_inverse(S0, kind, rng) for c, S0 in D["Sigma"].items()}
        per_case_inv[kind] = inv
        lit = np.array([F.S_literal(inv[g], d)
                        for g, d in zip(D["groups"], D["delta"])])
        mah = np.array([F.S_mahalanobis(inv[g], d)
                        for g, d in zip(D["groups"], D["delta"])])
        out[kind] = {"lit": lit, "mah": mah}
    return out, per_case_inv


def fold_dependent_inv(kind, train_ids, Sigma, rng):
    """Covariance replacements that may only use training-fold patients."""
    if kind == "population":
        pop = np.mean([Sigma[c] for c in train_ids], axis=0)
        return {c: np.linalg.inv(pop) for c in Sigma}
    if kind == "subject":
        donors = list(train_ids)
        inv = {}
        for c in Sigma:
            pool = [d for d in donors if d != c] or donors
            inv[c] = np.linalg.inv(Sigma[pool[rng.integers(len(pool))]])
        return inv
    raise ValueError(kind)


# --------------------------------------------------------------------- fitting
def cv_scores(X, y, groups, extra_fn=None, k=FOLDS, seed=SEED, fixed_lam=None):
    """Out-of-fold predictions. `extra_fn(train_ids)` returns an (n,1) extra
    column computed from training patients only.

    Returns BOTH the raw probability and a within-fold rank-normalised score.

    Harness bug 11 (found on calibration, fixed before confirmatory): pooling
    raw probabilities across folds corrupts the global ranking whenever folds
    differ in prevalence, because each fold carries its own intercept and
    standardisation. On the calibration set a single-feature model had a
    POSITIVE, stable coefficient and above-chance AUROC in all five folds, yet
    a pooled AUROC of 0.464 -- below chance -- purely because one fold had test
    prevalence 0.014 against 0.129 in training. Ranking within fold before
    pooling restores it (0.602 against a global 0.600).

    The rank transform is applied identically to every arm on identical folds,
    so it cannot move the M10-vs-M9 contrast in either direction.
    """
    oof = np.full(len(y), np.nan)
    oof_rank = np.full(len(y), np.nan)
    lams = []
    for tr, te in M.grouped_folds(groups, k, seed):
        Xf = X
        if extra_fn is not None:
            Xf = np.hstack([X, extra_fn(np.unique(groups[tr])).reshape(-1, 1)])
        if len(np.unique(y[tr])) < 2:
            oof[te] = y[tr].mean() if len(tr) else 0.5
            oof_rank[te] = 0.5
            continue
        if fixed_lam is not None:
            lam = fixed_lam
        else:
            lam, best = M.LAMBDAS[0], -np.inf
            for cand in M.LAMBDAS:
                ll = 0.0
                for itr, ite in M.grouped_folds(groups[tr], FOLDS, seed + 1):
                    if len(np.unique(y[tr][itr])) < 2:
                        continue
                    a, b = M._standardise(Xf[tr][itr], Xf[tr][ite])
                    w = M.fit_logistic(a, y[tr][itr], cand)
                    p = np.clip(M.predict_logistic(w, b), 1e-9, 1 - 1e-9)
                    yy = y[tr][ite]
                    ll += np.sum(yy * np.log(p) + (1 - yy) * np.log(1 - p))
                if ll > best:
                    best, lam = ll, cand
        lams.append(lam)
        a, b = M._standardise(Xf[tr], Xf[te])
        w = M.fit_logistic(a, y[tr], lam)
        p = M.predict_logistic(w, b)
        oof[te] = p
        oof_rank[te] = (M._rankdata(p) - 0.5) / len(p)
    return oof_rank, lams, oof


# --------------------------------------------------------------------- metrics
def summarise(y, s, lead, groups, p=None):
    """`s` is the within-fold rank score -- discrimination, false-alert rate and
    lead time. `p` is the raw probability -- calibration only, untransformed."""
    out = {"auroc": M.auroc(y, s), "auprc": M.auprc(y, s),
           "prevalence": float(y.mean())}
    if p is not None:
        out["brier"] = M.brier(y, p)
        sl, ic = M.calibration_slope(y, p)
        out["cal_slope"], out["cal_intercept"] = sl, ic
        out["net_benefit"] = {f"{t:.2f}": M.net_benefit(y, p, t)
                              for t in (0.05, 0.10, 0.20, 0.30)}
    for far in FAR_LEVELS:
        s_, thr = M.sens_at_far(y, s, far)
        out[f"sens@far{int(far*100)}"] = s_
        alerts = float((s >= thr).mean())
        out[f"alerts_per_hour@far{int(far*100)}"] = alerts * 60.0  # stride 60 s
        det = y == 1
        if det.any():
            hit = det & (s >= thr)
            out[f"lead_min@far{int(far*100)}"] = (
                float(np.nanmedian(lead[hit])) if hit.any() else np.nan)
    return out


def main(which="confirmatory"):
    t_start = time.time()
    rng = np.random.default_rng(SEED)
    cases, excl = load_all(which)
    D = assemble(cases)
    print(f"usable cases {len(cases)} | excluded {len(excl)} | "
          f"rows {len(D['groups'])}", flush=True)
    Scols, per_case_inv = s_columns(D, rng)

    report = {"n_cases": len(cases), "n_excluded": len(excl),
              "n_rows": int(len(D["groups"])),
              "exclusion_reasons": _tally(excl), "horizons": {}}

    for H in W.HORIZONS:
        hk = f"{H//60}min"
        keep = np.array([k[H] for k in D["keeps"]])
        y = np.array([lab[H] for lab in D["labels"]], float)[keep]
        g = D["groups"][keep]
        lead = D["lead"][keep]
        blocks = [b for b, kp in zip(D["blocks"], keep) if kp]
        ev_pat = len(np.unique(g[y == 1]))
        print(f"\n=== horizon {hk}: rows {len(y)} pos {int(y.sum())} "
              f"({y.mean():.4f}) event-patients {ev_pat} "
              f"of {len(np.unique(g))} ===", flush=True)

        X = {k: F.design(blocks, ks) for k, ks in F.SETS.items()}
        X9 = X["M9_strong_marginal"]
        X11 = F.design(blocks, F.M9 + ["cov"])

        scores, probs, lam_used = {}, {}, {}
        # unfitted raw scores
        scores["M3_max_z"] = F.design(blocks, ["maxz"]).ravel()
        scores["S_only_literal"] = Scols["patient"]["lit"][keep]
        scores["S_only_mahalanobis"] = Scols["patient"]["mah"][keep]
        # fitted marginal comparators
        for name, Xi in X.items():
            s, l, praw = cv_scores(Xi, y, g)
            scores[name] = s
            probs[name] = praw
            lam_used[name] = l
        s11, _, p11 = cv_scores(X11, y, g)
        scores["M11_marginal_plus_covdrift"] = s11
        probs["M11_marginal_plus_covdrift"] = p11
        # the incremental test
        for tag, key in (("M10_M9_plus_S", "lit"), ("M10b_M9_plus_Mahalanobis", "mah")):
            col = np.log1p(Scols["patient"][key][keep])
            s, l, praw = cv_scores(np.hstack([X9, col.reshape(-1, 1)]), y, g)
            scores[tag] = s
            probs[tag] = praw
            lam_used[tag] = l

        # ------------------------------------------------------------ ablations
        abl = {}
        for kind in COV_KINDS:
            if kind in ("patient", "diagonal", "identity", "shuffled"):
                col = np.log1p(Scols[kind]["lit"][keep])
                s, _, praw = cv_scores(np.hstack([X9, col.reshape(-1, 1)]), y, g)
                s_solo = Scols[kind]["lit"][keep]
            else:
                def mk(train_ids, kind=kind):
                    inv = fold_dependent_inv(kind, train_ids, D["Sigma"],
                                             np.random.default_rng(SEED))
                    return np.log1p(np.array(
                        [F.S_literal(inv[gg], d) for gg, d in
                         zip(D["groups"][keep], D["delta"][keep])]))
                s, _, praw = cv_scores(X9, y, g, extra_fn=mk)
                inv0 = fold_dependent_inv(kind, np.unique(g), D["Sigma"],
                                          np.random.default_rng(SEED))
                s_solo = np.array([F.S_literal(inv0[gg], d) for gg, d in
                                   zip(D["groups"][keep], D["delta"][keep])])
            abl[kind] = {"auroc_M9plusS": M.auroc(y, s),
                         "auprc_M9plusS": M.auprc(y, s),
                         "auroc_S_alone": M.auroc(y, s_solo)}
            scores[f"ABL_{kind}"] = s
            probs[f"ABL_{kind}"] = praw
            print(f"  ablation {kind:<11} AUROC(M9+S)={abl[kind]['auroc_M9plusS']:.4f} "
                  f"AUROC(S alone)={abl[kind]['auroc_S_alone']:.4f}", flush=True)

        # ------------------------------------------------------------ surrogate
        lam_fix = float(np.median(lam_used["M10_M9_plus_S"]))
        surr = []
        srng = np.random.default_rng(SEED + 7)
        dl = D["delta"][keep]
        gk = D["groups"][keep]
        base_delta_auprc = M.auprc(y, scores["M10_M9_plus_S"]) - \
            M.auprc(y, scores["M9_strong_marginal"])
        for _ in range(N_SURR):
            perm = srng.permutation(dl.shape[1])
            col = np.log1p(np.array(
                [F.S_literal(per_case_inv["patient"][gg], d[perm])
                 for gg, d in zip(gk, dl)]))
            s, _, _ = cv_scores(np.hstack([X9, col.reshape(-1, 1)]), y, g,
                                fixed_lam=lam_fix)
            surr.append(M.auprc(y, s) - M.auprc(y, scores["M9_strong_marginal"]))
        surr = np.array(surr)
        print(f"  surrogate dAUPRC: real={base_delta_auprc:+.5f} "
              f"surrogate mean={surr.mean():+.5f} p95={np.percentile(surr,95):+.5f}",
              flush=True)

        # -------------------------------------------------------------- metrics
        per_model = {k: summarise(y, v, lead, g, probs.get(k))
                     for k, v in scores.items()}
        key_models = ["M9_strong_marginal", "M10_M9_plus_S",
                      "M10b_M9_plus_Mahalanobis", "M11_marginal_plus_covdrift",
                      "M8_marginal_LR", "S_only_literal", "M3_max_z",
                      "ABL_diagonal", "ABL_population"]
        sub = {k: scores[k] for k in key_models if k in scores}
        ci_roc, draws_roc = M.patient_bootstrap(y, g, sub, M.auroc, N_BOOT, SEED)
        ci_prc, draws_prc = M.patient_bootstrap(y, g, sub, M.auprc, N_BOOT, SEED)
        deltas = {}
        for a in ("M10_M9_plus_S", "M10b_M9_plus_Mahalanobis",
                  "M11_marginal_plus_covdrift", "ABL_diagonal", "ABL_population"):
            deltas[a] = {
                "dAUROC": M.paired_delta_ci(draws_roc, a, "M9_strong_marginal"),
                "dAUPRC": M.paired_delta_ci(draws_prc, a, "M9_strong_marginal"),
                "dAUROC_bonf": M.paired_delta_ci(draws_roc, a,
                                                 "M9_strong_marginal", 0.05 / 3),
                "dAUPRC_bonf": M.paired_delta_ci(draws_prc, a,
                                                 "M9_strong_marginal", 0.05 / 3),
            }
        report["horizons"][hk] = {
            "n_rows": int(len(y)), "n_pos": int(y.sum()),
            "prevalence": float(y.mean()),
            "n_patients": int(len(np.unique(g))), "n_event_patients": int(ev_pat),
            "models": per_model, "ablations": abl,
            "ci_auroc": ci_roc, "ci_auprc": ci_prc, "deltas": deltas,
            "surrogate": {"real_dAUPRC": float(base_delta_auprc),
                          "mean": float(surr.mean()),
                          "p95": float(np.percentile(surr, 95)),
                          "p05": float(np.percentile(surr, 5)),
                          "n": int(N_SURR), "lambda_fixed": lam_fix},
            "lambda_chosen": {k: [float(x) for x in v] for k, v in lam_used.items()},
        }
        d = deltas["M10_M9_plus_S"]
        print(f"  M10-M9  dAUROC {d['dAUROC'][0]:+.4f} "
              f"[{d['dAUROC'][1]:+.4f},{d['dAUROC'][2]:+.4f}]   "
              f"dAUPRC {d['dAUPRC'][0]:+.5f} "
              f"[{d['dAUPRC'][1]:+.5f},{d['dAUPRC'][2]:+.5f}]", flush=True)

    report["elapsed_s"] = time.time() - t_start
    tag = which if THRESH_OVERRIDE is None else f"{which}_severe"
    out = os.path.join(RESULTS, f"sd_{tag}.json")
    json.dump(report, open(out, "w"), indent=1, default=float)
    print(f"\n-> {out}   ({report['elapsed_s']/60:.1f} min)")
    return report


def _tally(excl):
    t = {}
    for v in excl.values():
        k = "coverage" if "coverage" in v or "complete" in v else \
            "hypotension in baseline" if "hypotension" in v else \
            "analysable span" if "analysable" in v else v
        t[k] = t.get(k, 0) + 1
    return t


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "confirmatory")
