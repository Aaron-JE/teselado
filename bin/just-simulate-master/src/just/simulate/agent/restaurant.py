from datetime import timedelta
from typing import Generator, Optional

from just.simulate.agent.base_agent import BaseAgent
from just.simulate.agent.mixin.has_coords import HasCoords
from just.simulate.agent.mixin.has_shift import HasShift
from just.simulate.agent.mixin.has_wait import HasWait
from just.simulate.time_dist import TimeDist


class Restaurant(
        HasCoords,
        HasShift,
        HasWait,
        BaseAgent
):
    """Restaurant."""

    def __init__(
            self, id: str,
            lat: float,
            lng: float,
            start_time: Optional[timedelta] = None,
            end_time: Optional[timedelta] = None,
            wait: Optional[TimeDist] = None
    ) -> None:
        super().__init__(
            id=id,
            lat=lat,
            lng=lng,
            start_time=start_time,
            end_time=end_time,
            wait=wait)

    def courier_at_restaurant_handler(self, data: dict, **kwargs) \
            -> Generator[timedelta, None, None]:
        """Courier at restaurant => Restaurant order ready."""
        yield self.wait_time()
        self.env.publish('restaurant_order_ready', data={
            'order_id': data['order_id'],
            'restaurant_id': data['restaurant_id'],
            'customer_id': data['customer_id'],
            'courier_id': data['courier_id']})
