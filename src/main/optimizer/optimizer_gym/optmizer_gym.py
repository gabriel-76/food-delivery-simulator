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

    def __init__(self, environment: FoodDeliveryGymEnv, save_statistics: bool = True):
        self.gym_env = environment
        self.state = None
        self.done = False
        self.truncated = False

    def initialize(self, seed: int | None = None):
        self.state, info = self.gym_env.reset(seed=seed)
        self.done = False
        self.truncated = False

    @abstractmethod
    def select_driver(self, obs: dict, drivers: List[Driver], route: Route):
        pass

    def assign_driver_to_order(self, obs: dict, order: Order):
        segment_pickup = PickupRouteSegment(order)
        segment_delivery = DeliveryRouteSegment(order)
        route = Route(self.gym_env.get_simpy_env(), [segment_pickup, segment_delivery])

        drivers = self.gym_env.get_drivers()

        return self.select_driver(obs, drivers, route)

    def run(self):
        sum = 0
        while not (self.done or self.truncated):
            action = self.assign_driver_to_order(self.state, self.gym_env.get_last_order())
            self.state, reward, self.done, self.truncated, info = self.gym_env.step(action)
            sum += reward

            print(f"State: {self.state}, Reward: {reward}, Done: {self.done}, Truncated: {self.truncated}")

        print(f"\n\n\nTotal reward: {sum}")
        print(f"Final Time  Step: {info['info']}")
        self.gym_env.show_statistcs_board()

        return {
            "final_state": self.state,
            "final_reward": reward,
            "done": self.done,
            "truncated": self.truncated,
            "sum_reward": sum,
            "info": info,
        }
    
    def show_mean_statistic_board(self):
        self.gym_env.show_total_mean_statistics_board()