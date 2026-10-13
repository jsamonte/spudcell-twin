"""Closed-form plasmid inheritance at division.

This is the module that makes the benchmark scorable without a judge: for
plasmids partitioned at random when a cell divides, the probability that a
daughter inherits a complete set has an exact answer, so a simulation or an
agent can be checked against it rather than assessed.

It is also the analytic first step of the SpudCell inheritance project, whose
own plan insists on a closed-form calculation before any simulation: "A
Smoldyn model that reproduces what a binomial calculation already told us is
two wasted months."

**The partition probability is not 0.5 by default.** bioscrape's
LineageVolumeSplitter draws, once per division and shared across every
species in it:

    p = 0.5 - uniform(0, 1) * partition_noise / 2        (lineage.pyx:2226)

with `partition_noise` defaulting to 0.5. So p ~ Uniform(0.5 - nu/2, 0.5) and
one daughter is systematically the smaller. For seven single-copy plasmids
that moves P(a named daughter gets all seven) from 1/128 to about 1/512.
Every function here takes `noise` explicitly for that reason.

Verified against 400,000 Monte-Carlo draws on 2026-10-11; see
tests/test_inheritance.py, which re-checks it on every run.
"""

from dataclasses import dataclass


def complete_set_probability(n_plasmids, copy_number=1, noise=0.0):
    """P(one named daughter receives at least one copy of all N plasmid types).

    Each of the `copy_number` copies of each plasmid goes to this daughter
    independently with probability p, so a given plasmid type is missed with
    probability (1-p)^copy_number and the N types are independent given p.
    With noise, p is itself random and the result is E[(1-(1-p)^c)^N].

    noise = 0 gives the textbook fair-partition answer.
    """
    _validate(n_plasmids, copy_number, noise)
    if noise == 0.0:
        return (1.0 - 0.5 ** copy_number) ** n_plasmids
    return _average_over_p(
        lambda p: (1.0 - (1.0 - p) ** copy_number) ** n_plasmids, noise)


def any_copy_probability(copy_number=1, noise=0.0):
    """P(a named daughter receives at least one copy of ONE given plasmid)."""
    _validate(1, copy_number, noise)
    if noise == 0.0:
        return 1.0 - 0.5 ** copy_number
    return _average_over_p(lambda p: 1.0 - (1.0 - p) ** copy_number, noise)


def loss_probability(n_plasmids, copy_number=1, noise=0.0):
    """P(a named daughter is missing at least one plasmid type) -- the failure
    rate an experiment would report for that daughter."""
    return 1.0 - complete_set_probability(n_plasmids, copy_number, noise)


def either_daughter_complete_probability(n_plasmids, copy_number=1, noise=0.0):
    """P(at least one of the two daughters receives a complete set).

    Not twice the single-daughter figure: with one copy of each plasmid the two
    events are mutually exclusive, but above one copy they are not, so this is
    computed by inclusion-exclusion under the same p.
    """
    _validate(n_plasmids, copy_number, noise)

    def f(p):
        a = (1.0 - (1.0 - p) ** copy_number) ** n_plasmids      # this daughter
        b = (1.0 - p ** copy_number) ** n_plasmids              # the other one
        both = (1.0 - p ** copy_number - (1.0 - p) ** copy_number) ** n_plasmids
        return a + b - both

    return f(0.5) if noise == 0.0 else _average_over_p(f, noise)


def copies_needed_for(target, n_plasmids, noise=0.0, max_copies=200):
    """Smallest per-plasmid copy number reaching `target` complete inheritance.

    The question a wet-lab group can act on: how many copies would it take?
    Returns None if `max_copies` is not enough.
    """
    for c in range(1, max_copies + 1):
        if complete_set_probability(n_plasmids, c, noise) >= target:
            return c
    return None


def replicons_needed_for(target, copy_number=1, noise=0.0, max_replicons=64):
    """Largest number of separate plasmids still reaching `target`.

    The other actionable lever: consolidating a genome onto fewer replicons.
    Returns 0 if even a single replicon falls short.
    """
    best = 0
    for n in range(1, max_replicons + 1):
        if complete_set_probability(n, copy_number, noise) >= target:
            best = n
        else:
            break
    return best


@dataclass(frozen=True)
class InheritanceSummary:
    n_plasmids: int
    copy_number: int
    noise: float
    p_min: float
    p_max: float
    complete_one_daughter: float
    complete_either_daughter: float
    loss_one_daughter: float

    def as_dict(self):
        return {k: getattr(self, k) for k in self.__annotations__}


def summarize(n_plasmids, copy_number=1, noise=0.0):
    """Everything a tool or a benchmark scorer needs, in one small object."""
    _validate(n_plasmids, copy_number, noise)
    return InheritanceSummary(
        n_plasmids=n_plasmids,
        copy_number=copy_number,
        noise=noise,
        p_min=0.5 - noise / 2,
        p_max=0.5,
        complete_one_daughter=complete_set_probability(n_plasmids, copy_number, noise),
        complete_either_daughter=either_daughter_complete_probability(
            n_plasmids, copy_number, noise),
        loss_one_daughter=loss_probability(n_plasmids, copy_number, noise),
    )


# --- internals ---------------------------------------------------------

def _validate(n_plasmids, copy_number, noise):
    if n_plasmids < 1:
        raise ValueError(f"n_plasmids must be at least 1, got {n_plasmids}")
    if copy_number < 1:
        raise ValueError(f"copy_number must be at least 1, got {copy_number}")
    if not 0.0 <= noise <= 1.0:
        raise ValueError(
            f"noise must be between 0 and 1 (bioscrape's partition_noise range), got {noise}")


def _average_over_p(f, noise, n_nodes=2001):
    """E[f(p)] for p ~ Uniform(0.5 - noise/2, 0.5), by Simpson's rule.

    f is a polynomial in p, so Simpson's rule is exact for the low-degree cases
    and converges very fast for the rest; an odd node count keeps the rule
    well-formed. Chosen over a closed-form expansion because f changes with
    copy_number and the two-daughter case, and a single numerically exact
    routine is easier to trust than four hand-derived formulas.
    """
    lo, hi = 0.5 - noise / 2, 0.5
    h = (hi - lo) / (n_nodes - 1)
    total = f(lo) + f(hi)
    for i in range(1, n_nodes - 1):
        total += (4 if i % 2 else 2) * f(lo + i * h)
    return total * h / 3 / (hi - lo)
