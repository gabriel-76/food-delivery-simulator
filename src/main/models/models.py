import uuid
from enum import Enum, auto
from typing import Optional, List

from src.main.models.commons.capacity import Capacity
from src.main.models.commons.dimension import Dimension
from src.main.models.commons.item import Item
from src.main.models.commons.localizable import Localizable
from src.main.models.commons.types import Number, Coordinate


class RejectionType(Enum):
    ESTABLISHMENT_REJECTED = auto()
    SYSTEM_REJECTED = auto()
    DRIVER_REJECTED = auto()


class Rejection:
    def __init__(self, time: Number, rejection_type: RejectionType):
        self._time = time
        self._rejection_type = rejection_type

    @property
    def rejection_type(self):
        return self._rejection_type


class Order:
    def __init__(
            self,
            customer: 'Customer',
            establishment: 'Establishment',
            items: List[Item],
            identifier: uuid = uuid.uuid4()
    ):
        super().__init__()
        self._identifier = identifier
        self._customer: Customer = customer
        self._establishment: Establishment = establishment
        self._items: List[Item] = items
        self._dimension: Dimension = self._calculate_dimension()
        self._status: OrderStatus = OrderStatus.CREATED
        self._rejections: List[Rejection] = []

        # Time when the order was requested
        self._requested_at: Number = 0

        # Estimated time when the establishment accepted the order
        self._accepted_preparation_at: Number = 0
        # Estimated time when the establishment will finish the preparation
        self._estimated_preparation_at: Number = 0
        # Time when the establishment started the preparation
        self._start_preparation_at: Number = 0
        # Time when the establishment finished the preparation
        self._finish_preparation_at: Number = 0

        # Estimated time when the driver accepted pickup the order
        self._accepted_pickup_at: Number = 0
        # Estimated time when the driver will finish the pickup
        self._estimated_pickup_at: Number = 0
        # Time when the driver started the pickup
        self._start_pickup_at: Number = 0
        # Time when the driver finished the pickup
        self._finish_pickup_at: Number = 0

        # Estimated time when the driver accepted delivery the order
        self._accepted_delivery_at: Number = 0
        # Estimated time when the driver will finish the delivery
        self._estimated_delivery_at: Number = 0
        # Time when the driver started the delivery
        self._start_delivery_at: Number = 0
        # Time when the driver finished the delivery
        self._finish_delivery_at: Number = 0

    @property
    def identifier(self):
        return self._identifier

    @property
    def customer(self):
        return self._customer

    @property
    def establishment(self):
        return self._establishment

    @property
    def dimension(self):
        return self._dimension

    def placed(self, time: Number) -> None:
        self._status = OrderStatus.PLACED
        self._requested_at = time

    def accept_preparation(self, time: Number, estimated_time: Number) -> None:
        self._status = OrderStatus.ESTABLISHMENT_ACCEPTED
        self._accepted_preparation_at = time
        self._estimated_preparation_at = estimated_time

    def start_preparation(self, time: Number) -> None:
        self._status = OrderStatus.PREPARING
        self._start_preparation_at = time

    def finish_preparation(self, time: Number) -> None:
        self._status = OrderStatus.READY
        self._finish_preparation_at = time

    def accept_pickup(self, time: Number, estimated_time: Number) -> None:
        self._status = OrderStatus.DRIVER_ACCEPTED
        self._accepted_pickup_at = time
        self._estimated_pickup_at = estimated_time

    def start_pickup(self, time: Number) -> None:
        self._status = OrderStatus.PICKING_UP
        self._start_pickup_at = time

    def finish_pickup(self, time: Number) -> None:
        self._status = OrderStatus.PICKED_UP
        self._finish_pickup_at = time

    def accept_delivery(self, time: Number, estimated_time: Number) -> None:
        self._accepted_delivery_at = time
        self._estimated_delivery_at = estimated_time

    def start_delivery(self, time: Number) -> None:
        self._status = OrderStatus.DELIVERING
        self._start_delivery_at = time

    def finish_delivery(self, time: Number) -> None:
        self._status = OrderStatus.DELIVERED
        self._finish_delivery_at = time

    def reject(self, rejection: Rejection) -> None:
        if rejection.rejection_type == RejectionType.ESTABLISHMENT_REJECTED:
            self._status = OrderStatus.ESTABLISHMENT_REJECTED
        elif rejection.rejection_type == RejectionType.DRIVER_REJECTED:
            self._status = OrderStatus.DRIVER_REJECTED
        self._rejections.append(rejection)

    def _calculate_dimension(self) -> Dimension:
        if len(self._items) == 0:
            return Dimension.empty()
        self._dimension = Dimension.empty()
        for item in self._items:
            self._dimension += item.dimension
        return self._dimension


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
    def deliver(order: Order, time: Number) -> None:
        order.finish_delivery(time)


class Catalog:
    def __init__(self, items: List[Item]):
        self._items = items

    @property
    def items(self) -> List[Item]:
        return self._items

    @staticmethod
    def empty() -> 'Catalog':
        return Catalog([])


class Establishment(Localizable):
    def __init__(
            self,
            identifier: uuid = uuid.uuid4(),
            available: bool = True,
            coordinate: Coordinate = (0, 0),
            capacity: Capacity = Capacity.empty(),
            catalog: Catalog = Catalog.empty(),
            request_rate: Optional[Number] = None,
            production_rate: Optional[Number] = None,
            radius: Optional[Number] = None,
            estimate: bool = False
    ) -> None:
        super().__init__(identifier, available, coordinate)
        self._capacity = capacity
        self._catalog = catalog
        self._request_rate = request_rate
        self._production_rate = production_rate
        self._radius = radius
        self._estimate = estimate
        self._available_in: Number = 0
        self._requests: List[Order] = []
        self._accepted: List[Order] = []
        self._rejected: List[Order] = []

    def request(self, order: Order) -> None:
        self._requests.append(order)

    def accept(self, order: Order, time: Number, estimated_time: Number) -> None:
        self._accepted.append(order)
        order.accept_preparation(time, estimated_time)

    def reject(self, order: Order, time: Number) -> None:
        self._rejected.append(order)
        order.reject(EstablishmentRejection(self, time))


class Customer(Localizable):
    def __init__(
            self,
            identifier: uuid = uuid.uuid4(),
            available: bool = True,
            coordinate: Coordinate = (0, 0)
    ) -> None:
        super().__init__(identifier, available, coordinate)

    @staticmethod
    def place(order: Order, establishment: Establishment, time: Number) -> None:
        order.placed(time)
        establishment.request(order)

    @staticmethod
    def receive(order: Order, driver: Driver, time: Number) -> None:
        driver.deliver(order, time)


class SystemRejection(Rejection):
    def __init__(self, time: Number):
        super().__init__(time, RejectionType.SYSTEM_REJECTED)


class EstablishmentRejection(Rejection):
    def __init__(self, establishment: Establishment, time: Number):
        super().__init__(time, RejectionType.ESTABLISHMENT_REJECTED)
        self._establishment = establishment


class DriverRejection(Rejection):
    def __init__(self, driver: Driver, time: Number):
        super().__init__(time, RejectionType.DRIVER_REJECTED)
        self._driver = driver


class OrderStatus(Enum):
    CREATED = auto()
    PLACED = auto()
    ESTABLISHMENT_ACCEPTED = auto()
    ESTABLISHMENT_REJECTED = auto()
    PREPARING = auto()
    READY = auto()
    DRIVER_ACCEPTED = auto()
    DRIVER_REJECTED = auto()
    PICKING_UP = auto()
    PICKED_UP = auto()
    DELIVERING = auto()
    DRIVER_ARRIVED_DELIVERY_LOCATION = auto()
    RECEIVED = auto()
    DELIVERED = auto()

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value


class SegmentType(Enum):
    PICKUP = auto()
    DELIVERY = auto()


class Segment:
    def __init__(self, order: Order, segment_type: SegmentType):
        self._order = order
        self._segment_type = segment_type
        self._coordinate: Coordinate = self.extract_coordinate()
        self._dimension = self._order.dimension

    @property
    def coordinate(self):
        return self._coordinate

    @property
    def dimension(self):
        return self._dimension

    def extract_coordinate(self):
        if self.is_pickup():
            return self._order.establishment.coordinate
        return self._order.customer.coordinate

    def is_pickup(self) -> bool:
        return self._segment_type == SegmentType.PICKUP

    def is_delivery(self) -> bool:
        return self._segment_type == SegmentType.DELIVERY


class PickupSegment(Segment):
    def __init__(self, order: Order):
        super().__init__(order, SegmentType.PICKUP)


class DeliverySegment(Segment):
    def __init__(self, order: Order):
        super().__init__(order, SegmentType.DELIVERY)


class Route:
    def __init__(self, segments: List[Segment]):
        self.route_id = uuid.uuid4()
        self._segments = segments
        self._dimension: Dimension = self._calculate_dimension()

    @property
    def coordinates(self) -> List[Coordinate]:
        return [segment.coordinate for segment in self._segments]

    @property
    def segments(self) -> List[Segment]:
        return self._segments

    @property
    def dimension(self) -> Dimension:
        return self._dimension

    @property
    def size(self) -> int:
        return len(self._segments)

    def _calculate_dimension(self) -> Dimension:
        dimension = Dimension.empty()
        for segment in self._segments:
            dimension += segment.dimension
        return dimension

    def has_next(self):
        return len(self._segments) > 0

    def next(self):
        return self._segments.pop(0)

    def extend_route(self, route: 'Route'):
        self._dimension += route.dimension
        self._segments += route.segments
