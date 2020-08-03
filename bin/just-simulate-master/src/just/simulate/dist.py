from __future__ import annotations

import copy
import random

from scipy import stats


class Dist:
    """Dist."""

    class _Dist:
        """_Dist."""

        def __init__(
                self, name: str,
                *args,
                **kwargs
        ) -> None:
            self.name = name
            self.dist = stats.uniform(args[0], 0) \
                if name in ('fixed', 'static', ) \
                else getattr(stats, name)(*args, **kwargs)

        def random_variate(self) -> float:
            """Random variate."""
            return self.dist.rvs()

        def __getattr__(self, name):
            """Get attr."""
            def func(*args, **kwargs):
                return getattr(self.dist, name)(*args, **kwargs)
            return func

    def __init__(
            self, name: str,
            *args,
            weight: float = 1.0,
            **kwargs
    ) -> None:
        self._time_dists = list([Dist._Dist(
            name, *args, **kwargs)])
        self._weights = list([weight])

    def random_variate(self) -> float:
        """Random variate."""
        _time_dist = random.choices(
            self._time_dists, weights=self._weights, k=1)[0]
        return _time_dist.random_variate()

    def __add__(self, other: Dist) -> Dist:
        """Add."""
        this = copy.copy(self)
        this._time_dists = this._time_dists + other._time_dists
        this._weights = this._weights + other._weights
        return this
