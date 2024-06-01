from src.main.events.event import Event
from src.main.events.event_type import EventType


class RestaurantFinishedOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        self.event_type = EventType.RESTAURANT_FINISHED_ORDER

    def __str__(self):
        return (f"Restaurant {self.restaurant_id} has finished preparing the "
                f"order {self.order_id} from "
                f"client {self.client_id} in "
                f"time {self.time}")
