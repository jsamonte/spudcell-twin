"""The closed-form inheritance maths, checked against simulation.

These formulas are the benchmark's ground truth, so they are not taken on
trust: every analytic value is re-derived by Monte Carlo here, drawing p the
way bioscrape's splitter draws it. If the library changes how it partitions,
or if a formula is wrong, this fails.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.inheritance import (  # noqa: E402
    any_copy_probability, complete_set_probability, copies_needed_for,
    either_daughter_complete_probability, loss_probability,
    replicons_needed_for, summarize)

DRAWS = 200_000


def monte_carlo(n_plasmids, copy_number, noise, seed=0):
    """Simulate the splitter directly: one p per division, shared by all
    species, each copy assigned independently."""
    rng = np.random.default_rng(seed)
    p = 0.5 - rng.random(DRAWS) * noise / 2
    # copies of each plasmid type reaching this daughter
    got = rng.binomial(copy_number, p[:, None], size=(DRAWS, n_plasmids))
    return (got >= 1).all(axis=1).mean()


@pytest.mark.parametrize("n,c,noise", [
    (7, 1, 0.0), (7, 1, 0.25), (7, 1, 0.5),
    (1, 1, 0.0), (3, 2, 0.0), (7, 2, 0.5), (4, 3, 0.3),
])
def test_closed_form_matches_simulation(n, c, noise):
    analytic = complete_set_probability(n, c, noise)
    empirical = monte_carlo(n, c, noise)
    # Binomial standard error at this many draws, with room to spare.
    tol = 5 * (max(analytic, 1e-6) * (1 - analytic) / DRAWS) ** 0.5 + 2e-4
    assert abs(analytic - empirical) < tol, (analytic, empirical, tol)


def test_fair_partition_is_one_over_two_to_the_n():
    assert complete_set_probability(7, 1, 0.0) == pytest.approx(1 / 128)
    assert complete_set_probability(1, 1, 0.0) == pytest.approx(0.5)


def test_library_default_is_four_times_worse_than_a_fair_coin():
    """The finding that set this project's plan. SpudCell has seven plasmids,
    and accepting bioscrape's default silently costs a factor of about four."""
    fair = complete_set_probability(7, 1, noise=0.0)
    default = complete_set_probability(7, 1, noise=0.5)
    assert fair / default == pytest.approx(4.0, rel=0.02)
    assert default == pytest.approx(0.001945, rel=0.01)


def test_noise_only_ever_hurts():
    values = [complete_set_probability(7, 1, noise=x) for x in (0.0, 0.2, 0.5, 0.8, 1.0)]
    assert values == sorted(values, reverse=True)


def test_more_copies_and_fewer_plasmids_both_help():
    assert (complete_set_probability(7, 2, 0.0)
            > complete_set_probability(7, 1, 0.0))
    assert (complete_set_probability(3, 1, 0.0)
            > complete_set_probability(7, 1, 0.0))


def test_loss_is_the_complement():
    assert (loss_probability(7, 1, 0.5)
            == pytest.approx(1 - complete_set_probability(7, 1, 0.5)))


def test_single_plasmid_matches_any_copy():
    for c in (1, 2, 5):
        for noise in (0.0, 0.5):
            assert (complete_set_probability(1, c, noise)
                    == pytest.approx(any_copy_probability(c, noise)))


def test_either_daughter_is_exactly_double_at_single_copy():
    """With one copy of each plasmid the two daughters cannot both be
    complete, so the events are disjoint."""
    one = complete_set_probability(7, 1, 0.0)
    assert either_daughter_complete_probability(7, 1, 0.0) == pytest.approx(2 * one)


def test_either_daughter_is_less_than_double_above_single_copy():
    one = complete_set_probability(3, 4, 0.0)
    either = either_daughter_complete_probability(3, 4, 0.0)
    assert one < either < 2 * one


def test_actionable_levers_for_spudcell():
    """The two numbers a wet-lab group could act on, for seven plasmids at the
    library's default partitioning."""
    copies = copies_needed_for(0.95, 7, noise=0.5)
    assert 1 < copies < 50, copies
    assert complete_set_probability(7, copies, 0.5) >= 0.95
    assert complete_set_probability(7, copies - 1, 0.5) < 0.95

    replicons = replicons_needed_for(0.95, copy_number=1, noise=0.0)
    assert replicons == 0, "one single-copy replicon cannot reach 95%"


def test_summary_is_self_consistent():
    s = summarize(7, 1, 0.5)
    assert s.p_min == pytest.approx(0.25) and s.p_max == 0.5
    assert s.loss_one_daughter == pytest.approx(1 - s.complete_one_daughter)
    assert set(s.as_dict()) >= {"n_plasmids", "noise", "complete_one_daughter"}


@pytest.mark.parametrize("kwargs", [
    dict(n_plasmids=0), dict(n_plasmids=7, copy_number=0),
    dict(n_plasmids=7, noise=1.5), dict(n_plasmids=7, noise=-0.1),
])
def test_invalid_inputs_are_rejected(kwargs):
    with pytest.raises(ValueError):
        complete_set_probability(**kwargs)
