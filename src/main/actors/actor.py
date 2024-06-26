from abc import ABC
from typing import Optional, Any

from simpy import Process
from simpy.core import SimTime
from simpy.events import ProcessGenerator, Timeout

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv


class Actor(ABC):

    def __init__(self, environment) -> None:
        self._environment = environment

    def publish_event(self, event) -> None:
        self._environment.add_event(event)

    def process(self, generator: ProcessGenerator) -> Process:
        return self._environment.process(generator)

    def timeout(self, delay: SimTime = 0, value: Optional[Any] = None) -> Timeout:
        return self._environment.timeout(delay=delay, value=value)

    @property
    def now(self) -> SimTime:
        return self._environment.now

    @property
    def environment(self) -> FoodDeliverySimpyEnv:
        return self._environment
