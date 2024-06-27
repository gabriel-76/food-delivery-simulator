from src.main.models.common.types import Number
from src.main.models.order.rejection.status import Status


class Rejection:
    def __init__(self, time: Number, status: Status):
        self.time = time
        self.status = status
