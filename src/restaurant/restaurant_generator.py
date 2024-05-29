import random

from src import FoodDeliveryEnvironment
from src.base.dimensions import Dimensions
from src.order.item import Item
from src.restaurant.catalog import Catalog
from src.restaurant.restaurant import Restaurant

NUM_RESTAURANTS = 300


class RestaurantGenerator:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def generate(self):
        while True:
            dimension = Dimensions(1, 1, 1, 1)
            catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
            restaurants = [Restaurant(self.environment, (), True, catalog) for i in range(random.randrange(0, NUM_RESTAURANTS))]
            self.environment.add_restaurants(restaurants)
            yield self.environment.timeout(1)
