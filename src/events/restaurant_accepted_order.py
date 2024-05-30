from src.events.event import Event


class RestaurantAcceptedOrder(Event):
    def __init__(self, order_id, client_id, restaurant_id, time):
        super().__init__(order_id, client_id, restaurant_id, time)
