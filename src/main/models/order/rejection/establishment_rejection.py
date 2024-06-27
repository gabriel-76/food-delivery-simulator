from src.main.models.common.types import Number
from src.main.models.establishment.establishment import Establishment
from src.main.models.order.rejection.rejection import Rejection
from src.main.models.order.rejection.status import Status


class EstablishmentRejection(Rejection):
    def __init__(self, establishment: Establishment, time: Number):
        super().__init__(time, Status.ESTABLISHMENT_REJECTED)
        self.driver = establishment
