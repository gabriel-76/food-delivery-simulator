from src.main.events.order_event import OrderEvent
from src.main.events.event_type import EventType


class DriverRejectedDelivery(OrderEvent):
    def __init__(self, order_id, client_id, restaurant_id, driver_id, time):
        super().__init__(order_id, client_id, restaurant_id, time, EventType.DRIVER_REJECTED_DELIVERY)
        self.driver_id = driver_id

    def __str__(self):
        return (f"Driver {self.driver_id} reject to deliver "
                f"order {self.order_id} from "
                f"restaurant {self.restaurant_id} and from "
                f"client {self.client_id} in "
                f"time {self.time}")
