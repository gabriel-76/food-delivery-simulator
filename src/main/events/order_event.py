from src.main.events.event import Event


class OrderEvent(Event):
    def __init__(self, order_id, client_id, restaurant_id, time, event_type):
        super().__init__(time, event_type)
        self.order_id = order_id
        self.client_id = client_id
        self.restaurant_id = restaurant_id

    # def __lt__(self, other):
    #     return self.creation_date < other.creation_date
