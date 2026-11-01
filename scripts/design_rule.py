"""The inheritance cost of splitting a synthetic genome across replicons.

The headline comparison in `independence_check.py` is about one published
experiment. This script asks the general question behind it, which a group
designing a synthetic genome can act on:

  if a genome is divided across N separate replicons with no segregation
  machinery, how many copies of each are needed for a lineage to still hold
  a complete set after G generations?

Every number comes from the closed-form model in `src/inheritance.py`, which
is covered by unit tests. Nothing here is fitted.

Run:  .venv/Scripts/python scripts/design_rule.py
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

try:
    from inheritance import complete_set_probability, copies_needed_for
except ImportError:  # package layout
    from src.inheritance import complete_set_probability, copies_needed_for

OUT = ROOT / "results" / "design_rule.json"

GENERATIONS = 5
REPLICONS = list(range(1, 13))
TARGETS = [0.5, 0.9]
COPY_NUMBERS = [2, 3, 4, 5, 6, 8]


def over_generations(n, c, g=GENERATIONS):
    """A lineage stays complete through g successive divisions."""
    return complete_set_probability(n, c) ** g


def main():
    res = {
        "generations": GENERATIONS,
        "model": "src/inheritance.py, closed form, no fitted parameters",
        "question": (
            "How many copies of each replicon does a genome split across N "
            "replicons need, for a lineage to hold a complete set after "
            f"{GENERATIONS} generations of random partitioning?"
        ),
    }

    # --- the design rule: copies needed, by replicon count and target ---
    rule = {}
    for target in TARGETS:
        per_division = target ** (1.0 / GENERATIONS)
        rule[str(target)] = {
            "overall_target": target,
            "per_division_target": round(per_division, 6),
            "copies_needed": {
                str(n): copies_needed_for(per_division, n) for n in REPLICONS
            },
        }
    res["design_rule"] = rule

    # --- the cost of splitting: completeness against N at fixed copy number ---
    cost = {}
    for c in COPY_NUMBERS:
        cost[str(c)] = {str(n): round(over_generations(n, c), 6) for n in REPLICONS}
    res["completeness_by_replicons"] = cost

    # --- a single replicon is the reference: what does splitting cost? ---
    penalty = {}
    for c in COPY_NUMBERS:
        one = over_generations(1, c)
        penalty[str(c)] = {
            str(n): (round(over_generations(n, c) / one, 6) if one > 0 else None)
            for n in REPLICONS
        }
    res["fraction_of_single_replicon"] = penalty

    # --- where the published system sits ---
    res["gaut_2026"] = {
        "n_replicons": 7,
        "observed_complete_after_5_generations": 0.30,
        "copies_implied": copies_needed_for(0.30 ** (1.0 / GENERATIONS), 7),
        "copies_loaded_at_t0": 2.6,
        "note": (
            "The copy number the observation implies, against the number "
            "loaded at the start. The gap is the paper's open question."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")

    print(f"Copies of each replicon needed to stay complete through "
          f"{GENERATIONS} generations\n")
    print(f"{'replicons':>10} " + "".join(f"{'>=' + str(int(100*t)) + '%':>10}"
                                          for t in TARGETS))
    for n in REPLICONS:
        row = "".join(f"{rule[str(t)]['copies_needed'][str(n)]:>10}" for t in TARGETS)
        print(f"{n:>10} {row}")

    print(f"\n\nCompleteness after {GENERATIONS} generations, by copy number\n")
    hdr = "".join(f"{'c=' + str(c):>9}" for c in COPY_NUMBERS)
    print(f"{'replicons':>10}{hdr}")
    for n in REPLICONS:
        row = "".join(f"{cost[str(c)][str(n)]:>9.3f}" for c in COPY_NUMBERS)
        print(f"{n:>10}{row}")

    g = res["gaut_2026"]
    print(f"\n\nGaut et al. (2026): {g['n_replicons']} replicons, "
          f"{g['observed_complete_after_5_generations']:.0%} complete after "
          f"{GENERATIONS} generations")
    print(f"  implies ~{g['copies_implied']} copies each, "
          f"against {g['copies_loaded_at_t0']} loaded at t = 0")
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
