from datetime import timedelta

from ortools.linear_solver import pywraplp

from just.simulate.agent import Courier
from just.simulate.component.assigner.base_assigner import BaseAssigner
from just.simulate.order import Order


class MipAssigner(BaseAssigner):
    """MIP assigner."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._track_and_trace = dict()

    def _available_from(self, courier: Courier, order: Order) -> timedelta:
        """Available from."""
        if courier.id not in self._track_and_trace:
            lat = courier.lat
            lng = courier.lng
            timestamp = self.env.now
        else:
            lat = self._track_and_trace[courier.id]['lat']
            lng = self._track_and_trace[courier.id]['lng']
            timestamp = self._track_and_trace[courier.id]['timestamp']

        added = (
            self.env.addon.maps.estimated_travel_time(
                lat, lng, order.restaurant.lat, order.restaurant.lng)
            + self.env.manager.restaurant.get(
                order.restaurant.id).wait.most_likely_estimate()
            + self.env.addon.maps.estimated_travel_time(
                order.restaurant.lat, order.restaurant.lng,
                order.customer.lat, order.customer.lng))

        return timestamp + added

    def linear_sum_assignment(self):
        """Linear sum assignment."""

        orders = self.env.manager.order.get_all_pending()
        couriers = self.env.manager.courier.get_all_available()

        if not orders or not couriers:
            return

        cost = [[int(self._available_from(courier, order).total_seconds())
                 for order in orders] for courier in couriers]

        solver = pywraplp.Solver(
            'SolveAssignmentProblemMIP',
            pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

        num_couriers = len(cost)
        num_orders = len(cost[0])

        x = {}
        for i in range(num_couriers):
            for j in range(num_orders):
                x[i, j] = solver.BoolVar('x[%i,%i]' % (i, j))

        # Objective
        solver.Minimize(solver.Sum([
            cost[i][j] * x[i, j]
            for i in range(num_couriers)
            for j in range(num_orders)]))

        # Constraints
        for i in range(num_couriers):
            solver.Add(solver.Sum([x[i, j] for j in range(num_orders)]) <= 1)
        for j in range(num_orders):
            solver.Add(solver.Sum([x[i, j] for i in range(num_couriers)]) <= 1)
        solver.Add(solver.Sum([x[i, j] for i in range(num_couriers)
            for j in range(num_orders)]) == min(num_couriers, num_orders))

        sol = solver.Solve()

        for i in range(num_couriers):
            for j in range(num_orders):
                if x[i, j].solution_value() > 0:
                    this_order = orders[j]
                    self.env.publish('courier_assigned', data={
                        'order_id': this_order.id,
                        'restaurant_id': this_order.restaurant.id,
                        'customer_id': this_order.customer.id,
                        'courier_id': couriers[i].id})

    def simulation_started_handler(
            self, __: dict, **kwargs) -> None:
        """Simulation started => None."""
        while True:
            self.linear_sum_assignment()
            yield timedelta(minutes=5)

    def courier_order_accepted_handler(
            self, data: dict, **kwargs) -> None:
        """Courier order accepted => None."""

        order = self.env.manager.order.get(data['order_id'])
        courier = self.env.manager.courier.get(data['courier_id'])
        new_timestamp = self._available_from(courier, order)
        self._track_and_trace[courier.id] = {
            'lat': order.customer.lat,
            'lng': order.customer.lng,
            'timestamp': new_timestamp}
