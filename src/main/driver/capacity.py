from src.main.base.dimensions import Dimensions


class Capacity:
    def __init__(self, dimensions: Dimensions):
        self.dimensions = dimensions

    def fits(self, dimensions: Dimensions):
        return self.dimensions > dimensions

