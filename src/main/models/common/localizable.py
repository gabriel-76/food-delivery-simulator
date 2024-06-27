import uuid

from src.main.models.common.types import Coordinate


class Localizable:
    def __init__(
            self,
            identifier: uuid = uuid.uuid4(),
            available: bool = True,
            coordinate: Coordinate = (0, 0)
    ) -> None:
        self._identifier = identifier
        self._coordinate = coordinate
        self._available = available

    @property
    def identifier(self):
        return self._identifier

    @property
    def coordinate(self) -> Coordinate:
        return self._coordinate

    @property
    def available(self) -> bool:
        return self._available

    def enable(self) -> None:
        self._available = True

    def disable(self) -> None:
        self._available = False
