# The gate: is there anything here worth a paper?

**Run 2026-10-13, from the preprint's own numbers. Answer: yes — Case B.**

The project plan set a gate before any modelling: compute what random
partitioning predicts, compare it to what the paper measured, and only proceed
if the two disagree. They disagree by an order of magnitude, and the comparison
needs **no free parameters** — it uses two measurements the paper already
reports.

## The result

| | |
|---|---|
| Per-plasmid retention after 5 generations (Fig. 3p) | 71, 68, 63, 63, 57, 56, 52 % |
| mean retention | 61.4 % |
| **P(a cell has all 7) if the plasmids were independent** | **3.2 %** |
| **P(a cell has all 7) as measured (Fig. 3o)** | **30 %** |
| ratio | **9.4×** |
| of 95 single cells: predicted complete / observed complete | **3.0 / 28** |
| binomial test, 28 of 95 against p = 0.032 | **p = 1.3 × 10⁻¹⁹** |
| observed rate, 95 % CI | 29.5 % (20.6 – 39.7 %) |
| retention each plasmid would need for independence to hold | **84.2 %** |

Reproduce with `scripts\independence_check.py`. Nothing in it is fitted.

## Why this is the interesting direction

The gate had two possible outcomes. Case A — measured fidelity *below* what
chance predicts — would have been a story about an unmodelled loss mechanism.
This is **Case B**: fidelity far *above* chance. Something is making complete
genomes more common than independent partitioning allows.

That also sets up a direct quantitative test of a claim the authors make but do
not test (SI §7): that splitting the genome across seven plasmids *"limits the
possible influence of stochastic inequalities in plasmid partitioning"*. For
inheriting a complete set, independent partitioning says the opposite — each
extra plasmid multiplies in another chance to fail. The 3.2 % figure is that
argument made numerically.

## Two candidate explanations, and why the published data cannot separate them

**1. Copy number.** Phi29 replicates continuously with no checkpoint, so copy
number at the moment of division is not the ≈2.7 copies loaded at t = 0
(Methods 3 + Table S8). Working backwards: reaching 30 % over five generations
needs **≈4.9 copies per plasmid at each division**. A single partition at 3
copies already gives 39 %. So this explanation is numerically comfortable, and
it is a *physical* story.

**2. Selection.** The authors' own reading (SI §7): a cell that loses the
channel, the polymerase or the replicase grows badly and drops out, so the
surviving population is enriched for complete cells. This is *survivorship*,
not partitioning.

These make opposite predictions about which plasmids are lost, so the retention
ordering should discriminate. It does not — `scripts\retention_structure.py`:

```
retention vs SIZE       Spearman rho = -0.793  (p = 0.033)
retention vs NECESSITY  point-biserial r = +0.812  (p = 0.027)
size vs NECESSITY       Spearman rho = -0.433  (p = 0.332)
```

**Both fit, at n = 7.** The three largest plasmids (pLD1–3, 20–30 kbp) are also
the three the authors call dispensable, so the two predictors are partly
entangled and seven points cannot pull them apart.

One detail does cut against a pure size story: **GFP is the smallest plasmid at
2.5 kbp and is retained worse than αHL (4.3 kbp) and T7RNAP (5.4 kbp)**. Size
alone does not order them.

## The limitation that has to be stated up front

The 30 % comes from Figure 3, where division is **mechanical extrusion through
a 2 µm filter** (Methods 11), not the genetically encoded division of Figure 6.
The authors chose extrusion deliberately, for uniform daughters. So every
number here describes partitioning during extrusion of a grown liposome. Which
direction that biases the comparison is unknown.

Second: the 95 cells were selected from 204 as those with the **lowest 16S
abundance** (Methods 23), to favour one cell per sample. The authors flag it as
the only screening step in the paper. Whether it biases completeness up or down
is also unknown.

Both belong in the limitations, not in a footnote.
