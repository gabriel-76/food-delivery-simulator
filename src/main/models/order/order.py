import uuid
from enum import Enum, auto
from typing import List

from src.main.models.commons.dimension import Dimension
from src.main.models.commons.item import Item
from src.main.models.commons.types import Number
from src.main.models.customer.customer import Customer
from src.main.models.establishment.establishment import Establishment
from src.main.models.order.rejection import Rejection, RejectionType


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


class Order:
    def __init__(
            self,
            customer: Customer,
            establishment: Establishment,
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
    def customer(self) -> Customer:
        return self._customer

    @property
    def establishment(self) -> Establishment:
        return self._establishment

    @property
    def dimension(self):
        return self._dimension

    @property
    def status(self) -> OrderStatus:
        return self._status

    def is_ready(self) -> bool:
        return self._status == OrderStatus.READY

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
