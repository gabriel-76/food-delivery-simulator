from numbers import Number
import random

from simpy.core import SimTime
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.establishment.catalog import Catalog
from src.main.establishment.establishment import Establishment


class EstablishmentOrderRate(Establishment):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            coordinate,
            available: bool,
            catalog: Catalog,
            production_capacity,
            order_production_time_rate,
            operating_radius,
            id: Number = None,
            use_estimate: bool = False,
    ):
        super().__init__(environment, coordinate, available, catalog, id, production_capacity, use_estimate)
        self.order_production_time_rate = order_production_time_rate
        self.operating_radius = operating_radius

    def time_estimate_to_prepare_order(self) -> SimTime:
        # Não faz sentido o tempo de preparo ser menor que 1
        time_to_prepare = max(1, round(random.expovariate(1 / self.order_production_time_rate)))
        return time_to_prepare
