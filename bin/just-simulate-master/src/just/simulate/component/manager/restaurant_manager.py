from just.simulate.component.manager.base_manager import BaseManager


class RestaurantManager(BaseManager):
    """Restaurant manager."""

    def get_all_available(self):
        """Get all available."""
        return [
            restaurant
            for restaurant in self.get_all()
            if restaurant.available()
        ]
