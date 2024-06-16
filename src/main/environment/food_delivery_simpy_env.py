from typing import Optional, Union

from simpy import Environment, Event, FilterStore
from simpy.core import SimTime

from src.main.environment.food_delivery_state import FoodDeliveryState
from src.main.map.map import Map
from src.main.view.food_delivery_view import FoodDeliveryView


class FoodDeliverySimpyEnv(Environment):
    def __init__(self, map: Map, generators, optimizer, view: FoodDeliveryView = None):
        super().__init__()
        self.map = map
        self.generators = generators
        self.optimizer = optimizer

        self.state = FoodDeliveryState()
        self.events = []
        self.view = view

        # Orders ready for collection
        self.ready_orders = FilterStore(self)
        # Order deliveries rejected by driver
        self.rejected_deliveries = FilterStore(self)
        # Order preparation estimate
        self.estimated_orders = FilterStore(self)

        self.init()

    def add_clients(self, clients):
        self.state.add_clients(clients)

    def add_restaurants(self, restaurants):
        self.state.add_restaurants(restaurants)

    def add_drivers(self, drivers):
        self.state.add_drivers(drivers)

    def available_drivers(self, trip):
        return [driver for driver in self.state.drivers if driver.check_availability(trip)]

    def add_ready_order(self, order):
        self.ready_orders.put(order)

    def get_ready_orders(self):
        read_orders = []
        while len(self.ready_orders.items) > 0:
            order = yield self.ready_orders.get()
            read_orders.append(order)
        return read_orders

    def count_ready_orders(self):
        return len(self.ready_orders.items)

    def add_rejected_delivery(self, order):
        self.rejected_deliveries.put(order)

    def get_rejected_deliveries(self):
        rejected_orders = []
        while len(self.rejected_deliveries.items) > 0:
            order = yield self.rejected_deliveries.get()
            rejected_orders.append(order)
        return rejected_orders

    def add_estimated_order(self, order):
        self.estimated_orders.put(order)

    def get_estimated_orders(self):
        estimated_orders = []
        while len(self.estimated_orders.items) > 0:
            order = yield self.estimated_orders.get()
            estimated_orders.append(order)
        return estimated_orders

    def add_event(self, event):
        self.events.append(event)

    def init(self):
        for generator in self.generators:
            self.process(generator.generate(self))

        if self.optimizer:
            self.process(self.optimizer.generate(self))

    def log_events(self):
        for event in self.events:
            print(event)

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

    def render(self):
        if self.view is not None and not self.view.quited:
            self.view.render(self)

    def close(self):
        if self.view is not None and not self.view.quited:
            self.view.quit()
