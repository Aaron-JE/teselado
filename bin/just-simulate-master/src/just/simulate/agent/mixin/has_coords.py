from __future__ import annotations


class HasCoords:
    """Has coords."""

    env: 'Env'
    id: int
    _lat: float
    _lng: float

    def __init__(self, lat: float, lng: float, **kwargs) -> None:
        super().__init__(**kwargs)
        self._set_coords(lat, lng)

    @property
    def lat(self):
        """Latitude."""
        return self._lat

    @property
    def lng(self):
        """Longitude."""
        return self._lng

    def _set_coords(self, lat: float, lng: float) -> None:
        """Set coords."""
        msg = "Latitude ranges between -90 and 90 degrees"
        assert -90.0 <= lat <= 90.0, msg
        msg = "Longitude ranges between -180 and 180 degrees"
        assert -180.0 <= lng <= 180.0, msg
        self._lat = lat
        self._lng = lng

    def set_coords(self, lat: float, lng: float) -> None:
        """Set coords."""
        self._set_coords(lat, lng)
        name = self.__class__.__name__.lower()
        self.env.publish(f'{name}_coords_updated', data={
            f'{name}_id': self.id,
            'lat': lat,
            'lng': lng
        })
