from datetime import datetime

from src.order.item import Item


class Order:
    def __init__(
            self,
            order_id: str,
            client,
            restaurant,
            request_date: datetime,
            items: [Item]
    ):
        self.order_id = order_id
        self.client = client
        self.restaurant = restaurant
        self.request_date = request_date
        self.items = items
