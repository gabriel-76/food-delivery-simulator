from enum import Enum, auto


class DriverStatus(Enum):
    AVAILABLE = auto()
    PICKING_UP = auto()
    DELIVERING = auto()
