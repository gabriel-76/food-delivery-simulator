import random
import uuid
from typing import Optional, List

from simpy.events import ProcessGenerator

from src.main.actors.map_actor import MapActor
from src.main.base.types import Coordinate, Number
from src.main.driver.capacity import Capacity
from src.main.driver.driver_status import DriverStatus
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.driver_accepted_delivery import DriverAcceptedDelivery
from src.main.events.driver_accepted_route import DriverAcceptedRoute
from src.main.events.driver_accepted_route_extension import DriverAcceptedRouteExtension
from src.main.events.driver_arrived_delivery_location import DriverArrivedDeliveryLocation
from src.main.events.driver_delivered_order import DriverDeliveredOrder
from src.main.events.driver_delivering_order import DriverDeliveringOrder
from src.main.events.driver_picked_up_order import DriverPickedUpOrder
from src.main.events.driver_picking_up_order import DriverPickingUpOrder
from src.main.events.driver_rejected_delivery import DriverRejectedDelivery
from src.main.events.driver_rejected_route import DriverRejectedRoute
from src.main.order.driver_delivery_rejection import DriverDeliveryRejection
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus
from src.main.route.route import Route
from src.main.route.route_segment import RouteSegment


class Driver(MapActor):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            coordinate: Coordinate,
            available: bool,
            capacity: Capacity,
            status: DriverStatus,
            movement_rate: Number
    ):
        self.driver_id = uuid.uuid4()
        super().__init__(environment, coordinate, available)
        self.capacity = capacity
        self.status = status
        self.movement_rate = movement_rate

        self.current_route: Optional[Route] = None
        self.current_route_segment: Optional[RouteSegment] = None
        self.total_distance: Number = 0
        self.route_requests: List[Route] = []

        self.process(self.process_route_requests())
        self.process(self.move())

    def fits(self, route: Route) -> bool:
        return self.capacity.fits(route.required_capacity)

    def receive_route_requests(self, route: Route) -> None:
        self.route_requests.append(route)

    def process_route_requests(self) -> ProcessGenerator:
        while True:
            if len(self.route_requests) > 0:
                route = self.route_requests.pop(0)
                self.process_route_request(route)
                yield self.timeout(self.time_to_accept_or_reject_route(route))
            else:
                yield self.timeout(1)

    def process_route_request(self, route: Route) -> None:
        accept = self.accept_route_condition(route)
        self.accept_route(route) if accept else self.reject_route(route)

    def accept_route(self, route: Route) -> None:
        if self.current_route is None:
            self.current_route = route
            self.publish_event(DriverAcceptedRoute(
                driver_id=self.driver_id,
                route_id=self.current_route.route_id,
                distance=self.current_route.distance,
                time=self.now
            ))
            self.accept_route_segments(self.current_route.route_segments)
            self.process(self.sequential_processor())
        else:
            self.accepted_route_extension(route)

    def accept_route_segments(self, route_segments: List[RouteSegment]) -> None:
        for route_segment in route_segments:
            self.accept_route_segment(route_segment)

    def accept_route_segment(self, route_segment: RouteSegment) -> None:
        self.publish_event(DriverAcceptedDelivery(
            driver_id=self.driver_id,
            order_id=route_segment.order.order_id,
            customer_id=route_segment.order.customer.customer_id,
            establishment_id=route_segment.order.establishment.establishment_id,
            distance=self.current_route.distance,
            time=self.now
        ))
        route_segment.order.update_status(OrderStatus.DRIVER_ACCEPTED)

    def accepted_route_extension(self, route: Route) -> None:
        old_distance = self.current_route.distance
        self.current_route.extend_route(route)
        self.publish_event(DriverAcceptedRouteExtension(
            driver_id=self.driver_id,
            route_id=self.current_route.route_id,
            old_distance=old_distance,
            distance=self.current_route.distance,
            time=self.now
        ))
        self.accept_route_segments(route.route_segments)

    def sequential_processor(self) -> ProcessGenerator:
        if self.current_route_segment is not None and self.current_route_segment.order.status < OrderStatus.READY:
            # print(f"Driver {self.coordinate} is waiting for "
            #       f"order {self.current_route_segment.coordinate} "
            #       f"status {self.current_route_segment.order.status.name} "
            #       f"estimated time {self.current_route_segment.order.estimated_time_to_ready} "
            #       f"ready time {self.current_route_segment.order.time_it_was_ready} "
            #       f"current time {self.now}")
            yield self.timeout(1)
            self.process(self.sequential_processor())
        elif self.current_route.has_next():
            route_segment = self.current_route.next()
            self.current_route_segment = route_segment
            if route_segment.is_pickup():
                timeout = self.time_between_accept_and_start_picking_up(route_segment.order)
                yield self.timeout(timeout)
                self.process(self.picking_up(route_segment.order))
            if route_segment.is_delivery():
                timeout = self.time_between_picked_up_and_start_delivery(route_segment.order)
                yield self.timeout(timeout)
                self.process(self.delivering(route_segment.order))
        else:
            self.current_route = None
            self.current_route_segment = None

    def reject_route(self, route: Route) -> None:
        self.publish_event(DriverRejectedRoute(
            driver_id=self.driver_id,
            route_id=self.current_route.route_id,
            distance=self.current_route.distance,
            time=self.now
        ))
        self.reject_route_segments(route.route_segments)

    def reject_route_segments(self, route_segments: List[RouteSegment]) -> None:
        for route_segment in route_segments:
            self.reject_route_segment(route_segment)

    def reject_route_segment(self, route_segment: RouteSegment) -> None:
        self.publish_event(DriverRejectedDelivery(
            driver_id=self.driver_id,
            order_id=route_segment.order.order_id,
            customer_id=route_segment.order.customer.customer_id,
            establishment_id=route_segment.order.establishment.establishment_id,
            time=self.now
        ))
        route_segment.order.update_status(OrderStatus.DRIVER_REJECTED)
        rejection = DriverDeliveryRejection(self, self.now)
        self.environment.add_rejected_delivery(route_segment.order, rejection)

    def picking_up(self, order: Order) -> ProcessGenerator:
        self.status = DriverStatus.PICKING_UP
        order.update_status(OrderStatus.PICKING_UP)
        self.total_distance += self.environment.map.distance(self.coordinate, order.establishment.coordinate)
        self.publish_event(DriverPickingUpOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver_id,
            distance=self.environment.map.distance(self.coordinate, order.establishment.coordinate),
            time=self.now
        ))
        yield self.timeout(self.time_to_picking_up_order(order))
        self.picked_up(order)

    def picked_up(self, order: Order) -> None:
        self.publish_event(DriverPickedUpOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver_id,
            time=self.now
        ))
        self.coordinate = order.establishment.coordinate
        self.process(self.sequential_processor())

    def delivering(self, order: Order) -> ProcessGenerator:
        self.status = DriverStatus.DELIVERING
        order.update_status(OrderStatus.DELIVERING)
        self.total_distance += self.environment.map.distance(self.coordinate, order.customer.coordinate)
        self.publish_event(DriverDeliveringOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver_id,
            distance=self.environment.map.distance(self.coordinate, order.customer.coordinate),
            time=self.now
        ))
        yield self.timeout(self.time_to_deliver_order(order))
        self.process(self.wait_customer_pick_up_order(order))

    def wait_customer_pick_up_order(self, order: Order) -> ProcessGenerator:
        order.update_status(OrderStatus.DRIVER_ARRIVED_DELIVERY_LOCATION)
        self.publish_event(DriverArrivedDeliveryLocation(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver_id,
            time=self.now
        ))
        yield self.process(order.customer.receive_order(order, self))
        self.delivered(order)

    def delivered(self, order: Order) -> None:
        self.coordinate = order.customer.coordinate
        self.publish_event(DriverDeliveredOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver_id,
            time=self.now
        ))
        self.status = DriverStatus.AVAILABLE
        order.update_status(OrderStatus.DELIVERED)
        self.process(self.sequential_processor())

    def move(self) -> ProcessGenerator:
        while True:
            if self.current_route_segment is not None:
                self.coordinate = self.environment.map.move(
                    origin=self.coordinate,
                    destination=self.current_route_segment.coordinate,
                    rate=self.movement_rate
                )
            yield self.timeout(1)

    def accept_route_condition(self, route: Route) -> bool:
        return self.fits(route) and self.available

    def check_availability(self, route: Route) -> bool:
        return self.fits(route) and self.available

    def time_to_accept_or_reject_route(self, route: Route) -> int:
        return random.randrange(3, 10)

    def time_between_accept_and_start_picking_up(self, order: Order) -> int:
        return random.randrange(0, 3)

    def time_to_picking_up_order(self, order: Order):
        return self.environment.map.estimated_time(self.coordinate, order.establishment.coordinate, self.movement_rate)

    def time_between_picked_up_and_start_delivery(self, order: Order) -> int:
        return random.randrange(0, 3)

    def time_to_deliver_order(self, order: Order) -> int:
        establishment_coordinates = order.establishment.coordinate
        customer_coordinates = order.customer.coordinate
        return self.environment.map.estimated_time(establishment_coordinates, customer_coordinates, self.movement_rate)
