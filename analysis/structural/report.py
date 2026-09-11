"""
report.py -- render the confirmatory result and apply the FROZEN decision rule
from docs/PROTOCOL_STRUCTURAL_PREDICTION.md section 9, mechanically.
"""
from __future__ import annotations
import json, os, sys
import numpy as np

_H = os.path.dirname(__file__)
RESULTS = os.path.join(_H, "..", "results")
HK = ("5min", "10min", "15min")
MIN_EVENT_PATIENTS = 30
MIN_PREVALENCE = 0.01


def decide(R, C):
    """Return (status, per-criterion detail). Nothing here is negotiable."""
    d = {}
    # UNRESOLVED gate
    unres = [h for h in HK
             if R["horizons"][h]["n_event_patients"] < MIN_EVENT_PATIENTS
             or R["horizons"][h]["prevalence"] < MIN_PREVALENCE]
    d["underpowered_horizons"] = unres
    if len(unres) == len(HK):
        return "UNRESOLVED", d

    ok = {}
    for h in HK:
        hh = R["horizons"][h]
        dl = hh["deltas"]["M10_M9_plus_S"]
        prc, roc = dl["dAUPRC_bonf"], dl["dAUROC_bonf"]
        c1 = prc[0] > 0 and prc[1] > 0
        c2 = roc[0] > 0.01 and roc[1] > 0
        neg = prc[2] < 0                       # CI entirely below zero
        ok[h] = {"c1_auprc": c1, "c2_auroc": c2, "harmful": neg,
                 "dAUPRC": prc, "dAUROC": roc}
    d["per_horizon"] = ok
    n1 = sum(v["c1_auprc"] for v in ok.values())
    n2 = sum(v["c1_auprc"] and v["c2_auroc"] for v in ok.values())
    n_harm = sum(v["harmful"] for v in ok.values())

    if n_harm >= 2:
        return "FALSIFIED", d

    # criterion 3 -- patient-specific beats diagonal AND population
    c3 = {}
    for h in HK:
        if C is None or h not in C:
            c3[h] = None
            continue
        a = C[h]["dAUROC_patient_minus_diagonal"]
        b = C[h]["dAUROC_patient_minus_population"]
        c3[h] = bool(a[0] > 0 and a[1] > 0 and b[0] > 0 and b[1] > 0)
    d["c3_beats_diag_and_pop"] = c3

    # criterion 4 -- advantage destroyed by component permutation
    d["c4_surrogate"] = {h: bool(R["horizons"][h]["surrogate"]["real_dAUPRC"]
                                 > R["horizons"][h]["surrogate"]["p95"])
                         for h in HK}
    # criterion 5 -- calibration
    c5 = {}
    for h in HK:
        m = R["horizons"][h]["models"]
        b9, b10 = m["M9_strong_marginal"]["brier"], m["M10_M9_plus_S"]["brier"]
        sl = m["M10_M9_plus_S"]["cal_slope"]
        c5[h] = bool(b10 <= b9 + 0.005 and 0.8 <= sl <= 1.25)
    d["c5_calibration"] = c5
    # criterion 6 -- false-alert burden
    c6 = {}
    for h in HK:
        m = R["horizons"][h]["models"]
        c6[h] = bool(m["M10_M9_plus_S"]["sens@far10"] >=
                     m["M9_strong_marginal"]["sens@far10"])
    d["c6_false_alert"] = c6

    if n2 >= 2 and sum(bool(v) for v in c3.values()) >= 2 \
            and sum(d["c4_surrogate"].values()) >= 2 \
            and sum(c5.values()) >= 2 and sum(c6.values()) >= 2:
        return "SUPPORTED FOR INCREMENTAL PREDICTIVE VALUE", d
    if n2 >= 1:
        return "NOT SUPPORTED (narrow / exploratory signal at one horizon only)", d
    return "NOT SUPPORTED", d


def fmt(v, n=4):
    return "n/a" if v is None or (isinstance(v, float) and not np.isfinite(v)) \
        else f"{v:.{n}f}"


def main(which="confirmatory"):
    R = json.load(open(os.path.join(RESULTS, f"sd_{which}.json")))
    cp = os.path.join(RESULTS, f"sd_ablation_contrasts_{which}.json")
    C = json.load(open(cp)) if os.path.exists(cp) else None
    status, d = decide(R, C)

    L = ["# Structural displacement and prediction of deterioration — "
         f"{which} result", "",
         "Endpoint: intraoperative hypotension, `ART_MBP < 65 mmHg` for "
         "`>= 60 s`. Every window already containing hypotension is excluded, "
         "so this is prediction from a currently non-hypotensive state.", "",
         f"Usable cases **{R['n_cases']}** of 400 · excluded {R['n_excluded']} "
         f"({R['exclusion_reasons']}) · evaluation windows **{R['n_rows']}**", "",
         "## Verdict", "", f"# {status}", ""]

    L += ["## Power", "",
          "| horizon | windows | positives | prevalence | patients | with an event |",
          "|:--:|:--:|:--:|:--:|:--:|:--:|"]
    for h in HK:
        x = R["horizons"][h]
        L.append(f"| {h} | {x['n_rows']} | {x['n_pos']} | {x['prevalence']:.4f} "
                 f"| {x['n_patients']} | **{x['n_event_patients']}** |")

    L += ["", "## Primary comparison — M10 (M9 + S) vs M9 (marginals only)", "",
          "Bonferroni 95% CI over three horizons, patient-level bootstrap, "
          "2000 resamples of caseids.", "",
          "| horizon | AUROC M9 | AUROC M10 | ΔAUROC [CI] | AUPRC M9 | AUPRC M10 | ΔAUPRC [CI] |",
          "|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"]
    for h in HK:
        m = R["horizons"][h]["models"]
        dl = R["horizons"][h]["deltas"]["M10_M9_plus_S"]
        a, b = dl["dAUROC_bonf"], dl["dAUPRC_bonf"]
        L.append(f"| {h} | {fmt(m['M9_strong_marginal']['auroc'])} | "
                 f"{fmt(m['M10_M9_plus_S']['auroc'])} | "
                 f"**{a[0]:+.4f}** [{a[1]:+.4f}, {a[2]:+.4f}] | "
                 f"{fmt(m['M9_strong_marginal']['auprc'])} | "
                 f"{fmt(m['M10_M9_plus_S']['auprc'])} | "
                 f"**{b[0]:+.5f}** [{b[1]:+.5f}, {b[2]:+.5f}] |")

    L += ["", "## All comparators", ""]
    for h in HK:
        m = R["horizons"][h]["models"]
        L += [f"### {h}", "",
              "| model | AUROC | AUPRC | sens@5% FAR | sens@10% FAR | "
              "lead min | Brier | cal slope |", "|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"]
        for k in sorted(m, key=lambda k: -(m[k]["auroc"] or 0)):
            v = m[k]
            L.append(f"| {k} | {fmt(v['auroc'])} | {fmt(v['auprc'])} | "
                     f"{fmt(v.get('sens@far5'),3)} | {fmt(v.get('sens@far10'),3)} | "
                     f"{fmt(v.get('lead_min@far10'),1)} | "
                     f"{fmt(v.get('brier'))} | {fmt(v.get('cal_slope'),3)} |")
        L.append("")

    L += ["## Ablations — which covariance is used in S", "",
          "| horizon | " + " | ".join(k for k in R["horizons"]["5min"]["ablations"])
          + " |", "|:--:|" + ":--:|" * len(R["horizons"]["5min"]["ablations"])]
    for lab, field in (("AUROC of M9+S", "auroc_M9plusS"),
                       ("AUROC of S alone", "auroc_S_alone")):
        L.append(f"| **{lab}** |" + "|" * len(R["horizons"]["5min"]["ablations"]))
        for h in HK:
            ab = R["horizons"][h]["ablations"]
            L.append(f"| {h} | " + " | ".join(fmt(ab[k][field]) for k in ab) + " |")
    if C:
        L += ["", "### Criterion 3 — patient-specific vs diagonal and population", "",
              "| horizon | ΔAUROC patient − diagonal | ΔAUROC patient − population |",
              "|:--:|:--:|:--:|"]
        for h in HK:
            a = C[h]["dAUROC_patient_minus_diagonal"]
            b = C[h]["dAUROC_patient_minus_population"]
            L.append(f"| {h} | {a[0]:+.5f} [{a[1]:+.5f}, {a[2]:+.5f}] | "
                     f"{b[0]:+.5f} [{b[1]:+.5f}, {b[2]:+.5f}] |")

    L += ["", "## Surrogate — component permutation of δ against the same Σ₀", "",
          "| horizon | real ΔAUPRC | surrogate mean | surrogate p95 | real above p95? |",
          "|:--:|:--:|:--:|:--:|:--:|"]
    for h in HK:
        s = R["horizons"][h]["surrogate"]
        L.append(f"| {h} | {s['real_dAUPRC']:+.5f} | {s['mean']:+.5f} | "
                 f"{s['p95']:+.5f} | "
                 f"{'yes' if s['real_dAUPRC'] > s['p95'] else 'no'} |")

    L += ["", "## Frozen decision criteria", "",
          "| # | criterion | 5min | 10min | 15min |", "|:--:|---|:--:|:--:|:--:|"]
    pc = d.get("per_horizon", {})
    rows = [("1", "ΔAUPRC > 0, CI excludes 0",
             {h: pc[h]["c1_auprc"] for h in HK} if pc else {}),
            ("2", "ΔAUROC > 0.01, CI excludes 0",
             {h: pc[h]["c2_auroc"] for h in HK} if pc else {}),
            ("3", "patient-specific beats diagonal and population",
             d.get("c3_beats_diag_and_pop", {})),
            ("4", "advantage destroyed by permutation", d.get("c4_surrogate", {})),
            ("5", "no calibration penalty", d.get("c5_calibration", {})),
            ("6", "no false-alert penalty", d.get("c6_false_alert", {}))]
    for n, name, vals in rows:
        cells = " | ".join(
            ("—" if vals.get(h) is None else ("**yes**" if vals.get(h) else "no"))
            for h in HK)
        L.append(f"| {n} | {name} | {cells} |")

    L += ["", f"**Status: {status}**", "",
          "© 2026 Davarn Morrison · Transition Dynamics"]
    out = os.path.join(RESULTS, f"sd_{which}.md")
    open(out, "w").write("\n".join(L) + "\n")
    print("\n".join(L[:60]))
    print(f"\n-> {out}")
    return status


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "confirmatory")
