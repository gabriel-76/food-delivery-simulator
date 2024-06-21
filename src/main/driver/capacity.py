from src.main.base.dimensions import Dimensions


class Capacity:
    def __init__(self, dimensions: Dimensions) -> None:
        self.dimensions = dimensions

    def fits(self, dimensions: Dimensions) -> bool:
        return self.dimensions > dimensions

