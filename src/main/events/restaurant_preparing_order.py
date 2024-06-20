from src.main.events.event_type import EventType
from src.main.events.order_event import OrderEvent


class RestaurantPreparingOrder(OrderEvent):
    def __init__(self, order_id, customer_id, restaurant_id, time):
        super().__init__(order_id, customer_id, restaurant_id, time, EventType.RESTAURANT_PREPARING_ORDER)

    def __str__(self):
        return (f"Restaurant {self.restaurant_id} is preparing the "
                f"order {self.order_id} from "
                f"customer {self.customer_id} in "
                f"time {self.time}")
