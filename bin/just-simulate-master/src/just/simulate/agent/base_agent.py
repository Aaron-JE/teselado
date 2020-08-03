import abc

from just.simulate.registrable import Registrable


class BaseAgent(Registrable, abc.ABC):
    """Base agent."""

    def __init__(self, id: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = id

    def filtering(self, data: dict) -> bool:
        """Filtering."""
        key = f'{self.__class__.__name__.lower()}_id'
        "key = r'[courier|customer|restaurant]_id'"
        return data[key] == self.id if key in data else True
