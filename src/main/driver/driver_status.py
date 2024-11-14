from enum import Enum, auto


class DriverStatus(Enum):
    AVAILABLE = auto()
    PICKING_UP = auto()
    PICKING_UP_WAINTING = auto()
    DELIVERING = auto()
    DELIVERING_WAITING = auto()
