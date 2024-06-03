import math
import random


class Map:
    def __init__(self, length):
        self.length = length

    def distance(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def collection_distance(self, order, driver):
        return self.distance(driver.coordinates, order.restaurant.coordinates)

    def delivery_distance(self, order):
        return self.distance(order.restaurant.coordinates, order.client.coordinates)

    def total_distance(self, order, driver):
        return self.collection_distance(order, driver) + self.delivery_distance(order)

    def estimated_time(self, coord1, coord2, rate):
        return round(self.distance(coord1, coord2) / rate)

    def random_point(self):
        return random.randrange(self.length), random.randrange(self.length)

    def random_point_in_radius(self, coordinates, inf_limit, sup_limit):
        # Gere um ângulo aleatório entre 0 e 2π
        theta = random.uniform(0, 2 * math.pi)

        # Gere um raio aleatório, entre os limites
        r = random.uniform(inf_limit, sup_limit)

        # Converta as coordenadas polares para coordenadas cartesianas
        x = coordinates[0] + r * math.cos(theta)
        y = coordinates[1] + r * math.sin(theta)

        return round(x), round(y)

    def random_point_in_circle(self, coordinates, radius):
        while True:
            # print("Gerando ponto no circulo")
            x, y = self.random_point_in_radius(coordinates, 0, radius)
            if 0 <= x <= self.length and 0 <= y <= self.length:
                # print(f"Ponto no circulo gerado {x, y}")
                return x, y

    def random_point_outside_circle(self, coordinates, radius):
        while True:
            # print("Gerando ponto fora do circulo")
            x, y = self.random_point_in_radius(coordinates, radius + 1, self.length)
            if 0 <= x <= self.length and 0 <= y <= self.length:
                # print(f"Ponto no fora do circulo gerado {x, y}")
                return x, y
            # else:
            #     print(f"Ponto no fora do circulo gerado {x, y} fora do limite")
