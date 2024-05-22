import random
from datetime import datetime
from uuid import uuid4

import simpy

from src.base.dimensions import Dimensions
from src.client.client import Client
from src.driver.capacity import Capacity
from src.driver.driver import Driver
from src.order.order import Order
from src.restaurant.restaurant import Restaurant

NUM_RESTAURANTS = 3
NUM_DRIVERS = 5
NUM_CLIENTS = 8
SIMULATION_TIME = 40


def generate_orders(env, clients: [Client], restaurants: [Restaurant], drivers: [Driver]):
    cliente_id = 0
    while True:
        client = random.choice(clients)
        restaurant = random.choice(restaurants)
        driver = random.choice(drivers)

        order = Order(str(uuid4()), client, restaurant, datetime.now(), [])

        env.process(client.make_a_request(order, restaurant))

        env.process(restaurant.receive_order(order))

        env.process(driver.deliver_order(order))

        cliente_id += 1
        yield env.timeout(random.expovariate(1.0 / 2))  # novo pedido a cada ~2 minutos


def main():
    env = simpy.Environment()
    clients = [Client(env, f"Client {i}", ()) for i in range(NUM_CLIENTS)]
    restaurants = [Restaurant(env, f"Restaurant {i}", (), True) for i in range(NUM_RESTAURANTS)]
    capacity = Capacity(Dimensions(1, 1, 1, 1))
    drivers = [Driver(env, f"Driver {i}", (), f"type_{i}", capacity) for i in range(NUM_DRIVERS)]

    env.process(generate_orders(env, clients, restaurants, drivers))
    env.run(until=SIMULATION_TIME)


if __name__ == '__main__':
    main()
