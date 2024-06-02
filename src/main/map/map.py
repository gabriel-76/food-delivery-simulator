import random

from src.main.driver.driver import Driver
from src.main.order.order import Order


class Map:
    def __init__(self, length):
        self.length = length

    def distance(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def collection_distance(self, order: Order, driver: Driver):
        return self.distance(driver.coordinates, order.restaurant.coordinates,)

    def delivery_distance(self, order: Order):
        return self.distance(order.restaurant.coordinates, order.client.coordinates)

    def total_distance(self, order: Order, driver: Driver):
        return self.collection_distance(order, driver) + self.delivery_distance(order)

    def estimated_time(self, coord1, coord2, rate):
        return round(self.distance(coord1, coord2) / rate)

    def random_point(self):
        return random.randrange(self.length), random.randrange(self.length)
