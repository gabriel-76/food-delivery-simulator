from enum import Enum, auto


class DriverStatus(Enum):
    WAITING = auto()
    COLLECTING = auto()
    DELIVERING = auto()
