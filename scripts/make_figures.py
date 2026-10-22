"""Draw the paper's one figure, with every number read from results/.

No value here is typed by hand: the panels are built from
results/independence_check.json, so re-running the analysis redraws the figure
and the two can never disagree.

The figure carries the whole argument. Panel A shows the seven measured
per-plasmid retention rates against the rate that independent partitioning
would require; every bar falls short. Panel B multiplies those seven together
and sets the product beside what was actually measured.

Colours are the validated two-slot categorical pair (blue #2a78d6 measured,
orange #eb6834 model-derived), checked for colour-vision separation rather
than chosen by eye: worst-pair CVD dE 24.7, normal-vision dE 33.6, both clear
of the floors. Blue means "measured" in both panels and orange means "what a
model says", which is the only thing colour encodes here.

    .venv\\Scripts\\python scripts\\make_figures.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

#: Display names. The results files keep ASCII keys so nothing downstream has
#: to handle non-ASCII; only the rendered labels are typeset properly.
DISPLAY = {"aHL": "αHL"}

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "paper" / "figures"

# Validated categorical slots 1 and 2, light surface.
MEASURED = "#2a78d6"
MODEL = "#eb6834"
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
    data = json.loads((RESULTS / "independence_check.json").read_text())
    retention = data["retention"]
    needed = data["retention_needed_for_independence"]
    predicted = data["p_all_seven_if_independent"]
    observed = data["p_all_seven_observed"]
    ratio = data["ratio_observed_over_independent"]
    n_cells = data["n_cells"]
    expected_n = data["expected_complete_cells"]
    observed_n = data["observed_complete_cells"]

    order = sorted(retention.items(), key=lambda kv: kv[1])   # low to high
    names = [DISPLAY.get(k, k) for k, _ in order]
    values = [v * 100 for _, v in order]

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(7.2, 3.1), gridspec_kw={"width_ratios": [1.65, 1.0]})

    # ---- Panel A: the seven measured retention rates ---------------------
    ypos = range(len(names))
    ax1.barh(list(ypos), values, height=0.62, color=MEASURED, zorder=3)
    ax1.axvline(needed * 100, color=MODEL, linestyle=(0, (4, 2.5)),
                linewidth=1.4, zorder=4)
    # Right of the line and level with the middle bars: left of it collides
    # with the top bar's own value label, which is where this first sat.
    ax1.text(needed * 100 + 2.2, len(names) - 1.6,
             f"{needed:.1%}\nrequired",
             ha="left", va="center", fontsize=7.4, color=MODEL,
             linespacing=1.4)

    for y, v in zip(ypos, values):
        ax1.text(v - 1.6, y, f"{v:.0f}%", va="center", ha="right",
                 color=SURFACE, fontsize=7.6, fontweight="bold", zorder=5)

    ax1.set_yticks(list(ypos), names, fontsize=8)
    ax1.set_xlim(0, 100)
    ax1.set_xticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
    ax1.set_xlabel("daughters retaining this plasmid", color=INK_2)
    ax1.set_title("A   Per-plasmid retention, five generations",
                  loc="left", fontsize=9, color=INK, pad=9)
    ax1.grid(axis="x", color=INK_3, alpha=0.22, linewidth=0.6, zorder=0)
    ax1.set_axisbelow(True)
    ax1.tick_params(length=0)

    # ---- Panel B: the product, against the measurement -------------------
    labels = ["if the seven were\nindependent", "observed"]
    heights = [predicted * 100, observed * 100]
    bars = ax2.bar([0, 1], heights, width=0.52,
                   color=[MODEL, MEASURED], zorder=3)

    for bar, h, n in zip(bars, heights, [expected_n, observed_n]):
        ax2.text(bar.get_x() + bar.get_width() / 2, h + 1.1,
                 f"{h:.1f}%", ha="center", va="bottom",
                 fontsize=9, fontweight="bold", color=INK)
        ax2.text(bar.get_x() + bar.get_width() / 2, h + 4.2,
                 f"{float(n):.0f} of {n_cells} cells", ha="center", va="bottom",
                 fontsize=7.2, color=INK_2)

    # The gap is the result: mark it between the two bars.
    top = max(heights)
    ax2.annotate("", xy=(0.5, predicted * 100 + 0.4), xytext=(0.5, top),
                 arrowprops=dict(arrowstyle="<->", color=INK_2, linewidth=1.0))
    ax2.text(0.55, (predicted * 100 + top) / 2, f"{ratio:.1f}×",
             ha="left", va="center", fontsize=11, fontweight="bold", color=INK)

    ax2.set_xticks([0, 1], labels, fontsize=8)
    ax2.set_ylim(0, top * 1.38)
    ax2.set_yticks([0, 10, 20, 30], ["0", "10", "20", "30%"])
    ax2.set_ylabel("daughters with all seven plasmids", color=INK_2)
    ax2.set_title("B   The complete genome", loc="left",
                  fontsize=9, color=INK, pad=9)
    ax2.grid(axis="y", color=INK_3, alpha=0.22, linewidth=0.6, zorder=0)
    ax2.set_axisbelow(True)
    ax2.tick_params(length=0)

    fig.tight_layout(w_pad=2.4)
    FIGURES.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "png"):
        out = FIGURES / f"fig1_independence.{ext}"
        fig.savefig(out, dpi=300, bbox_inches="tight")
        print(f"  wrote {out.relative_to(ROOT)}")
    plt.close(fig)

    print(f"\n  panel A: {len(names)} plasmids, {min(values):.0f}-{max(values):.0f}%"
          f", reference line at {needed:.1%}")
    print(f"  panel B: {predicted:.1%} predicted vs {observed:.0%} observed"
          f"  ({ratio:.1f}x)")
    print("  every value read from results/independence_check.json")


if __name__ == "__main__":
    main()
