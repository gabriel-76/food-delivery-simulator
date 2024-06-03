import random

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.item import Item
from src.main.restaurant.catalog import Catalog
from src.main.restaurant.restaurant import Restaurant
from src.main.restaurant.restaurant_generator import RestaurantGenerator
from src.main.restaurant.restaurant_order_rate import RestaurantOrderRate


class RestaurantOrderRateGenerator(RestaurantGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, number_of_restaurants: int):
        super().__init__(environment)
        self.number_of_restaurants = number_of_restaurants

    def generate(self):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        restaurants = [
            RestaurantOrderRate(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True,
                catalog=catalog,
                order_rate=random.randint(0, 10),
                operating_radius=random.randint(10, 30)
            )
            for _ in range(self.number_of_restaurants)
        ]
        self.environment.add_restaurants(restaurants)
        yield self.environment.timeout(1)
