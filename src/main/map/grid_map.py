import math
import random

from src.main.map.map import Map


class GridMap(Map):
    def __init__(self, length):
        self.length = length

    def distance(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def estimated_time(self, coord1, coord2, rate):
        return round(self.distance(coord1, coord2) / rate)

    def random_point(self):
        return random.randrange(self.length), random.randrange(self.length)

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

    def random_point_in_radius(self, centroid, inf_limit, sup_limit):
        # Gere um ângulo aleatório entre 0 e 2π
        theta = random.uniform(0, 2 * math.pi)

        # Gere um raio aleatório, entre os limites
        r = random.uniform(inf_limit, sup_limit)

        # Converta as coordenadas polares para coordenadas cartesianas
        x = centroid[0] + r * math.cos(theta)
        y = centroid[1] + r * math.sin(theta)

        return round(x), round(y)


    def random_point_in_radius_gauss(self, centroid, radius):
        # Generate a random angle between 0 and 2π
        theta = random.uniform(0, 2 * math.pi)

        # Generate a random radius in the normal distribution
        r = abs(random.gauss(0, radius))

        # Convert polar coordinates to Cartesian coordinates
        x = centroid[0] + r * math.cos(theta)
        y = centroid[1] + r * math.sin(theta)

        return round(x), round(y)

    def random_point_in_circle(self, centroid, radius):
        while True:
            x, y = self.random_point_in_radius(centroid, 0, radius)
            if 0 <= x <= self.length and 0 <= y <= self.length:
                return x, y

    def random_point_outside_circle(self, centroid, radius):
        while True:
            x, y = self.random_point_in_radius(centroid, radius + 1, self.length)
            if 0 <= x <= self.length and 0 <= y <= self.length:
                return x, y
