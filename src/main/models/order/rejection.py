from enum import Enum, auto
from typing import TYPE_CHECKING

from src.main.commons.types import Number

if TYPE_CHECKING:
    from src.main.models.establishment.establishment import Establishment
    from src.main.models.driver.driver import Driver


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


class SystemRejection(Rejection):
    def __init__(self, time: Number):
        super().__init__(time, RejectionType.SYSTEM_REJECTED)


class EstablishmentRejection(Rejection):
    def __init__(self, establishment: 'Establishment', time: Number):
        super().__init__(time, RejectionType.ESTABLISHMENT_REJECTED)
        self._establishment = establishment


class DriverRejection(Rejection):
    def __init__(self, driver: 'Driver', time: Number):
        super().__init__(time, RejectionType.DRIVER_REJECTED)
        self._driver = driver
