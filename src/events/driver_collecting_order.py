from src.events.event import Event


class DriverCollectingOrder(Event):
    def __init__(self, client_id, restaurant_id, driver_id, time):
        super().__init__(client_id, restaurant_id, time)
        self.driver_id = driver_id
