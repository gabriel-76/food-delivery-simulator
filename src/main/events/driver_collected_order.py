from src.main.events.event import Event


class DriverCollectedOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, driver_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        self.driver_id = driver_id
        print(self)

    def __str__(self):
        return (f"Driver {self.driver_id} collected "
                f"order {self.order_id} from "
                f"restaurant {self.restaurant_id} and "
                f"client {self.client_id} in "
                f"time {self.time}")
