"""Static/unit checks. No data access, no network, no outcomes."""
from __future__ import annotations
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import beats as BT

F = []
def chk(name, ok, det=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  {det}" if det else ""))
    if not ok: F.append(name)

rng = np.random.default_rng(0)
x = np.cumsum(rng.normal(size=600)) * 3 + 80          # non-constant series

# 1 injection identity at the base cadence with no quantisation
chk("inject(hold=2 s, quant=None) is the identity",
    np.array_equal(BT.inject(x, None, 2.0), x))

# 2 hold produces exactly (k-1)/k identical adjacent pairs
for h, k in ((4.0, 2), (6.0, 3), (8.0, 4)):
    y = BT.inject(x, None, h)
    frac = np.mean(np.diff(y) == 0)
    chk(f"hold {h:.0f}s gives implied hold fraction {1-1/k:.3f}",
        abs(frac - (1 - 1 / k)) < 0.01, f"observed {frac:.3f}")

# 3 quantisation lands on the grid and is bounded by half a step
y = BT.inject(x, 1.0, 2.0)
chk("quantisation rounds to the 1 mmHg grid", np.allclose(y, np.round(y)))
chk("quantisation error <= half a step", np.max(np.abs(y - x)) <= 0.5 + 1e-9)

# 4 injection never invents values where the source is missing
z = x.copy(); z[10:20] = np.nan
chk("missing source at a refresh instant stays missing",
    not np.isfinite(BT.inject(z, 1.0, 4.0)[10]))

# 5 injection is strictly downstream: it cannot change beat-derived input
a = BT.inject(x, 1.0, 4.0); b = BT.inject(x, 1.0, 4.0)
chk("injection is deterministic", np.array_equal(a, b, equal_nan=True))

# 6 lag1 sanity
chk("lag1 of white noise ~ 0", abs(BT.lag1(rng.normal(size=500))) < 0.15)
chk("lag1 of a held series is high", BT.lag1(BT.inject(x, None, 8.0)) > 0.8)

# 7 detector recovers a synthetic pulse train at a known rate
fs, hr = BT.FS, 75.0
t = np.arange(0, 120, 1 / fs)
w = 80 + 25 * np.maximum(0, np.sin(2 * np.pi * hr / 60 * t)) ** 2
bt = BT.detect_beats(w)
got = len(bt) / 2.0 if bt is not None else 0          # beats per minute over 2 min
chk("detector recovers a 75 bpm synthetic pulse train",
    bt is not None and abs(got - hr) < 5, f"detected {got:.1f} bpm")

# 8 bin_beats never interpolates
chk("empty bins stay NaN", np.isnan(BT.bin_beats(np.zeros((0, 5)), 10)).all())

print("\n" + ("ALL CHECKS PASSED" if not F else f"FAILURES: {F}"))
sys.exit(1 if F else 0)
