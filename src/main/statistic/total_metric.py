from collections import defaultdict

import numpy as np

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.event_type import EventType


class TotalMetric:

    def __init__(self, environment: FoodDeliverySimpyEnv):
        self.environment = environment

    def metric(self):
        print("TOTAL RESTAURANTS", len(self.environment.state.restaurants))
        print("TOTAL CLIENTS", len(self.environment.state.clients))
        print("TOTAL DRIVERS", len(self.environment.state.drivers))
        print("TOTAL ORDERS", len(self.environment.state.orders))
