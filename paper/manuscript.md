# Genome fidelity in a synthetic cell exceeds what independent plasmid partitioning allows

*Methods, Results and Limitations are generated from `results/` by `scripts/build_manuscript.py`; do not edit numbers here. Abstract, Introduction and Discussion are in `paper/sections/` and are the author's to write.*

Independent researcher, Beaumont, TX

## Abstract

A synthetic cell whose genome is divided across seven plasmids must deliver all seven to a daughter for that daughter to be complete. Using only two measurements reported by [the source preprint], and no fitted parameters, we show that independent partitioning of the seven plasmids predicts that 3.2% of daughters inherit a complete genome, against 30.0% measured: a factor of 9.4. Of 95 single cells, independence predicts 3 complete and 28 were observed (binomial p = 1.4e-19). Measured genome fidelity therefore exceeds what chance allows, and the excess is the quantity to explain. We show two explanations remain live and that the published data cannot separate them.

*(Outline above is generated. Rewrite in your own voice.)*

## 1. Introduction

*Outline to write: why a multi-plasmid genome makes inheritance a
combinatorial problem rather than a single-copy one; the authors'
claim that splitting the genome across plasmids *limits* the
influence of stochastic partitioning (SI section 7), and why that is
exactly backwards for inheriting a complete set; what a closed-form
calculation settles that a simulation would obscure.*

## 2. Methods

### 2.1 Source of every parameter

All values are taken from Gaut NJ, Deich C, Cash B, Hoog T, Engelhart AE, Adamala KP. *A Chemically Defined Synthetic Cell Capable Of Growth And Replication.* bioRxiv 2026.07.01.735724 (2026). doi:10.64898/2026.07.01.735724 and each is cited to the figure, table or methods section it came from in `docs/PARAMETERS.md`. No parameter is estimated, fitted or assumed. Two are used here:

| Quantity | Value | Source |
|---|---|---|
| Daughters retaining aHL | 71.0% | Fig. 3p |
| Daughters retaining T7RNAP | 68.0% | Fig. 3p |
| Daughters retaining GFP | 63.0% | Fig. 3p |
| Daughters retaining pREP | 63.0% | Fig. 3p |
| Daughters retaining pLD2 | 57.0% | Fig. 3p |
| Daughters retaining pLD3 | 56.0% | Fig. 3p |
| Daughters retaining pLD1 | 52.0% | Fig. 3p |
| Daughters retaining **all seven** | **30.0%** | Fig. 3o |
| Single cells analysed | 95 | Methods 23 |
| Generations | 5 | Fig. 3; Methods 11 |

Retention for &alpha;HL is stated numerically in SI section 6; the remaining six are read from the bar chart in Fig. 3p and carry approximately &plusmn;3 percentage points.

### 2.2 The independence prediction

If each plasmid reaches a given daughter independently of the others, the probability that daughter receives all seven is the product of the seven individual retention rates. This requires no model of division, no simulation and no free parameter; it is a consequence of the measurements themselves. The comparison is therefore a test of the independence assumption alone.

### 2.3 Significance

The 95 single cells are each complete or not, so the counts carry the test: a one-sided exact binomial test of the observed number of complete cells against the rate independence predicts. The interval on the observed rate is reported two-sided. One-sided is appropriate because the question is whether fidelity *exceeds* chance.

### 2.4 The copy-number alternative

A cell carrying *c* copies of each plasmid at division misses a given plasmid only if all *c* copies go to the other daughter. Writing *p* for the probability a copy reaches this daughter, the chance of a complete set is (1 - (1 - p)^c)^7. This is implemented in `src/inheritance.py` and is exercised by 21 unit tests. It matters here because &Phi;29 replicates continuously with no checkpoint, so copy number at division is not the 2.6 copies loaded at t = 0.

## 3. Results

### 3.1 Independent partitioning underpredicts fidelity ninefold

| | |
|---|---|
| Mean per-plasmid retention | 61.4% |
| **P(all seven) if independent** | **3.2%** |
| **P(all seven) measured** | **30.0%** |
| Ratio | **9.4×** |
| Complete cells of 95: predicted / observed | 3.0 / 28 |
| Binomial test | **p = 1.36e-19** |
| Observed rate (95% CI) | 29.5% (20.6%–39.7%) |
| Retention needed for independence to hold | 84.2% |

For independence to be consistent with the measured 30.0%, every one of the seven plasmids would have to be retained at 84.2% — against a measured mean of 61.4% and a measured maximum of 71.0%. No reading of Fig. 3p supports that.

This also tests a claim the source makes but does not quantify: that dividing the genome across seven plasmids *"limits the possible influence of stochastic inequalities in plasmid partitioning"* (SI section 7). For inheriting a **complete set**, independent partitioning implies the opposite — each additional plasmid multiplies in a further chance to fail. The 3.2% figure is that argument stated numerically.

### 3.2 Copy number alone can account for the gap

Independent partitioning of *c* copies per plasmid gives:

| Copies at division | One division | After 5 generations |
|---|---|---|
| 1 | 0.0078 | 0.0000 |
| 2 | 0.1335 | 0.0000 |
| 3 | 0.3927 | 0.0093 |
| 4 | 0.6365 | 0.1045 |
| 5 | 0.8007 | 0.3292 |

Surviving 5 independent divisions at 30.0% overall requires 78.6% per division, which independent partitioning reaches at **5 copies** per plasmid — against 2.6 loaded at t = 0.

**So the ninefold gap does not by itself demonstrate correlated partitioning.** Continuous replication to roughly twice the loaded copy number would produce the same observation with partitioning that is perfectly independent. The two explanations are not distinguishable from the reported data, and this paper does not claim to distinguish them.

### 3.3 The retention ordering does not separate the explanations

The two explanations predict different *orderings* of which plasmids are lost. A selective mechanism — the authors' own reading in SI section 7, that losing the channel, the polymerase or the replicase impairs growth — predicts retention tracks functional necessity. A physical mechanism predicts it tracks size or copy number. Both fit:

| Predictor | Statistic | p |
|---|---|---|
| Plasmid size | Spearman ρ = -0.793 | 0.033 |
| Functional necessity | point-biserial r = +0.812 | 0.027 |
| *size vs necessity (the confound)* | *Spearman ρ = -0.433* | *0.332* |

| Plasmid | Size (kbp) | Retention | Role |
|---|---|---|---|
| aHL | 4.3 | 71% | needed for growth |
| T7RNAP | 5.4 | 68% | needed for growth |
| GFP | 2.5 | 63% | resupplied / inert |
| pREP | 4.6 | 63% | needed for growth |
| pLD2 | 20.0 | 57% | resupplied / inert |
| pLD3 | 23.4 | 56% | resupplied / inert |
| pLD1 | 30.1 | 52% | resupplied / inert |

With n = 7 the two predictors cannot be separated: the three largest plasmids are also the three the authors describe as dispensable. One detail does cut against a purely size-driven account — GFP is the smallest plasmid at 2.5 kbp and is retained less well than two larger ones — but this is a single data point, not a discrimination.

## 4. Discussion

*Outline to write: what a ninefold excess over chance implies for
multi-plasmid synthetic genomes; why the authors' protection
argument needs reversing for complete-set inheritance; the one
experiment that would separate copy number from selection (per-cell
plasmid copy number at the moment of division, or retention measured
after genetically encoded rather than mechanical division); and what
this predicts for the single-chromosome design the authors propose.*

## 5. Limitations

These are properties of the source measurements, not of the calculation, and none of them can be removed by analysis.

1. **The division mechanism is mechanical, not genetically encoded.** The 30.0% figure comes from Fig. 3, where daughters are produced by extrusion through a 2 µm membrane filter (Methods 11), chosen deliberately to give uniform daughters. Genetically encoded division is demonstrated (Fig. 6) but at low yield, and the authors report no per-cell completeness distribution for it. Every number here therefore describes partitioning during extrusion of a grown liposome. Whether that is closer to or further from ideal random partitioning is unknown and is not assumed either way.

2. **The analysed cells were screened.** Of 384 aliquots, 204 had detectable 16S rRNA and 95 were selected as those with the *lowest* 16S abundance, to favour one cell per sample (Methods 23). The authors identify this as the only screening step in the work. Whether it biases completeness upward or downward is unknown.

3. **Six of seven retention values are read from a figure** and carry roughly ±3 percentage points. The conclusion is insensitive to this: the independence prediction would have to rise by a factor of nine to meet the observation, and no plausible re-reading of Fig. 3p moves it that far.

4. **Copy number at division is not reported**, and it is the single quantity that decides between the two explanations in §3.2.

5. **The source is a preprint** and not yet peer reviewed. It also contains an internal inconsistency — seven plasmids in Results, Fig. 3o and Table S6, but "eight" on p. 5. Table S6 lists seven and their sizes sum to the stated 90.3 kbp, so seven is used throughout.

## References

1. Gaut NJ, Deich C, Cash B, Hoog T, Engelhart AE, Adamala KP. *A Chemically Defined Synthetic Cell Capable Of Growth And Replication.* bioRxiv 2026.07.01.735724 (2026). doi:10.64898/2026.07.01.735724

*Reproduce every number above with `.venv\Scripts\python scripts\independence_check.py` and `scripts\retention_structure.py`.*
