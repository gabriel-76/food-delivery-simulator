import math
import random

from src.main.map.map import Map


class GridMap(Map):
    def __init__(self, size):
        super().__init__(size)

    def distance(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def estimated_time(self, coord1, coord2, rate):
        return round(self.distance(coord1, coord2) / rate)

    def random_point(self):
        return random.randrange(self.size), random.randrange(self.size)

    def move(self, origin, destination, rate):

        x, y = origin
        dest_x, dest_y = destination
        rate = round(rate)

        if x < dest_x:
            x += min(rate, dest_x - x)
        elif x > dest_x:
            x -= min(rate, x - dest_x)

        if y < dest_y:
            y += min(rate, dest_y - y)
        elif y > dest_y:
            y -= min(rate, y - dest_y)

        return x, y
