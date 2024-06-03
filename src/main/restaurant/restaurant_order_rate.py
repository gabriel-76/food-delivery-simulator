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
            order_rate,
            operating_radius
    ):
        super().__init__(environment, coordinates, available, catalog)
        self.order_rate = order_rate
        self.operating_radius = operating_radius
