<!-- DRAFT -->
The design rule is the part of this work that generalises. A synthetic genome
divided across *N* replicons and partitioned at random needs roughly log2 *N*
more copies of each replicon than an undivided one would, and that is the
whole of the inheritance cost. Across the range a synthetic biologist is
likely to work in, one to twelve replicons, it comes to four extra copies at
the 50% target and four again at the 90% target. The reason the penalty is
that small is structural. Replicon count sits in the exponent, but every
additional copy halves the chance of losing a given replicon, so a geometric
lever is available against a geometric cost.

Two readings of the same arithmetic are easy to confuse, and the difference
matters for how a result like this is used. Hold copy number fixed at five
and split a genome twelve ways, and completeness after five generations falls
from 85.3% to 14.9%, a factor of 5.7, which reads as a design being
destroyed. Ask instead what it would take to restore it, and the answer is
four more copies. The first reading describes what happens to a design left
alone; the second describes what it costs to repair one, and only the second
is a decision anybody actually makes. A multipartite synthetic genome is
better understood as a copy-number requirement than as an inheritance
problem.

The test against the one system that has been built is almost shockingly
simple, and that is its point.
Seven measured retention rates, multiplied together, give 3.2%. The measured
figure is 30%. Nothing is fitted, nothing is simulated, and no parameter is
estimated. Therefore, there is no model to attack but only an arithmetic consequence of
two numbers Gaut et al. already report.

However, what the gap means is less simple. A factor of 9.4 is not a discrepancy to be explained away by measurement error, because for independent partitioning to hold, every one of the seven plasmids would have to be retained at 84.2%, against a
measured mean of 61.4% and a measured best of 71%. Something is making
complete genomes commoner than chance allows.

Two explanations survive, but we cannot choose between them. The first is copy
number. The replication enzyme operates continuously with no checkpoint, so
the number of copies present when a cell divides is not the ≈2.7 loaded at the
start. Reaching 30% over five generations requires roughly five copies per plasmid at each division, and that assumption is not extravagant. The second
is selection, which is the authors' own reading. The claim is that a cell that loses the
membrane channel, the polymerase or the replicase grows poorly and is
outcompeted, so the surviving population is enriched for complete genomes.
These are different claims. One is about partitioning, the other about survivorship, and they predict different orderings of which plasmids are lost.

That prediction is testable with the data in hand, and it fails to
discriminate. Retention correlates with plasmid size (Spearman ρ = −0.79) and
with functional necessity (point-biserial r = +0.81), both significant at
n = 7, because the three largest plasmids are also the three the authors
describe as dispensable. Seven points cannot separate two entangled
predictors. One detail argues against a purely physical account, which is that the GFP
plasmid is the smallest at 2.5 kbp and is retained worse than two larger ones. However, one detail is not a discrimination, and we do not treat it as one.

The result bears directly on a design claim Gaut et al. make without testing it. That claim is that dividing the genome across seven plasmids *limits* the influence of stochastic partitioning. For the inheritance of a **complete
set**, independent partitioning implies the opposite, and each additional plasmid
is another independent opportunity to fail. The product of seven sub-unity probabilities falls quickly. Splitting a genome may well protect
against other failure modes but for complete-set inheritance it is a cost, and 3.2% is the size of that inheritance cost under the
assumption the claim implicitly makes. However, the split certainly makes the construct easier to
modify, which is the authors' stated engineering reason.

Two limitations condition everything above, and both come from the authors'
own methods. The 30% figure is measured on daughters produced by
mechanical extrusion through a 2 µm filter, not by the genetically encoded
division the same paper demonstrates. Also, extrusion was chosen deliberately, for
uniform daughters and higher yield. Whether forcing division through a pore
partitions contents more or less evenly than spontaneous scission is unknown,
and we do not assume either. Separately, the 95 single cells analysed were
selected from 204 as those with the lowest ribosomal RNA content, to maximise
the chance that each sample held one cell, and the authors identify this as the
only screening step in the work. Whether that selection biases completeness
upward or downward is likewise unknown.

The experiment that would settle this is a measurement of per-cell plasmid copy number at the moment of division. If the copy number at division is four or fewer, selection, as Gaut et al. claim, could be doing the work. If it is near five, partitioning may be independent after all, and cells receive a full set on the strength of multiple copies alone. If that were the case, no correlation would need to be invoked. The same measurement would convert this calculation from a lower bound into a prediction.

The rule also says something about where such a design should go next. The
authors propose consolidating onto a single chromosome, and the calculation
supports it for a reason worth stating precisely. Consolidation does not make
inheritance reliable on its own. Even on a single replicon, a lineage holds a
complete genome through five generations only 23.7% of the time at two copies
and 51.3% at three, so a consolidated genome at the copy number this system
loads would still lose most lineages. What consolidation buys is that the
copy number needed to reach
any given target stops rising, so the same replication effort goes further.
Raising copy number and reducing replicon count are substitutes, and at small
N the first is usually the cheaper of the two.
