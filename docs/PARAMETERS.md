# Parameters

**Status: EMPTY ON PURPOSE. This file is the project's gate.**

Nothing in `src/` may use a number that is not in the first table below with a
figure or table number beside it. A parameter is either (a) cited to the
preprint or another paper, naming where it came from, or (b) explicitly marked
FREE. There is no third category, and inventing a plausible value is the worst
thing that can happen in this repository.

The analytic machinery is already written and tested (`src/inheritance.py`,
mirrored from `cellfree-mcp`). It takes these numbers as arguments. The moment
the table below is filled, `scripts/analytic_baseline.py` runs and the project
reaches its first real gate in minutes rather than days.

## How to fill this in

Read **Gaut NJ et al. (2026), "A chemically defined synthetic cell capable of
growth and replication", bioRxiv 2026.07.01.735724**. One paper, one evening.
Search bioRxiv for `2026.07.01.735724`, or Google Scholar for "SpudCell
chemically defined synthetic cell". It is a preprint, so it is free.

bioRxiv blocks automated fetching, which is why this has to be a person
reading it rather than a script. Everything anyone has said about SpudCell in
this project so far comes from news coverage, and news coverage does not carry
parameter values with error bars.

Write what you find straight into the tables, with the figure or table number.
If the paper does not report something, write "not reported" — that is the
answer, and it moves the row to the second table.

## Table 1 — parameters taken from the paper

| Parameter | Value | Units | Source (figure/table) | Notes |
|---|---|---|---|---|
| Number of distinct plasmids | | count | | news coverage says 7 — VERIFY |
| Copy number, per plasmid | | copies | | the single most important number here |
| Total genome size | | kbp | | news coverage says ~90 — VERIFY |
| Fraction of daughters inheriting a complete genome | | fraction | | **the number the whole project compares against** |
| Vesicle or cell diameter | | µm | | and its spread |
| Division trigger | | — | | spontaneous, or assisted? |
| **Is division assisted by extrusion through a filter or sieve?** | | yes/no | | **see the warning below** |
| Cycle time | | min or h | | |
| Protein concentrations or expression rates | | | | if given |

## Table 2 — parameters the model needs that the paper does not report

Every row here is a FREE parameter. If this table ends up longer than Table 1,
stop and narrow the question before writing any model code.

| Parameter | Why the model needs it | Candidate source | Status |
|---|---|---|---|
| Per-plasmid partition correlation | whether copies of one plasmid co-segregate | — | FREE |
| Plasmid diffusion coefficient | whether contents equilibrate before the membrane closes | literature on DNA diffusion in crowded media | FREE |
| Time from membrane constriction to scission | sets the window for the above | — | FREE |

## Table 3 — what the authors say is unresolved

Their own "future work" paragraph is where the project's question should come
from. Copy the relevant sentences here.

## The warning that could change the whole model

News coverage stated that SpudCell daughters are produced by pushing cells
through a **filter or sieve**, rather than dividing by themselves. **Check this
specifically.** If division is physically assisted, then idealised geometric
division is not what happened, and a model of spontaneous partitioning is
modelling the wrong process. This single fact changes the design, so find it
before anything else.

## What happens once this file is filled

`scripts/analytic_baseline.py` computes, under independent partitioning, the
probability that a daughter receives at least one copy of every plasmid, and
compares it against the inheritance rate the paper reports. That comparison
decides which of three papers this project becomes:

- **A — the binomial explains it.** Stochastic partitioning alone accounts for
  the observed failure rate; no active mechanism is needed. A short, clean
  result, written up as a brief report. Two months saved and a preprint in hand.
- **B — the binomial predicts worse than observed.** Something is helping.
  Model candidate mechanisms and ask which could produce the observed fidelity.
- **C — the binomial predicts better than observed.** Something hurts beyond
  chance. Spatial effects, aggregation, or asymmetric division, and now a
  spatial model is justified and you know what it has to explain.

All three are publishable. The point of the gate is to learn which one you are
writing in an afternoon, rather than in week eight.
