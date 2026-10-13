# Parameters

**Status: FILLED from the preprint, 2026-10-13.** Source throughout:

> Gaut NJ, Deich C, Cash B, Hoog T, Engelhart AE, Adamala KP.
> *A Chemically Defined Synthetic Cell Capable Of Growth And Replication.*
> bioRxiv 2026.07.01.735724, posted 2 July 2026.
> doi:10.64898/2026.07.01.735724

Every number below names the figure, table or methods section it came from. A
number without provenance is a bug; a plausible guess is worse than a bug.

## The warning, resolved — and it is the most important fact here

The project plan flagged a risk: that daughters are produced by pushing cells
through a filter rather than dividing by themselves. **Confirmed, and it
applies to exactly the measurement this project compares against.**

> "Our synthetic cells divide without cytoskeleton. Division is first achieved
> by **mechanical extrusion through a membrane filter** (Figures 3, 4 and 5)."
> — Results and Discussion, p. 3

> "After 12 hours at 30°C, the samples were extruded using a mini-extruder
> (Avanti, 610023) with a **2 µm membrane** (Whatman, 76457-184)."
> — Methods 11

The 30% complete-genome figure comes from **Figure 3**, i.e. from extrusion.
Their own rationale (Methods 11): mechanical division "ensures complete
division and uniform size of daughter cells", chosen deliberately to decouple
variables while optimising the cell cycle.

Genetically encoded division exists (Figure 6) but has **low yield**, and the
authors say so: "relatively low yields of this division mechanism make it
difficult to investigate with more granularity" (SI §9). Figure 6r confirms
every plasmid reaches the daughter fraction, but gives no per-cell completeness
distribution.

**Consequence for this project:** the model being compared is extrusion of a
grown liposome through a 2 µm pore, not spontaneous scission. Whether that is
closer to or further from ideal random partitioning is an open question and
should be stated as a limitation, not assumed either way.

## Table 1 — parameters taken from the paper

| Parameter | Value | Units | Source | Notes |
|---|---|---|---|---|
| Number of distinct plasmids | **7** | count | Results p. 3; Table S6; Fig. 1b | See the discrepancy note below |
| Plasmid identities | pREP, pLD1, pLD2, pLD3, GFP, T7RNAP, αHL | — | Table S6 | |
| Plasmid sizes | 4.6 / 30.1 / 20.0 / 23.4 / 2.5 / 5.4 / 4.3 | kbp | Table S6; Fig. 1b | sums to 90.3 |
| Total genome size | **90.3** | kbp | Table S6 | |
| Plasmid concentration, genome experiments | **2.5** | nM each | Methods 3 | "in experiments with the whole 90kb genome, each plasmid was at 2.5nM" |
| Concentration → copy number | 1 nM ≈ **1.06** copies | copies/nM | Table S8 | for 1.5 µm liposomes, 1.77 fL |
| **Copy number per plasmid** | **≈ 2.7** | copies | derived: 2.5 × 1.06 | **the single most important number** |
| **Daughters with a complete genome** | **30%** | % of cells | **Results p. 6; Fig. 3o, 3p** | **the number this project compares against** |
| Generations | 5 | cycles | Fig. 3; Methods 11 | |
| Cycle time | 12 | h per generation | Methods 11 | at 30 °C |
| Division method (for the 30%) | mechanical extrusion, 2 µm pore | — | Methods 11 | **see the warning above** |
| Single cells analysed | 95 | cells | Methods 23; Fig. S32 | of 384 aliquots; 204 had 16S; 95 kept |
| Starting liposome size | extruded at 2 µm | µm | Methods 4, 11 | 1 mM total lipid |
| Cell diameter, undivided | ≈ 950 | nm | Fig. S64 (DLS) | |
| Cell diameter, after division | ≈ 800 | nm | Fig. S64 (DLS) | His system |
| Replication | Phi29, rolling circle | — | Methods 2; ref 20 | active continuously, no checkpoint |
| Cell number growth | 420 → 730 → 1160 /µL | cells/µL | Fig. S39 | gens 3, 4, 5 |

### Per-plasmid retention after 5 generations (Fig. 3p / Fig. S33)

Read off the figure, so treat as approximate (±3 points):

| Plasmid | Detected in | Note |
|---|---|---|
| αHL | **71%** | stated numerically in SI §6 |
| T7RNAP | ~68% | |
| GFP | ~63% | |
| pREP | ~63% | |
| pLD2 | ~57% | |
| pLD3 | ~56% | |
| pLD1 | ~52% | largest plasmid, 30.1 kbp |

The authors' own reading (SI §7): pLD1–3 and GFP are lost at the highest rates,
αHL / T7RNAP / pREP are retained best, and they attribute this to selection —
losing the membrane channel, the polymerase or the replicase hurts a cell's
ability to grow, whereas losing a tRNA-synthetase plasmid or GFP does not,
because feeder liposomes resupply ribosomes and GFP does nothing.

**This is a direct, testable alternative to random partitioning**, and it is the
authors' hypothesis rather than ours.

### A discrepancy worth knowing about

The paper says **seven** plasmids in Results (p. 3), Figure 3o ("the 7-plasmid
genome") and Table S6 — but **eight** on p. 5 ("divided into eight plasmids
(Table S6)"). Table S6 lists seven, and their sizes sum to 90.3 kbp, matching
the stated genome size. **Seven is correct**; the "eight" is an error in the
preprint. Use seven and do not cite the p. 5 sentence.

## Table 2 — parameters the model needs that the paper does not report

Every row is a FREE parameter.

| Parameter | Why the model needs it | Status |
|---|---|---|
| Copy number *at the moment of division* | Phi29 runs continuously, so copy number at extrusion is not the 2.7 copies loaded at t=0 | **FREE — and it dominates the answer** |
| Per-plasmid partition correlation | whether a cell that keeps one plasmid tends to keep all | FREE |
| Whether replication restores copy number each cycle | decides whether 5 generations compound or not | FREE (Fig. 3a/e/i show new DNA each generation, but not per-cell copy number) |
| Plasmid-size dependence of partitioning | pLD1 is 30 kbp and lost most; is that size or selection? | FREE |
| Survival bias in the single-cell assay | 95 of 384 aliquots were kept, selected for *lowest* 16S | FREE — see below |

### The selection step in the single-cell assay

Methods 23: of 384 aliquots, 204 had detectable 16S rRNA, and **95 were chosen
— those with the lowest 16S abundance**, to maximise the chance of one cell per
sample. The authors flag this as "the only experiment in this project where
some samples were removed based on initial screening."

So the 30% is measured on cells selected for low ribosome content. Whether that
biases completeness up or down is unknown and should be stated.

## Table 3 — what the authors say is unresolved

From SI §9 ("The limitations and ways forward") and SI §7:

- "Synthetic cells presented here have **no such spatial organization aids**"
  — no cytoskeleton, no segregation machinery.
- "**Future work on this system is needed to investigate genome distribution
  after the genetically encoded division.**" ← this project's opening, in their
  words.
- "not all daughter cells receive full complement of plasmids. **This is the
  main limitation of multi-part genome**, one that will hopefully be solved
  after the genome is optimized and placed on single chromosome."
- They justify the multi-plasmid design as *protective*: "The fact that genes
  are divided into multiple, physically separate plasmids, **limits the possible
  influence of stochastic inequalities in plasmid partitioning**" (SI §7) —
  a quantitative claim they do not test, and one a binomial calculation can.

**That last point is the sharpest opening.** The authors argue splitting the
genome across seven plasmids *protects against* partition noise. The opposite
is arguably true for inheriting a complete set, and the maths settles it.
