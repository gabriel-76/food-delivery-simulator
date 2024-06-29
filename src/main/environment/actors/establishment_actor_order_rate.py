import random

from src.main.environment.actors.establishment_actor import EstablishmentActor
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.models.establishment.establishment import Establishment


class EstablishmentActorOrderRate(EstablishmentActor):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            establishment: Establishment
    ):
        super().__init__(environment, establishment)

    def time_to_prepare_order(self, order):
        time_to_prepare = round(random.expovariate(1 / self._establishment.order_production_time_rate))
        return time_to_prepare

    def time_estimate_to_prepare_order(self, order):
        return self._establishment._available_in + self.time_to_prepare_order(order)
