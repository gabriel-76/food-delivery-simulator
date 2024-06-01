import random
import uuid

import simpy

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.events.estimated_order_preparation_time import EstimatedOrderPreparationTime
from src.main.events.restaurant_accepted_order import RestaurantAcceptedOrder
from src.main.events.restaurant_finished_order import RestaurantFinishedOrder
from src.main.events.restaurant_preparing_order import RestaurantPreparingOrder
from src.main.events.restaurant_rejected_order import RestaurantRejectedOrder
from src.main.order.order import Order
from src.main.restaurant.catalog import Catalog


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
            yield self.environment.timeout(self.time_process_orders())

    def process_order(self, order):
        yield self.environment.timeout(self.time_to_accept_or_reject_order(order))
        if self.accept_order_condition(order):
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
        self.estimate_preparation_time(order)
        self.confirmed_orders.put(order)

    def estimate_preparation_time(self, order):
        event = EstimatedOrderPreparationTime(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=self.restaurant_id,
            estimated_time=self.time_to_prepare_order(order) + random.randrange(-5, 5),
            time=self.environment.now
        )
        self.environment.add_event(event)


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
            yield self.environment.timeout(self.time_check_orders_ready_for_preparation())

    def prepare_order(self, order):
        event = RestaurantPreparingOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=self.restaurant_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(self.time_to_prepare_order(order))
        self.finish_order(order)

    def finish_order(self, order):
        event = RestaurantFinishedOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=self.restaurant_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        self.environment.add_ready_order(order)

    def time_process_orders(self):
        return random.randrange(1, 5)

    def time_check_orders_ready_for_preparation(self):
        return random.randrange(1, 5)

    def time_to_accept_or_reject_order(self, order: Order):
        return random.randrange(1, 5)

    def time_to_prepare_order(self, order):
        return random.randrange(8, 20)

    def accept_order_condition(self, order):
        return self.available
