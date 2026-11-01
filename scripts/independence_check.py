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
import sys
from pathlib import Path

from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.inheritance import complete_set_probability  # noqa: E402

RESULTS = ROOT / "results"

GENERATIONS = 5            # Fig. 3; Methods 11
COPIES_AT_LOAD = 2.65      # 2.5 nM x 1.06 copies/nM, Methods 3 + Table S8

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
    observed_n = round(OBSERVED_COMPLETE * N_CELLS)
    print(f"\n  out of {N_CELLS} single cells: independence predicts "
          f"{expected:.1f} complete, {observed_n} were seen")

    # Is that gap bigger than sampling noise? The counts are the only thing
    # that can carry a p-value here: 95 cells, each complete or not, against
    # the rate independence predicts.
    # One-sided, because the question is whether fidelity EXCEEDS what chance
    # allows. The interval is taken two-sided, so it reports the uncertainty on
    # the observed rate rather than a bound implied by the test direction.
    # Six of the seven rates are read off a bar chart. Pushing every read
    # value to the top of its +/-3 point band is the reading most favourable
    # to independence, so the p-value there is the one worth quoting.
    FIGURE_READ_TOLERANCE = 0.03
    STATED_NUMERICALLY = {"aHL"}          # SI section 6
    product_hi = 1.0
    for name, p in RETENTION.items():
        product_hi *= p if name in STATED_NUMERICALLY else min(
            1.0, p + FIGURE_READ_TOLERANCE)

    test = stats.binomtest(observed_n, N_CELLS, product, alternative="greater")
    test_hi = stats.binomtest(observed_n, N_CELLS, product_hi,
                              alternative="greater")
    ci = stats.binomtest(observed_n, N_CELLS, product).proportion_ci(
        confidence_level=0.95)
    print(f"\n  binomial test, {observed_n}/{N_CELLS} against p={product:.4f}:")
    print(f"    p-value = {test.pvalue:.3e}")
    print(f"    observed rate {observed_n / N_CELLS:.1%} "
          f"(95% CI {ci.low:.1%}-{ci.high:.1%}) vs predicted {product:.1%}")
    print(f"\n  most favourable reading of Fig. 3p (+{FIGURE_READ_TOLERANCE:.0%} "
          f"on each read value):")
    print(f"    independence predicts {product_hi:.1%}, ratio "
          f"{OBSERVED_COMPLETE / product_hi:.1f}x, p = {test_hi.pvalue:.1e}")

    # One physical explanation needs no correlation at all: more than one copy
    # of each plasmid at the moment of division. Phi29 replicates continuously
    # with no checkpoint, so copy number at division is NOT the ~2.7 copies
    # loaded at t=0. How many copies would independent partitioning need?
    print("\n  if instead each plasmid were present in c copies at division,")
    print("  independent partitioning alone would give:")
    single = {}
    for c in (1, 2, 3, 4, 5):
        p1 = complete_set_probability(7, copy_number=c)
        single[c] = p1
        print(f"    c={c}  single division {p1:.4f}   "
              f"over {GENERATIONS} generations {p1 ** GENERATIONS:.4f}")

    # Copies needed so that surviving 5 independent divisions gives 30%.
    per_gen_target = OBSERVED_COMPLETE ** (1 / GENERATIONS)
    copies_needed = None
    c = 1.0
    while c < 60:
        if complete_set_probability(7, copy_number=int(round(c))) >= per_gen_target:
            copies_needed = int(round(c))
            break
        c += 1
    print(f"\n  to reach {OBSERVED_COMPLETE:.0%} after {GENERATIONS} generations a cell "
          f"needs {per_gen_target:.1%} per division,")
    print(f"  which independent partitioning reaches at c = {copies_needed} copies "
          f"(vs {COPIES_AT_LOAD:.1f} loaded at t=0)")
    print("\n  So the gap does NOT prove correlated partitioning: continuous")
    print("  replication to ~2x the loaded copy number would also explain it.")
    print("  Distinguishing the two needs per-cell copy number at division,")
    print("  which the preprint does not report. See docs/PARAMETERS.md.")

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independence_check.json").write_text(json.dumps({
        "source": "Gaut et al. 2026, bioRxiv 2026.07.01.735724, Fig. 3o and 3p",
        "retention": RETENTION,
        "n_plasmids": 7,
        "n_cells": N_CELLS,
        "generations": GENERATIONS,
        "mean_retention": round(sum(RETENTION.values()) / 7, 4),
        "p_all_seven_if_independent": round(product, 6),
        "p_all_seven_observed": OBSERVED_COMPLETE,
        "ratio_observed_over_independent": round(ratio, 3),
        "retention_needed_for_independence": round(q_needed, 4),
        "expected_complete_cells": round(expected, 2),
        "observed_complete_cells": observed_n,
        "binomial_p_value": float(test.pvalue),
        "figure_read_tolerance": FIGURE_READ_TOLERANCE,
        "p_all_seven_if_independent_favourable": round(product_hi, 6),
        "ratio_favourable": round(OBSERVED_COMPLETE / product_hi, 3),
        "binomial_p_value_favourable": float(test_hi.pvalue),
        "observed_rate": round(observed_n / N_CELLS, 4),
        "observed_rate_ci95": [round(ci.low, 4), round(ci.high, 4)],
        "copies_at_load": COPIES_AT_LOAD,
        "single_division_by_copy_number": {
            str(c): round(p, 6) for c, p in single.items()},
        "five_generations_by_copy_number": {
            str(c): round(p ** GENERATIONS, 6) for c, p in single.items()},
        "per_generation_target": round(per_gen_target, 4),
        "copies_needed_for_observed": copies_needed,
    }, indent=2) + "\n")
    print("\nWrote results/independence_check.json")


if __name__ == "__main__":
    main()
