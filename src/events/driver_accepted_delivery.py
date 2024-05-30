from src.events.event import Event


class DriverAcceptedDelivery(Event):
    def __init__(self, order_id, client_id, restaurant_id, driver_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        self.driver_id = driver_id
        print(self)

    def __str__(self):
        return (f"Driver {self.driver_id} accepted to deliver "
                f"order {self.order_id} "
                f"from restaurant {self.restaurant_id} and "
                f"from client {self.client_id} "
                f"in time {self.time}")
