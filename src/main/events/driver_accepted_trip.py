from src.main.events.event_type import EventType


class DriverAcceptedTrip:
    def __init__(self, driver_id, trip_id, distance, time):
        self.driver_id = driver_id
        self.trip_id = trip_id
        self.distance = distance
        self.time = time
        self.event_type = EventType.DRIVER_ACCEPTED_TRIP

    def __str__(self):
        return (f"Driver {self.driver_id} accepted the "
                f"trip {self.trip_id} of total "
                f"distance {self.distance} in "
                f"time {self.time}")
