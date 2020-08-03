import random
from datetime import timedelta

from just.simulate.component.assigner.base_assigner import BaseAssigner


class RandomAssigner(BaseAssigner):
    """Random assigner."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def _handler(self, data: dict, **kwargs) -> None:
        """Order created => Courier order [accepted|rejected]."""
        while True:  # TODO if not couriers
            couriers = self.env.manager.courier.get_all_available()
            if couriers: break
            yield timedelta(minutes=5)

        courier = random.choice(couriers)
        self.env.publish('courier_assigned', data={
            'order_id': data['order_id'],
            'restaurant_id': data['restaurant_id'],
            'customer_id': data['customer_id'],
            'courier_id': courier.id})

    def order_created_handler(self, data: dict, **kwargs) -> None:
        """Order created => Courier order [accepted|rejected]."""
        return self._handler(data, **kwargs)

    def courier_order_rejected_handler(self, data: dict, **kwargs) -> None:
        """Order created => Courier order [accepted|rejected]."""
        return self._handler(data, **kwargs)
