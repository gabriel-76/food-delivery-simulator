import uuid
from typing import Optional, List

from src.main.base.types import Coordinate, Number
from src.main.establishment.catalog import Catalog


class Establishment:
    def __init__(
            self,
            coordinate: Coordinate,
            available: bool,
            catalog: Catalog,
            production_capacity: Number = float('inf'),
            order_request_time_rate: Optional[Number] = None,
            order_production_time_rate: Optional[Number] = None,
            operating_radius: Optional[Number] = None,
            use_estimate: bool = False
    ) -> None:
        self.establishment_id = uuid.uuid4()
        self.coordinate = coordinate
        self.available = available
        self.catalog = catalog
        self.production_capacity = production_capacity
        self.order_request_time_rate = order_request_time_rate
        self.order_production_time_rate = order_production_time_rate
        self.operating_radius = operating_radius
        self.use_estimate = use_estimate
        self.orders_in_preparation: int = 0
        self.overloaded_until: Number = 0
        self.order_requests: List = []
        self.orders_accepted: List = []
        self.orders_rejected: List = []
