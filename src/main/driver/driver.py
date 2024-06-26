import uuid

from src.main.base.types import Coordinate, Number
from src.main.driver.capacity import Capacity
from src.main.driver.driver_status import DriverStatus


class Driver:
    def __init__(
            self,
            coordinate: Coordinate,
            capacity: Capacity,
            available: bool,
            status: DriverStatus,
            movement_rate: Number,
            max_distance: Number = 0
    ):
        self.driver_id = uuid.uuid4()
        self.coordinate = coordinate
        self.capacity = capacity
        self.available = available
        self.status = status
        self.movement_rate = movement_rate
        self.max_distance = max_distance
        self.current_route = None
        self.current_route_segment = None
        self.total_distance: Number = 0
        self.route_requests: list = []

    def check_availability(self, route) -> bool:
        return self.capacity.fits(route) and self.available

