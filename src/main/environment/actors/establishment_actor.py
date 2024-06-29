import random
from typing import List, Union, TYPE_CHECKING

from simpy.core import SimTime
from simpy.events import ProcessGenerator

from src.main.environment.actors.actor import Actor
from src.main.events.establishment_accepted_order import EstablishmentAcceptedOrder
from src.main.events.establishment_finished_order import EstablishmentFinishedOrder
from src.main.events.establishment_preparing_order import EstablishmentPreparingOrder
from src.main.events.establishment_rejected_order import EstablishmentRejectedOrder
from src.main.events.estimated_order_preparation_time import EstimatedOrderPreparationTime
from src.main.models.establishment.establishment import Establishment
from src.main.models.order.order import Order

if TYPE_CHECKING:
    from src.main.environment.delivery_environment import DeliveryEnvironment


class EstablishmentActor(Actor):
    def __init__(self, environment: 'DeliveryEnvironment', establishment: Establishment) -> None:
        super().__init__(environment)
        self._establishment = establishment
        self.process(self._process_requests())
        self.process(self.process_accepted())

    def request(self, orders: Union[Order, List[Order]]) -> None:
        self._establishment.request(orders)

    def _process_requests(self) -> ProcessGenerator:
        while True:
            for order in self._establishment.get_requests():
                self.process(self._process_request(order))
            yield self.timeout(self.time_to_process_requests())

    def _process_request(self, order: Order) -> ProcessGenerator:
        yield self.timeout(self.time_to_accept_or_reject(order))
        accept = self.condition_to_accept(order)
        self.accept(order) if accept else self.reject(order)

    def accept(self, order: Order) -> None:
        self.publish_event(EstablishmentAcceptedOrder(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=self._establishment.identifier,
            time=self.now
        ))
        estimated_time = self._estimate_time(order)
        self._establishment.accept(order, self.now, estimated_time)
        # TODO: Adding order in environment or filter indexes ?

    # TODO: refactor this method
    def update_overload_time(self, estimated_time) -> None:
        env_now = self.now
        # if self.is_empty():
        #     self._establishment._available_in = max(self._establishment._available_in - env_now, env_now)
        # elif self.is_within_capacity():
        #     self._establishment._available_in = env_now + max(
        #         self._establishment._available_in - env_now,
        #         estimated_time
        #     )
        # else:
        #     batch_size = len(self._establishment.orders_accepted) // self._establishment.production_capacity
        #     self._establishment._available_in = env_now + max(
        #         self._establishment._available_in - env_now,
        #         batch_size * estimated_time
        #     )

        # print(f"{self.now} "
        #       f"full_until_time = {self.full_until_time} "
        #       f"orders_in_preparation = {self.orders_in_preparation} "
        #       f"order_waiting = {len(self.confirmed_orders.items)} ")

    def _estimate_time(self, order: Order) -> SimTime:
        estimated_time = self.time_estimate_to_prepare_order(order)
        self.publish_event(EstimatedOrderPreparationTime(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=self._establishment.identifier,
            estimated_time=self.time_estimate_to_prepare_order(order),
            time=self.now
        ))
        # TODO: Adding order in environment or filter indexes ?
        # if self._establishment.use_estimate:
        #     self.environment.add_ready_order(order)
        return estimated_time

    def reject(self, order: Order) -> None:
        self.publish_event(EstablishmentRejectedOrder(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=self._establishment.identifier,
            time=self.now
        ))
        self._establishment.reject(order, self.now)

    # TODO: Refactor this method
    def process_accepted(self) -> ProcessGenerator:
        while True:
            accepted = self._establishment.get_accepted_within_capacity()
            timeout = 1
            if accepted:
                for order in accepted:
                    self.process(self._prepare(order))
                timeout = self.time_check_to_start_preparation()
            yield self.timeout(timeout)

    def _prepare(self, order) -> ProcessGenerator:
        self.publish_event(EstablishmentPreparingOrder(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=self._establishment.identifier,
            time=self.now
        ))
        time_to_prepare = self.time_to_prepare_order(order)
        # order._finished_time = self.now + time_to_prepare
        self._establishment.prepare(order, self.now)
        yield self.timeout(time_to_prepare)
        self._finish(order)

    def _finish(self, order: Order) -> None:
        self.publish_event(EstablishmentFinishedOrder(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=self._establishment.identifier,
            time=self.now
        ))
        # TODO: Adding order in environment or filter indexes ?
        # self._establishment.orders_in_preparation -= 1
        # if not self._establishment.use_estimate:
        #     self.environment.add_ready_order(order)
        self._establishment.finish(order, self.now)
        self.update_overload_time(0)

    # def is_empty(self) -> bool:
    #     return self._establishment.orders_in_preparation == 0
    #
    # def is_within_capacity(self) -> bool:
    #     return self._establishment.orders_in_preparation < self._establishment.production_capacity
    #
    # def is_full(self) -> bool:
    #     return self._establishment.orders_in_preparation >= self._establishment.production_capacity

    def time_to_process_requests(self) -> SimTime:
        return random.randrange(1, 5)

    def time_to_accept_or_reject(self, order: Order) -> SimTime:
        return random.randrange(1, 5)

    def time_check_to_start_preparation(self) -> SimTime:
        return random.randrange(1, 5)

    def time_to_prepare_order(self, order) -> SimTime:
        return random.randrange(8, 20)

    def time_estimate_to_prepare_order(self, order) -> SimTime:
        return self.time_to_prepare_order(order) + random.randrange(-5, 5)

    def condition_to_accept(self, order) -> bool:
        return self._establishment.available
