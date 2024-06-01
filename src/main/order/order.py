import uuid
from datetime import datetime

from src.main.order.item import Item


class Order:
    def __init__(
            self,
            client,
            restaurant,
            request_date: datetime,
            items: [Item]
    ):
        self.order_id = uuid.uuid4()
        self.client = client
        self.restaurant = restaurant
        self.request_date = request_date
        self.items = items
