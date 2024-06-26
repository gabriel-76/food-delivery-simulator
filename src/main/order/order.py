import uuid
from typing import List

from src.main.base.dimensions import Dimensions
from src.main.order.delivery_rejection import DeliveryRejection
from src.main.order.item import Item
from src.main.order.order_status import OrderStatus


class Order:
    def __init__(
            self,
            customer,
            establishment,
            request_date: int,
            items: List[Item]
    ):
        self.order_id = uuid.uuid4()
        self.customer = customer
        self.establishment = establishment
        self.request_date = request_date
        self.items = items
        self.status: OrderStatus = OrderStatus.CREATED
        self.estimated_time_to_ready = 0
        self.time_it_was_ready = 0
        self.required_capacity = self.calculate_required_capacity()
        self.delivery_rejections: List[DeliveryRejection] = []

    def calculate_required_capacity(self):
        dimensions = Dimensions(0, 0, 0, 0)
        for item in self.items:
            dimensions += item.dimensions
        return dimensions

    def update_status(self, status: OrderStatus):
        self.status = status

    def establishment_accepted(self, estimated_time_to_ready: int):
        self.status = OrderStatus.ESTABLISHMENT_ACCEPTED
        self.estimated_time_to_ready = estimated_time_to_ready

    def add_delivery_rejection(self, delivery_rejection: DeliveryRejection):
        self.delivery_rejections.append(delivery_rejection)
