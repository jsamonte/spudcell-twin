<!-- DRAFT -->

A cell that divides must give each daughter a complete copy of its genome.
Bacteria achieve this with dedicated machinery; synthetic cells assembled from
purified components generally have none, and must rely on the contents of the
parent being distributed by chance. How well that works sets a ceiling on how
many generations such a system can run.

For a single plasmid present in many copies, the answer is classical and
reassuring. If each copy independently enters one daughter or the other with
equal probability, a daughter receives none of them with probability
2^(1−n) in the mother's copy number n, so loss falls exponentially as copy
number rises. This is why reviews of synthetic cell division observe that
random partitioning suffices provided the cargo consists of a large number of
relatively small, identical molecules (Olivi et al., 2021).

A multipartite genome breaks that assumption in a way that has not, to our
knowledge, been analysed. When the genome is divided across several
*distinct* plasmids, a daughter is viable only if it receives at least one
copy of **every** type. If the types partition independently, the probability
of a complete set is the product of the individual retention probabilities,
and a product of numbers below one falls quickly in the number of terms. The
design decision that makes a synthetic genome easier to assemble and modify
therefore carries an inheritance cost, and the size of that cost has not been
quantified.

We searched for prior treatments of joint retention across multiple distinct
replicons and found none. The literature on plasmid segregation is extensive
but concerns copy number of a single type; natural multipartite genomes, such
as that of *Vibrio cholerae*, maintain their replicons with active
segregation systems rather than by chance.

> **>>> ADD ANY PRIOR WORK YOU HAVE READ, IN YOUR OWN WORDS <<<**
>
> I verified: Olivi L, Berger M, Creyghton R, De Franceschi N, Dekker C,
> Mulder B, Claassens N, ten Wolde P, van der Oost J. *Towards a synthetic
> cell cycle.* Nature Communications 12, 4531 (2021).
> doi:10.1038/s41467-021-24772-8 — checked against Crossref.
>
> I searched the plasmid-segregation and synthetic-cell literature and found
> nothing modelling joint retention of several distinct replicons. That search
> was not exhaustive: no theses, no paywalled work. Write "to our knowledge",
> never "none exists".

Gaut et al. (2026) report a synthetic cell whose 90 kbp genome is carried on
seven plasmids, which feeds, grows, replicates its DNA and divides, and which
sustains five generations with 30% of daughters retaining the complete genome
despite having no segregation machinery. They also report the per-plasmid
retention rates. Those two measurements are sufficient, on their own, to test
whether the plasmids are inherited independently — a test the paper does not
perform. We perform it here.
