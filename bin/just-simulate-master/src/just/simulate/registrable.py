from __future__ import annotations

import inspect
import re
from typing import Callable, List, Optional


class Registrable:
    """Registrable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.env: Optional['Env'] = None
        self._subscriptions = None

    @property
    def subscriptions(self) -> List[str]:
        """Subscriptions."""
        return self._subscriptions

    def filtering(self, data: dict) -> bool:
        """Filtering."""
        return True

    def add_subscription(
            self, topic: str,
            handler: Callable
    ) -> None:
        """Add subscription."""
        filtering = self.filtering
        self.env.add_subscription(
            topic, handler, filtering)
        if self._subscriptions is None:
            self._subscriptions = list()
        subscription = (topic, handler, filtering)
        self._subscriptions.append(subscription)

    def auto_subscribe(self):
        """Auto subscribe."""
        methods = inspect.getmembers(
            self, predicate=inspect.ismethod)
        for name, method in methods:
            if re.match(r'[a-zA-Z0-9_]+_handler$', name):
                topic = name.replace('_handler', '')
                self.add_subscription(topic, method)

    def subscribe(self):
        """Subscribe."""
        pass
