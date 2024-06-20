from src.main.events.order_event import OrderEvent
from src.main.events.event_type import EventType


class CustomerReceivedOrder(OrderEvent):
    def __init__(self, order_id, customer_id, restaurant_id, driver_id, time):
        super().__init__(order_id, customer_id, restaurant_id, time, EventType.CUSTOMER_RECEIVED_ORDER)
        self.driver_id = driver_id

    def __str__(self):
        return (f"Customer {self.customer_id} picked up the "
                f"order {self.order_id} with "
                f"driver {self.driver_id} from "
                f"restaurant {self.restaurant_id} in "
                f"time {self.time}")
