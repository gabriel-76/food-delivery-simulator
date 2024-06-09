import simpy

from src.main.environment.food_delivery_state import FoodDeliveryState
from src.main.map.map import Map


class FoodDeliveryEnvironment(simpy.Environment):
    def __init__(self, map: Map, generators, optimizer):
        super().__init__()
        self.map = map
        self.state = FoodDeliveryState()
        self.events = []

        # Orders ready for collection
        self.ready_orders = simpy.FilterStore(self)
        # Order deliveries rejected by driver
        self.rejected_deliveries = simpy.FilterStore(self)

        self.generators = generators
        self.optimizer = optimizer
        self.init()

    def add_clients(self, clients):
        self.state.add_clients(clients)

    def add_restaurants(self, restaurants):
        self.state.add_restaurants(restaurants)

    def add_drivers(self, drivers):
        self.state.add_drivers(drivers)

    def add_ready_order(self, order):
        self.ready_orders.put(order)

    def get_ready_order(self):
        return self.ready_orders.get()

    def count_ready_orders(self):
        return len(self.ready_orders.items)

    def add_rejected_delivery(self, order):
        self.rejected_deliveries.put(order)

    def get_rejected_deliveries(self):
        return self.rejected_deliveries.get()

    def count_rejected_deliveries(self):
        return len(self.rejected_deliveries.items)

    def add_event(self, event):
        self.events.append(event)

    def init(self):
        for generator in self.generators:
            self.process(generator.generate(self))

        if self.optimizer:
            self.process(self.optimizer.optimize(self))
