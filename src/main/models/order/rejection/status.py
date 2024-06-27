from enum import Enum, auto


class Status(Enum):
    ESTABLISHMENT_REJECTED = auto()
    SYSTEM_REJECTED = auto()
    DRIVER_REJECTED = auto()
