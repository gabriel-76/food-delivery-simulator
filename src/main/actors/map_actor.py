from src.main.actors.actor import Actor
from src.main.base.types import Coordinates
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv


class MapActor(Actor):

    def __init__(self, environment: FoodDeliverySimpyEnv, coordinates: Coordinates, available: bool) -> None:
        super().__init__(environment)
        self.coordinates = coordinates
        self.available = available
