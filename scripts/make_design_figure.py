"""Draw Figure 1, the general design rule, from results/design_rule.json.

No value here is typed by hand. The panels are built from the file
`scripts/design_rule.py` writes, which in turn comes from the closed form in
`src/inheritance.py`, so the figure, the tables and the text cannot disagree.

Panel A is the actionable result: for a genome split across N replicons with
no segregation machinery, the per-replicon copy number a lineage needs to
still hold a complete set after five generations. Panel B is the same model
read the other way, as the completeness a given copy number buys, and shows
why the answer in panel A rises so slowly.

Colour does two different jobs here and the two palettes are kept apart.
Panel A has two series that differ in *identity* (the two completeness
targets), so it uses the validated categorical pair also used by Figure 2,
blue #2a78d6 and orange #eb6834: worst adjacent pair CVD dE 24.7 (protan),
normal-vision dE 33.6, both clear of the floors, and both direct-labelled as
well. Panel B's series differ in *magnitude* (copy number is ordered), so it
uses a single-hue sequential ramp, light to dark as copy number rises,
monotonic in OKLab lightness from 0.878 down to 0.358 in even steps. A
sequential ramp is the rule for an ordered quantity; cycling six categorical
hues through it would be wrong.

    .venv\\Scripts\\python scripts\\make_design_figure.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "paper" / "figures"

# Validated categorical slots 1 and 2, light surface -- shared with Figure 2
# so that a reader who has seen one figure reads the other the same way.
TARGET_50 = "#2a78d6"
TARGET_90 = "#eb6834"

# Single-hue sequential ramp for copy number, light to dark.
COPY_RAMP = {
    2: "#c3d9f5",
    3: "#93bbec",
    4: "#5f9ae1",
    5: "#2a78d6",
    6: "#1d5aa6",
    8: "#133c70",
}

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
INK_3 = "#8a8984"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8.5,
    "axes.edgecolor": INK_3,
    "axes.labelcolor": INK_2,
    "text.color": INK,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def main():
    data = json.loads((RESULTS / "design_rule.json").read_text())
    gens = data["generations"]
    rule = data["design_rule"]
    cost = data["completeness_by_replicons"]
    gaut = data["gaut_2026"]

    # Replicon axis, read from the file rather than assumed.
    ns = sorted(int(k) for k in rule["0.5"]["copies_needed"])

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(7.2, 3.2), gridspec_kw={"width_ratios": [1.0, 1.12]})

    # ---- Panel A: the copy number a split genome needs -------------------
    for target, colour, label in (
        ("0.9", TARGET_90, "90% complete"),
        ("0.5", TARGET_50, "50% complete"),
    ):
        ys = [rule[target]["copies_needed"][str(n)] for n in ns]
        ax1.step(ns, ys, where="mid", color=colour, linewidth=2.0, zorder=3,
                 label=label)
        ax1.plot(ns, ys, "o", color=colour, markersize=4.6,
                 markeredgecolor=SURFACE, markeredgewidth=1.2, zorder=4)
        # Direct label at the right end, so identity is never colour alone.
        ax1.text(ns[-1] + 0.35, ys[-1], label, color=colour, fontsize=7.6,
                 va="center", ha="left", fontweight="bold")

    # What the published system actually loaded, as the reference the design
    # rule is read against.
    loaded = gaut["copies_loaded_at_t0"]
    ax1.axhline(loaded, color=INK_3, linestyle=(0, (3, 2.5)), linewidth=1.1,
                zorder=2)
    ax1.text(1.0, loaded - 0.32, f"{loaded} copies loaded at t = 0",
             color=INK_2, fontsize=7.2, va="top", ha="left")

    ax1.set_xticks(ns)
    ax1.set_xlim(0.4, ns[-1] + 3.4)
    ax1.set_ylim(0, 11.6)
    ax1.set_yticks(range(0, 12, 2))
    ax1.set_xlabel("replicons the genome is split across", color=INK_2)
    ax1.set_ylabel("copies of each replicon needed", color=INK_2)
    ax1.set_title(f"A   What splitting a genome costs, {gens} generations",
                  loc="left", fontsize=9, color=INK, pad=9)
    # Upper left is the one empty corner: both series start at 6 or below and
    # rise, so nothing ever reaches it. Lower right, where this first sat,
    # collides with the loaded-copy-number note.
    ax1.legend(frameon=False, fontsize=7.6, loc="upper left",
               handlelength=1.5, borderpad=0.2)
    ax1.grid(axis="y", color=INK_3, alpha=0.22, linewidth=0.6, zorder=0)
    ax1.set_axisbelow(True)
    ax1.tick_params(length=0, labelsize=7.6)

    # ---- Panel B: completeness bought by a given copy number -------------
    # The low copy numbers all converge on zero, so labelling every curve at
    # the right edge stacks three labels on top of each other. Each is
    # labelled instead at the last replicon count where its curve is still
    # clearly off the floor.
    label_at = {2: 1, 3: 3, 4: 7, 5: ns[-1], 6: ns[-1], 8: ns[-1]}
    for c in sorted(COPY_RAMP):
        ys = [cost[str(c)][str(n)] * 100 for n in ns]
        ax2.plot(ns, ys, color=COPY_RAMP[c], linewidth=2.0, zorder=3)
        x = label_at[c]
        y = cost[str(c)][str(x)] * 100
        # Pale ramp steps are too light to read as text, so the label for the
        # low copy numbers wears a text token instead of the series colour.
        colour = COPY_RAMP[c] if c >= 5 else INK_2
        if x == ns[-1]:
            ax2.text(x + 0.3, y, f"{c} copies", color=colour, fontsize=7.2,
                     va="center", ha="left")
        else:
            ax2.text(x + 0.18, y + 2.6, f"{c} copies", color=colour,
                     fontsize=7.2, va="bottom", ha="left")

    # The published measurement, as a single labelled point rather than a
    # series: it is one observation, not a curve. What it implies about copy
    # number is in the caption, which keeps the label off the curves.
    obs = gaut["observed_complete_after_5_generations"] * 100
    ax2.plot([gaut["n_replicons"]], [obs], marker="D", markersize=6.4,
             color=INK, markeredgecolor=SURFACE, markeredgewidth=1.3, zorder=6)
    ax2.text(gaut["n_replicons"] + 0.34, obs, f"measured, {obs:.0f}%",
             ha="left", va="center", fontsize=7.4, color=INK,
             fontweight="bold", zorder=6)

    ax2.set_xticks(ns)
    ax2.set_xlim(0.4, ns[-1] + 3.0)
    ax2.set_ylim(0, 104)
    ax2.set_yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
    ax2.set_xlabel("replicons the genome is split across", color=INK_2)
    ax2.set_ylabel(f"lineages complete after {gens} generations", color=INK_2)
    ax2.set_title("B   What a given copy number buys", loc="left",
                  fontsize=9, color=INK, pad=9)
    ax2.grid(axis="y", color=INK_3, alpha=0.22, linewidth=0.6, zorder=0)
    ax2.set_axisbelow(True)
    ax2.tick_params(length=0, labelsize=7.6)

    fig.tight_layout(w_pad=2.2)
    FIGURES.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "png"):
        out = FIGURES / f"fig1_design_rule.{ext}"
        fig.savefig(out, dpi=300, bbox_inches="tight")
        print(f"  wrote {out.relative_to(ROOT)}")
    plt.close(fig)

    lo = rule["0.5"]["copies_needed"]["1"]
    hi = rule["0.5"]["copies_needed"][str(ns[-1])]
    print(f"\n  panel A: 50% target rises {lo} -> {hi} copies "
          f"over 1 -> {ns[-1]} replicons")
    print(f"  panel B: {len(COPY_RAMP)} copy numbers, measured point at "
          f"({gaut['n_replicons']}, {obs:.0f}%)")


if __name__ == "__main__":
    main()
