from typing import List, Tuple, Union

import numpy as np


def distance(
        from_lat: List[float],
        from_lng: List[float],
        to_lat: List[float],
        to_lng: List[float]
) -> np.array:
    from_lat, from_lng, to_lat, to_lng = map(
        np.deg2rad, [from_lat, from_lng, to_lat, to_lng])
    x = (to_lng - from_lng) * np.cos((to_lat + from_lat) / 2.)
    y = to_lat - from_lat
    return 6371008.8 * np.sqrt(x * x + y * y)


def travel_time(
        from_lat: List[float],
        from_lng: List[float],
        to_lat: List[float],
        to_lng: List[float],
        average_speed: float
) -> np.array:
    return distance(
        from_lat,
        from_lng,
        to_lat,
        to_lng
    ) / average_speed


def random_lat_lng(
        center_lat,
        center_lng,
        radius,
        size=None
) -> Union[
        Tuple[float, float],
        List[Tuple[float, float]]
]:
    r = radius / 111_300
    u, v = np.random.uniform(size=(2, None or 1))
    w = r * np.sqrt(u)
    t = 2 * np.pi * v
    x = w * np.cos(t) / np.cos(np.deg2rad(center_lat))
    y = w * np.sin(t)
    lat = center_lat + y
    lng = center_lng + x
    if size is None:
        return lat[0], lng[0]
    return [(lat, lng) for lat, lng in zip(lat, lng)]
