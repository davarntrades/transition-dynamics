"""
models.py -- L2 logistic regression (IRLS), grouped CV, and metrics.
numpy/scipy only, so the harness has no hidden library behaviour.
"""
from __future__ import annotations
import numpy as np


# ----------------------------------------------------------------- regression
def fit_logistic(X, y, lam, max_iter=100, tol=1e-8):
    """Ridge-penalised logistic regression by IRLS. The intercept is the
    appended column of ones and is NOT penalised."""
    n, p = X.shape
    A = np.hstack([np.ones((n, 1)), X])
    w = np.zeros(p + 1)
    pen = np.eye(p + 1) * lam
    pen[0, 0] = 0.0
    for _ in range(max_iter):
        eta = np.clip(A @ w, -30, 30)
        mu = 1.0 / (1.0 + np.exp(-eta))
        s = np.clip(mu * (1 - mu), 1e-6, None)
        z = eta + (y - mu) / s
        H = A.T @ (A * s[:, None]) + pen
        g = A.T @ (s * z)
        try:
            w_new = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            w_new = np.linalg.lstsq(H, g, rcond=None)[0]
        if np.max(np.abs(w_new - w)) < tol:
            w = w_new
            break
        w = w_new
    return w


def predict_logistic(w, X):
    eta = np.clip(np.hstack([np.ones((X.shape[0], 1)), X]) @ w, -30, 30)
    return 1.0 / (1.0 + np.exp(-eta))


# ------------------------------------------------------------------- CV plumbing
def grouped_folds(groups, k, seed=0):
    """Deterministic patient-level folds: every row of a group lands together."""
    uniq = np.unique(groups)
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(uniq))
    assign = {g: order[i] % k for i, g in enumerate(uniq)}
    fold = np.array([assign[g] for g in groups])
    return [(np.flatnonzero(fold != f), np.flatnonzero(fold == f))
            for f in range(k)]


LAMBDAS = np.geomspace(1e-2, 1e3, 11)


def _standardise(Xtr, Xte):
    m = Xtr.mean(axis=0)
    s = Xtr.std(axis=0)
    s[s < 1e-12] = 1.0
    return (Xtr - m) / s, (Xte - m) / s


def cv_predict(X, y, groups, k=5, seed=0, lambdas=LAMBDAS, inner_k=5):
    """Out-of-fold probabilities. Lambda is chosen by INNER grouped CV inside
    the training folds only -- the outer test fold is never seen while fitting."""
    oof = np.full(len(y), np.nan)
    chosen = []
    for tr, te in grouped_folds(groups, k, seed):
        if len(np.unique(y[tr])) < 2:
            oof[te] = y[tr].mean() if len(tr) else 0.5
            continue
        best, best_ll = lambdas[0], -np.inf
        inner = grouped_folds(groups[tr], inner_k, seed + 1)
        for lam in lambdas:
            ll = 0.0
            for itr, ite in inner:
                if len(np.unique(y[tr][itr])) < 2:
                    continue
                a, b = _standardise(X[tr][itr], X[tr][ite])
                w = fit_logistic(a, y[tr][itr], lam)
                p = np.clip(predict_logistic(w, b), 1e-9, 1 - 1e-9)
                yy = y[tr][ite]
                ll += np.sum(yy * np.log(p) + (1 - yy) * np.log(1 - p))
            if ll > best_ll:
                best_ll, best = ll, lam
        chosen.append(best)
        a, b = _standardise(X[tr], X[te])
        w = fit_logistic(a, y[tr], best)
        oof[te] = predict_logistic(w, b)
    return oof, chosen


# ----------------------------------------------------------------------- metrics
def auroc(y, s):
    y = np.asarray(y); s = np.asarray(s)
    n1, n0 = y.sum(), (1 - y).sum()
    if n1 == 0 or n0 == 0:
        return np.nan
    r = _rankdata(s)
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def _rankdata(a):
    a = np.asarray(a, float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), float)
    sa = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def auprc(y, s):
    """Average precision -- the step-wise estimator, which does not
    interpolate and so does not overstate a sparse positive class."""
    y = np.asarray(y); s = np.asarray(s)
    if y.sum() == 0:
        return np.nan
    o = np.argsort(-s, kind="mergesort")
    ys = y[o]
    tp = np.cumsum(ys)
    prec = tp / np.arange(1, len(ys) + 1)
    return float(np.sum(prec * ys) / y.sum())


def sens_at_far(y, s, far):
    """Sensitivity at a window-level false-alert rate among true negatives."""
    y = np.asarray(y); s = np.asarray(s)
    neg = s[y == 0]
    if len(neg) == 0 or y.sum() == 0:
        return np.nan, np.nan
    thr = np.quantile(neg, 1 - far)
    return float((s[y == 1] >= thr).mean()), float(thr)


def brier(y, p):
    return float(np.mean((np.asarray(p) - np.asarray(y)) ** 2))


def calibration_slope(y, p):
    """Logistic recalibration of the logit. Slope 1 / intercept 0 is perfect."""
    p = np.clip(np.asarray(p, float), 1e-6, 1 - 1e-6)
    X = np.log(p / (1 - p))[:, None]
    w = fit_logistic(X, np.asarray(y, float), lam=1e-9)
    return float(w[1]), float(w[0])


def net_benefit(y, p, thr):
    y = np.asarray(y); p = np.asarray(p)
    n = len(y)
    alert = p >= thr
    tp = np.sum(alert & (y == 1)); fp = np.sum(alert & (y == 0))
    return (tp / n) - (fp / n) * (thr / (1 - thr))


def patient_bootstrap(y, groups, scores_by_model, stat, n_boot=2000, seed=0):
    """Resample PATIENTS with replacement; recompute the statistic on the
    resampled rows. Returns {model: (point, lo, hi)} and paired differences."""
    rng = np.random.default_rng(seed)
    uniq = np.unique(groups)
    idx_by_g = {g: np.flatnonzero(groups == g) for g in uniq}
    names = list(scores_by_model)
    point = {m: stat(y, scores_by_model[m]) for m in names}
    draws = {m: [] for m in names}
    for _ in range(n_boot):
        gs = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([idx_by_g[g] for g in gs])
        yy = y[idx]
        if yy.sum() == 0 or yy.sum() == len(yy):
            continue
        for m in names:
            draws[m].append(stat(yy, scores_by_model[m][idx]))
    out = {}
    for m in names:
        d = np.array(draws[m], float)
        d = d[np.isfinite(d)]
        out[m] = (point[m], float(np.percentile(d, 2.5)),
                  float(np.percentile(d, 97.5)))
    return out, {m: np.array(draws[m], float) for m in names}


def paired_delta_ci(draws, a, b, alpha=0.05):
    """CI for stat(a) - stat(b) from the SAME bootstrap resamples -- paired,
    so the patient-level correlation between models is carried correctly."""
    da, db = draws[a], draws[b]
    n = min(len(da), len(db))
    d = da[:n] - db[:n]
    d = d[np.isfinite(d)]
    return (float(np.mean(d)), float(np.percentile(d, 100 * alpha / 2)),
            float(np.percentile(d, 100 * (1 - alpha / 2))))
