"""Prespecified SECONDARY endpoint: MAP < 55 mmHg for >= 60 s.
Identical harness, identical split, identical models. Only the endpoint moves."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import run_confirmatory as R, windows as W
R.THRESH_OVERRIDE = W.MAP_SEVERE
if __name__ == "__main__":
    R.main("confirmatory")
