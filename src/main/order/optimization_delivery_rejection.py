from simpy.core import SimTime

from src.main.order.delivery_rejection import DeliveryRejection
from src.main.order.delivery_rejection_type import DeliveryRejectionType


class OptimizationDeliveryRejection(DeliveryRejection):
    def __init__(self, time: SimTime):
        super().__init__(time, DeliveryRejectionType.REJECTED_BY_OPTIMIZATION)
