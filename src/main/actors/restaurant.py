import random
import uuid
from typing import List

from src.main.actors.map_actor import MapActor
from src.main.base.types import Coordinates
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.estimated_order_preparation_time import EstimatedOrderPreparationTime
from src.main.events.restaurant_accepted_order import RestaurantAcceptedOrder
from src.main.events.restaurant_finished_order import RestaurantFinishedOrder
from src.main.events.restaurant_preparing_order import RestaurantPreparingOrder
from src.main.events.restaurant_rejected_order import RestaurantRejectedOrder
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus
from src.main.restaurant.catalog import Catalog


class Restaurant(MapActor):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            coordinates: Coordinates,
            available: bool,
            catalog: Catalog,
            order_production_capacity=float('inf')
    ):
        self.restaurant_id = uuid.uuid4()
        super().__init__(environment, coordinates, available)
        self.catalog = catalog
        self.order_production_capacity = order_production_capacity
        self.orders_in_preparation = 0
        self.overloaded_until = int(self.now)

        self.order_requests: List[Order] = []
        self.orders_accepted: List[Order] = []
        self.rejected_orders: List[Order] = []

        self.process(self.process_orders())
        self.process(self.prepare_orders())

    def receive_order_requests(self, orders):
        self.order_requests += orders

    def process_orders(self):
        while True:
            while len(self.order_requests) > 0:
                order = self.order_requests.pop(0)
                self.process(self.process_order(order))
            yield self.timeout(self.time_process_orders())

    def process_order(self, order):
        yield self.timeout(self.time_to_accept_or_reject_order(order))
        if self.accept_order_condition(order):
            self.accept_order(order)
        else:
            self.reject_order(order)

    def accept_order(self, order):
        self.publish_event(RestaurantAcceptedOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=self.restaurant_id,
            time=self.now
        ))
        estimated_time = self.estimate_preparation_time(order)
        order.restaurant_accepted(self.now + estimated_time)
        self.update_overload_time(estimated_time)
        self.orders_accepted.append(order)

    def update_overload_time(self, estimated_time):
        env_now = self.now
        if self.orders_in_preparation == 0:
            self.overloaded_until = max(self.overloaded_until - env_now, env_now)
        elif self.orders_in_preparation < self.order_production_capacity:
            self.overloaded_until = env_now + max(self.overloaded_until - env_now, estimated_time)
        else:
            batch_size = len(self.orders_accepted) // self.order_production_capacity
            self.overloaded_until = env_now + max(self.overloaded_until - env_now, batch_size * estimated_time)

        # print(f"{self.now} "
        #       f"full_until_time = {self.full_until_time} "
        #       f"orders_in_preparation = {self.orders_in_preparation} "
        #       f"order_waiting = {len(self.confirmed_orders.items)} ")

    def estimate_preparation_time(self, order):
        estimated_time = self.time_estimate_to_prepare_order(order)
        self.publish_event(EstimatedOrderPreparationTime(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=self.restaurant_id,
            estimated_time=self.time_estimate_to_prepare_order(order),
            time=self.now
        ))
        self.environment.add_estimated_order(order)
        return estimated_time

    def reject_order(self, order):
        self.publish_event(RestaurantRejectedOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=self.restaurant_id,
            time=self.now
        ))
        order.update_status(OrderStatus.RESTAURANT_REJECTED)
        self.rejected_orders.append(order)

    def prepare_orders(self):
        while True:
            while len(self.orders_accepted) > 0 and self.orders_in_preparation < self.order_production_capacity:
                self.orders_in_preparation += 1
                order = self.orders_accepted.pop(0)
                self.process(self.prepare_order(order))
            yield self.timeout(self.time_check_orders_ready_for_preparation())

    def prepare_order(self, order):
        self.publish_event(RestaurantPreparingOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=self.restaurant_id,
            time=self.now
        ))
        order.update_status(OrderStatus.PREPARING)
        time_to_prepare = self.time_to_prepare_order(order)
        order.time_it_was_ready = self.now + time_to_prepare
        yield self.timeout(time_to_prepare)
        self.finish_order(order)

    def finish_order(self, order):
        self.publish_event(RestaurantFinishedOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=self.restaurant_id,
            time=self.now
        ))
        order.update_status(OrderStatus.READY)
        self.orders_in_preparation -= 1
        self.environment.add_ready_order(order)
        self.update_overload_time(0)

    def time_process_orders(self):
        return random.randrange(1, 5)

    def time_check_orders_ready_for_preparation(self):
        return random.randrange(1, 5)

    def time_to_accept_or_reject_order(self, order: Order):
        return random.randrange(1, 5)

    def time_to_prepare_order(self, order):
        return random.randrange(8, 20)

    def time_estimate_to_prepare_order(self, order):
        return self.time_to_prepare_order(order) + random.randrange(-5, 5)

    def accept_order_condition(self, order):
        return self.available
