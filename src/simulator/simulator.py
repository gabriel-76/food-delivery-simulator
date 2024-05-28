import random
from datetime import datetime

from src import FoodDeliveryEnvironment
from src.base.dimensions import Dimensions
from src.client.client import Client
from src.driver.capacity import Capacity
from src.driver.driver import Driver
from src.order.item import Item
from src.order.order import Order
from src.restaurant.catalog import Catalog
from src.restaurant.restaurant import Restaurant

NUM_RESTAURANTS = 300
NUM_DRIVERS = 50
NUM_CLIENTS = 3000
SIMULATION_TIME = 1000000


class Simulator:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def clients_generation_policy(self):
        return [Client(self.environment, f"client_{i}", ()) for i in range(NUM_CLIENTS)]

    def restaurants_generation_policy(self):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        return [Restaurant(self.environment, f"restaurant_{i}", (), True, catalog) for i in range(NUM_RESTAURANTS)]

    def drivers_generation_policy(self):
        capacity = Capacity(Dimensions(10, 10, 10, 10))
        return [Driver(self.environment, f"driver_{i}", (), f"type_{i}", capacity) for i in range(NUM_DRIVERS)]

    def order_generation_policy(self, clients: [Client], restaurants: [Restaurant]):
        order_id = 0
        while True:
            selected_clients = random.sample(clients, 1)
            selected_restaurants = random.sample(restaurants, 1)

            for client in selected_clients:
                restaurant = random.choice(selected_restaurants)

                items = random.sample(restaurant.catalog.items, 2)

                order = Order(str(order_id), client, restaurant, datetime.now(), items)

                client.place_order(order, restaurant)

                order_id += 1
            yield self.environment.timeout(random.expovariate(1.0 / 2))

    def optimizer(self, drivers: [Driver]):
        while True:
            while len(self.environment.ready_orders.items) > 0:
                order = yield self.environment.ready_orders.get()
                filtered_drivers = [d for d in drivers if d.fits(order)]
                driver = random.choice(filtered_drivers)
                self.environment.process(driver.deliver_order(order))
            yield self.environment.timeout(1)

    def run(self):
        clients = self.clients_generation_policy()
        restaurants = self.restaurants_generation_policy()
        drivers = self.drivers_generation_policy()

        self.environment.process(self.order_generation_policy(clients, restaurants))

        self.environment.process(self.optimizer(drivers))
