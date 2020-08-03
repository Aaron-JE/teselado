from __future__ import annotations

from datetime import timedelta
from typing import List, Optional

from just.simulate.agent.base_agent import BaseAgent
from just.simulate.agent.mixin.has_coords import HasCoords
from just.simulate.agent.mixin.has_rejection import HasRejection
from just.simulate.agent.mixin.has_shift import HasShift


class Courier(
    HasCoords,
    HasShift,
    HasRejection,
    BaseAgent
):

    def __init__(
            self,
            id: str,
            lat: float,
            lng: float,
            start_time: Optional[timedelta] = None,
            end_time: Optional[timedelta] = None,
            rejection_rate: Optional[float] = None
    ) -> None:
        super().__init__(
            id=id,
            lat=lat,
            lng=lng,
            start_time=start_time,
            end_time=end_time,
            rate=rejection_rate)
        self._active: Optional['Order'] = None
        self._backlog: List['Order'] = list([])

    def courier_assigned_handler(self, data: dict, **kwargs) -> None:
        """Courier assigned => Courier [accepted|rejected]."""
        choice = 'rejected' if self.rejected() else 'accepted'
        self.env.publish(f'courier_order_{choice}', data={
            'order_id': data['order_id'],
            'restaurant_id': data['restaurant_id'],
            'customer_id': data['customer_id'],
            'courier_id': data['courier_id']})

    def courier_order_accepted_handler(self, data: dict, **kwargs) -> None:
        """Courier order accepted => Courier job started."""
        order = self.env.manager.order.get(data['order_id'])
        if self._active is not None:
            self._backlog.append(order)
            return  # queue order

        assert not self._backlog
        self._active = order
        self.env.publish('courier_job_started', data={
            'order_id': data['order_id'],
            'restaurant_id': data['restaurant_id'],
            'customer_id': data['customer_id'],
            'courier_id': data['courier_id']})

    def courier_job_started_handler(self, data: dict, **kwargs) -> None:
        """Courier job started => Courier at restaurant."""
        yield self._travel_time(
            self._active.restaurant.lat,
            self._active.restaurant.lng)
        # courier at restaurant
        self.set_coords(
            self._active.restaurant.lat,
            self._active.restaurant.lng)
        self.env.publish('courier_at_restaurant', data={
            'order_id': data['order_id'],
            'restaurant_id': data['restaurant_id'],
            'customer_id': data['customer_id'],
            'courier_id': data['courier_id']})

    def restaurant_order_ready_handler(self, data: dict, **kwargs) -> None:
        """Restaurant order ready => Courier at customer."""
        yield self._travel_time(
            self._active.customer.lat,
            self._active.customer.lng)
        # courier at customer
        self.set_coords(
            self._active.customer.lat,
            self._active.customer.lng)
        self.env.publish('courier_at_customer', data={
            'order_id': data['order_id'],
            'restaurant_id': data['restaurant_id'],
            'customer_id': data['customer_id'],
            'courier_id': data['courier_id']})

    def customer_order_collected_handler(self, data: dict, **kwargs) -> None:
        """Customer order collected => Order delivered."""
        self.env.publish('order_delivered', data={
            'order_id': data['order_id'],
            'restaurant_id': data['restaurant_id'],
            'customer_id': data['customer_id'],
            'courier_id': data['courier_id']})

        # queue
        self._active = None
        if self._backlog:
            self._active = self._backlog.pop(0)
            self.env.publish('courier_job_started', data={
                'order_id': self._active.id,
                'restaurant_id': self._active.restaurant.id,
                'customer_id': self._active.customer.id,
                'courier_id': self.id})

    def _travel_time(self, lat: float, lng: float) -> timedelta:
        """Travel ... => Courier location."""
        maps = self.env.addon.maps
        time = maps.travel_time(self.lat, self.lng, lat, lng)
        return max(timedelta(seconds=1), time)  # padded
