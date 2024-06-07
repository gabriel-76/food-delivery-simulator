import asyncio
import random
from datetime import datetime

from src.main.client.client import Client
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.order import Order
from src.main.order.order_generator import OrderGenerator


class OrderRestaurantRateGenerator(OrderGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment):
        super().__init__(environment)

    def is_in_normal_distribution(self, radius):
        value = random.gauss(0, radius)
        return -radius <= value <= radius

    def process_restaurant(self, restaurant):
        for _ in range(restaurant.order_rate):

            client_coordinates = self.environment.map.random_point_in_circle(
                restaurant.coordinates,
                restaurant.operating_radius
            )

            if not self.is_in_normal_distribution(restaurant.operating_radius):
                client_coordinates = self.environment.map.random_point_outside_circle(
                    restaurant.coordinates,
                    restaurant.operating_radius
                )

            client = Client(
                environment=self.environment,
                coordinates=client_coordinates,
                available=True
            )

            self.environment.clients.append(client)

            items = random.sample(restaurant.catalog.items, 2)

            order = Order(client, restaurant, datetime.now(), items)

            client.place_order(order, restaurant)

    def generate(self):
        while True:
            start_time = datetime.now()
            for restaurant in self.environment.restaurants:
                self.process_restaurant(restaurant)

            end_time = datetime.now()
            print(self.environment.now, (end_time - start_time).total_seconds())
            # print("restaurants", len(self.environment.restaurants))
            # print("clients", len(self.environment.clients))
            # print("drivers", len(self.environment.drivers))
            # print("orders delivered", len(self.environment.delivered_orders.items))
            # print("orders waiting", len(self.environment.ready_orders.items))
            yield self.environment.timeout(1)
