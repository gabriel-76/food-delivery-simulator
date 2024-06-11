import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.restaurant.catalog import Catalog
from src.main.restaurant.restaurant import Restaurant


class RestaurantOrderRate(Restaurant):
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            coordinates,
            available: bool,
            catalog: Catalog,
            order_production_capacity,
            order_request_rate,
            order_production_rate,
            operating_radius
    ):
        super().__init__(environment, coordinates, available, catalog, order_production_capacity)
        self.order_request_rate = order_request_rate
        self.order_production_rate = order_production_rate
        self.operating_radius = operating_radius

    def time_to_prepare_order(self, order):
        return round(random.expovariate(1/self.order_production_rate))
