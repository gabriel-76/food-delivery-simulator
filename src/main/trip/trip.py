import uuid
from functools import reduce

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.order.order import Order
from src.main.trip.segment import Segment, SegmentType


class Trip:
    def __init__(self, environment: FoodDeliverySimpyEnv, segments: [Segment]):
        self.tripe_id = uuid.uuid4()
        self.environment = environment
        self.segments = segments
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()

    def calculate_required_capacity(self):
        dimensions = Dimensions(0, 0, 0, 0)
        for segment in self.segments:
            dimensions += segment.required_capacity
        return dimensions

    def has_next_segments(self):
        return len(self.segments) > 0

    def next_segments(self):
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()
        return self.segments.pop(0)

    def calculate_total_distance(self):
        distance = 0

        if len(self.segments) <= 1:
            return distance

        previous_segments = self.segments[0]
        for segment in self.segments[1:]:
            distance += self.environment.map.distance(previous_segments.coordinates, segment.coordinates)
            previous_segments = segment

        return distance

    def extend_trip(self, other_trip):
        self.segments += other_trip.segments
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()

    def size(self):
        return len(self.segments)
