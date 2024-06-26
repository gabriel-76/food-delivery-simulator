import uuid

from src.main.base.types import Coordinate


class Customer:
    def __init__(self, coordinate: Coordinate, available: bool) -> None:
        self.customer_id = uuid.uuid4()
        self.coordinate = coordinate
        self.available = available
