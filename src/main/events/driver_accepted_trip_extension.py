from src.main.events.driver_accepted_trip import DriverAcceptedTrip
from src.main.events.event_type import EventType


class DriverAcceptedTripExtension(DriverAcceptedTrip):
    def __init__(self, driver_id, trip_id, old_distance, distance, time):
        super().__init__(driver_id, trip_id, distance, time)
        self.old_distance = old_distance
        self.event_type = EventType.DRIVER_ACCEPTED_EXTENSION_TRIP

    def __str__(self):
        return (f"Driver {self.driver_id} accepted the "
                f"trip extension {self.trip_id} and the total "
                f"distance increased from {self.old_distance} to {self.distance} in "
                f"time {self.time}")
