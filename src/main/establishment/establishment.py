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
            id: Number = None,
            production_capacity: Number = float('inf'),
            use_estimate: bool = False
    ) -> None:
        
        if id is not None:
            self.establishment_id = id
        else:
            self.establishment_id = uuid.uuid4()
            
        super().__init__(environment, coordinate, available)
        self.catalog = catalog
        self.production_capacity = production_capacity
        self.use_estimate = use_estimate
        self.orders_in_preparation: int = 0
        
        self.overloaded_until = 0
        self.current_order_duration = 0
        self.order_list_duration = 0

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
        event = EstablishmentAcceptedOrder(
            order=order,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            time=self.now
        )
        self.publish_event(event)
        estimated_time = self.estimate_preparation_time(order) + self.time_check_to_start_preparation()
        self.update_overload_time(estimated_time)
        order.establishment_accepted(self.now, estimated_time, self.overloaded_until)
        self.orders_accepted.append(order)
        self.environment.add_core_event(event)

    def get_establishment_busy_time(self) -> SimTime:
        # É necessário verificar se tempo de ocupação é pelo menos o momento atual para evitar valores negativos
        self.update_overload_time()
        establishment_busy_time = self.overloaded_until - self.now
        return establishment_busy_time

    def update_overload_time(self, estimated_time = None, calledInProcessAcceptedOrders = False) -> None:
        # Se uma estimativa é passada, ela é usada para calcular o tempo de ocupação
        if estimated_time is not None:

            # Se esse método for chamado dentro do método process_accepted_orders
            if calledInProcessAcceptedOrders:

                #   Garantimos que as durações sejam atualizadas somente se o restaurante estiver vazio e com a duração 
                # do pedido atual igual a 0, pois se a duração do pedido atual é diferente de 0, significa que esse é o 
                # primeiro pedido ou o primeiro pedido depois certo tempo vazio
                if self.is_empty() and self.current_order_duration == 0:

                    if self.order_list_duration != 0:
                        self.order_list_duration -= estimated_time

                    self.current_order_duration = estimated_time

                else:
                    self.overloaded_until = max(self.overloaded_until, self.now)
                    return

            #   Se esse método for chamado fora do método process_accepted_orders só irá atualizar a duração do pedido atual 
            # caso seja o primeiro pedido ou o primeiro pedido depois certo tempo vazio
            #   Além disso a estimativa só será adicionada na duração da lista de pedidos aceitos se for chamado fora do método
            # process_accepted_orders
            else:
                if self.is_empty() and self.order_list_duration != 0:
                    self.current_order_duration = estimated_time
                else:
                    self.order_list_duration += estimated_time

            self.overloaded_until = self.now + self.current_order_duration + self.order_list_duration
        
        # Se nenhuma estimativa é passada, o tempo de sobrecarga é atualizado com o tempo atual
        else:
            self.overloaded_until = max(self.overloaded_until, self.now)

    def estimate_preparation_time(self, order) -> SimTime:
        estimated_time = self.time_estimate_to_prepare_order(order)
        event = EstimatedOrderPreparationTime(
            order=order,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            estimated_time=estimated_time,
            time=self.now
        )
        self.publish_event(event)
        if self.use_estimate:
            self.environment.add_ready_order(order, event)
        return estimated_time

    def reject_order(self, order) -> None:
        self.publish_event(EstablishmentRejectedOrder(
            order=order,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            time=self.now
        ))
        order.update_status(OrderStatus.ESTABLISHMENT_REJECTED)
        self.orders_rejected.append(order)

    def process_accepted_orders(self) -> ProcessGenerator:
        while True:
            while len(self.orders_accepted) > 0 and self.is_within_capacity():
                order = self.orders_accepted.pop(0)
                self.update_overload_time(order.estimated_time_to_prepare, True)
                self.orders_in_preparation += 1 # TODO: O Motorista sai para buscar o pedido antes de entrar em preparação porque o pedido foi aceito antes de ser preparado
                self.process(self.prepare_order(order))
            yield self.timeout(self.time_check_to_start_preparation()) # TODO: Mostrar isso ao Julio

    def prepare_order(self, order) -> ProcessGenerator:
        self.publish_event(EstablishmentPreparingOrder(
            order=order,
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
            order=order,
            customer_id=order.customer.customer_id,
            establishment_id=self.establishment_id,
            time=self.now
        )
        self.publish_event(event)
        order.update_status(OrderStatus.READY)
        self.orders_in_preparation -= 1
        self.current_order_duration = 0
        print(f"\nPedido pronto no estabelecimento {self.establishment_id}: ")
        print(order)
        if not self.use_estimate:
            self.environment.add_ready_order(order, event)

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
        if (len(self.orders_accepted) == 0):
            return 0
        next_order = self.orders_accepted[0]
        return next_order.estimated_time_to_ready - next_order.time_preparation_started
