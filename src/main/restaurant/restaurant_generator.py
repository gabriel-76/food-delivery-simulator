import random

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.item import Item
from src.main.restaurant.catalog import Catalog
from src.main.restaurant.restaurant import Restaurant

NUM_RESTAURANTS = 300


class RestaurantGenerator:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def generate(self):
        while True:
            dimension = Dimensions(1, 1, 1, 1)
            catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
            restaurants = [
                Restaurant(
                    environment=self.environment,
                    coordinates=self.environment.map.random_point(),
                    available=True,
                    catalog=catalog
                )
                for _ in range(random.randrange(0, NUM_RESTAURANTS))
            ]
            self.environment.add_restaurants(restaurants)
            yield self.environment.timeout(1)
