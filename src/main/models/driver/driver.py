import uuid
from typing import Optional, List

from src.main.models.common.types import Coordinate, Number
from src.main.models.common.localizable import Localizable
from src.main.models.common.capacity import Capacity
from src.main.models.driver.status import Status
from src.main.models.route.route import Route
from src.main.models.route.segment.segment import Segment


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
        self._capacity = capacity
        self._status = status
        self._movement_rate = movement_rate
        self._max_distance = max_distance
        self._current_route: Optional[Route] = None
        self._current_segment: Optional[Segment] = None
        self._travelled_distance: Number = 0
        self._requests: List[Route] = []

