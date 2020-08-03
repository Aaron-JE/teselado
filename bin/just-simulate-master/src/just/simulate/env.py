from __future__ import annotations

from datetime import timedelta
from typing import Callable, Generator, Optional, Tuple

from just.simulate.agent import Courier, Customer, Restaurant
from just.simulate.bus import Bus
from just.simulate.component.addon import DataLake
from just.simulate.component.manager import CourierManager, CustomerManager, \
    OrderManager, RestaurantManager
from just.simulate.maps import Maps


class Env:
    """Env."""

    class Manager:
        """Manager."""

        def __init__(self, env: Env):
            self.restaurant = RestaurantManager()
            env.register(self.restaurant)
            self.customer = CustomerManager()
            env.register(self.customer)
            self.courier = CourierManager()
            env.register(self.courier)
            self.order = OrderManager()
            env.register(self.order)

    class Addon:
        """Addon."""

        maps: Maps

        def __init__(self, env: Env):
            self.data_lake = DataLake()
            env.register(self.data_lake)
            self.data_lake.env.add_subscription(
                '*', self.data_lake.handler)

    def __init__(self, maps: Optional[Maps] = None):
        self.bus = Bus()
        # globally registered
        self.manager = Env.Manager(self)
        self.addon = Env.Addon(self)
        self.addon.maps = maps or Maps()

    @property
    def now(self):
        """Now."""
        return self.bus.now

    def publish(
            self, topic: str,
            data: Optional[dict] = None,
            delay: timedelta = None
    ) -> None:
        """Publish."""
        self.bus.publish(topic, data, delay)

    def add_subscription(
            self, topic: str,
            handler: Callable,
            filtering: Optional[Callable] = None
    ) -> None:
        """Add subscription."""
        self.bus.add_subscription(topic, handler, filtering)

    def run(self, until: Optional[timedelta] = None) \
            -> Generator[Tuple[str, dict], None, None]:
        """Run."""
        return self.bus.run(until)

    def register(self, registrable: 'Registrable') -> None:
        """Register."""
        registrable.env = self
        registrable.auto_subscribe()
        registrable.subscribe()

        if isinstance(registrable, Restaurant):
            self.manager.restaurant.add(registrable)
        elif isinstance(registrable, Customer):
            self.manager.customer.add(registrable)
        elif isinstance(registrable, Courier):
            self.manager.courier.add(registrable)
