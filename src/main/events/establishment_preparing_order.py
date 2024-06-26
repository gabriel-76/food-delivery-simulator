from src.main.events.event_type import EventType
from src.main.events.order_event import OrderEvent


class EstablishmentPreparingOrder(OrderEvent):
    def __init__(self, order_id, customer_id, establishment_id, time):
        super().__init__(order_id, customer_id, establishment_id, time, EventType.ESTABLISHMENT_PREPARING_ORDER)

    def __str__(self):
        return (f"Establishment {self.establishment_id} is preparing the "
                f"order {self.order_id} from "
                f"customer {self.customer_id} in "
                f"time {self.time}")
