import uuid
from typing import TYPE_CHECKING

from src.main.models.commons.localizable import Localizable
from src.main.models.commons.types import Coordinate, Number


if TYPE_CHECKING:
    from src.main.models.order.order import Order
    from src.main.models.establishment.establishment import Establishment
    from src.main.models.driver.driver import Driver


class Customer(Localizable):
    def __init__(
            self,
            identifier: uuid = uuid.uuid4(),
            available: bool = True,
            coordinate: Coordinate = (0, 0)
    ) -> None:
        super().__init__(identifier, available, coordinate)

    @staticmethod
    def place(order: 'Order', establishment: 'Establishment', time: Number) -> None:
        order.placed(time)
        establishment.request(order)

    @staticmethod
    def receive(order: 'Order', driver: 'Driver', time: Number) -> None:
        driver.deliver(order, time)
