from src.main.events.event import Event


class TripEvent(Event):
    def __init__(self, driver_id, trip_id, distance, time, event_type):
        super().__init__(time, event_type)
        self.driver_id = driver_id
        self.trip_id = trip_id
        self.distance = distance
