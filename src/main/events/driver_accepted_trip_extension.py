from src.main.events.event_type import EventType
from src.main.events.trip_event import TripEvent


class DriverAcceptedTripExtension(TripEvent):
    def __init__(self, driver_id, trip_id, old_distance, distance, time):
        super().__init__(driver_id, trip_id, distance, time, EventType.DRIVER_ACCEPTED_EXTENSION_TRIP)
        self.old_distance = old_distance

    def __str__(self):
        return (f"Driver {self.driver_id} accepted the "
                f"trip extension {self.trip_id} and the total "
                f"distance increased from {self.old_distance} to {self.distance} in "
                f"time {self.time}")
