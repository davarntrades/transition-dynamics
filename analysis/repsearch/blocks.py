"""
blocks.py -- feature blocks for the representation search.

Imports the completed experiment's feature machinery unchanged and ADDS new
blocks. Nothing here alters the design matrix of any model already evaluated:
`design()` selects blocks by key, so a new key is invisible to old feature sets.
"""
from __future__ import annotations
import os, sys
import numpy as np

_S = os.path.join(os.path.dirname(__file__), "..", "structural")
sys.path.insert(0, _S)
import features as F            # noqa
import windows as W             # noqa
from cohort import SHORT        # noqa

P = len(SHORT)


def base_blocks(row, prep):
    """M9's blocks, plus elapsed time.

    Elapsed time belongs in the BASELINE, not in any candidate. Every
    persistence or trajectory quantity is bounded by time since the baseline
    window closed, so without this a candidate could win simply by proxying for
    'later in the case'. Putting it in the comparator closes that door.
    """
    b = F.row_blocks(row, prep)
    t = float(row["t_min"])
    b["elapsed"] = np.array([t, np.log1p(t)])
    return b


# M9 exactly as frozen in the completed experiment
M9 = list(F.M9)

CANDIDATE_BASELINES = {
    "B1_z":                 ["absz"],
    "B2_z_slope":           ["absz", "slope"],
    "B3_signed_slope":      ["signed", "slope"],
    "B4_signed_slope_disp": ["signed", "slope", "disp"],
    "B5_compact":           ["signed", "slope", "disp", "maxz", "aggz"],
    "B6_M9":                M9,
    "B7_M9_elapsed":        M9 + ["elapsed"],
    "B8_compact_elapsed":   ["signed", "slope", "disp", "maxz", "aggz", "elapsed"],
    "B9_B4_elapsed":        ["signed", "slope", "disp", "elapsed"],
    "B10_raw_only":         ["raw", "elapsed"],
}

BLOCK_WIDTH = {"raw": 2 * P, "signed": 2 * P, "absdelta": P, "absz": P,
               "disp": 2 * P, "slope": P, "aggz": 2, "maxz": 1,
               "cov": 3, "elapsed": 2}
