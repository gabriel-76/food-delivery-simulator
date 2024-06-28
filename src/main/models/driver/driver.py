import uuid
from enum import Enum, auto
from typing import Optional, List, TYPE_CHECKING

from src.main.models.commons.capacity import Capacity
from src.main.models.commons.localizable import Localizable
from src.main.models.commons.types import Number, Coordinate
from src.main.models.route.route import Route
from src.main.models.route.segment import Segment

if TYPE_CHECKING:
    from src.main.models.order.order import Order


class DriverStatus(Enum):
    AVAILABLE = auto()
    PICKING_UP = auto()
    DELIVERING = auto()


class Driver(Localizable):
    def __init__(
            self,
            identifier: uuid = uuid.uuid4(),
            available: bool = True,
            coordinate: Coordinate = (0, 0),
            capacity: Capacity = Capacity.empty(),
            status: DriverStatus = DriverStatus.AVAILABLE,
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

    @staticmethod
    def deliver(order: 'Order', time: Number) -> None:
        order.finish_delivery(time)


