from src.main.events.order_event import OrderEvent
from src.main.events.event_type import EventType


class RestaurantRejectedOrder(OrderEvent):
    def __init__(self, order_id, client_id, restaurant_id, time):
        super().__init__(order_id, client_id, restaurant_id, time, EventType.RESTAURANT_REJECTED_ORDER)

    def __str__(self):
        return (f"Restaurant {self.restaurant_id} rejected "
                f"order {self.order_id} from "
                f"client {self.client_id} in "
                f"time {self.time}")
