from __future__ import annotations

from datetime import timedelta
from enum import Enum

from just.simulate.agent.customer import Customer
from just.simulate.agent.restaurant import Restaurant


class Order:
    """Order."""

    class State(Enum):
        """State."""

        PENDING = 0
        ASSIGNED = 1
        READY = 2
        DELIVERED = 3

    def __init__(
        self,
        timestamp: timedelta,
        restaurant: Restaurant,
        customer: Customer
    ) -> None:
        self.id = id(self)
        self.timestamp = timestamp
        self.restaurant = restaurant
        self.customer = customer
        self.state = Order.State.PENDING

    def set_state(self, state: Order.State):
        """Set state."""
        if self.state.value != state.value - 1:
            msg = f'{self.state.name} => {state.name}'
            raise ValueError(f"Forbidden transition '{msg}'")
        self.state = state
