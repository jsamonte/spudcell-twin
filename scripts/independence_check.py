"""The assumption-free test: are the seven plasmids inherited independently?

This uses ONLY two numbers the preprint reports, and no free parameters:

  * the fraction of daughters retaining each plasmid individually (Fig. 3p / S33)
  * the fraction retaining all seven at once        (Fig. 3o, stated as 30%)

If inheritance of each plasmid were independent of the others, the second
follows from the first by multiplication. It does not have to be assumed, fitted
or simulated. Any gap is a measurement of how correlated plasmid retention is
inside a cell, and it needs no model of division at all.

    .venv\Scripts\python scripts\independence_check.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

# Fig. 3p / Fig. S33, after 5 generations, n = 95 single cells.
# aHL is stated numerically in SI section 6 ("71% cells analyzed"); the rest are
# read off the bar chart and carry roughly +/-3 points.
RETENTION = {
    "aHL":    0.71,   # SI section 6, stated
    "T7RNAP": 0.68,
    "GFP":    0.63,
    "pREP":   0.63,
    "pLD2":   0.57,
    "pLD3":   0.56,
    "pLD1":   0.52,
}

OBSERVED_COMPLETE = 0.30   # Results p. 6; Fig. 3o, 3p
N_CELLS = 95               # Methods 23


def main():
    product = 1.0
    for p in RETENTION.values():
        product *= p

    ratio = OBSERVED_COMPLETE / product

    # How far off would the per-plasmid numbers have to be to rescue
    # independence? If every plasmid were retained at rate q, independence
    # would need q**7 == 0.30.
    q_needed = OBSERVED_COMPLETE ** (1 / 7)

    print("Per-plasmid retention after 5 generations (Fig. 3p):")
    for name, p in sorted(RETENTION.items(), key=lambda kv: -kv[1]):
        print(f"  {name:8} {p:.0%}")
    print(f"\n  mean retention                         {sum(RETENTION.values())/7:.1%}")
    print(f"  P(all 7) IF independent  = product    = {product:.4f}  ({product:.1%})")
    print(f"  P(all 7) OBSERVED        (Fig. 3o)    = {OBSERVED_COMPLETE:.4f}  ({OBSERVED_COMPLETE:.0%})")
    print(f"\n  observed / independent                = {ratio:.1f}x")
    print(f"\n  for independence to hold, every plasmid would need to be")
    print(f"  retained at {q_needed:.1%} -- against a measured mean of "
          f"{sum(RETENTION.values())/7:.1%}")

    # Expected count of complete cells under independence, out of 95.
    expected = product * N_CELLS
    observed = OBSERVED_COMPLETE * N_CELLS
    print(f"\n  out of {N_CELLS} single cells: independence predicts "
          f"{expected:.1f} complete, {observed:.0f} were seen")

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independence_check.json").write_text(json.dumps({
        "source": "Gaut et al. 2026, bioRxiv 2026.07.01.735724, Fig. 3o and 3p",
        "retention": RETENTION,
        "n_cells": N_CELLS,
        "p_all_seven_if_independent": round(product, 6),
        "p_all_seven_observed": OBSERVED_COMPLETE,
        "ratio_observed_over_independent": round(ratio, 3),
        "retention_needed_for_independence": round(q_needed, 4),
        "expected_complete_cells": round(expected, 2),
        "observed_complete_cells": round(observed, 1),
    }, indent=2) + "\n")
    print("\nWrote results/independence_check.json")


if __name__ == "__main__":
    main()
