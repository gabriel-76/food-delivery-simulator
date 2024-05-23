import random
from datetime import datetime
from uuid import uuid4

from simpy import Environment

from src.base.dimensions import Dimensions
from src.client.client import Client
from src.driver.capacity import Capacity
from src.driver.driver import Driver
from src.order.order import Order
from src.restaurant.restaurant import Restaurant

NUM_RESTAURANTS = 1
NUM_DRIVERS = 1
NUM_CLIENTS = 1
SIMULATION_TIME = 40


class Simulator:
    def __init__(self, environment: Environment):
        self.environment = environment

    def generate_orders(self, clients: [Client], restaurants: [Restaurant], drivers: [Driver]):
        cliente_id = 0
        while True:
            client = random.choice(clients)
            restaurant = random.choice(restaurants)
            driver = random.choice(drivers)

            order = Order(str(cliente_id), client, restaurant, datetime.now(), [])

            self.environment.process(client.make_a_request(order, restaurant))

            self.environment.process(restaurant.receive_order(order))

            self.environment.process(driver.deliver_order(order))

            cliente_id += 1
            yield self.environment.timeout(random.expovariate(1.0 / 2))  # novo pedido a cada ~2 minutos

    def run(self):
        clients = [Client(self.environment, f"Client {i}", ()) for i in range(NUM_CLIENTS)]
        restaurants = [Restaurant(self.environment, f"Restaurant {i}", (), True) for i in range(NUM_RESTAURANTS)]
        capacity = Capacity(Dimensions(1, 1, 1, 1))
        drivers = [Driver(self.environment, f"Driver {i}", (), f"type_{i}", capacity) for i in range(NUM_DRIVERS)]

        self.environment.process(self.generate_orders(clients, restaurants, drivers))
