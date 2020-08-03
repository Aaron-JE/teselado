from typing import List, Type

from just.simulate.metric import BaseMetric


class Reporting:
    """Reporting."""

    def __init__(self, metrics: List[BaseMetric]) -> None:
        super().__init__()
        self.data_lake = None
        self.metrics = metrics

    def create_connection(self, data_lake) -> None:
        """Create connection."""
        self.data_lake = data_lake

    def get_results(self) -> dict:
        """Get results."""
        return {
            metric.name:
            metric.calculate(self.data_lake)
            for metric in self.metrics
        }
