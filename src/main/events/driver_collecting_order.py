from src.main.events.event import Event
from src.main.events.event_type import EventType


class DriverCollectingOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, driver_id, distance, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        self.driver_id = driver_id
        self.distance = distance
        self.event_type = EventType.DRIVER_COLLECTING_ORDER

    def __str__(self):
        return (f"Driver {self.driver_id} is collecting "
                f"order {self.order_id} from "
                f"restaurant {self.restaurant_id} and "
                f"client {self.client_id} at a "
                f"distance {self.distance} in "
                f"time {self.time}")
