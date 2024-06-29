import uuid
from typing import Optional

from src.main.commons.types import Coordinate


class Localizable:
    def __init__(
            self,
            identifier: Optional[uuid] = None,
            available: bool = True,
            coordinate: Coordinate = (0, 0)
    ) -> None:
        if identifier is None:
            identifier = uuid.uuid4()
        self._identifier = identifier
        self._coordinate = coordinate
        self._available = available

    @property
    def identifier(self) -> uuid:
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
