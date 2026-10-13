"""The branch point: does independent partitioning explain the observed losses?

Runs the moment docs/PARAMETERS.md is filled in, and refuses to run before
then. No simulation, no model code — a closed-form calculation and a
comparison, which is all this question needs to be answered.

Its output decides which of three papers the project becomes (see
docs/PARAMETERS.md). The plan is explicit that a spatial model reproducing what
a binomial calculation already told us is two wasted months.

    .venv\\Scripts\\python scripts\\analytic_baseline.py \\
        --plasmids 7 --copy-number 1 --observed-complete 0.42
"""

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.inheritance import (complete_set_probability, copies_needed_for,  # noqa: E402
                             loss_probability, summarize)

RESULTS = ROOT / "results"
PARAMS = ROOT / "docs" / "PARAMETERS.md"


def refuse_if_parameters_are_unfilled(args):
    """The gate. Numbers must come from the paper, not from a default."""
    if args.plasmids is None or args.copy_number is None:
        sys.exit(
            "Refusing to run: --plasmids and --copy-number have no defaults.\n"
            "Both must come from the SpudCell preprint and be recorded in\n"
            f"{PARAMS.relative_to(ROOT)} with the figure or table they came from.\n"
            "A plausible guess here would silently become the paper's premise.")
    if args.observed_complete is None:
        print("NOTE: no --observed-complete given, so the calculation runs but the\n"
              "      branch cannot be called. Fill in the inheritance rate the\n"
              "      preprint reports to decide between cases A, B and C.\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--plasmids", type=int, default=None,
                    help="number of distinct plasmids (from the preprint)")
    ap.add_argument("--copy-number", type=int, default=None,
                    help="copies of each plasmid (from the preprint)")
    ap.add_argument("--observed-complete", type=float, default=None,
                    help="fraction of daughters the preprint reports with a complete genome")
    ap.add_argument("--noise", type=float, default=0.0,
                    help="partition bias; 0 is an independent fair split")
    ap.add_argument("--tolerance", type=float, default=0.25,
                    help="relative agreement counted as 'the binomial explains it'")
    args = ap.parse_args()
    refuse_if_parameters_are_unfilled(args)

    n, c = args.plasmids, args.copy_number
    summary = summarize(n, c, args.noise)
    predicted = summary.complete_one_daughter

    print(f"{n} plasmids at {c} cop{'y' if c == 1 else 'ies'} each, "
          f"partition noise {args.noise}")
    print(f"  P(a daughter inherits a complete set) = {predicted:.6f}")
    print(f"  P(a daughter is missing at least one) = {summary.loss_one_daughter:.6f}")
    print(f"  P(at least one daughter is complete)  = {summary.complete_either_daughter:.6f}")

    print("\n  how the prediction moves with copy number:")
    for extra in range(1, 9):
        print(f"    {extra} cop{'y' if extra == 1 else 'ies'}: "
              f"{complete_set_probability(n, extra, args.noise):.6f}")
    need = copies_needed_for(0.95, n, args.noise)
    print(f"  copies needed for 95% complete inheritance: {need}")

    case, reasoning = None, ""
    if args.observed_complete is not None:
        obs = args.observed_complete
        rel = abs(predicted - obs) / obs if obs else float("inf")
        print(f"\n  observed (from the preprint): {obs:.6f}")
        print(f"  predicted / observed:         {predicted / obs:.3f}" if obs else "")
        if rel <= args.tolerance:
            case = "A"
            reasoning = ("Independent stochastic partitioning accounts for the observed "
                         "rate. No active mechanism is required. Write the short report.")
        elif predicted < obs:
            case = "B"
            reasoning = ("Observed fidelity is HIGHER than chance allows, so something is "
                         "helping: co-segregation, tethering, or a higher effective copy "
                         "number. Model the candidate mechanisms.")
        else:
            case = "C"
            reasoning = ("Observed fidelity is LOWER than chance predicts, so something "
                         "hurts beyond randomness: spatial effects, aggregation, or "
                         "asymmetric division. A spatial model is now justified.")
        print(f"\n  CASE {case}: {reasoning}")
        print("\n  Stop here and discuss before going further.")

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "analytic_baseline.json").write_text(json.dumps({
        "inputs": {"plasmids": n, "copy_number": c, "noise": args.noise,
                   "observed_complete": args.observed_complete},
        "predicted": summary.as_dict(),
        "copies_for_95_percent": need,
        "case": case, "reasoning": reasoning,
    }, indent=2) + "\n")
    with (RESULTS / "analytic_baseline.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["copy_number", "p_complete_one_daughter", "p_loss"])
        for extra in range(1, 21):
            w.writerow([extra,
                        round(complete_set_probability(n, extra, args.noise), 8),
                        round(loss_probability(n, extra, args.noise), 8)])
    print(f"\nWrote results/analytic_baseline.json and .csv")


if __name__ == "__main__":
    main()
