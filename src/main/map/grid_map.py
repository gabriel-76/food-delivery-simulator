import random
from typing import List

from src.main.commons.types import Coordinate, Number
from src.main.map.map import Map


class GridMap(Map):
    def __init__(self, size):
        super().__init__(size)
        self.generated_points = {}

    def distance(self, coord1: Coordinate, coord2: Coordinate) -> Number:
        return max(abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1]), 1)

    def acc_distance(self, coordinates: List[Coordinate]) -> Number:
        distance = 0
        if len(coordinates) <= 1:
            return distance

        previous_coordinate = coordinates[0]
        for coordinate in coordinates[1:]:
            distance += self.distance(previous_coordinate, coordinate)
            previous_coordinate = coordinate

        return distance

    def estimated_time(self, coord1: Coordinate, coord2: Coordinate, rate: Number) -> Number:
        return round(self.distance(coord1, coord2) / rate)

    def random_point(self, not_repeated=False) -> Coordinate:
        point = random.randrange(self.size), random.randrange(self.size)
        if not_repeated:
            while point in self.generated_points:
                point = random.randrange(self.size), random.randrange(self.size)
            self.generated_points[point] = True
        return point

    def move(self, origin: Coordinate, destination: Coordinate, rate: Number) -> Coordinate:

        x, y = origin
        dest_x, dest_y = destination
        # rate = round(rate)

        if x < dest_x:
            x += min(rate, dest_x - x)
        elif x > dest_x:
            x -= min(rate, x - dest_x)

        if y < dest_y:
            y += min(rate, dest_y - y)
        elif y > dest_y:
            y -= min(rate, y - dest_y)

        return x, y
