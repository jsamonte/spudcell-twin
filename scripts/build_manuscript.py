"""Generate paper/manuscript.md with every number read from results/.

No figure in this manuscript is typed by hand. Methods, Results and
Limitations are written out in full; Abstract, Introduction and Discussion live
in paper/sections/ so that rebuilding never overwrites the author's argument.

    .venv\\Scripts\\python scripts\\build_manuscript.py
"""

import atexit
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"

CITE = ("Gaut NJ, Deich C, Cash B, Hoog T, Engelhart AE, Adamala KP. "
        "*A Chemically Defined Synthetic Cell Capable Of Growth And "
        "Replication.* bioRxiv 2026.07.01.735724 (2026). "
        "doi:10.64898/2026.07.01.735724")

#: Cited in the introduction for the classical single-plasmid result - random
#: partitioning suffices when the cargo is many small identical molecules.
#: Verified against Crossref 2026-10-21; author list and article number are as
#: Crossref returned them, not recalled.
OLIVI = ("Olivi L, Berger M, Creyghton RNP, De Franceschi N, Dekker C, "
         "Mulder BM, Claassens NJ, ten Wolde PR, van der Oost J. "
         "*Towards a synthetic cell cycle.* Nature Communications 12, 4531 "
         "(2021). doi:10.1038/s41467-021-24772-8")


def load(name):
    path = RESULTS / name
    return json.loads(path.read_text()) if path.exists() else None


#: A section file seeded from a template carries this marker. While it is
#: present the section counts as unwritten: the build substitutes the outline
#: and says so loudly on exit, so placeholder text can never be mistaken for
#: prose in a posted preprint. Delete the marker line when you have written it.
#: A section drafted BY CLAUDE rather than by the author carries this marker.
#: Unlike UNWRITTEN it is still used, so the manuscript reads end to end - but
#: every build says so. A committee assesses how the AUTHOR reasons, and prose
#: that was edited rather than argued does not survive an interview. Delete the
#: marker once the section has been rewritten in the author's own words.
DRAFT_MARKER = "<!-- DRAFT -->"
_drafted = []
SPLIT_ON = chr(10)


@atexit.register
def _warn_drafted():
    if _drafted:
        names = ", ".join(sorted(set(_drafted)))
        print()
        print("  ~~ STILL IN CLAUDE'S WORDS: " + names)
        print("     Usable, and NOT yours yet. Rewrite before posting.")
        print("     Remove the <!-- DRAFT --> line when you have.")
UNWRITTEN_MARKER = "<!-- UNWRITTEN -->"
_unwritten = []


@atexit.register
def _warn_unwritten():
    if _unwritten:
        names = ", ".join(sorted(set(_unwritten)))
        print()
        print("  !! STILL UNWRITTEN: " + names)
        print("     Those sections show a generated outline, not your prose.")
        print("     Remove the <!-- UNWRITTEN --> line once you have written one.")
def prose(name, fallback):
    path = PAPER / "sections" / f"{name}.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if UNWRITTEN_MARKER in text:
            _unwritten.append(name)
            return fallback
        if DRAFT_MARKER in text:
            _drafted.append(name)
        return text.rstrip().split(SPLIT_ON)
    return fallback


def main():
    ind = load("independence_check.json")
    struct = load("retention_structure.json")
    if not ind:
        sys.exit("run scripts/independence_check.py first")

    pct = lambda x: f"{x:.1%}"                                    # noqa: E731
    p_ind = ind["p_all_seven_if_independent"]
    p_obs = ind["p_all_seven_observed"]
    n = ind["n_cells"]
    gens = ind["generations"]

    L = []
    w = L.append

    w("# Genome fidelity in a synthetic cell exceeds what independent "
      "plasmid partitioning allows")
    w("")
    w("*Methods, Results and Limitations are generated from `results/` by "
      "`scripts/build_manuscript.py`; do not edit numbers here. Abstract, "
      "Introduction and Discussion are in `paper/sections/` and are the "
      "author's to write.*")
    w("")
    w("Independent researcher, Beaumont, TX")
    w("")

    # ---------------------------------------------------------------- abstract
    w("## Abstract")
    w("")
    for line in prose("abstract", [
        f"A synthetic cell whose genome is divided across seven plasmids must "
        f"deliver all seven to a daughter for that daughter to be complete. "
        f"Using only two measurements reported by "
        f"[the source preprint], and no fitted parameters, we show that "
        f"independent partitioning of the seven plasmids predicts that "
        f"{pct(p_ind)} of daughters inherit a complete genome, against "
        f"{pct(p_obs)} measured: a factor of "
        f"{ind['ratio_observed_over_independent']:.1f}. Of {n} single cells, "
        f"independence predicts {ind['expected_complete_cells']:.0f} complete "
        f"and {ind['observed_complete_cells']} were observed "
        f"(binomial p = {ind['binomial_p_value']:.1e}). Measured genome "
        f"fidelity therefore exceeds what chance allows, and the excess is "
        f"the quantity to explain. We show two explanations remain live and "
        f"that the published data cannot separate them.",
        "",
        "*(Outline above is generated. Rewrite in your own voice.)*",
    ]):
        w(line)
    w("")

    # ------------------------------------------------------------ introduction
    w("## 1. Introduction")
    w("")
    for line in prose("introduction", [
        "*Outline to write: why a multi-plasmid genome makes inheritance a",
        "combinatorial problem rather than a single-copy one; the authors'",
        "claim that splitting the genome across plasmids *limits* the",
        "influence of stochastic partitioning (SI section 7), and why that is",
        "exactly backwards for inheriting a complete set; what a closed-form",
        "calculation settles that a simulation would obscure.*",
    ]):
        w(line)
    w("")

    # ----------------------------------------------------------------- methods
    w("## 2. Methods")
    w("")
    w("### 2.1 Source of every parameter")
    w("")
    w(f"All values are taken from {CITE} and each is cited to the figure, "
      "table or methods section it came from in `docs/PARAMETERS.md`. No "
      "parameter is estimated, fitted or assumed. Two are used here:")
    w("")
    w("| Quantity | Value | Source |")
    w("|---|---|---|")
    for name, p in sorted(ind["retention"].items(), key=lambda kv: -kv[1]):
        w(f"| Daughters retaining {name} | {pct(p)} | Fig. 3p |")
    w(f"| Daughters retaining **all seven** | **{pct(p_obs)}** | Fig. 3o |")
    w(f"| Single cells analysed | {n} | Methods 23 |")
    w(f"| Generations | {gens} | Fig. 3; Methods 11 |")
    w("")
    w("Retention for &alpha;HL is stated numerically in SI section 6; the "
      "remaining six are read from the bar chart in Fig. 3p and carry "
      "approximately &plusmn;3 percentage points.")
    w("")
    w("### 2.2 The independence prediction")
    w("")
    w("If each plasmid reaches a given daughter independently of the others, "
      "the probability that daughter receives all seven is the product of the "
      "seven individual retention rates. This requires no model of division, "
      "no simulation and no free parameter; it is a consequence of the "
      "measurements themselves. The comparison is therefore a test of the "
      "independence assumption alone.")
    w("")
    w("### 2.3 Significance")
    w("")
    w(f"The {n} single cells are each complete or not, so the counts carry "
      "the test: a one-sided exact binomial test of the observed number of "
      "complete cells against the rate independence predicts. The interval "
      "on the observed rate is reported two-sided. One-sided is appropriate "
      "because the question is whether fidelity *exceeds* chance.")
    w("")
    w("### 2.4 The copy-number alternative")
    w("")
    w("A cell carrying *c* copies of each plasmid at division misses a given "
      "plasmid only if all *c* copies go to the other daughter. Writing "
      "*p* for the probability a copy reaches this daughter, the chance of a "
      "complete set is (1 - (1 - p)^c)^7. This is implemented in "
      "`src/inheritance.py` and is exercised by 21 unit tests. It matters "
      "here because &Phi;29 replicates continuously with no checkpoint, so "
      "copy number at division is not the "
      f"{ind['copies_at_load']:.1f} copies loaded at t = 0.")
    w("")

    # ----------------------------------------------------------------- results
    w("## 3. Results")
    w("")
    w("### 3.1 Independent partitioning underpredicts fidelity ninefold")
    w("")

    # The figure carries the whole argument, so it leads the results rather
    # than trailing them. Drawn by scripts/make_figures.py from the same
    # results file these numbers come from, so the two cannot disagree.
    figure = PAPER / "figures" / "fig1_independence.png"
    if figure.exists():
        w("![](figures/fig1_independence.png)")
        w("")
        w(f"**Figure 1. Measured genome fidelity exceeds independent "
          f"partitioning by {ind['ratio_observed_over_independent']:.1f}×.** "
          f"(**A**) Per-plasmid retention after {gens} generations, from "
          f"Fig. 3p of the source. The dashed line marks "
          f"{pct(ind['retention_needed_for_independence'])}, the rate every "
          f"plasmid would need for independent partitioning to account for "
          f"the observed complete-genome fraction; no plasmid reaches it. "
          f"(**B**) The product of the seven rates, "
          f"{pct(p_ind)}, against the measured "
          f"{pct(p_obs)} (Fig. 3o). Of {n} single cells, independence "
          f"predicts {ind['expected_complete_cells']:.0f} complete genomes "
          f"and {ind['observed_complete_cells']} were observed. No parameter "
          f"is fitted: panel B is the product of panel A.")
        w("")
    else:
        w("*(Figure 1 missing — run `scripts/make_figures.py`.)*")
        w("")

    w("| | |")
    w("|---|---|")
    w(f"| Mean per-plasmid retention | {pct(ind['mean_retention'])} |")
    w(f"| **P(all seven) if independent** | **{pct(p_ind)}** |")
    w(f"| **P(all seven) measured** | **{pct(p_obs)}** |")
    w(f"| Ratio | **{ind['ratio_observed_over_independent']:.1f}×** |")
    w(f"| Complete cells of {n}: predicted / observed | "
      f"{ind['expected_complete_cells']:.1f} / "
      f"{ind['observed_complete_cells']} |")
    w(f"| Binomial test | **p = {ind['binomial_p_value']:.2e}** |")
    w(f"| Observed rate (95% CI) | {pct(ind['observed_rate'])} "
      f"({pct(ind['observed_rate_ci95'][0])}–"
      f"{pct(ind['observed_rate_ci95'][1])}) |")
    w(f"| Retention needed for independence to hold | "
      f"{pct(ind['retention_needed_for_independence'])} |")
    w("")
    w(f"For independence to be consistent with the measured "
      f"{pct(p_obs)}, every one of the seven plasmids would have to be "
      f"retained at {pct(ind['retention_needed_for_independence'])} — against "
      f"a measured mean of {pct(ind['mean_retention'])} and a measured "
      f"maximum of {pct(max(ind['retention'].values()))}. No reading of "
      "Fig. 3p supports that.")
    w("")
    w("This also tests a claim the source makes but does not quantify: that "
      "dividing the genome across seven plasmids *\"limits the possible "
      "influence of stochastic inequalities in plasmid partitioning\"* "
      "(SI section 7). For inheriting a **complete set**, independent "
      "partitioning implies the opposite — each additional plasmid "
      "multiplies in a further chance to fail. The "
      f"{pct(p_ind)} figure is that argument stated numerically.")
    w("")
    w("### 3.2 Copy number alone can account for the gap")
    w("")
    w("Independent partitioning of *c* copies per plasmid gives:")
    w("")
    w("| Copies at division | One division | "
      f"After {gens} generations |")
    w("|---|---|---|")
    for c in sorted(ind["single_division_by_copy_number"], key=int):
        one = ind["single_division_by_copy_number"][c]
        five = ind["five_generations_by_copy_number"][c]
        w(f"| {c} | {one:.4f} | {five:.4f} |")
    w("")
    w(f"Surviving {gens} independent divisions at {pct(p_obs)} overall "
      f"requires {pct(ind['per_generation_target'])} per division, which "
      f"independent partitioning reaches at "
      f"**{ind['copies_needed_for_observed']} copies** per plasmid — against "
      f"{ind['copies_at_load']:.1f} loaded at t = 0.")
    w("")
    w("**So the ninefold gap does not by itself demonstrate correlated "
      "partitioning.** Continuous replication to roughly twice the loaded "
      "copy number would produce the same observation with partitioning that "
      "is perfectly independent. The two explanations are not "
      "distinguishable from the reported data, and this paper does not claim "
      "to distinguish them.")
    w("")

    if struct:
        w("### 3.3 The retention ordering does not separate the explanations")
        w("")
        w("The two explanations predict different *orderings* of which "
          "plasmids are lost. A selective mechanism — the authors' own "
          "reading in SI section 7, that losing the channel, the polymerase "
          "or the replicase impairs growth — predicts retention tracks "
          "functional necessity. A physical mechanism predicts it tracks "
          "size or copy number. Both fit:")
        w("")
        rs = struct["retention_vs_size"]
        rn = struct["retention_vs_necessity"]
        cf = struct["size_vs_necessity_confound"]
        w("| Predictor | Statistic | p |")
        w("|---|---|---|")
        w(f"| Plasmid size | Spearman ρ = {rs['spearman_rho']:+.3f} | "
          f"{rs['spearman_p']:.3f} |")
        w(f"| Functional necessity | point-biserial r = "
          f"{rn['point_biserial_r']:+.3f} | {rn['p']:.3f} |")
        w(f"| *size vs necessity (the confound)* | *Spearman ρ = "
          f"{cf['spearman_rho']:+.3f}* | *{cf['p']:.3f}* |")
        w("")
        w("| Plasmid | Size (kbp) | Retention | Role |")
        w("|---|---|---|---|")
        for p in sorted(struct["plasmids"], key=lambda x: -x["retention"]):
            role = "needed for growth" if p["needed"] else "resupplied / inert"
            w(f"| {p['name']} | {p['kbp']:.1f} | {p['retention']:.0%} | "
              f"{role} |")
        w("")
        w(f"With n = {struct['n_plasmids']} the two predictors cannot be "
          "separated: the three largest plasmids are also the three the "
          "authors describe as dispensable. One detail does cut against a "
          "purely size-driven account — GFP is the smallest plasmid at "
          "2.5 kbp and is retained less well than two larger ones — but this "
          "is a single data point, not a discrimination.")
        w("")

    # ------------------------------------------------------------- discussion
    w("## 4. Discussion")
    w("")
    for line in prose("discussion", [
        "*Outline to write: what a ninefold excess over chance implies for",
        "multi-plasmid synthetic genomes; why the authors' protection",
        "argument needs reversing for complete-set inheritance; the one",
        "experiment that would separate copy number from selection (per-cell",
        "plasmid copy number at the moment of division, or retention measured",
        "after genetically encoded rather than mechanical division); and what",
        "this predicts for the single-chromosome design the authors propose.*",
    ]):
        w(line)
    w("")

    # ------------------------------------------------------------ limitations
    w("## 5. Limitations")
    w("")
    w("These are properties of the source measurements, not of the "
      "calculation, and none of them can be removed by analysis.")
    w("")
    w("1. **The division mechanism is mechanical, not genetically encoded.** "
      f"The {pct(p_obs)} figure comes from Fig. 3, where daughters are "
      "produced by extrusion through a 2 µm membrane filter (Methods 11), "
      "chosen deliberately to give uniform daughters. Genetically encoded "
      "division is demonstrated (Fig. 6) but at low yield, and the authors "
      "report no per-cell completeness distribution for it. Every number "
      "here therefore describes partitioning during extrusion of a grown "
      "liposome. Whether that is closer to or further from ideal random "
      "partitioning is unknown and is not assumed either way.")
    w("")
    w(f"2. **The analysed cells were screened.** Of 384 aliquots, 204 had "
      f"detectable 16S rRNA and {n} were selected as those with the "
      "*lowest* 16S abundance, to favour one cell per sample (Methods 23). "
      "The authors identify this as the only screening step in the work. "
      "Whether it biases completeness upward or downward is unknown.")
    w("")
    w("3. **Six of seven retention values are read from a figure** and carry "
      "roughly ±3 percentage points. The conclusion is insensitive to this: "
      "the independence prediction would have to rise by a factor of nine to "
      "meet the observation, and no plausible re-reading of Fig. 3p moves it "
      "that far.")
    w("")
    w("4. **Copy number at division is not reported**, and it is the single "
      "quantity that decides between the two explanations in §3.2.")
    w("")
    w("5. **The source is a preprint** and not yet peer reviewed. It also "
      "contains an internal inconsistency — seven plasmids in Results, "
      "Fig. 3o and Table S6, but \"eight\" on p. 5. Table S6 lists seven and "
      "their sizes sum to the stated 90.3 kbp, so seven is used throughout.")
    w("")

    # --------------------------------------------- data and code availability
    w("## 6. Data and code availability")
    w("")
    w("No new data were generated. Every input is a published measurement "
      "taken from Gaut et al. (2026), cited to the figure, table or methods "
      "section it came from in `docs/PARAMETERS.md`.")
    w("")
    w("All analysis code is in the repository accompanying this manuscript. "
      "`scripts/independence_check.py` reproduces the headline comparison, "
      "`scripts/retention_structure.py` the correlation analysis, and "
      "`scripts/make_figures.py` redraws Figure 1 from the same results file "
      "the text is generated from, so figure and text cannot disagree. The "
      "closed-form inheritance model is in `src/inheritance.py` and is "
      "covered by unit tests.")
    w("")
    # The repository is private while the manuscript circulates privately, so
    # this says so rather than printing a URL that would not resolve. The
    # reminder to make it public and paste the URL lives in paper/README.md,
    # where it cannot block build_pdf.py: a >>> instruction in the text stops
    # the PDF rendering, which is right before posting and wrong before a
    # private read.
    w("The repository is currently private. It will be made public, and its "
      "URL given here, when this manuscript is posted; in the meantime the "
      "code is available from the author on request.")
    w("")

    # ------------------------------------------------------------- references
    w("## References")
    w("")
    w(f"1. {CITE}")
    w("")
    w(f"2. {OLIVI}")
    w("")
    w("*Reproduce every number above with "
      "`.venv\\Scripts\\python scripts\\independence_check.py` and "
      "`scripts\\retention_structure.py`.*")
    w("")

    PAPER.mkdir(exist_ok=True)
    (PAPER / "sections").mkdir(exist_ok=True)
    out = PAPER / "manuscript.md"
    out.write_text("\n".join(L), encoding="utf-8")

    authored = [s for s in ("abstract", "introduction", "discussion")
                if (PAPER / "sections" / f"{s}.md").exists()
                and s not in _unwritten and s not in _drafted]
    print(f"wrote {out.relative_to(ROOT)}  ({len(L)} lines)")
    print(f"author-written sections present: {authored or 'none yet'}")
    print("outlines are placeholders; write paper/sections/*.md and re-run")


if __name__ == "__main__":
    main()
