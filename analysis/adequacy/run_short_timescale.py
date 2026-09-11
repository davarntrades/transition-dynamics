"""
run_short_timescale.py — confirmatory test of H-ST.

Primary analysis is WITHIN channel across subjects. Channel-pooled figures are
reported only as a deliberately inflated comparator, per the protocol.
"""
from __future__ import annotations
import json, os, sys
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
from vitaldb_fetch import load_case                          # noqa
from st_cohort import split                                  # noqa
from short_timescale import (BANDS, DT, BASELINE_S, tau_ac1, tau_int,  # noqa
                             tau_hwhm, find_perturbations, tau_mrt,
                             tau_exp_free, tau_stretched)

MIN_SUBJ_BAND = 30
MIN_SUBJ_TOTAL = 50
ALPHA = 0.05 / 3           # Bonferroni over three bands


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 5:
        return np.nan
    ra = np.argsort(np.argsort(a[ok])).astype(float)
    rb = np.argsort(np.argsort(b[ok])).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    d = np.sqrt(np.dot(ra, ra) * np.dot(rb, rb))
    return float(np.dot(ra, rb) / d) if d > 0 else np.nan


def fisher_pool(rs, ns):
    rs = np.asarray(rs, float); ns = np.asarray(ns, float)
    ok = np.isfinite(rs) & (ns > 3)
    if not ok.any():
        return np.nan, (np.nan, np.nan)
    z = np.arctanh(np.clip(rs[ok], -0.999, 0.999))
    w = ns[ok] - 3
    zb = float(np.sum(w * z) / np.sum(w))
    se = float(1.0 / np.sqrt(np.sum(w)))
    from scipy.stats import norm
    q = norm.ppf(1 - ALPHA / 2)
    return float(np.tanh(zb)), (float(np.tanh(zb - q * se)),
                                float(np.tanh(zb + q * se)))


def extract(caseid):
    try:
        d = load_case(caseid)
    except Exception:
        return None
    X = d["X"]
    if X.size == 0 or len(d["channels"]) < 4:
        return None
    Xc = X[np.isfinite(X).all(axis=1)]
    nb = int(BASELINE_S / DT)
    if len(Xc) < nb + 3000:
        return None
    base, seg = Xc[:nb], Xc[nb:]
    rows = []
    for j, ch in enumerate(d["channels"]):
        b = base[:, j]
        if np.std(b) <= 0:
            continue
        pred = {"tau_int": tau_int(b), "tau_ac1": tau_ac1(b),
                "tau_hwhm": tau_hwhm(b), "sd": float(np.std(b))}
        for band, (lo, hi, W) in BANDS.items():
            mrt, fre, stre, amp = [], [], [], []
            for (i, lev, mad) in find_perturbations(seg[:, j], W):
                t = tau_mrt(seg[:, j], i, lev, W)
                if np.isfinite(t) and lo <= t <= hi:
                    mrt.append(t)
                    fre.append(tau_exp_free(seg[:, j], i, lev, W))
                    stre.append(tau_stretched(seg[:, j], i, lev, W))
                    amp.append(abs(seg[i, j] - lev))
            if mrt:
                rows.append({"caseid": caseid, "channel": ch, "band": band,
                             "tau_mrt": float(np.median(mrt)),
                             "tau_free": float(np.nanmedian(fre)) if np.any(np.isfinite(fre)) else np.nan,
                             "tau_stretch": float(np.nanmedian(stre)) if np.any(np.isfinite(stre)) else np.nan,
                             "amp": float(np.median(amp)), "n_ev": len(mrt),
                             **pred})
    return rows


def analyse(rows, band):
    R = [r for r in rows if r["band"] == band]
    chans = sorted({r["channel"] for r in R})
    out = {"n_subjects": len({r["caseid"] for r in R}),
           "n_events": int(sum(r["n_ev"] for r in R)), "per_channel": {}}
    rs, ns = [], []
    for ch in chans:
        S = [r for r in R if r["channel"] == ch]
        if len(S) < 5:
            continue
        x = [r["tau_int"] for r in S]; y = [r["tau_mrt"] for r in S]
        r_ = spearman(x, y)
        out["per_channel"][ch] = {"n": len(S), "rho": r_,
                                  "rho_ac1": spearman([r["tau_ac1"] for r in S], y),
                                  "rho_hwhm": spearman([r["tau_hwhm"] for r in S], y),
                                  "rho_free": spearman(x, [r["tau_free"] for r in S]),
                                  "rho_stretch": spearman(x, [r["tau_stretch"] for r in S]),
                                  "rho_amp": spearman([r["amp"] for r in S], y),
                                  "rho_sd": spearman([r["sd"] for r in S], y),
                                  "median_tau_mrt": float(np.median(y)),
                                  "median_tau_int": float(np.median(x))}
        rs.append(r_); ns.append(len(S))
    out["pooled_within"], out["ci"] = fisher_pool(rs, ns)
    # C6 surrogate: permute predictor across subjects within channel
    rng = np.random.default_rng(0)
    sur = []
    for _ in range(200):
        rr, nn = [], []
        for ch in chans:
            S = [r for r in R if r["channel"] == ch]
            if len(S) < 5:
                continue
            x = rng.permutation([r["tau_int"] for r in S])
            rr.append(spearman(x, [r["tau_mrt"] for r in S])); nn.append(len(S))
        v, _ = fisher_pool(rr, nn)
        if np.isfinite(v):
            sur.append(v)
    out["surrogate_mean"] = float(np.mean(sur)) if sur else np.nan
    out["surrogate_ci"] = [float(np.quantile(sur, .025)),
                           float(np.quantile(sur, .975))] if sur else [np.nan, np.nan]
    # C5 channel identity: correlation when channels are POOLED (inflated)
    out["pooled_across_channels"] = spearman([r["tau_int"] for r in R],
                                             [r["tau_mrt"] for r in R])
    # channel-mean-only predictor
    cm = {ch: np.median([r["tau_mrt"] for r in R if r["channel"] == ch]) for ch in chans}
    out["rho_channel_mean_only"] = spearman([cm[r["channel"]] for r in R],
                                            [r["tau_mrt"] for r in R])
    return out


def main() -> str:
    ids = split()["confirmatory"]
    rows = []
    for c in ids:
        r = extract(c)
        if r:
            rows.extend(r)
    res = {b: analyse(rows, b) for b in BANDS}
    json.dump({"rows": rows, "analysis": res},
              open(os.path.join(_H, "..", "results", "short_timescale.json"), "w"),
              indent=1, default=float)

    o, w = [], lambda s: o.append(s)
    w("# Short-timescale relaxation transfer — confirmatory result\n")
    w("Primary analysis is **within channel across subjects**. "
      "Channel-pooled figures are an inflated comparator, not the result.\n")
    n_tot = len({r["caseid"] for r in rows})
    w(f"\nSubjects screened: {len(ids)} · contributing at least one event: "
      f"**{n_tot}**\n")

    for band, (lo, hi, W) in BANDS.items():
        a = res[band]
        w(f"\n## Band {band} — τ ∈ [{lo:g}, {hi:g}] s, window {W:g} s\n")
        w(f"\nsubjects {a['n_subjects']} · events {a['n_events']}\n")
        if a["n_subjects"] < MIN_SUBJ_BAND:
            w(f"\n**UNRESOLVED** — fewer than {MIN_SUBJ_BAND} subjects.\n")
            continue
        w(f"\n| quantity | value | Bonferroni 95% CI |\n|---|:--:|:--:|")
        w(f"| **pooled within-channel ρ** | **{a['pooled_within']:+.3f}** | "
          f"[{a['ci'][0]:+.3f}, {a['ci'][1]:+.3f}] |")
        w(f"| surrogate (subject-permuted) | {a['surrogate_mean']:+.3f} | "
          f"[{a['surrogate_ci'][0]:+.3f}, {a['surrogate_ci'][1]:+.3f}] |")
        w(f"| channel-pooled (inflated) | {a['pooled_across_channels']:+.3f} | – |")
        w(f"| channel-identity-only predictor | {a['rho_channel_mean_only']:+.3f} | – |")
        w("\n### Per channel\n")
        w("\n| channel | n | ρ(τ_int) | ρ(τ_AC1) | ρ(τ_HWHM) | ρ(amp) | ρ(SD) | med τ_MRT | med τ_int |")
        w("|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|")
        for ch, v in a["per_channel"].items():
            w(f"| {ch.split('/')[-1]} | {v['n']} | **{v['rho']:+.2f}** | "
              f"{v['rho_ac1']:+.2f} | {v['rho_hwhm']:+.2f} | {v['rho_amp']:+.2f} "
              f"| {v['rho_sd']:+.2f} | {v['median_tau_mrt']:.1f} | {v['median_tau_int']:.1f} |")

    w("\n## Verdict\n")
    ok_bands = [b for b in BANDS
                if res[b]["n_subjects"] >= MIN_SUBJ_BAND
                and np.isfinite(res[b]["pooled_within"])
                and res[b]["pooled_within"] >= 0.30
                and res[b]["ci"][0] > 0
                and res[b]["surrogate_ci"][0] <= 0 <= res[b]["surrogate_ci"][1]]
    testable = [b for b in BANDS if res[b]["n_subjects"] >= MIN_SUBJ_BAND]
    if n_tot < MIN_SUBJ_TOTAL or not testable:
        v = "UNRESOLVED — insufficient subjects"
    elif len(ok_bands) >= 2:
        v = "SUPPORTED (narrow) — short-timescale relaxation transfer"
    elif len(ok_bands) == 1:
        v = f"RESTRICTED — holds only in band {ok_bands[0]}"
    else:
        v = "NOT SUPPORTED"
    w(f"\n### **{v}**\n")
    w(f"\nBands testable: {testable}. Bands meeting all criteria: {ok_bands}.\n")
    return "\n".join(o)


if __name__ == "__main__":
    txt = main()
    with open(os.path.join(_H, "..", "results", "short_timescale.md"), "w") as fh:
        fh.write(txt)
    print(txt)
