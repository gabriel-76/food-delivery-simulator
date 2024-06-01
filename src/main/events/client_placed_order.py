from src.main.events.event import Event


class ClientPlacedOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        print(self)

    def __str__(self):
        return (f"Client {self.client_id} placed an "
                f"order {self.order_id} to "
                f"restaurant {self.restaurant_id} in "
                f"time {self.time}")
