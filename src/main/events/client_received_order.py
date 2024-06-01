from src.main.events.event import Event
from src.main.events.event_type import EventType


class ClientReceivedOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, driver_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        self.driver_id = driver_id
        self.event_type = EventType.CLIENT_RECEIVED_ORDER

    def __str__(self):
        return (f"Client {self.client_id} picked up the "
                f"order {self.order_id} with "
                f"driver {self.driver_id} from "
                f"restaurant {self.restaurant_id} in "
                f"time {self.time}")
