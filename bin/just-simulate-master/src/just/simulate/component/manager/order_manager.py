from just.simulate.component.manager.base_manager import BaseManager
from just.simulate.order import Order


class OrderManager(BaseManager):
    """Order manager."""

    def __init__(self) -> None:
        super().__init__()

    def get_all_pending(self):
        """Get all pending."""
        return [
            order for order in self.get_all()
            if order.state == Order.State.PENDING]

    def order_placed_handler(self, data: dict, **kwargs) -> None:
        """Order placed => Order created."""
        manager = self.env.manager.restaurant
        restaurant = manager.get(data['restaurant_id'])
        manager = self.env.manager.customer
        customer = manager.get(data['customer_id'])
        order = Order(self.env.now, restaurant, customer)
        self.add(order)  # add order
        self.env.publish('order_created', data={
            'order_id': order.id,
            'restaurant_id': order.restaurant.id,
            'customer_id': order.customer.id
        })

    def courier_order_accepted_handler(self, data: dict, **kwargs) -> None:
        """Courier order accepted => None."""
        order = self.get(data['order_id'])
        order.set_state(order.State.ASSIGNED)

    def restaurant_order_ready_handler(self, data: dict, **kwargs) -> None:
        """Restaurant order ready => None."""
        order = self.get(data['order_id'])
        order.set_state(order.State.READY)

    def order_delivered_handler(self, data: dict, **kwargs) -> None:
        """Order delivered => None."""
        order = self.get(data['order_id'])
        order.set_state(order.State.DELIVERED)
