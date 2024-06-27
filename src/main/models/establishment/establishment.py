import uuid
from typing import Optional, List

from src.main.models.common.types import Coordinate, Number
from src.main.models.common.localizable import Localizable
from src.main.models.common.capacity import Capacity
from src.main.models.establishment.catalog import Catalog


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
        self.capacity = capacity
        self.catalog = catalog
        self.request_rate = request_rate
        self.production_rate = production_rate
        self.radius = radius
        self.estimate = estimate

        self.orders_in_preparation: int = 0
        self.overloaded_until: Number = 0
        self.requests: List = []
        self.accepted: List = []
        self.rejected: List = []
