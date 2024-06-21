import math
import random


def random_point_in_radius(centroid, inf_limit, sup_limit):
    theta = random.uniform(0, 2 * math.pi)
    r = random.uniform(inf_limit, sup_limit)
    x = centroid[0] + r * math.cos(theta)
    y = centroid[1] + r * math.sin(theta)
    return round(x), round(y)


def point_in_gauss_radius(centroid, radius):
    theta = random.uniform(0, 2 * math.pi)
    r = abs(random.gauss(0, radius))
    x = centroid[0] + r * math.cos(theta)
    y = centroid[1] + r * math.sin(theta)
    return round(x), round(y)


def point_in_gauss_circle(centroid, radius, limit):
    while True:
        x, y = point_in_gauss_radius(centroid, radius)
        if 0 <= x <= limit and 0 <= y <= limit:
            return x, y


def random_point_in_circle(centroid, radius, limit):
    while True:
        x, y = random_point_in_radius(centroid, 0, radius)
        if 0 <= x <= limit and 0 <= y <= limit:
            return x, y


def random_point_outside_circle(centroid, radius, limit):
    while True:
        x, y = random_point_in_radius(centroid, radius + 1, limit)
        if 0 <= x <= limit and 0 <= y <= limit:
            return x, y
