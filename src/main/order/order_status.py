from enum import Enum, auto


class OrderStatus(Enum):
    CREATED = auto()
    CLIENT_PLACED = auto()
    RESTAURANT_ACCEPTED = auto()
    RESTAURANT_REJECTED = auto()
    RESTAURANT_PREPARING = auto()
    RESTAURANT_FINISHED = auto()
    DRIVER_ACCEPTED = auto()
    DRIVER_REJECTED = auto()
    DRIVER_COLLECTING = auto()
    DRIVER_COLLECTED = auto()
    DRIVER_DELIVERING = auto()
    DRIVER_ARRIVED_DELIVERY_LOCATION = auto()
    CLIENT_RECEIVED = auto()
    DRIVER_DELIVERED = auto()

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
