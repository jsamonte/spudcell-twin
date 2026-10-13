"""Does per-plasmid retention track plasmid SIZE or FUNCTIONAL necessity?

This is the question that would discriminate between the two explanations for
the 9.4x gap found by independence_check.py:

  physical  - big plasmids partition worse, so the gap is about copy number and
              segregation mechanics
  selection - cells that lose a plasmid they need grow worse and drop out, so
              the gap is survivorship, which is the authors' own hypothesis
              (SI section 7)

The honest answer, below, is that the published data cannot separate them: the
three largest plasmids are also the three the authors call dispensable, so size
and necessity are collinear. That is a limitation to state, not a result to
dress up.

    .venv\Scripts\python scripts\retention_structure.py
"""

import json
from pathlib import Path

from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

# Table S6 (sizes) and Fig. 3p / SI section 6 (retention). Retention is read off
# a figure for six of the seven, so treat it as +/- 3 points.
PLASMIDS = [
    # name,      kbp,  retention, needed-for-growth per the authors' SI section 7
    ("aHL",      4.3,  0.71, True),   # membrane channel: feeding
    ("T7RNAP",   5.4,  0.68, True),   # transcription of everything
    ("GFP",      2.5,  0.63, False),  # reporter, does nothing for the cell
    ("pREP",     4.6,  0.63, True),   # Phi29 replication
    ("pLD2",    20.0,  0.57, False),  # tRNA synthetases: resupplied by feeders
    ("pLD3",    23.4,  0.56, False),
    ("pLD1",    30.1,  0.52, False),
]


def main():
    size = [p[1] for p in PLASMIDS]
    keep = [p[2] for p in PLASMIDS]
    need = [1 if p[3] else 0 for p in PLASMIDS]

    rho_s, p_s = stats.spearmanr(size, keep)
    r_s, pp_s = stats.pearsonr(size, keep)
    r_n, p_n = stats.pointbiserialr(need, keep)
    # The confound itself, quantified: are size and necessity independent?
    rho_sn, p_sn = stats.spearmanr(size, need)

    print(f"n = {len(PLASMIDS)} plasmids\n")
    print("  retention vs SIZE       Spearman rho = "
          f"{rho_s:+.3f}  (p = {p_s:.3f})")
    print(f"                          Pearson   r  = {r_s:+.3f}  (p = {pp_s:.3f})")
    print(f"  retention vs NECESSITY  point-biserial r = {r_n:+.3f}  (p = {p_n:.3f})")
    print(f"\n  size vs NECESSITY       Spearman rho = {rho_sn:+.3f}  "
          f"(p = {p_sn:.3f})   <- the confound")

    print("\n  ordered by retention:")
    for name, kb, k, n in sorted(PLASMIDS, key=lambda x: -x[2]):
        print(f"    {name:7} {kb:5.1f} kbp  {k:.0%}  "
              f"{'needed' if n else 'dispensable'}")

    # The one data point that is NOT explained by size alone.
    smallest = min(PLASMIDS, key=lambda p: p[1])
    better_retained = [p for p in PLASMIDS if p[2] > smallest[2]]
    print(f"\n  {smallest[0]} is the smallest plasmid ({smallest[1]} kbp) yet "
          f"{len(better_retained)} larger plasmid(s) are retained better "
          f"({', '.join(p[0] for p in better_retained)}).")
    print("  So size is not a sufficient explanation on its own. Neither test\n"
          "  can be preferred over the other with n=7 collinear points.")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "retention_structure.json").write_text(json.dumps({
        "n_plasmids": len(PLASMIDS),
        "plasmids": [{"name": n, "kbp": k, "retention": r, "needed": b}
                     for n, k, r, b in PLASMIDS],
        "retention_vs_size": {"spearman_rho": round(rho_s, 4),
                              "spearman_p": round(p_s, 4),
                              "pearson_r": round(r_s, 4),
                              "pearson_p": round(pp_s, 4)},
        "retention_vs_necessity": {"point_biserial_r": round(r_n, 4),
                                   "p": round(p_n, 4)},
        "size_vs_necessity_confound": {"spearman_rho": round(rho_sn, 4),
                                       "p": round(p_sn, 4)},
        "conclusion": ("Both size and functional necessity correlate with "
                       "retention, but they are collinear in this dataset "
                       "(the three largest plasmids are the three the authors "
                       "call dispensable), so the published data cannot "
                       "distinguish a physical from a selective mechanism. "
                       "GFP, the smallest plasmid, is retained worse than two "
                       "larger ones, so size alone is insufficient."),
        "source": "sizes Table S6; retention Fig. 3p and SI section 6; "
                  "necessity assignment from the authors' argument in SI section 7",
    }, indent=2) + "\n")
    print(f"\nwrote results/retention_structure.json")


if __name__ == "__main__":
    main()
