import random


class Map:
    def __init__(self, length):
        self.length = length

    def distance(self, coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def estimated_time(self, coord1, coord2, rate):
        return round(self.distance(coord1, coord2) / rate)

    def random_point(self):
        return random.randrange(self.length), random.randrange(self.length)
