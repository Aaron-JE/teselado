import copy
from collections import defaultdict

import pandas as pd

from just.simulate.registrable import Registrable


class DataLake(Registrable):
    """Date lake."""

    def __init__(self):
        super().__init__()
        self.storage = defaultdict(list)

    def handler(self, data: dict, topic: str, **kwargs) -> None:
        """Handler."""
        _data = copy.deepcopy(data)
        _data['timestamp'] = self.env.now
        self.storage[topic].append(_data)

    def get_table(self, topic: str) -> pd.DataFrame:
        """Get table."""
        if topic not in self.storage:
            raise KeyError(f'"{topic}" not found')
        data = self.storage[topic]
        return pd.DataFrame(data)
