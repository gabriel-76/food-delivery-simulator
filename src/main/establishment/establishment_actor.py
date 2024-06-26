import random
from typing import List

from simpy.core import SimTime
from simpy.events import ProcessGenerator

from src.main.actors.map_actor import MapActor
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.establishment.establishment import Establishment
from src.main.events.establishment_accepted_order import EstablishmentAcceptedOrder
from src.main.events.establishment_finished_order import EstablishmentFinishedOrder
from src.main.events.establishment_preparing_order import EstablishmentPreparingOrder
from src.main.events.establishment_rejected_order import EstablishmentRejectedOrder
from src.main.events.estimated_order_preparation_time import EstimatedOrderPreparationTime
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus


class EstablishmentActor(MapActor):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            establishment: Establishment
    ) -> None:
        self.establishment_id = establishment.establishment_id
        super().__init__(environment, establishment.coordinate, establishment.available)
        self.catalog = establishment.catalog
        self.production_capacity = establishment.production_capacity
        self.use_estimate = establishment.use_estimate
        self.orders_in_preparation: int = 0
        self.overloaded_until: SimTime = int(self.now)

        self.order_requests: List[Order] = []
        self.orders_accepted: List[Order] = []
        self.orders_rejected: List[Order] = []

        self.process(self.process_order_requests())
        self.process(self.process_accepted_orders())

    def receive_order_requests(self, orders: List[Order]) -> None:
        self.order_requests += orders

    def process_order_requests(self) -> ProcessGenerator:
        while True:
            while len(self.order_requests) > 0:
                order = self.order_requests.pop(0)
                self.process(self.process_order_request(order))
            yield self.timeout(self.time_to_process_order_requests())

    def process_order_request(self, order) -> ProcessGenerator:
        yield self.timeout(self.time_to_accept_or_reject_order(order))
        accept = self.condition_to_accept(order)
        self.accept_order(order) if accept else self.reject_order(order)

    def accept_order(self, order) -> None:
        self.publish_event(EstablishmentAcceptedOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            time=self.now
        ))
        estimated_time = self.estimate_preparation_time(order)
        order.establishment_accepted(self.now + estimated_time)
        self.update_overload_time(estimated_time)
        self.orders_accepted.append(order)

    def update_overload_time(self, estimated_time) -> None:
        env_now = self.now
        if self.is_empty():
            self.overloaded_until = max(self.overloaded_until - env_now, env_now)
        elif self.is_within_capacity():
            self.overloaded_until = env_now + max(self.overloaded_until - env_now, estimated_time)
        else:
            batch_size = len(self.orders_accepted) // self.production_capacity
            self.overloaded_until = env_now + max(self.overloaded_until - env_now, batch_size * estimated_time)

        # print(f"{self.now} "
        #       f"full_until_time = {self.full_until_time} "
        #       f"orders_in_preparation = {self.orders_in_preparation} "
        #       f"order_waiting = {len(self.confirmed_orders.items)} ")

    def estimate_preparation_time(self, order) -> SimTime:
        estimated_time = self.time_estimate_to_prepare_order(order)
        self.publish_event(EstimatedOrderPreparationTime(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            estimated_time=self.time_estimate_to_prepare_order(order),
            time=self.now
        ))
        if self.use_estimate:
            self.environment.add_ready_order(order)
        return estimated_time

    def reject_order(self, order) -> None:
        self.publish_event(EstablishmentRejectedOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            time=self.now
        ))
        order.update_status(OrderStatus.ESTABLISHMENT_REJECTED)
        self.orders_rejected.append(order)

    def process_accepted_orders(self) -> ProcessGenerator:
        while True:
            while len(self.orders_accepted) > 0 and self.is_within_capacity():
                self.orders_in_preparation += 1
                order = self.orders_accepted.pop(0)
                self.process(self.prepare_order(order))
            yield self.timeout(self.time_check_to_start_preparation())

    def prepare_order(self, order) -> ProcessGenerator:
        self.publish_event(EstablishmentPreparingOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            time=self.now
        ))
        order.update_status(OrderStatus.PREPARING)
        time_to_prepare = self.time_to_prepare_order(order)
        order.time_it_was_ready = self.now + time_to_prepare
        yield self.timeout(time_to_prepare)
        self.finish_order(order)

    def finish_order(self, order) -> None:
        self.publish_event(EstablishmentFinishedOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            time=self.now
        ))
        order.update_status(OrderStatus.READY)
        self.orders_in_preparation -= 1
        if not self.use_estimate:
            self.environment.add_ready_order(order)
        self.update_overload_time(0)

    def is_empty(self) -> bool:
        return self.orders_in_preparation == 0

    def is_within_capacity(self) -> bool:
        return self.orders_in_preparation < self.production_capacity

    def is_full(self) -> bool:
        return self.orders_in_preparation >= self.production_capacity

    def time_to_process_order_requests(self) -> SimTime:
        return random.randrange(1, 5)

    def time_to_accept_or_reject_order(self, order: Order) -> SimTime:
        return random.randrange(1, 5)

    def time_check_to_start_preparation(self) -> SimTime:
        return random.randrange(1, 5)

    def time_to_prepare_order(self, order) -> SimTime:
        return random.randrange(8, 20)

    def time_estimate_to_prepare_order(self, order) -> SimTime:
        return self.time_to_prepare_order(order) + random.randrange(-5, 5)

    def condition_to_accept(self, order) -> bool:
        return self.available
