from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.item import Item
from src.main.restaurant.catalog import Catalog
from src.main.actors.restaurant import Restaurant


class TimeShiftRestaurantGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliverySimpyEnv):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        restaurants = [
            Restaurant(
                environment=env,
                coordinates=env.map.random_point(),
                available=True,
                catalog=catalog
            )
            for _ in self.range(env)
        ]
        env.add_restaurants(restaurants)
