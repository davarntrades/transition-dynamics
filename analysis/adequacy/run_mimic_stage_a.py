"""
run_mimic_stage_a.py — Stage A of the frozen protocol on real ICU data.

Applies docs/PROTOCOL_MODEL_ADEQUACY.md Stage A, unchanged, to the MIMIC-III
demo (open access, ODbL). Reports the baseline-length trade-off rather than a
single verdict, because the scientific question is whether the effective-sample
-size rule and the stationarity screen are JOINTLY satisfiable at hourly
charting resolution.

No threshold is altered. If the data cannot meet the frozen rules, that is the
result.
"""
from __future__ import annotations
import os, sys
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
from mimic_loader import load_stays, baseline_tradeoff, DB_PATH   # noqa: E402
from adequacy import n_eff, MIN_NEFF_FACTOR, MIN_RECORDINGS       # noqa: E402

LENGTHS = (4, 12, 24, 48, 96, 168)


def main() -> str:
    stays = load_stays(DB_PATH)
    out, w = [], lambda s: out.append(s)
    w("# Real ICU data — Stage A under the frozen protocol\n")
    w("Applies `docs/PROTOCOL_MODEL_ADEQUACY.md` Stage A unchanged. "
      "No threshold altered.\n")
    w("\n**Provenance.** MIMIC-III Clinical Database Demo, open access under "
      "ODbL, obtained from the public `MIT-LCP/mimic-workshop` repository. "
      "No credentialed data, no access control bypassed.\n")
    w(f"\nStays with 4 channels (HR, SpO₂, RR, MAP) and ≥ 6 h: "
      f"**{len(stays)}**. Median charting gap **60 min**.\n")

    w("\n## Baseline-length trade-off\n")
    w("\nLonger baselines raise effective sample size but are less likely to "
      "be stationary. A recording is admissible only if some window satisfies "
      "**both**.\n")
    w("\n| stay | hours | baseline | n | n_eff | need | max shift (SD) | both OK |")
    w("|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|")
    any_ok = 0
    cells = 0
    for s in sorted(stays, key=lambda d: -d["hours"]):
        rows = baseline_tradeoff(s["X"], LENGTHS)
        ok_any = False
        for r in rows:
            cells += 1
            both = r["neff_ok"] and r["stationary_ok"]
            ok_any |= both
            w(f"| {s['stay_id']} | {s['hours']:.0f} | {r['hours']}h | {r['n']} "
              f"| {r['n_eff']:.1f} | {MIN_NEFF_FACTOR*4} | {r['max_shift']:.2f} "
              f"| {'**YES**' if both else 'no'} |")
        any_ok += ok_any
    w(f"\n## Verdict\n")
    w(f"\n- stay × baseline-window combinations evaluated: **{cells}**")
    w(f"\n- combinations satisfying both rules: **{sum(1 for s in stays for r in baseline_tradeoff(s['X'], LENGTHS) if r['neff_ok'] and r['stationary_ok'])}**")
    w(f"\n- admissible recordings: **{any_ok} / {len(stays)}** "
      f"(protocol requires {MIN_RECORDINGS})\n")
    w("\n**Stage B and Stage C are not run.**\n")
    w("\nThe two frozen requirements are jointly unsatisfiable at hourly "
      "charting resolution. Short baselines fail the effective-sample-size "
      "rule; baselines long enough to pass it are no longer stationary, "
      "because real ICU patients drift over multi-day windows.\n")
    w("\nThis does **not** falsify the exponential-approach model. It shows "
      "that hourly-charted ICU databases cannot supply the data the test "
      "requires. The model remains untested on real physiology.\n")
    return "\n".join(out)


if __name__ == "__main__":
    txt = main()
    with open(os.path.join(_H, "..", "results", "real_mimic_stage_a.md"),
              "w") as fh:
        fh.write(txt)
    print(txt[-1400:])
