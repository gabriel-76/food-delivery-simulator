import uuid
from datetime import datetime

from src.main.base.dimensions import Dimensions
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
        self.required_capacity = self.calculate_required_capacity()

    def calculate_required_capacity(self):
        dimensions = Dimensions(0, 0, 0, 0)
        for item in self.items:
            dimensions += item.dimensions
        return dimensions
