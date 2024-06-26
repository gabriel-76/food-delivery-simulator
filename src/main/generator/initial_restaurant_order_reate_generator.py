import random

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator
from src.main.order.item import Item
from src.main.restaurant.catalog import Catalog
from src.main.restaurant.restaurant_order_rate import RestaurantOrderRate


class InitialRestaurantOrderRateGenerator(InitialGenerator):
    def __init__(self, num_restaurants,  use_estimate: bool = False):
        self.num_restaurants = num_restaurants
        self.use_estimate = use_estimate

    def run(self, env: FoodDeliverySimpyEnv):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        restaurants = [
            RestaurantOrderRate(
                environment=env,
                coordinates=env.map.random_point(),
                available=True,
                catalog=catalog,
                production_capacity=float('inf'),
                use_estimate=self.use_estimate,
                order_request_time_rate=random.uniform(5.0, 10.0),
                order_production_time_rate=random.uniform(5.0, 10.0),
                operating_radius=random.randint(5, 30),
            )
            for _ in range(self.num_restaurants)
        ]
        env.add_restaurants(restaurants)
