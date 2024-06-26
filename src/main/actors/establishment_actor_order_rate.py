import random

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.establishment.establishment import Establishment
from src.main.actors.establishment_actor import EstablishmentActor


class EstablishmentActorOrderRate(EstablishmentActor):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            establishment: Establishment
    ):
        super().__init__(environment, establishment)
        self.order_request_time_rate = establishment.order_request_time_rate
        self.order_production_time_rate = establishment.order_production_time_rate
        self.operating_radius = establishment.operating_radius

    def time_to_prepare_order(self, order):
        time_to_prepare = round(random.expovariate(1 / self.order_production_time_rate))
        return time_to_prepare

    def time_estimate_to_prepare_order(self, order):
        return self.overloaded_until + self.time_to_prepare_order(order)
