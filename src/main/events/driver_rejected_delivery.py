from src.main.events.event_type import EventType
from src.main.events.order_event import OrderEvent


class DriverRejectedDelivery(OrderEvent):
    def __init__(self, order_id, customer_id, restaurant_id, driver_id, time):
        super().__init__(order_id, customer_id, restaurant_id, time, EventType.DRIVER_REJECTED_DELIVERY)
        self.driver_id = driver_id

    def __str__(self):
        return (f"Driver {self.driver_id} reject to deliver "
                f"order {self.order_id} from "
                f"restaurant {self.restaurant_id} and from "
                f"customer {self.customer_id} in "
                f"time {self.time}")
