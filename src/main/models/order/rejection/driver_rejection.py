from src.main.models.common.types import Number
from src.main.models.driver.driver import Driver
from src.main.models.order.rejection.rejection import Rejection
from src.main.models.order.rejection.status import Status


class DriverRejection(Rejection):
    def __init__(self, driver: Driver, time: Number):
        super().__init__(time, Status.DRIVER_REJECTED)
        self.driver = driver
