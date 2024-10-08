from typing import List, Optional, Union

import numpy as np
import random
from simpy import Environment, Event
from simpy.core import SimTime

from src.main.environment.delivery_env_state import DeliveryEnvState
from src.main.map.map import Map
from src.main.order.delivery_rejection import DeliveryRejection
from src.main.view.food_delivery_view import FoodDeliveryView


class FoodDeliverySimpyEnv(Environment):
    def __init__(self, map: Map, generators, optimizer, view: FoodDeliveryView = None):
        super().__init__()
        self.map = map
        self.generators = generators
        self.optimizer = optimizer
        self.view = view
        self._state = DeliveryEnvState()
        self.init()

        self.core_events: List[Event] = []

    def add_core_event(self, event):
        self.core_events.append(event)
    
    def dequeue_core_event(self):
        if self.core_events:
            return self.core_events.pop(0)
        else:
            return None
    
    def clear_core_events(self):
        self.core_events.clear()

    @property
    def events(self):
        return self._state.events

    @property
    def state(self):
        return self._state

    def add_customers(self, customers):
        self._state.add_customers(customers)

    def add_establishments(self, establishments):
        self._state.add_establishments(establishments)

    def add_drivers(self, drivers):
        self._state.add_drivers(drivers)

    def available_drivers(self, route):
        return [driver for driver in self._state.drivers if driver.check_availability(route)]

    def add_ready_order(self, order, event):
        self._state.orders_awaiting_delivery.append(order)
        self.add_core_event(event)

    def get_ready_orders(self):
        read_orders = []
        while len(self._state.orders_awaiting_delivery) > 0:
            read_orders = self._state.orders_awaiting_delivery
            self._state.orders_awaiting_delivery = []
        return read_orders

    def count_ready_orders(self):
        return len(self._state.orders_awaiting_delivery)

    def add_rejected_delivery(self, order, delivery_rejection: DeliveryRejection, event):
        order.add_delivery_rejection(delivery_rejection)
        self._state.orders_awaiting_delivery.append(order)
        self.add_core_event(event)

    def get_rejected_deliveries(self):
        rejected_orders = []
        while len(self._state.rejected_deliveries) > 0:
            rejected_orders = self._state.rejected_deliveries
            self._state.rejected_deliveries = []
        return rejected_orders

    def add_event(self, event):
        self._state.add_event(event)

    def init(self):
        for generator in self.generators:
            self.process(generator.generate(self))

        if self.optimizer:
            self.process(self.optimizer.generate(self))

    def log_events(self):
        self._state.log_events()

    def run(self, until: Optional[Union[SimTime, Event]] = None, render_mode=None):
        if render_mode == "human" and self.view is not None:
            if not isinstance(until, Event):
                until = until if isinstance(until, int) else float(until)
                while self.now < until and not self.view.quited:
                    self.view.render(self)
                    super().run(until=self.now + 1)
                if self.view.quited:
                    self.view.quit()
        else:
            super().run(until=until)

        if self.view is not None and self.view.quited:
            self.view.quit()

    def step(self, render_mode=None):
        super().step()
        if render_mode == "human" and self.view is not None:
            self.view.render(self)
            if self.view.quited:
                self.view.quit()

    def render(self):
        if self.view is not None and not self.view.quited:
            self.view.render(self)

    def close(self):
        if self.view is not None and not self.view.quited:
            self.view.quit()

    def seed(self, seed: Optional[int] = None):
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
