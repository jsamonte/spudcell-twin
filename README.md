# spudcell-twin

**Why do SpudCell daughters lose plasmids, and what would fix it?**

SpudCell is a synthetic cell built from purified, non-living parts that feeds,
grows, replicates its genome and divides. Its genome sits on seven separate
plasmids, and at division every one has to reach both daughters. Seven
independent things going right is a demanding requirement, and that may be the
whole explanation.

## Status: blocked, deliberately

This project cannot start until [`docs/PARAMETERS.md`](docs/PARAMETERS.md) is
filled in from the preprint — by a person, because bioRxiv blocks automated
fetching and because everything said about SpudCell so far comes from news
coverage. News coverage does not carry parameter values with error bars.

`scripts/analytic_baseline.py` refuses to run without those numbers rather than
falling back on plausible defaults.

## The first step is a calculation, not a simulation

If each plasmid partitions independently, what fraction of daughters get all
seven? That is closed form, already implemented and tested here. Comparing it
against the rate the preprint reports decides which of three papers this
becomes:

| | |
|---|---|
| **A** | Binomial explains it → no active mechanism needed; a short report, two months saved |
| **B** | Observed fidelity beats chance → something helps; model the candidate mechanisms |
| **C** | Observed fidelity is worse than chance → something hurts; a spatial model is justified |

All three are publishable. The point is to learn which one in an afternoon
rather than in week eight.

## License

MIT.
