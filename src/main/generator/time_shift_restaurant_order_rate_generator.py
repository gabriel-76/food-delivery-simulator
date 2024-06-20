import random

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.item import Item
from src.main.restaurant.catalog import Catalog
from src.main.actors.restaurant_order_rate import RestaurantOrderRate


class TimeShiftRestaurantOrderRateGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliverySimpyEnv):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        restaurants = [
            RestaurantOrderRate(
                environment=env,
                coordinates=env.map.random_point(),
                available=True,
                catalog=catalog,
                production_capacity=1,
                order_request_time_rate=random.randint(1, 10),
                order_production_time_rate=random.randint(1, 10),
                operating_radius=random.randint(10, 30)
            )
            for _ in self.range(env)
        ]
        env.add_restaurants(restaurants)
