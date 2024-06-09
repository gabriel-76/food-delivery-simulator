from src.main.events.event_type import EventType
from src.main.events.trip_event import TripEvent


class DriverRejectedTrip(TripEvent):
    def __init__(self, driver_id, trip_id, distance, time):
        super().__init__(driver_id, trip_id, distance, time, EventType.DRIVER_REJECTED_TRIP)

    def __str__(self):
        return (f"Driver {self.driver_id} rejected the "
                f"trip {self.trip_id} of total "
                f"distance {self.distance} in "
                f"time {self.time}")
