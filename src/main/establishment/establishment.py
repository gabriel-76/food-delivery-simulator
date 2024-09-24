import random
import uuid
from typing import List

from simpy.core import SimTime
from simpy.events import ProcessGenerator

from src.main.actors.map_actor import MapActor
from src.main.base.types import Coordinate, Number
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.estimated_order_preparation_time import EstimatedOrderPreparationTime
from src.main.events.establishment_accepted_order import EstablishmentAcceptedOrder
from src.main.events.establishment_finished_order import EstablishmentFinishedOrder
from src.main.events.establishment_preparing_order import EstablishmentPreparingOrder
from src.main.events.establishment_rejected_order import EstablishmentRejectedOrder
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus
from src.main.establishment.catalog import Catalog


class Establishment(MapActor):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            coordinate: Coordinate,
            available: bool,
            catalog: Catalog,
            production_capacity: Number = float('inf'),
            use_estimate: bool = False
    ) -> None:
        self.establishment_id = uuid.uuid4()
        super().__init__(environment, coordinate, available)
        self.catalog = catalog
        self.production_capacity = production_capacity
        self.use_estimate = use_estimate
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
        #   Se o restaurante está vazio, ele ajusta o tempo de sobrecarga para ser pelo menos o tempo atual, pois o restaurante 
        # não está mais processando pedidos.
        if self.is_empty():
            self.overloaded_until = max(self.overloaded_until - env_now, env_now)
        #   Se o restaurante está dentro de sua capacidade, o tempo de sobrecarga é ajustado com base no tempo de preparação do 
        # pedido atual.
        elif self.is_within_capacity():
            # Atualiza self.overloaded_until para refletir o tempo atual mais o tempo necessário para processar o pedido.
            self.overloaded_until = env_now + max(self.overloaded_until - env_now, estimated_time)
        else:
            batch_size = len(self.orders_accepted) // self.production_capacity
            #   Atualiza o tempo de sobrecarga, considerando o número de lotes a serem processados. Multiplica-se o tempo estimado 
            # de preparação pelo tamanho do lote para garantir que a sobrecarga reflita a carga adicional de pedidos.
            self.overloaded_until = env_now + max(self.overloaded_until - env_now, batch_size * estimated_time)

        # print(f"{self.now} "
        #       f"full_until_time = {self.full_until_time} "
        #       f"orders_in_preparation = {self.orders_in_preparation} "
        #       f"order_waiting = {len(self.confirmed_orders.items)} ")

    def estimate_preparation_time(self, order) -> SimTime:
        estimated_time = self.time_estimate_to_prepare_order(order)
        event = EstimatedOrderPreparationTime(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            estimated_time=estimated_time,
            time=self.now
        )
        self.publish_event(event)
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
        event = EstablishmentFinishedOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            time=self.now
        )
        self.publish_event(event)
        order.update_status(OrderStatus.READY)
        self.orders_in_preparation -= 1
        if not self.use_estimate:
            self.environment.add_ready_order(order, event)
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
    
    def estimate_time_to_next_order_ready(self) -> SimTime:
        next_order = self.orders_accepted[0]
        return (self.now - next_order.time_preparation_started) + next_order.estimated_time_to_ready 
