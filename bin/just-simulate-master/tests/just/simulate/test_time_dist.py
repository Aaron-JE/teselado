import random
from collections import Counter
from datetime import timedelta

from just.simulate.time_dist import TimeDist


def test_time_dist_fixed():
    time_dist = TimeDist('fixed', 1, unit='minutes')
    assert time_dist.random_variate() == timedelta(minutes=1)


def test_time_dist_fixed_add():
    time_dist = TimeDist('fixed', 1, unit='minutes', weight=1.0) \
        + TimeDist('fixed', 2, unit='minutes', weight=1.0)
    assert time_dist.random_variate() in (
        timedelta(minutes=1), timedelta(minutes=2), )


def test_time_dist_fixed_add_another():
    time_dist = TimeDist('fixed', 1, unit='minutes', weight=1.0) \
        + TimeDist('fixed', 2, unit='minutes', weight=1.0) \
        + TimeDist('fixed', 3, unit='minutes', weight=1.0)
    assert time_dist.random_variate() in (
        timedelta(minutes=1), timedelta(minutes=2), timedelta(minutes=3))


def test_time_dist_fixed_add_with_weight():
    random.seed(0)
    time_dist = TimeDist('fixed', 1, unit='minutes', weight=0.1) \
        + TimeDist('fixed', 2, unit='minutes', weight=0.9)
    counter = Counter([time_dist.random_variate() for i in range(1_000)])
    assert counter[timedelta(minutes=1)] == 114
    assert counter[timedelta(minutes=2)] == 886


def test_time_dist_fixed_add_another_with_weight():
    random.seed(0)
    time_dist = TimeDist('fixed', 1, unit='minutes', weight=0.1) \
        + TimeDist('fixed', 2, unit='minutes', weight=0.2) \
        + TimeDist('fixed', 3, unit='minutes', weight=0.7)
    counter = Counter([time_dist.random_variate() for i in range(1_000)])
    assert counter[timedelta(minutes=1)] == 114
    assert counter[timedelta(minutes=2)] == 182
    assert counter[timedelta(minutes=3)] == 704


def test_time_dist_fixed_most_likely_estimate():
    time_dist = TimeDist('fixed', 1, unit='minutes')
    assert time_dist.most_likely_estimate() == timedelta(minutes=1)


def test_time_dist_fixed_add_most_likely_estimate():
    time_dist = TimeDist('fixed', 1, unit='minutes', weight=1.0) \
        + TimeDist('fixed', 2, unit='minutes', weight=1.0)
    assert time_dist.most_likely_estimate() == timedelta(seconds=90)
