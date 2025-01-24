from abc import ABC, abstractmethod
from typing import List

from src.main.driver.driver import Driver
from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.optimizer.optimizer import Optimizer
from src.main.order.order import Order
from src.main.route.delivery_route_segment import DeliveryRouteSegment
from src.main.route.pickup_route_segment import PickupRouteSegment
from src.main.route.route import Route


class OptimizerGym(Optimizer, ABC):

    def __init__(self, environment: FoodDeliveryGymEnv, seed: int | None = None):
        self.gym_env = environment
        self.seed = seed
        self.state = None
        self.done = False
        self.truncated = False

    def initialize(self):
        self.state = self.gym_env.reset(seed=self.seed)
        self.done = False
        self.truncated = False

    @abstractmethod
    def select_driver(self, drivers: List[Driver], route: Route):
        pass

    def process_order(self, order: Order):
        segment_pickup = PickupRouteSegment(order)
        segment_delivery = DeliveryRouteSegment(order)
        route = Route(self.gym_env.get_simpy_env(), [segment_pickup, segment_delivery])

        drivers = self.gym_env.get_available_drivers(route)

        driver_index = self.select_driver(drivers, route)

        if driver_index is not None:
            self.gym_env.step(driver_index)
        else:
            raise Exception("Driver not found")

    def run(self):
        self.initialize()

        while not (self.done or self.truncated):
            action = self.process_order(self.gym_env.get_last_order())
            self.state, reward, self.done, self.truncated, info = self.gym_env.step(action)
            
            print(f"State: {self.state}, Reward: {reward}, Done: {self.done}, Truncated: {self.truncated}")

        self.gym_env.show_statistcs_board()

        return {
            "final_state": self.state,
            "reward": reward,
            "done": self.done,
            "truncated": self.truncated,
            "info": info,
        }