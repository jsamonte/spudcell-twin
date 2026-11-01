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

#: A rule quoted at one horizon is not a rule. Five generations is what the
#: source reports, so it leads, but the requirement has to be shown growing
#: with the horizon or a reader cannot tell whether it is a general result.
HORIZONS = [1, 5, 10, 20]

#: `src/inheritance.py` takes the partition probability as 0.5 by default and
#: warns in its own docstring that bioscrape's splitter does not: it draws
#: p ~ Uniform(0.5 - nu/2, 0.5) with nu = 0.5, so one daughter is
#: systematically the smaller. Reporting only the symmetric case would quote
#: the optimistic end of the model without saying so.
NOISE_LEVELS = [0.0, 0.25, 0.5]


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

    # --- how the requirement grows with the horizon ---
    horizon = {}
    for g in HORIZONS:
        per_division = 0.5 ** (1.0 / g)
        horizon[str(g)] = {
            "per_division_target": round(per_division, 6),
            "copies_needed": {
                str(n): copies_needed_for(per_division, n) for n in REPLICONS
            },
        }
    res["horizon_sensitivity"] = {
        "target": 0.5,
        "note": "Copies needed for 50% complete lineages after g generations.",
        "by_generations": horizon,
    }

    # --- how much the symmetric-partition assumption is worth ---
    noise = {}
    for nu in NOISE_LEVELS:
        per_division = 0.5 ** (1.0 / GENERATIONS)
        noise[str(nu)] = {
            "p_range": [0.5 - nu / 2, 0.5],
            "copies_needed": {
                str(n): copies_needed_for(per_division, n, noise=nu)
                for n in REPLICONS
            },
        }
    res["noise_sensitivity"] = {
        "target": 0.5,
        "generations": GENERATIONS,
        "note": (
            "Copies needed when the partition probability is not fixed at "
            "0.5 but drawn from Uniform(0.5 - nu/2, 0.5), as bioscrape's "
            "LineageVolumeSplitter does. nu = 0.5 is its default."
        ),
        "by_noise": noise,
    }

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

    print("\n\nCopies needed for 50% complete, by horizon\n")
    hdr = "".join(f"{'g=' + str(g):>8}" for g in HORIZONS)
    print(f"{'replicons':>10}{hdr}")
    for n in REPLICONS:
        row = "".join(f"{horizon[str(g)]['copies_needed'][str(n)]:>8}"
                      for g in HORIZONS)
        print(f"{n:>10}{row}")

    print("\n\nCopies needed for 50% complete over "
          f"{GENERATIONS} generations, by partition asymmetry\n")
    hdr = "".join(f"{'nu=' + str(nu):>10}" for nu in NOISE_LEVELS)
    print(f"{'replicons':>10}{hdr}")
    for n in REPLICONS:
        row = "".join(f"{noise[str(nu)]['copies_needed'][str(n)]:>10}"
                      for nu in NOISE_LEVELS)
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
