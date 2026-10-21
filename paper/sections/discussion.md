<!-- DRAFT -->

The calculation above is almost embarrassingly simple, and that is its point.
Seven measured retention rates, multiplied together, give 3.2%. The measured
figure is 30%. Nothing is fitted, nothing is simulated, and no parameter is
estimated — so there is no model to attack, only an arithmetic consequence of
two numbers the source paper already reports.

What the gap means is less simple. A factor of 9.4 is not a discrepancy to be
explained away by measurement error: for independent partitioning to hold,
every one of the seven plasmids would have to be retained at 84.2%, against a
measured mean of 61.4% and a measured best of 71%. Something is making
complete genomes commoner than chance allows.

Two explanations survive, and we cannot choose between them. The first is copy
number. The replication enzyme operates continuously with no checkpoint, so
the number of copies present when a cell divides is not the ≈2.7 loaded at the
start; reaching 30% over five generations requires roughly five copies per
plasmid at each division, which is not an extravagant assumption. The second
is selection, which is the source paper's own reading: a cell that loses the
membrane channel, the polymerase or the replicase grows poorly and is
outcompeted, so the surviving population is enriched for complete genomes.
These are different claims — one about partitioning, one about survivorship —
and they predict different orderings of which plasmids are lost.

That prediction is testable with the data in hand, and it fails to
discriminate. Retention correlates with plasmid size (Spearman ρ = −0.79) and
with functional necessity (point-biserial r = +0.81), both significant at
n = 7, because the three largest plasmids are also the three the authors
describe as dispensable. Seven points cannot separate two entangled
predictors. One detail argues against a purely physical account — the GFP
plasmid is the smallest at 2.5 kbp and is retained worse than two larger ones —
but one detail is not a discrimination, and we do not treat it as one.

The result bears directly on a design claim the source paper makes without
testing it: that dividing the genome across seven plasmids *limits* the
influence of stochastic partitioning. For the inheritance of a **complete
set**, independent partitioning implies the opposite. Each additional plasmid
is another independent opportunity to fail, and the product of seven
sub-unity probabilities falls quickly. Splitting a genome may well protect
against other failure modes — it certainly makes the construct easier to
modify, which is the authors' stated engineering reason — but for complete-set
inheritance it is a cost, and 3.2% is the size of that cost under the
assumption the claim implicitly makes.

Two limitations condition everything above, and both come from the source
paper's own methods. The 30% figure is measured on daughters produced by
mechanical extrusion through a 2 µm filter, not by the genetically encoded
division the same paper demonstrates; extrusion was chosen deliberately, for
uniform daughters and higher yield. Whether forcing division through a pore
partitions contents more or less evenly than spontaneous scission is unknown,
and we do not assume either. Separately, the 95 single cells analysed were
selected from 204 as those with the lowest ribosomal RNA content, to maximise
the chance that each sample held one cell; the authors identify this as the
only screening step in the work. Whether that selection biases completeness
upward or downward is likewise unknown.

The experiment that would settle the mechanism is a measurement of per-cell
plasmid copy number at the moment of division. If copy number at division is
near the ≈2.7 loaded, selection is doing the work; if it is near five,
partitioning may be independent after all and nothing further is required. The
same measurement would also convert this calculation from a bound into a
prediction.
