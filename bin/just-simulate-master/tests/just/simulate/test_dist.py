import random
from collections import Counter

from just.simulate.dist import Dist


def test_dist_fixed():
    time_dist = Dist('fixed', 1)
    assert time_dist.random_variate() == 1


def test_dist_fixed_add():
    time_dist = Dist('fixed', 1, weight=1.0) \
        + Dist('fixed', 2, weight=1.0)
    assert time_dist.random_variate() in (1, 2, )


def test_dist_fixed_add_another():
    time_dist = Dist('fixed', 1, weight=1.0) \
        + Dist('fixed', 2, weight=1.0) \
        + Dist('fixed', 3, weight=1.0)
    assert time_dist.random_variate() in (1, 2, 3, )


def test_dist_fixed_add_with_weight():
    random.seed(0)
    time_dist = Dist('fixed', 1, weight=0.1) \
        + Dist('fixed', 2, weight=0.9)
    counter = Counter([time_dist.random_variate() for i in range(1_000)])
    assert counter[1] == 114
    assert counter[2] == 886


def test_dist_fixed_add_another_with_weight():
    random.seed(0)
    time_dist = Dist('fixed', 1, weight=0.1) \
        + Dist('fixed', 2, weight=0.2) \
        + Dist('fixed', 3, weight=0.7)
    counter = Counter([time_dist.random_variate() for i in range(1_000)])
    assert counter[1] == 114
    assert counter[2] == 182
    assert counter[3] == 704
