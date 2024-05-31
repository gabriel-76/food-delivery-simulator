from src.events.event import Event


class EstimatedOrderPreparationTime(Event):
    def __init__(self, order_id, client_id, restaurant_id, estimated_time, time):
        super().__init__(order_id, client_id, restaurant_id, time)
        self.estimated_time = estimated_time
        print(self)

    def __str__(self):
        return (f"Order {self.order_id} placed by "
                f"client {self.client_id} for "
                f"restaurant {self.restaurant_id} has an "
                f"estimated preparation time of {self.estimated_time} and is expected to be "
                f"ready in time {self.estimated_time + self.time} this event was generated in "
                f"time {self.time}")

