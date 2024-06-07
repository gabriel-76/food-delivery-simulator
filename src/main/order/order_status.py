from enum import Enum, auto


class OrderStatus(Enum):
    CREATED = auto()
    PLACED = auto()
    RESTAURANT_ACCEPTED = auto()
    RESTAURANT_REJECTED = auto()
    PREPARING = auto()
    READY = auto()
    DRIVER_ACCEPTED = auto()
    DRIVER_REJECTED = auto()
    COLLECTING = auto()
    COLLECTED = auto()
    DELIVERING = auto()
    DRIVER_ARRIVED_DELIVERY_LOCATION = auto()
    RECEIVED = auto()
    DELIVERED = auto()

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
