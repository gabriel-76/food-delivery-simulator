import math
import random
from typing import Tuple

from src.main.models.common.types import Number, Coordinate


def random_point_in_radius(centroid: Coordinate, inf_limit: Number, sup_limit: Number) -> Tuple[Number, Number]:
    theta = random.uniform(0, 2 * math.pi)
    r = random.uniform(inf_limit, sup_limit)
    x = centroid[0] + r * math.cos(theta)
    y = centroid[1] + r * math.sin(theta)
    return x, y


def point_in_gauss_radius(centroid: Coordinate, radius: Number) -> Tuple[Number, Number]:
    theta = random.uniform(0, 2 * math.pi)
    r = abs(random.gauss(0, radius))
    x = centroid[0] + r * math.cos(theta)
    y = centroid[1] + r * math.sin(theta)
    return x, y


def point_in_gauss_circle(centroid: Coordinate, radius: Number, inf_limit: Number, sup_limit: Number) -> Tuple[Number, Number]:
    while True:
        x, y = point_in_gauss_radius(centroid, radius)
        if inf_limit <= x <= sup_limit and inf_limit <= y <= sup_limit:
            return x, y


def random_point_in_circle(centroid: Coordinate,  radius: Number, inf_limit: Number, sup_limit: Number) -> Tuple[Number, Number]:
    while True:
        x, y = random_point_in_radius(centroid, 0, radius)
        if inf_limit <= x <= sup_limit and inf_limit <= y <= sup_limit:
            return x, y


def random_point_outside_circle(centroid, radius, limit):
    while True:
        x, y = random_point_in_radius(centroid, radius + 1, limit)
        if 0 <= x <= limit and 0 <= y <= limit:
            return x, y
