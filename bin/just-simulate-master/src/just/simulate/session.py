from datetime import timedelta


class Session:
    """Session."""

    def __init__(
            self,
            customer_id: str,
            restaurant_id: str,
            timestamp: timedelta
    ) -> None:
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.timestamp = timestamp
