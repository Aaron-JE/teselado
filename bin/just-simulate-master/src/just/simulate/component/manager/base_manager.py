from abc import ABC

from just.simulate.registrable import Registrable


class BaseManager(Registrable, ABC):
    """Base manager."""

    def __init__(self, items=None):
        super().__init__()
        self.items = dict({})
        if items is not None:
            for item in items:
                self.add(item)

    def add(self, item):
        """Add."""
        msg = f"Duplicate key '{item.id}'"
        assert item.id not in self.items, msg
        self.items[item.id] = item

    def get(self, id):
        """Get."""
        return self.items[id]

    def get_all(self):
        """Get all."""
        return list(self.items.values())
