import random
import uuid

import simpy

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.events.restaurant_accepted_order import RestaurantAcceptedOrder
from src.events.restaurant_finish_order import RestaurantFinishOrder
from src.events.restaurant_preparing_order import RestaurantPreparingOrder
from src.events.restaurant_rejected_order import RestaurantRejectedOrder
from src.restaurant.catalog import Catalog


class Restaurant:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            coordinates,
            available: bool,
            catalog: Catalog
    ):
        self.restaurant_id = uuid.uuid4()
        self.environment = environment
        self.coordinates = coordinates
        self.available = available
        self.catalog = catalog
        self.new_orders = simpy.Store(self.environment)
        self.confirmed_orders = simpy.Store(self.environment)
        self.canceled_orders = simpy.Store(self.environment)

        self.environment.process(self.process_orders())
        self.environment.process(self.prepare_orders())

    def receive_orders(self, orders):
        for order in orders:
            self.new_orders.put(order)

    def process_orders(self):
        while True:
            while len(self.new_orders.items) > 0:
                order = yield self.new_orders.get()
                self.environment.process(self.process_order(order))
            yield self.environment.timeout(2)

    def process_order(self, order):
        yield self.environment.timeout(1)
        if self.accept_order_policy(order):
            self.accept_order(order)
        else:
            self.reject_order(order)

    def accept_order(self, order):
        event = RestaurantAcceptedOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=self.restaurant_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        self.confirmed_orders.put(order)

    def reject_order(self, order):
        event = RestaurantRejectedOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=self.restaurant_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        self.canceled_orders.put(order)

    def prepare_orders(self):
        while True:
            while len(self.confirmed_orders.items) > 0:
                order = yield self.confirmed_orders.get()
                self.environment.process(self.prepare_order(order))
            yield self.environment.timeout(1)

    def prepare_order(self, order):
        orders_time_policy = self.prepare_order_time_policy(order)
        event = RestaurantPreparingOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=self.restaurant_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(orders_time_policy)
        self.finish_order(order)

    def finish_order(self, order):
        event = RestaurantFinishOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=self.restaurant_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        self.environment.add_ready_order(order)

    def prepare_order_time_policy(self, order):
        return random.randrange(1, 12)

    def accept_order_policy(self, order):
        return self.available
