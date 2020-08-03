from __future__ import annotations

from typing import Optional

from just.simulate.dist import Dist


class HasRejection:
    """Has rejection."""

    env: 'Env'

    def __init__(
            self, rate: Optional[float] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.rate = rate or 0.0
        self.__dist = Dist('uniform', 0, 1)

    def rejected(self) -> bool:
        """Rejected."""
        if self.rate == 0.0:
            return False
        elif self.rate == 1.0:
            return True
        else:
            p = self.__dist.random_variate()
            return p < self.rate

    def accepted(self) -> bool:
        """Accepted."""
        return not self.rejected()
