from __future__ import annotations

from datetime import timedelta
from typing import List, Optional

from just.simulate.agent import Courier, Customer, Restaurant
from just.simulate.component.assigner.base_assigner import BaseAssigner
from just.simulate.env import Env
from just.simulate.maps import Maps
from just.simulate.metric import BaseMetric
from just.simulate.reporting import Reporting
from just.simulate.session import Session


class Simulation:
    """Simulation."""

    def __init__(
        self,
        restaurants: List[Restaurant],
        customers: List[Customer],
        sessions: List[Session],
        couriers: List[Courier],
        assigner: BaseAssigner,
        metrics: List[BaseMetric],
        maps: Optional[Maps] = None,
    ) -> None:

        self.env = Env(maps)
        self.env.register(assigner)
        self.reporting = Reporting(metrics)
        self.reporting.create_connection(
            self.env.addon.data_lake)

        for restaurant in restaurants:
            self.env.register(restaurant)

        for customer in customers:
            self.env.register(customer)

        for session in sessions:
            self.env.publish(
                'customer_session_started', data={
                    'customer_id': session.customer_id,
                    'restaurant_id': session.restaurant_id,
                }, delay=session.timestamp)

        for courier in couriers:
            self.env.register(courier)

    def run(
            self, verbose: int = 0,
            until: Optional[timedelta] = None
    ) -> dict:
        """Run."""
        self.env.publish('simulation_started')
        # get event with earliest time
        for topic, data in self.env.run(until):
            if verbose > 0 and topic is not None and data is not None:
                print(f"{self.env.now} {topic or '':<16} {data or ''}")
        return self.reporting.get_results()
