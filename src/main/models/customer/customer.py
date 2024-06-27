import uuid

from src.main.models.common.types import Coordinate
from src.main.models.common.localizable import Localizable


class Customer(Localizable):
    def __init__(
            self,
            identifier: uuid = uuid.uuid4(),
            available: bool = True,
            coordinate: Coordinate = (0, 0)
    ) -> None:
        super().__init__(identifier, available, coordinate)
