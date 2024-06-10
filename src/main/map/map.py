import math
import random
from abc import ABC, abstractmethod


class Map(ABC):

    @abstractmethod
    def distance(self, coord1, coord2): pass

    @abstractmethod
    def estimated_time(self, coord1, coord2, rate): pass

    @abstractmethod
    def random_point(self): pass

    @abstractmethod
    def move(self, origin, destination, rate): pass