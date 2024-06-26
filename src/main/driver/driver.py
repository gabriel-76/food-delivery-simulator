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
            movement_rate: Number
    ):
        self.driver_id = uuid.uuid4()
        self.coordinate = coordinate
        self.capacity = capacity
        self.available = available
        self.status = status
        self.movement_rate = movement_rate

