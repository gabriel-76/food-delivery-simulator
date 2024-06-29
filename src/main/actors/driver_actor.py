import random
from typing import List, TYPE_CHECKING

from simpy.events import ProcessGenerator

from src.main.actors.actor import Actor
from src.main.actors.customer_actor import CustomerActor
from src.main.models.driver.driver import Driver
from src.main.models.order.order import OrderStatus, Order
from src.main.models.order.rejection import DriverRejection
from src.main.models.route.route import Route
from src.main.events.driver_accepted_delivery import DriverAcceptedDelivery
from src.main.events.driver_accepted_route import DriverAcceptedRoute
from src.main.events.driver_arrived_delivery_location import DriverArrivedDeliveryLocation
from src.main.events.driver_delivered_order import DriverDeliveredOrder
from src.main.events.driver_delivering_order import DriverDeliveringOrder
from src.main.events.driver_picked_up_order import DriverPickedUpOrder
from src.main.events.driver_picking_up_order import DriverPickingUpOrder
from src.main.events.driver_rejected_delivery import DriverRejectedDelivery
from src.main.events.driver_rejected_route import DriverRejectedRoute
from src.main.models.route.segment import Segment

if TYPE_CHECKING:
    from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv


class DriverActor(Actor):
    def __init__(self, environment: 'FoodDeliverySimpyEnv', driver: Driver):
        super().__init__(environment)
        self._driver = driver
        self.process(self.process_requests())
        self.process(self.move())

    def request(self, route: Route) -> None:
        self._driver.request(route)

    # TODO: refactor this method
    def process_requests(self) -> ProcessGenerator:
        while True:
            timeout = 1
            route = self._driver.get_request()
            if route:
                timeout = self.time_to_accept_or_reject_route(route)
                self.process_request(route)
            yield self.timeout(timeout)

    def process_request(self, route: Route) -> None:
        accept = self.accept_route_condition(route)
        self.accept_route(route) if accept else self.reject_route(route)

    def accept_route(self, route: Route) -> None:
        self._driver.accept(route, self.now, 0)  # TODO: Calculate estimated time
        self.publish_event(DriverAcceptedRoute(
            driver_id=self._driver.identifier,
            route_id=self._driver.route.route_id,
            distance=self.environment.map.acc_distance([self._driver.coordinate] + route.coordinates),
            time=self.now
        ))
        self.accept_route_segments(route.segments)
        self.process(self.sequential_processor())

    # TODO: refactor this method
    def accept_route_segments(self, route_segments: List[Segment]) -> None:
        for route_segment in route_segments:
            self.accept_route_segment(route_segment)

    # TODO: refactor this method
    def accept_route_segment(self, segment: Segment) -> None:
        self.publish_event(DriverAcceptedDelivery(
            driver_id=self._driver.identifier,
            order_id=segment.order.identifier,
            customer_id=segment.order.customer.identifier,
            establishment_id=segment.order.establishment.identifier,
            distance=0,  # TODO: Calculate distance posteriorly
            time=self.now
        ))

    def sequential_processor(self) -> ProcessGenerator:
        if self._driver.is_waiting_to_collect():
            # print(f"Driver {self._driver.coordinate} is waiting for "
            #       f"order {self._driver.current_segment.coordinate} "
            #       f"status {self._driver.current_segment.order.status.name} "
            #       f"estimated time {self._driver.current_segment.order._estimated_preparation_at} "
            #       f"ready time {self._driver.current_segment.order._finish_preparation_at} "
            #       f"current time {self.now}")
            yield self.timeout(1)
            self.process(self.sequential_processor())
        elif self._driver.has_next():
            segment = self._driver.segment
            if segment.is_pickup():
                timeout = self.time_between_accept_and_start_picking_up(segment.order)
                yield self.timeout(timeout)
                self.process(self.picking_up(segment.order))
            if segment.is_delivery():
                timeout = self.time_between_picked_up_and_start_delivery(segment.order)
                yield self.timeout(timeout)
                self.process(self.delivering(segment.order))

    def reject_route(self, route: Route) -> None:
        self.publish_event(DriverRejectedRoute(
            driver_id=self._driver.identifier,
            route_id=self._driver.route.route_id,
            distance=self.environment.map.acc_distance([self._driver.coordinate] + route.coordinates),
            time=self.now
        ))
        self.reject_route_segments(route.segments)

    def reject_route_segments(self, route_segments: List[Segment]) -> None:
        for route_segment in route_segments:
            self.reject_route_segment(route_segment)

    # TODO: refactor this method
    def reject_route_segment(self, route_segment: Segment) -> None:
        self.publish_event(DriverRejectedDelivery(
            driver_id=self._driver.identifier,
            order_id=route_segment.order.identifier,
            customer_id=route_segment.order.customer.identifier,
            establishment_id=route_segment.order.establishment.identifier,
            time=self.now
        ))
        rejection = DriverRejection(self._driver, self.now)
        route_segment.order.reject(rejection)
        self.environment.add_rejected_delivery(route_segment.order, rejection)

    def picking_up(self, order: Order) -> ProcessGenerator:
        self._driver.picking_up(self.now, 0)  # TODO: Calculate estimated time
        # self._driver._travelled_distance += self.environment.map.distance(
        #     self._driver.coordinate, order._establishment._coordinate
        # )
        self.publish_event(DriverPickingUpOrder(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=order.establishment.identifier,
            driver_id=self._driver.identifier,
            distance=self.environment.map.distance(self._driver.coordinate, order.establishment.coordinate),
            time=self.now
        ))
        yield self.timeout(self.time_to_picking_up_order(order))
        self.picked_up(order)

    def picked_up(self, order: Order) -> None:
        self.publish_event(DriverPickedUpOrder(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=order.establishment.identifier,
            driver_id=self._driver.identifier,
            time=self.now
        ))
        self._driver.picked_up(self.now)
        self.process(self.sequential_processor())

    def delivering(self, order: Order) -> ProcessGenerator:
        self._driver.delivering(self.now)
        self._driver._travelled_distance += self.environment.map.distance(self._driver.coordinate, order.customer.coordinate)
        self.publish_event(DriverDeliveringOrder(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=order.establishment.identifier,
            driver_id=self._driver.identifier,
            distance=self.environment.map.distance(self._driver.coordinate, order.customer.coordinate),
            time=self.now
        ))
        yield self.timeout(self.time_to_deliver_order(order))
        self.process(self.wait_customer_pick_up_order(order))

    # TODO: refactor this method
    def wait_customer_pick_up_order(self, order: Order) -> ProcessGenerator:
        order._status = OrderStatus.DRIVER_ARRIVED_DELIVERY_LOCATION
        self.publish_event(DriverArrivedDeliveryLocation(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=order.establishment.identifier,
            driver_id=self._driver.identifier,
            time=self.now
        ))
        # TODO: Refactor this, find a better way to get the customer actor
        customer_actor = CustomerActor(self.environment, order.customer)
        yield self.process(customer_actor.receive(order, self._driver))
        self.delivered(order)

    def delivered(self, order: Order) -> None:
        self.publish_event(DriverDeliveredOrder(
            order_id=order.identifier,
            customer_id=order.customer.identifier,
            establishment_id=order.establishment.identifier,
            driver_id=self._driver.identifier,
            time=self.now
        ))
        self._driver.delivered(self.now)
        self.process(self.sequential_processor())

    def move(self) -> ProcessGenerator:
        while True:
            if self._driver.segment is not None:
                self._driver.move(
                    self.environment.map.move(
                        origin=self._driver.coordinate,
                        destination=self._driver.segment.coordinate,
                        rate=self._driver.movement_rate
                    )
                )
            yield self.timeout(1)

    def accept_route_condition(self, route: Route) -> bool:
        return self._driver.fits(route) and self._driver.available

    def check_availability(self, route: Route) -> bool:
        return self._driver.fits(route) and self._driver.available

    def time_to_accept_or_reject_route(self, route: Route) -> int:
        return random.randrange(3, 10)

    def time_between_accept_and_start_picking_up(self, order: Order) -> int:
        return random.randrange(0, 3)

    def time_to_picking_up_order(self, order: Order):
        return self.environment.map.estimated_time(
            self._driver.coordinate,
            order.establishment.coordinate,
            self._driver.movement_rate
        )

    def time_between_picked_up_and_start_delivery(self, order: Order) -> int:
        return random.randrange(0, 3)

    def time_to_deliver_order(self, order: Order) -> int:
        establishment_coordinates = order.establishment.coordinate
        customer_coordinates = order.customer.coordinate
        return self.environment.map.estimated_time(
            establishment_coordinates,
            customer_coordinates,
            self._driver.movement_rate
        )
