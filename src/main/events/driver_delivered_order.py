from src.main.events.event import Event
from src.main.events.event_type import EventType


class DriverDeliveredOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, driver_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        self.driver_id = driver_id
        self.event_type = EventType.DRIVER_DELIVERED_ORDER

    def __str__(self):
        return (f"Driver {self.driver_id} delivered "
                f"order {self.order_id} from "
                f"restaurant {self.restaurant_id} to "
                f"client {self.client_id} in "
                f"time {self.time}")
