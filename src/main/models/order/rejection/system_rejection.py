from src.main.models.common.types import Number
from src.main.models.order.rejection.rejection import Rejection
from src.main.models.order.rejection.status import Status


class SystemRejection(Rejection):
    def __init__(self, time: Number):
        super().__init__(time, Status.SYSTEM_REJECTED)
