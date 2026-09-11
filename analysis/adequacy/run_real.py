"""
run_real.py — apply the preregistered protocol to whatever real recordings are
present in data/real/.

Refuses to analyse any recording that fails Stage A admissibility. That refusal
is the result, not a failure to try.
"""
from __future__ import annotations
import os, sys
import numpy as np

_H = os.path.dirname(__file__)
sys.path.insert(0, _H)
from real_loader import load_csv, derive_channels          # noqa: E402
from adequacy import (admissible, n_eff, MIN_NEFF_FACTOR,  # noqa: E402
                      MIN_CHANNELS, MIN_RECORDINGS)

BASE = os.path.join(_H, "..", "..", "data", "real")


def main() -> str:
    out, w = [], lambda s: out.append(s)
    w("# Real-data Stage A admissibility\n")
    w("Applies `docs/PROTOCOL_MODEL_ADEQUACY.md` Stage A to the real "
      "recordings reachable from this environment.\n")
    w("\n**Provenance.** Real human ECG/RSP/EDA at 100 Hz from the NeuroKit "
      "project, resting and event-related protocols in healthy adults. These "
      "contain **no clinical deterioration and no transition events**.\n")

    files = sorted(f for f in os.listdir(BASE) if f.endswith(".csv")) \
        if os.path.isdir(BASE) else []
    if not files:
        return "No recordings in data/real/."

    w("\n| recording | channels | n (1 Hz) | mean lag-1 AC | n_eff | required | admissible |")
    w("|---|:--:|:--:|:--:|:--:|:--:|:--:|")
    rows = []
    for f in files:
        names, X = derive_channels(load_csv(os.path.join(BASE, f)))
        ok, reasons = admissible(X, names)
        ac = np.mean([np.corrcoef(X[:-1, j], X[1:, j])[0, 1]
                      for j in range(X.shape[1])])
        rows.append((f, names, X, ok, reasons))
        w(f"| {f} | {len(names)} | {len(X)} | {ac:.3f} | {n_eff(X):.0f} "
          f"| {MIN_NEFF_FACTOR*X.shape[1]} | {'yes' if ok else '**no**'} |")

    w("\n## Exclusion reasons\n")
    for f, names, X, ok, reasons in rows:
        if not ok:
            w(f"\n**{f}** — excluded:")
            for r in reasons:
                w(f"\n- {r}")
            w("")

    # how much longer would the recording need to be?
    w("\n## How far short?\n")
    w("\n| recording | n_eff | needed | shortfall | recording length needed |")
    w("|---|:--:|:--:|:--:|:--:|")
    for f, names, X, ok, reasons in rows:
        ne, need = n_eff(X), MIN_NEFF_FACTOR * X.shape[1]
        factor = need / max(ne, 1e-9)
        w(f"| {f} | {ne:.0f} | {need} | {factor:.1f}× | "
          f"~{factor*len(X)/60:.0f} min at this channel set |")

    n_adm = sum(1 for r in rows if r[3])
    w(f"\n## Verdict\n")
    w(f"\nAdmissible recordings: **{n_adm}** of {len(rows)}. "
      f"Protocol requires **{MIN_RECORDINGS}** for any adequacy conclusion.\n")
    w("\n**Stage B and Stage C are not run.** Running them on inadmissible "
      "recordings would produce exactly the kind of confident, meaningless "
      "result this programme has already generated four times.\n")
    w("\nThe blocker is not access to *some* real physiology — that was "
      "obtained. The blocker is that the reachable recordings are minutes "
      "long, while the protocol needs hours of multichannel recording per "
      "patient with an observed transition. See "
      "`docs/DATA_REQUIREMENTS_REAL.md`.\n")
    return "\n".join(out)


if __name__ == "__main__":
    txt = main()
    os.makedirs(os.path.join(_H, "..", "results"), exist_ok=True)
    with open(os.path.join(_H, "..", "results", "real_stage_a.md"), "w") as fh:
        fh.write(txt)
    print(txt)
