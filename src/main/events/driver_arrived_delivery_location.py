from src.main.events.order_event import OrderEvent
from src.main.events.event_type import EventType


class DriverArrivedDeliveryLocation(OrderEvent):
    def __init__(self, order_id, customer_id, restaurant_id, driver_id, time):
        super().__init__(order_id, customer_id, restaurant_id, time, EventType.DRIVER_ARRIVED_DELIVERY_LOCATION)
        self.driver_id = driver_id

    def __str__(self):
        return (f"Driver {self.driver_id} has arrived at the delivery location for "
                f"order {self.order_id} from "
                f"restaurant {self.restaurant_id} and is waiting for "
                f"customer {self.customer_id} in "
                f"time {self.time}")
