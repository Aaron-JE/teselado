from datetime import timedelta
from typing import Optional

import numpy as np

from just.simulate.time_dist import TimeDist


class Maps:
    """Maps."""

    def __init__(
            self, average_speed: float = 10.0,
            noise: Optional[TimeDist] = None
    ) -> None:
        self.average_speed = average_speed  # average speed m/s
        self.noise = noise or TimeDist('fixed', 0.0)  # default

    @staticmethod
    def distance(
            from_lat: float, from_lng: float,
            to_lat: float, to_lng: float
    ) -> float:
        """Distance in meters."""
        from_lat, from_lng, to_lat, to_lng = map(
            np.deg2rad, [from_lat, from_lng, to_lat, to_lng])
        x = (to_lng - from_lng) * np.cos((to_lat + from_lat) / 2.)
        y = to_lat - from_lat
        earth_radius = 6371008.8
        return earth_radius * np.sqrt(x * x + y * y)  # m

    def travel_time(
            self, from_lat: float, from_lng: float,
            to_lat: float, to_lng: float
    ) -> timedelta:
        """Travel time in m/s."""
        distance = Maps.distance(
            from_lat, from_lng, to_lat, to_lng)
        return timedelta(seconds=int(distance / self.average_speed))

    def estimated_travel_time(
            self, from_lat: float, from_lng: float,
            to_lat: float, to_lng: float
    ) -> timedelta:
        """Estimated travel time in m/s."""
        travel_time = self.travel_time(from_lat, from_lng, to_lat, to_lng)
        return travel_time + self.noise.random_variate()
