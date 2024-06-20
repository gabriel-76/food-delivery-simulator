from src.main.events.event_type import EventType
from src.main.events.order_event import OrderEvent


class CustomerPlacedOrder(OrderEvent):
    def __init__(self, order_id, customer_id, restaurant_id, time):
        super().__init__(order_id, customer_id, restaurant_id, time, EventType.CUSTOMER_PLACED_ORDER)

    def __str__(self):
        return (f"Customer {self.customer_id} placed an "
                f"order {self.order_id} to "
                f"restaurant {self.restaurant_id} in "
                f"time {self.time}")
