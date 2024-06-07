from enum import Enum, auto


class DriverStatus(Enum):
    AVAILABLE = auto()
    COLLECTING = auto()
    DELIVERING = auto()
