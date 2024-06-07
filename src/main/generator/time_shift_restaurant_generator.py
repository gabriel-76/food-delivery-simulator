import random

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.item import Item
from src.main.restaurant.catalog import Catalog
from src.main.restaurant.restaurant import Restaurant


class TimeShiftRestaurantGenerator(TimeShiftGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, function, time_shift=1):
        super().__init__(environment, function, time_shift)

    def run(self):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        restaurants = [
            Restaurant(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True,
                catalog=catalog
            )
            for _ in self.range()
        ]
        self.environment.add_restaurants(restaurants)
