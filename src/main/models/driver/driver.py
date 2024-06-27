import uuid
from typing import Optional

from src.main.models.common.types import Coordinate, Number
from src.main.models.common.localizable import Localizable
from src.main.models.common.capacity import Capacity
from src.main.models.driver.status import Status
from src.main.models.route.route import Route
from src.main.models.route.segment import Segment


class Driver(Localizable):
    def __init__(
            self,
            identifier: uuid = uuid.uuid4(),
            available: bool = True,
            coordinate: Coordinate = (0, 0),
            capacity: Capacity = Capacity.empty(),
            status: Status = Status.AVAILABLE,
            movement_rate: Number = 0,
            max_distance: Number = 0
    ):
        super().__init__(identifier, available, coordinate)
        self.capacity = capacity
        self.status = status
        self.movement_rate = movement_rate
        self.max_distance = max_distance
        self.current_route: Optional[Route] = None
        self.current_route_segment: Optional[Segment] = None
        self.total_distance: Number = 0
        self.route_requests: list = []

