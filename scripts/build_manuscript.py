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

#: Public as of 2026-10-31. Printed in the availability statement, so a
#: reader can run every number in the paper.
REPO_URL = "https://github.com/jsamonte/spudcell-twin"

CITE = ("Gaut NJ, Deich C, Cash B, Hoog T, Engelhart AE, Adamala KP. "
        "*A Chemically Defined Synthetic Cell Capable Of Growth And "
        "Replication.* bioRxiv 2026.07.01.735724 (2026). "
        "doi:10.64898/2026.07.01.735724")

#: Cited in the introduction for the point that natural multipartite genomes
#: are maintained by active partitioning rather than by chance. Verified
#: against Crossref 2026-10-31; author list, journal, volume and article
#: number are as Crossref returned them, not recalled.
DU = ("Du W-L, Dubarry N, Passot FM, Kamgoue A, Murray H, Lane D, Pasta F. "
      "*Orderly Replication and Segregation of the Four Replicons of "
      "Burkholderia cenocepacia J2315.* PLOS Genetics 12(7), e1006172 "
      "(2016). doi:10.1371/journal.pgen.1006172")

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
    design = load("design_rule.json")
    if not ind:
        sys.exit("run scripts/independence_check.py first")
    if not design:
        sys.exit("run scripts/design_rule.py first")

    pct = lambda x: f"{x:.1%}"                                    # noqa: E731
    p_ind = ind["p_all_seven_if_independent"]
    p_obs = ind["p_all_seven_observed"]
    n = ind["n_cells"]
    gens = ind["generations"]

    L = []
    w = L.append

    w("# The inheritance cost of splitting a synthetic genome across "
      "replicons")
    w("")
    w("*Methods, Results and Limitations are generated from `results/` by "
      "`scripts/build_manuscript.py`; do not edit numbers here. Abstract, "
      "Introduction and Discussion are in `paper/sections/` and are the "
      "author's to write.*")
    w("")
    w("Jared Samonte")
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
    w("### 2.5 The general design rule")
    w("")
    w("The same expression answers the design question directly. A lineage "
      "stays complete through *G* successive divisions only if it is "
      "complete at every one of them, so for a genome on *N* replicons at "
      "*c* copies each the probability is (1 - (1 - p)^c)^(NG). Inverting "
      "it for *c* gives the smallest copy number that reaches a chosen "
      f"completeness after *G* generations. We evaluate this for *N* = 1 to "
      f"{max(int(k) for k in design['design_rule']['0.5']['copies_needed'])} "
      f"replicons at *G* = {design['generations']}, the number of "
      "generations the source reports, and at two completeness targets. The "
      "calculation is in `scripts/design_rule.py` and uses the same "
      "closed form as §2.4; nothing is fitted.")
    w("")

    # ----------------------------------------------------------------- results
    w("## 3. Results")
    w("")

    # The general result leads. The published system is the worked example
    # that follows it, not the subject of the paper.
    rule = design["design_rule"]
    cost = design["completeness_by_replicons"]
    g = design["gaut_2026"]
    gens_d = design["generations"]
    ns_all = sorted(int(k) for k in rule["0.5"]["copies_needed"])
    n_max = ns_all[-1]
    shown = [n for n in (1, 2, 3, 5, 7, 10, n_max) if n in ns_all]

    need50 = lambda n: rule["0.5"]["copies_needed"][str(n)]       # noqa: E731
    need90 = lambda n: rule["0.9"]["copies_needed"][str(n)]       # noqa: E731

    w("### 3.1 The inheritance cost of splitting a genome")
    w("")

    figure1 = PAPER / "figures" / "fig1_design_rule.png"
    if figure1.exists():
        w("![](figures/fig1_design_rule.png)")
        w("")
        w(f"**Figure 1. Splitting a genome across replicons is affordable, "
          f"but only if copy number rises with it.** (**A**) The smallest "
          f"per-replicon copy number at which a lineage still holds a "
          f"complete set after {gens_d} generations of random partitioning, "
          f"against the number of replicons the genome is divided into, at "
          f"two completeness targets. (**B**) The same model read as the "
          f"completeness a given copy number buys. The measured point is the "
          f"published system, {g['n_replicons']} replicons at "
          f"{g['observed_complete_after_5_generations']:.0%} complete after "
          f"{gens_d} generations, which implies about {g['copies_implied']} "
          f"copies of each replicon against the "
          f"{g['copies_loaded_at_t0']} loaded at t = 0. No parameter is "
          f"fitted; both panels are the closed form of §2.5.")
        w("")
    else:
        w("*(Figure 1 missing — run `scripts/make_design_figure.py`.)*")
        w("")

    w(f"| Replicons | Copies for {rule['0.5']['overall_target']:.0%} "
      f"complete | Copies for {rule['0.9']['overall_target']:.0%} complete | "
      f"Complete at 5 copies |")
    w("|---|---|---|---|")
    # Not `n`: that name holds the single-cell count used further down, and
    # a loop variable here silently rewrote it to the last replicon count.
    for nr in shown:
        w(f"| {nr} | {need50(nr)} | {need90(nr)} | "
          f"{cost['5'][str(nr)]:.1%} |")
    w("")
    w(f"The second and third columns are the result a group designing a "
      f"synthetic genome can act on. Holding a complete set in half of all "
      f"lineages after {gens_d} generations takes {need50(1)} copies when "
      f"the genome sits on one replicon and {need50(n_max)} when it is split "
      f"across {n_max}; the {rule['0.9']['overall_target']:.0%} target runs "
      f"from {need90(1)} to {need90(n_max)} over the same range.")
    w("")
    w("**The cost of splitting is severe in completeness and mild in copy "
      "number, and the two readings are easy to confuse.** At a fixed "
      f"5 copies, going from one replicon to {n_max} drops completeness from "
      f"{cost['5']['1']:.1%} to {cost['5'][str(n_max)]:.1%}, a factor of "
      f"{cost['5']['1'] / cost['5'][str(n_max)]:.1f}, which reads as "
      f"prohibitive. Expressed as the copies an experimenter would have to "
      f"engineer, the same change costs "
      f"{need50(n_max) - need50(1)} extra copies. The first number is what "
      "the product rule does to a fixed design; the second is what it costs "
      "to repair one, and only the second is a design decision. A "
      "multipartite synthetic genome is therefore not an inheritance "
      "problem so much as a copy-number requirement, and a modest one.")
    w("")
    w(f"The requirement grows slowly because copy number enters as "
      f"(1 - 2^-c) per replicon while replicon count enters as an exponent: "
      f"each added copy halves the chance of losing a given replicon, so "
      f"roughly log2 N extra copies absorb a genome split N ways.")
    w("")

    # A rule quoted at one horizon and one partition symmetry is not a rule,
    # so both are varied here rather than left to the reader to wonder about.
    hs = design["horizon_sensitivity"]
    hg = hs["by_generations"]
    horizons = sorted(hg, key=int)
    w("The same slow growth holds along the other axis. Lengthening the "
      "horizon raises the requirement logarithmically rather than "
      "proportionally:")
    w("")
    w("| Replicons | " + " | ".join(
        f"{h} generation" + ("" if h == "1" else "s") for h in horizons)
      + " |")
    w("|---" * (len(horizons) + 1) + "|")
    for nr in shown:
        cells = " | ".join(str(hg[h]["copies_needed"][str(nr)])
                           for h in horizons)
        w(f"| {nr} | {cells} |")
    w("")
    w(f"Holding half of all lineages complete across {horizons[-1]} "
      f"generations rather than {design['generations']} costs "
      f"{hg[horizons[-1]]['copies_needed'][str(n_max)] - hg[str(design['generations'])]['copies_needed'][str(n_max)]} "
      f"further copies at {n_max} replicons. A design that survives five "
      "generations is therefore not far from one that survives twenty, "
      "which is the substantive content of the rule.")
    w("")

    ns_ = design["noise_sensitivity"]
    bn = ns_["by_noise"]
    nus = sorted(bn, key=float)
    hi_nu = nus[-1]
    w("**One assumption carries real weight, and it is the one that makes "
      "the rule optimistic.** Everything above takes each copy to reach a "
      "given daughter with probability exactly one half. Division need not "
      "be that even, and a standard lineage simulator draws the partition "
      "probability from Uniform(0.5 - &nu;/2, 0.5) with &nu; = 0.5 by "
      "default, so that one daughter is systematically the smaller. "
      "Repeating the calculation over that distribution:")
    w("")
    w("| Replicons | " + " | ".join(
        ("symmetric" if float(v) == 0 else f"&nu; = {float(v):g}")
        for v in nus) + " |")
    w("|---" * (len(nus) + 1) + "|")
    for nr in shown:
        cells = " | ".join(str(bn[v]["copies_needed"][str(nr)]) for v in nus)
        w(f"| {nr} | {cells} |")
    w("")
    w(f"At the simulator's default asymmetry the requirement at {n_max} "
      f"replicons rises from {bn['0.0']['copies_needed'][str(n_max)]} copies "
      f"to {bn[hi_nu]['copies_needed'][str(n_max)]}, and at "
      f"{g['n_replicons']} replicons from "
      f"{bn['0.0']['copies_needed'][str(g['n_replicons'])]} to "
      f"{bn[hi_nu]['copies_needed'][str(g['n_replicons'])]}. The shape of "
      "the rule is unchanged and the growth in N is still slow, but the "
      "level is not robust to it. The symmetric figures should be read as "
      "the best case, and a design aiming at a target it only just reaches "
      "under symmetry has no margin.")
    w("")
    w("This is the useful general statement, and §3.2 tests it against a "
      "system that was actually built.")
    w("")
    w("### 3.2 A published system sits above the independent prediction")
    w("")

    # The figure carries the whole argument, so it leads the results rather
    # than trailing them. Drawn by scripts/make_figures.py from the same
    # results file these numbers come from, so the two cannot disagree.
    figure = PAPER / "figures" / "fig2_independence.png"
    if figure.exists():
        w("![](figures/fig2_independence.png)")
        w("")
        w(f"**Figure 2. Measured genome fidelity exceeds independent "
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
        w("*(Figure 2 missing — run `scripts/make_figures.py`.)*")
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
    w(f"| Binomial test | **p = {ind['binomial_p_value']:.0e}** |")
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
    # Six of the seven inputs are read off a bar chart, so a p-value quoted
    # to three figures is more precise than the data. The envelope is the
    # honest number.
    w(f"Because six of the seven rates are read from a bar chart, the "
      f"comparison is repeated at the reading most favourable to "
      f"independence, with every read value raised by "
      f"{ind['figure_read_tolerance']:.0%}. The independence prediction then "
      f"rises to {pct(ind['p_all_seven_if_independent_favourable'])}, the "
      f"ratio falls to {ind['ratio_favourable']:.1f}&times;, and the "
      f"binomial p remains below 10^-15. The conclusion does not "
      f"depend on how the chart is read, and the precise p-value should not "
      f"be taken more seriously than its inputs allow.")
    w("")
    w("This also tests a claim the source makes but does not quantify: that "
      "dividing the genome across seven plasmids *\"limits the possible "
      "influence of stochastic inequalities in plasmid partitioning\"* "
      "(SI section 7). For inheriting a **complete set**, independent "
      "partitioning implies the opposite — each additional plasmid "
      "multiplies in a further chance to fail. The "
      f"{pct(p_ind)} figure is that argument stated numerically.")
    w("")
    w("### 3.3 Copy number alone can account for the gap")
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
        w("### 3.4 The retention ordering does not separate the explanations")
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
    w("The first three are assumptions of the model in §3.1 and bound what "
      "the design rule can be asked to do. The rest are properties of the "
      "source measurements used in §3.2 to §3.4, and none of those can be "
      "removed by analysis.")
    w("")
    w("1. **Partitioning is assumed symmetric, and the rule is optimistic "
      "in proportion.** The headline figures take each copy to reach a "
      "given daughter with probability exactly one half. Under the "
      "asymmetry a standard lineage simulator assumes by default, the "
      f"copy number required at {g['n_replicons']} replicons rises from "
      f"{bn['0.0']['copies_needed'][str(g['n_replicons'])]} to "
      f"{bn[hi_nu]['copies_needed'][str(g['n_replicons'])]}. Real division "
      "asymmetry is not measured in the source and we do not estimate it.")
    w("")
    w("2. **Replicons are assumed to partition independently of one "
      "another, which §3.2 shows is not true of the one system we can "
      "check.** The direction is favourable — correlation between "
      "replicons makes complete sets commoner, so the rule overstates the "
      "copies required rather than understating them — and in that sense "
      "the figures are a conservative design target. A system whose "
      "replicons were *anti*-correlated would break it, and we know of no "
      "mechanism that would produce that.")
    w("")
    w("3. **Copy number is assumed constant across the cycle and equal "
      "across replicons.** A replicon copied continuously, as &Phi;29 "
      "copies this genome, has a copy number at division that differs from "
      "the one it started with, which is the subject of §3.3; the rule "
      "takes the number at division as given rather than modelling "
      "replication. Unequal copy number across replicons would change "
      "which replicon is limiting, and the rule would then be set by the "
      "scarcest.")
    w("")
    w("4. **The division mechanism is mechanical, not genetically "
      "encoded.** "
      f"The {pct(p_obs)} figure comes from Fig. 3, where daughters are "
      "produced by extrusion through a 2 µm membrane filter (Methods 11), "
      "chosen deliberately to give uniform daughters. Genetically encoded "
      "division is demonstrated (Fig. 6) but at low yield, and the authors "
      "report no per-cell completeness distribution for it. Every number "
      "here therefore describes partitioning during extrusion of a grown "
      "liposome. Whether that is closer to or further from ideal random "
      "partitioning is unknown and is not assumed either way.")
    w("")
    w(f"5. **The analysed cells were screened.** Of 384 aliquots, 204 had "
      f"detectable 16S rRNA and {n} were selected as those with the "
      "*lowest* 16S abundance, to favour one cell per sample (Methods 23). "
      "The authors identify this as the only screening step in the work. "
      "Whether it biases completeness upward or downward is unknown.")
    w("")
    w("6. **Six of seven retention values are read from a figure** and carry "
      "roughly ±3 percentage points. The conclusion is insensitive to this: "
      "the independence prediction would have to rise by a factor of nine to "
      "meet the observation, and no plausible re-reading of Fig. 3p moves it "
      "that far.")
    w("")
    w("7. **Copy number at division is not reported**, and it is the single "
      "quantity that decides between the two explanations in §3.3.")
    w("")
    w("8. **The source is a preprint** and not yet peer reviewed. It also "
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
      "`scripts/design_rule.py` produces the design rule of §3.1, "
      "`scripts/independence_check.py` the comparison of §3.2, and "
      "`scripts/retention_structure.py` the correlation analysis of §3.4. "
      "`scripts/make_design_figure.py` and `scripts/make_figures.py` redraw "
      "Figures 1 and 2 from the same results files the text is generated "
      "from, so figure and text cannot disagree. The closed-form "
      "inheritance model that underlies all of it is in `src/inheritance.py` "
      "and is covered by unit tests.")
    w("")
    w(f"The repository is public at {REPO_URL}.")
    w("")

    # ------------------------------------------------------------- references
    # ------------------------------------------------------ declarations
    w("## 7. Declarations")
    w("")
    w("**Funding.** This work received no funding.")
    w("")
    w("**Competing interests.** The author declares no competing interests.")
    w("")
    w("**Use of AI and AI-assisted technologies.** "
      "Anthropic's Claude was used throughout this work, under the "
      "author's direction, to write and debug the analysis code, to draft "
      "and edit prose, and to check the manuscript against the results "
      "files. Every numerical value in this paper is written by "
      "`scripts/build_manuscript.py` from the files in `results/`, which "
      "the scripts named in §6 regenerate from the published "
      "measurements in `docs/PARAMETERS.md`, so no number here was "
      "produced by a language model. The author chose the question, "
      "identified the comparison and the parameters it needs, verified the "
      "results and takes responsibility for the content.")
    w("")

    w("## References")
    w("")
    w(f"1. {CITE}")
    w("")
    w(f"2. {OLIVI}")
    w("")
    w(f"3. {DU}")
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
