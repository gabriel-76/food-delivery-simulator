import uuid
from typing import List, Optional, TYPE_CHECKING, Union

from src.main.models.commons.capacity import Capacity
from src.main.models.commons.dimension import Dimension
from src.main.models.commons.localizable import Localizable
from src.main.commons.types import Coordinate, Number
from src.main.models.establishment.catalog import Catalog
from src.main.models.order.rejection import EstablishmentRejection

if TYPE_CHECKING:
    from src.main.models.order.order import Order


class Establishment(Localizable):
    def __init__(
            self,
            identifier: uuid = None,
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
        self._preparing: List[Order] = []
        self._rejected: List[Order] = []

    @property
    def catalog(self) -> Catalog:
        return self._catalog

    @property
    def request_rate(self) -> Optional[Number]:
        return self._request_rate

    @property
    def radius(self) -> Optional[Number]:
        return self._radius

    def request(self, orders: Union['Order', List['Order']]) -> None:
        if isinstance(orders, list):
            self._requests.extend(orders)
        else:
            self._requests.append(orders)

    def get_requests(self) -> List['Order']:
        requests = self._requests
        self._requests = []
        return requests

    def get_accepted(self) -> List['Order']:
        accepted = self._accepted
        self._accepted = []
        return accepted

    def get_accepted_within_capacity(self) -> List['Order']:
        occupation = self._occupation()
        orders: List['Order'] = []
        for order in self._accepted:
            if occupation + order.dimension <= self._capacity.dimension:
                orders.append(order)
                occupation += order.dimension
        for order in orders:
            self._accepted.remove(order)
        return orders

    def accept(self, order: 'Order', time: Number, estimated_time: Number) -> None:
        self._accepted.append(order)
        order.accept_preparation(time, estimated_time)

    def reject(self, order: 'Order', time: Number) -> None:
        self._rejected.append(order)
        order.reject(EstablishmentRejection(self, time))

    def prepare(self, order: 'Order', time: Number) -> None:
        self._preparing.append(order)
        order.start_preparation(time)

    def finish(self, order: 'Order', time: Number) -> None:
        self._preparing.remove(order)  # TODO: Verify efficiency of remove method
        order.finish_preparation(time)

    def _occupation(self) -> Dimension:
        return sum([order.dimension for order in self._preparing], Dimension.empty())

    def is_empty(self) -> bool:
        return len(self._preparing) == 0

    def is_within_capacity(self) -> bool:
        return self._occupation() <= self._capacity

    # def is_full(self) -> bool:
    #     return len(self._preparing) >= self._capacity.max