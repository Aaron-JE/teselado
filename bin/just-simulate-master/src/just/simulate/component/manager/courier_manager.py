from just.simulate.component.manager.base_manager import BaseManager


class CourierManager(BaseManager):
    """Courier manager."""

    def get_all_available(self):
        """Get all available."""
        return [
            courier
            for courier in self.get_all()
            if courier.available()
        ]
