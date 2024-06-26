import random

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.establishment.catalog import Catalog
from src.main.establishment.establishment import Establishment


class EstablishmentOrderRate(Establishment):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            coordinates,
            available: bool,
            catalog: Catalog,
            production_capacity,
            order_request_time_rate,
            order_production_time_rate,
            operating_radius,
            use_estimate: bool = False,
    ):
        super().__init__(environment, coordinates, available, catalog, production_capacity, use_estimate)
        self.order_request_time_rate = order_request_time_rate
        self.order_production_time_rate = order_production_time_rate
        self.operating_radius = operating_radius

    def time_to_prepare_order(self, order):
        time_to_prepare = round(random.expovariate(1 / self.order_production_time_rate))
        return time_to_prepare

    def time_estimate_to_prepare_order(self, order):
        return self.overloaded_until + self.time_to_prepare_order(order)
