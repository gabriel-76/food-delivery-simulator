import simpy

from src.main.environment.food_delivery_state import FoodDeliveryState
from src.main.map.map import Map


class FoodDeliveryEnvironment(simpy.Environment):
    def __init__(self, map: Map, generators, optimizer):
        super().__init__()
        self.map = map
        self.state = FoodDeliveryState()
        self.events = simpy.Store(self)
        # Orders ready for collection
        self.ready_orders = simpy.FilterStore(self)
        # Order deliveries rejected by driver
        self.rejected_delivery_orders = simpy.FilterStore(self)
        # Orders delivered by drivers
        self.delivered_orders = simpy.Store(self)

        self.generators = generators
        self.optimizer = optimizer
        self.init()

    def add_clients(self, clients):
        self.state.clients += clients

    def add_restaurants(self, restaurants):
        self.state.restaurants += restaurants

    def add_drivers(self, drivers):
        self.state.drivers += drivers

    def add_ready_order(self, order):
        self.ready_orders.put(order)

    def get_ready_order(self):
        return self.ready_orders.get()

    def count_ready_orders(self):
        return len(self.ready_orders.items)

    def add_rejected_delivery_order(self, order):
        self.rejected_delivery_orders.put(order)

    def get_rejected_delivery_order(self):
        return self.rejected_delivery_orders.get()

    def count_rejected_delivery_orders(self):
        return len(self.rejected_delivery_orders.items)

    def add_delivered_order(self, order):
        self.delivered_orders.put(order)

    def get_delivered_order(self):
        self.delivered_orders.get()

    def count_delivered_orders(self):
        return len(self.delivered_orders.items)

    def add_event(self, event):
        self.events.put(event)

    def get_event(self):
        return self.events.get()

    def count_event(self):
        return len(self.events.items)

    def init(self):
        for generator in self.generators:
            self.process(generator.generate(self))

        if self.optimizer:
            self.process(self.optimizer.optimize(self))

    # def run(self, *args, **kwargs):
    #     super().run(*args, **kwargs)
