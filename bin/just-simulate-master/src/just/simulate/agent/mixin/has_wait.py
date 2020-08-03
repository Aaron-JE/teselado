from __future__ import annotations

from datetime import timedelta
from typing import Optional

from just.simulate.time_dist import TimeDist


class HasWait:
    """Has wait."""

    def __init__(
            self, wait: Optional[TimeDist] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.wait = wait or TimeDist('fixed', 0)

    def wait_time(self) -> timedelta:
        """Wait time."""
        return self.wait.random_variate()
