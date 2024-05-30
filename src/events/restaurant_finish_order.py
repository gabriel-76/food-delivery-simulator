from src.events.event import Event


class RestaurantFinishOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        print(self)

    def __str__(self):
        return (f"Restaurant {self.restaurant_id} "
                f"has finished preparing the order {self.order_id} "
                f"from client {self.client_id} "
                f"in time {self.time}")
