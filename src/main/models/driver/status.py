from enum import Enum, auto


class Status(Enum):
    AVAILABLE = auto()
    PICKING_UP = auto()
    DELIVERING = auto()
