import uuid
from typing import Optional, List

from src.main.models.common.types import Coordinate, Number
from src.main.models.common.localizable import Localizable
from src.main.models.common.capacity import Capacity
from src.main.models.establishment.catalog import Catalog
from src.main.models.order.order import Order


class Establishment(Localizable):
    def __init__(
            self,
            identifier: uuid = uuid.uuid4(),
            available: bool = True,
            coordinate: Coordinate = (0, 0),
            capacity: Capacity = Capacity.empty(),
            catalog: Catalog = Catalog.empty(),
            request_rate: Optional[Number] = None,
            production_rate: Optional[Number] = None,
            radius: Optional[Number] = None,
            estimate: bool = False
    ) -> None:
        super().__init__(identifier, available, coordinate)
        self._capacity = capacity
        self._catalog = catalog
        self._request_rate = request_rate
        self._production_rate = production_rate
        self._radius = radius
        self._estimate = estimate
        self._available_in: Number = 0
        self._requests: List[Order] = []
        self._accepted: List[Order] = []
        self._rejected: List[Order] = []
