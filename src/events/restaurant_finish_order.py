from src.events.event import Event


class RestaurantFinishOrder(Event):
    def __init__(self, client_id, restaurant_id, time):
        super().__init__(client_id, restaurant_id, time)
