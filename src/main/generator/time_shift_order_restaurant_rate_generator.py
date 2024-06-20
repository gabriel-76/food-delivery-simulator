import random

from src.main.base.geometry import point_in_gauss_circle
from src.main.customer.customer import Customer
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderRestaurantRateGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)
        self.hash_timeout = {}

    def process_restaurant(self, env: FoodDeliverySimpyEnv, restaurant):

        if restaurant.restaurant_id not in self.hash_timeout or self.hash_timeout[restaurant.restaurant_id] == env.now:

            customer = Customer(
                environment=env,
                coordinates=point_in_gauss_circle(
                    restaurant.coordinates,
                    restaurant.operating_radius,
                    env.map.size
                ),
                available=True
            )

            items = random.sample(restaurant.catalog.items, 2)

            order = Order(customer, restaurant, env.now, items)

            env.state.customers.append(customer)
            env.state.orders.append(order)

            customer.place_order(order, restaurant)

            timeout = round(random.expovariate(1 / restaurant.order_request_time_rate))
            # print("generated in time", env.now, timeout)

            self.hash_timeout[restaurant.restaurant_id] = env.now + max(timeout, 1)

    def run(self, env: FoodDeliverySimpyEnv):
        for _ in self.range(env):
            for restaurant in env.state.restaurants:
                self.process_restaurant(env, restaurant)
