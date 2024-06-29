import uuid
from enum import Enum, auto
from typing import Optional, List, TYPE_CHECKING, Union

from src.main.models.commons.capacity import Capacity
from src.main.models.commons.localizable import Localizable
from src.main.commons.types import Number, Coordinate
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
            identifier: uuid = None,
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
        self._route: Route = Route.empty()
        self._segment: Optional[Segment] = None
        self._travelled_distance: Number = 0
        self._requests: List[Route] = []

    @property
    def capacity(self) -> Capacity:
        return self._capacity

    @property
    def status(self) -> DriverStatus:
        return self._status

    @property
    def movement_rate(self) -> Number:
        return self._movement_rate

    @property
    def max_distance(self) -> Number:
        return self._max_distance

    @property
    def route(self) -> Optional[Route]:
        return self._route

    @property
    def segment(self) -> Optional[Segment]:
        return self._segment

    @property
    def travelled_distance(self) -> Number:
        return self._travelled_distance

    def request(self, routes: Union[Route, List[Route]]) -> None:
        if isinstance(routes, list):
            self._requests.extend(routes)
        else:
            self._requests.append(routes)

    def get_request(self) -> Optional[Route]:
        return self._requests.pop(0) if self._requests else None

    def accept(self, route: Route, time: Number, estimated_time: Number) -> None:
        self._route.extend(route)
        route.accept_pickup(time, estimated_time)
        if self._segment is None:
            self._segment = self._route.next()

    def is_waiting_to_collect(self) -> bool:
        return self._route and not self._segment.is_ready()

    def has_next(self) -> bool:
        return self._route.size > 0

    def _next(self):
        self._segment = self._route.next()

    def picking_up(self, time: Number, estimated_time: Number) -> None:
        self._status = DriverStatus.PICKING_UP
        self._segment.order.accept_pickup(time, estimated_time)

    def picked_up(self, time: Number) -> None:
        self._coordinate = self._segment.coordinate
        self._segment.order.start_pickup(time)
        self._next()

    def delivering(self, time: Number) -> None:
        self._status = DriverStatus.DELIVERING
        self._segment.order.start_delivery(time)

    def delivered(self, time: Number) -> None:
        self._coordinate = self._segment.coordinate
        self._segment.order.finish_delivery(time)
        self._status = DriverStatus.AVAILABLE
        self._next()

    def fits(self, route: Route) -> bool:
        return self._capacity.fits(route.dimension)

    def move(self, coordinate: Coordinate) -> None:
        self._coordinate = coordinate

    @staticmethod
    def deliver(order: 'Order', time: Number) -> None:
        order.finish_delivery(time)
