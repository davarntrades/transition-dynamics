"""
suite_report.py -- print the Markdown tables of docs/VT_VF_FALSIFICATION_SUITE.md
from analysis/results/vtvf_falsification_suite.json (no recomputation).

Run: python3 analysis/vtvf/suite_report.py
"""
from __future__ import annotations

import json

IN = "analysis/results/vtvf_falsification_suite.json"
SHORT = {"pshape_hp": "pshape", "shape_hp": "shape_hp", "shape_raw": "shape_raw", "td3": "td3",
         "dG_hp": "dG_hp", "corrFrob_hp": "corrFrob", "meanabsr_hp": "meanabsr", "logdet_hp": "logdet",
         "diagAIRM_hp": "diagAIRM", "covFrob_hp": "covFrob", "conv_hr": "conv_hr", "conv_sdnn": "conv_sdnn"}
ORDER = ("null", "conventional", "acquisition", "positive", "subgroup")


def main():
    r = json.load(open(IN))
    S, fam, stats = r["studies"], r["meta"]["families"], r["meta"]["stats"]
    for setn in ("selection", "holdout"):
        scens = sorted({k.split("|")[1] for k in S if k.startswith(setn + "|")},
                       key=lambda s: (ORDER.index(fam[s]), s))
        print(f"\n#### {setn} set: rate of any positive structure-specific verdict, n = 80 "
              f"(EXPLORATORY rate in brackets for null scenarios)\n")
        print("| family | scenario | " + " | ".join(SHORT[s] for s in stats) + " |")
        print("|---|---|" + "---:|" * len(stats))
        for s in scens:
            cells = []
            for st in stats:
                c = S[f"{setn}|{s}|{st}|n80"]
                v = f"{c['any_positive']:.3f}"
                if fam[s] == "null":
                    v += f" ({c['exploratory']:.3f})"
                bad = (fam[s] == "null" and (c["exploratory"] > 0.01 or c["any_positive"] > 0.02)) or \
                      (fam[s] in ("conventional", "acquisition") and c["any_positive"] > 0.02)
                cells.append(f"**{v}**" if bad else v)
            print(f"| {fam[s]} | {s} | " + " | ".join(cells) + " |")
        print("\nBold = violates the pre-specified admissibility bound (A1-A3).")
    print("\n#### Admissibility\n")
    print("| statistic | selection | holdout |")
    print("|---|---|---|")
    for st in stats:
        a, b = r["admissibility"][f"selection|{st}"], r["admissibility"][f"holdout|{st}"]
        print(f"| {st} | {'PASS' if a['admissible'] else 'FAIL: ' + ', '.join(a['failures'])} | "
              f"{'PASS' if b['admissible'] else 'FAIL: ' + ', '.join(b['failures'])} |")
    print("\n#### Coverage of the 95% t-interval, n = 40 (B5, B10, B15, B30)\n")
    print("| statistic | sel. null | sel. corr0.10 | hold. null | hold. corr0.10 |")
    print("|---|---|---|---|---|")
    for st in stats:
        row = []
        for k in ("selection|null", "selection|corr0.10", "holdout|null", "holdout|corr0.10"):
            row.append(" / ".join(f"{v:.3f}" for v in r["coverage_n40"][f"{k}|{st}"].values()))
        print(f"| {st} | " + " | ".join(row) + " |")


if __name__ == "__main__":
    main()
