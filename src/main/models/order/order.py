import uuid
from typing import List

from src.main.models.common.dimension import Dimension
from src.main.models.common.item import Item
from src.main.models.customer.customer import Customer
from src.main.models.establishment.establishment import Establishment
from src.main.models.order.rejection.rejection import Rejection
from src.main.models.order.status import Status


class Order:
    def __init__(
            self,
            customer: Customer,
            establishment: Establishment,
            request_date: int,
            items: List[Item]
    ):
        self.order_id = uuid.uuid4()
        self.customer = customer
        self.establishment = establishment
        self.request_date = request_date
        self.items = items
        self.status: Status = Status.CREATED
        self.estimated_time_to_ready = 0
        self.time_it_was_ready = 0
        self.dimension: Dimension = Dimension.empty()
        self.delivery_rejections: List[Rejection] = []
