import random
from datetime import datetime

from src.main.client.client import Client
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderRestaurantRateGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift):
        super().__init__(function, time_shift)

    def is_in_normal_distribution(self, radius):
        value = random.gauss(0, radius)
        return -radius <= value <= radius

    def process_restaurant(self, env: FoodDeliveryEnvironment, restaurant):
        for _ in range(restaurant.order_rate):

            client_coordinates = env.map.random_point_in_circle(
                restaurant.coordinates,
                restaurant.operating_radius
            )

            if not self.is_in_normal_distribution(restaurant.operating_radius):
                client_coordinates = env.map.random_point_outside_circle(
                    restaurant.coordinates,
                    restaurant.operating_radius
                )

            client = Client(
                environment=env,
                coordinates=client_coordinates,
                available=True
            )

            env.state.clients.append(client)

            items = random.sample(restaurant.catalog.items, 2)

            order = Order(client, restaurant, env.now, items)

            client.place_order(order, restaurant)

    def run(self, env: FoodDeliveryEnvironment):
        start_time = datetime.now()
        for restaurant in env.state.restaurants:
            self.process_restaurant(env, restaurant)

        end_time = datetime.now()
        print(env.now, (end_time - start_time).total_seconds())
        # print("restaurants", len(self.environment.restaurants))
        # print("clients", len(self.environment.clients))
        # print("drivers", len(self.environment.drivers))
        # print("orders delivered", len(self.environment.delivered_orders.items))
        # print("orders waiting", len(self.environment.ready_orders.items))
