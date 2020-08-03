from __future__ import annotations

from datetime import timedelta

from just.simulate.dist import Dist


class TimeDist(Dist):
    """Time dist."""

    def __init__(
            self, name: str,
            *args,
            unit: str = 'minutes',
            weight: float = 1.0,
            **kwargs
    ) -> None:
        super().__init__(name, *args, weight=weight, **kwargs)
        self.unit = unit

    def __add__(self, other: TimeDist) -> TimeDist:
        """Add."""
        assert self.unit == other.unit, \
            "Units are not commensurate"
        return super().__add__(other)

    def random_variate(self) -> timedelta:
        """Random variate."""
        value = max(0.0, super().random_variate())
        return timedelta(**{self.unit: value})

    def most_likely_estimate(self) -> timedelta:
        """Most likely estimate."""
        values = list()
        sum_weights = sum(self._weights)
        for weight, dist in zip(self._weights, self._time_dists):
            _mean = dist.dist.mean() \
                if dist.name not in ('fixed', 'static', ) \
                else dist.random_variate()
            values.append(weight * _mean / sum_weights)

        return timedelta(**{self.unit: sum(values)})
