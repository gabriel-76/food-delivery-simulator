from typing import Optional, Union

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
        self.state = DeliveryEnvState()
        self.init()

    @property
    def events(self):
        return self.state.events

    def add_customers(self, customers):
        self.state.add_customers(customers)

    def add_establishments(self, establishments):
        self.state.add_establishments(establishments)

    def add_drivers(self, drivers):
        self.state.add_drivers(drivers)

    def available_drivers(self, route):
        return [driver for driver in self.state.drivers if driver.check_availability(route)]

    def add_ready_order(self, order):
        self.state.orders_awaiting_delivery.append(order)

    def get_ready_orders(self):
        read_orders = []
        while len(self.state.orders_awaiting_delivery) > 0:
            read_orders = self.state.orders_awaiting_delivery
            self.state.orders_awaiting_delivery = []
        return read_orders

    def count_ready_orders(self):
        return len(self.state.orders_awaiting_delivery)

    def add_rejected_delivery(self, order, delivery_rejection: DeliveryRejection):
        order.add_delivery_rejection(delivery_rejection)
        self.state.orders_awaiting_delivery.append(order)

    def get_rejected_deliveries(self):
        rejected_orders = []
        while len(self.state.rejected_deliveries) > 0:
            rejected_orders = self.state.rejected_deliveries
            self.state.rejected_deliveries = []
        return rejected_orders

    def add_event(self, event):
        self.state.add_event(event)

    def init(self):
        for generator in self.generators:
            self.process(generator.generate(self))

        if self.optimizer:
            self.process(self.optimizer.generate(self))

    def log_events(self):
        self.state.log_events()

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
