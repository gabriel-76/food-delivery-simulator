from src.events.event import Event


class ClientReceivedOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, driver_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        self.driver_id = driver_id
        print(self)

    def __str__(self):
        return (f"Client {self.client_id} "
                f"picked up the order {self.order_id} "
                f"with driver {self.driver_id} "
                f"from restaurant {self.restaurant_id} "
                f"in time {self.time}")
