from __future__ import annotations

from typing import Optional

from just.simulate.agent.base_agent import BaseAgent
from just.simulate.agent.mixin.has_coords import HasCoords
from just.simulate.agent.mixin.has_wait import HasWait
from just.simulate.time_dist import TimeDist


class Customer(
        HasCoords,
        HasWait,
        BaseAgent
):
    """Customer."""

    def __init__(
            self,
            id: str,
            lat: float,
            lng: float,
            wait: Optional[TimeDist] = None
    ) -> None:
        super().__init__(
            id=id,
            lat=lat,
            lng=lng,
            wait=wait)

    def customer_session_started_handler(self, data: dict, **kwargs) -> None:
        """Customer session started. => Order placed."""
        restaurant = self.env.manager.restaurant.get(data['restaurant_id'])
        if restaurant.available():
            self.env.publish('order_placed', data={
                'customer_id': self.id,
                'restaurant_id': data['restaurant_id']})

    def courier_at_customer_handler(self, data: dict, **kwargs) -> None:
        """Courier at customer => Customer order collected."""
        yield self.wait_time()
        self.env.publish('customer_order_collected', data={
            'order_id': data['order_id'],
            'restaurant_id': data['restaurant_id'],
            'customer_id': data['customer_id'],
            'courier_id': data['courier_id']})
