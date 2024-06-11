import random
from datetime import datetime

from src.main.base.geometry import point_in_gauss_circle
from src.main.client.client import Client
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderRestaurantRateGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def process_restaurant(self, env: FoodDeliveryEnvironment, restaurant):
        request_estimate = random.expovariate(1 / restaurant.order_request_rate)
        for _ in range(round(request_estimate)):

            client = Client(
                environment=env,
                coordinates=point_in_gauss_circle(
                    restaurant.coordinates,
                    restaurant.operating_radius,
                    env.map.size
                ),
                available=True
            )

            items = random.sample(restaurant.catalog.items, 2)

            order = Order(client, restaurant, env.now, items)

            env.state.clients.append(client)
            env.state.orders.append(order)

            client.place_order(order, restaurant)

    def run(self, env: FoodDeliveryEnvironment):
        for restaurant in env.state.restaurants:
            conf_order = len(restaurant.confirmed_orders.items)
            if conf_order > 0:
                print(env.now, conf_order, restaurant.orders_in_preparation)
            self.process_restaurant(env, restaurant)
