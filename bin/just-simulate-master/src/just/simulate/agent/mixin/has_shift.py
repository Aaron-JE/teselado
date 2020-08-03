from __future__ import annotations

from datetime import timedelta
from typing import Optional


class HasShift:
    """Has shift."""

    env: 'Env'
    id: int
    _start_time: timedelta
    _end_time: timedelta

    def __init__(
            self,
            start_time: Optional[timedelta] = None,
            end_time: Optional[timedelta] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._set_shift(start_time, end_time)

    @property
    def start_time(self):
        """Start time."""
        return self._start_time

    @property
    def end_time(self):
        """End time."""
        return self._end_time

    def _set_shift(self, start_time: timedelta, end_time: timedelta) -> None:
        """Set shift."""
        assert start_time is None \
            or end_time is None \
            or start_time <= end_time
        self._start_time = start_time
        self._end_time = end_time

    def set_shift(self, start_time: timedelta, end_time: timedelta) -> None:
        """Set shift."""
        self._set_shift(start_time, end_time)
        name = self.__class__.__name__.lower()
        self.env.publish(f'{name}_shift_updated', data={
            f'{name}_id': self.id,
            'start_time': start_time,
            'end_time': end_time
        })

    def available(self):
        """Available."""
        return (self.start_time is None and self.end_time is None) \
            or (self.start_time is None and self.env.now < self.end_time) \
            or (self.start_time <= self.env.now and self.end_time is None) \
            or (self.start_time <= self.env.now < self.end_time)
