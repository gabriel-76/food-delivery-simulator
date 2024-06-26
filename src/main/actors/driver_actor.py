import random
from typing import List

from simpy.events import ProcessGenerator

from src.main.actors.actor import Actor
from src.main.actors.customer_actor import CustomerActor
from src.main.driver.driver import Driver
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


class DriverActor(Actor):
    def __init__(self, environment: FoodDeliverySimpyEnv, driver: Driver):
        super().__init__(environment)
        self.driver = driver
        self.process(self.process_route_requests())
        self.process(self.move())

    def fits(self, route: Route) -> bool:
        return self.driver.capacity.fits(route.required_capacity)

    def receive_route_requests(self, route: Route) -> None:
        self.driver.route_requests.append(route)

    def process_route_requests(self) -> ProcessGenerator:
        while True:
            if len(self.driver.route_requests) > 0:
                route = self.driver.route_requests.pop(0)
                self.process_route_request(route)
                yield self.timeout(self.time_to_accept_or_reject_route(route))
            else:
                yield self.timeout(1)

    def process_route_request(self, route: Route) -> None:
        accept = self.accept_route_condition(route)
        self.accept_route(route) if accept else self.reject_route(route)

    def accept_route(self, route: Route) -> None:
        if self.driver.current_route is None:
            self.driver.current_route = route
            self.publish_event(DriverAcceptedRoute(
                driver_id=self.driver.driver_id,
                route_id=self.driver.current_route.route_id,
                distance=self.environment.map.acc_distance([self.driver.coordinate] + route.coordinates),
                time=self.now
            ))
            self.accept_route_segments(self.driver.current_route.route_segments)
            self.process(self.sequential_processor())
        else:
            self.accepted_route_extension(route)

    def accept_route_segments(self, route_segments: List[RouteSegment]) -> None:
        for route_segment in route_segments:
            self.accept_route_segment(route_segment)

    def accept_route_segment(self, route_segment: RouteSegment) -> None:
        self.publish_event(DriverAcceptedDelivery(
            driver_id=self.driver.driver_id,
            order_id=route_segment.order.order_id,
            customer_id=route_segment.order.customer.customer_id,
            establishment_id=route_segment.order.establishment.establishment_id,
            # TODO: Calculate distance posteriorly
            distance=0,
            time=self.now
        ))
        route_segment.order.update_status(OrderStatus.DRIVER_ACCEPTED)

    def accepted_route_extension(self, route: Route) -> None:
        old_distance = self.environment.map.acc_distance([self.driver.coordinate] + route.coordinates)
        self.driver.current_route.extend_route(route)
        self.publish_event(DriverAcceptedRouteExtension(
            driver_id=self.driver.driver_id,
            route_id=self.driver.current_route.route_id,
            old_distance=old_distance,
            distance=self.environment.map.acc_distance([self.driver.coordinate] + route.coordinates),
            time=self.now
        ))
        self.accept_route_segments(route.route_segments)

    def sequential_processor(self) -> ProcessGenerator:
        if (self.driver.current_route_segment is not None
                and self.driver.current_route_segment.order.status < OrderStatus.READY):
            # print(f"Driver {self.coordinate} is waiting for "
            #       f"order {self.current_route_segment.coordinate} "
            #       f"status {self.current_route_segment.order.status.name} "
            #       f"estimated time {self.current_route_segment.order.estimated_time_to_ready} "
            #       f"ready time {self.current_route_segment.order.time_it_was_ready} "
            #       f"current time {self.now}")
            yield self.timeout(1)
            self.process(self.sequential_processor())
        elif self.driver.current_route.has_next():
            route_segment = self.driver.current_route.next()
            self.driver.current_route_segment = route_segment
            if route_segment.is_pickup():
                timeout = self.time_between_accept_and_start_picking_up(route_segment.order)
                yield self.timeout(timeout)
                self.process(self.picking_up(route_segment.order))
            if route_segment.is_delivery():
                timeout = self.time_between_picked_up_and_start_delivery(route_segment.order)
                yield self.timeout(timeout)
                self.process(self.delivering(route_segment.order))
        else:
            self.driver.current_route = None
            self.driver.current_route_segment = None

    def reject_route(self, route: Route) -> None:
        self.publish_event(DriverRejectedRoute(
            driver_id=self.driver.driver_id,
            route_id=self.driver.current_route.route_id,
            distance=self.environment.map.acc_distance([self.driver.coordinate] + route.coordinates),
            time=self.now
        ))
        self.reject_route_segments(route.route_segments)

    def reject_route_segments(self, route_segments: List[RouteSegment]) -> None:
        for route_segment in route_segments:
            self.reject_route_segment(route_segment)

    def reject_route_segment(self, route_segment: RouteSegment) -> None:
        self.publish_event(DriverRejectedDelivery(
            driver_id=self.driver.driver_id,
            order_id=route_segment.order.order_id,
            customer_id=route_segment.order.customer.customer_id,
            establishment_id=route_segment.order.establishment.establishment_id,
            time=self.now
        ))
        route_segment.order.update_status(OrderStatus.DRIVER_REJECTED)
        rejection = DriverDeliveryRejection(self, self.now)
        self.environment.add_rejected_delivery(route_segment.order, rejection)

    def picking_up(self, order: Order) -> ProcessGenerator:
        self.driver.status = DriverStatus.PICKING_UP
        order.update_status(OrderStatus.PICKING_UP)
        self.driver.total_distance += self.environment.map.distance(
            self.driver.coordinate, order.establishment.coordinate
        )
        self.publish_event(DriverPickingUpOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver.driver_id,
            distance=self.environment.map.distance(self.driver.coordinate, order.establishment.coordinate),
            time=self.now
        ))
        yield self.timeout(self.time_to_picking_up_order(order))
        self.picked_up(order)

    def picked_up(self, order: Order) -> None:
        self.publish_event(DriverPickedUpOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver.driver_id,
            time=self.now
        ))
        self.driver.coordinate = order.establishment.coordinate
        self.process(self.sequential_processor())

    def delivering(self, order: Order) -> ProcessGenerator:
        self.driver.status = DriverStatus.DELIVERING
        order.update_status(OrderStatus.DELIVERING)
        self.driver.total_distance += self.environment.map.distance(self.driver.coordinate, order.customer.coordinate)
        self.publish_event(DriverDeliveringOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver.driver_id,
            distance=self.environment.map.distance(self.driver.coordinate, order.customer.coordinate),
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
            driver_id=self.driver.driver_id,
            time=self.now
        ))
        customer_actor = CustomerActor(self.environment, order.customer)
        yield self.process(customer_actor.receive_order(order, self.driver))
        self.delivered(order)

    def delivered(self, order: Order) -> None:
        self.driver.coordinate = order.customer.coordinate
        self.publish_event(DriverDeliveredOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=self.driver.driver_id,
            time=self.now
        ))
        self.driver.status = DriverStatus.AVAILABLE
        order.update_status(OrderStatus.DELIVERED)
        self.process(self.sequential_processor())

    def move(self) -> ProcessGenerator:
        while True:
            if self.driver.current_route_segment is not None:
                self.driver.coordinate = self.environment.map.move(
                    origin=self.driver.coordinate,
                    destination=self.driver.current_route_segment.coordinate,
                    rate=self.driver.movement_rate
                )
            yield self.timeout(1)

    def accept_route_condition(self, route: Route) -> bool:
        return self.fits(route) and self.driver.available

    def check_availability(self, route: Route) -> bool:
        return self.fits(route) and self.driver.available

    def time_to_accept_or_reject_route(self, route: Route) -> int:
        return random.randrange(3, 10)

    def time_between_accept_and_start_picking_up(self, order: Order) -> int:
        return random.randrange(0, 3)

    def time_to_picking_up_order(self, order: Order):
        return self.environment.map.estimated_time(
            self.driver.coordinate,
            order.establishment.coordinate,
            self.driver.movement_rate
        )

    def time_between_picked_up_and_start_delivery(self, order: Order) -> int:
        return random.randrange(0, 3)

    def time_to_deliver_order(self, order: Order) -> int:
        establishment_coordinates = order.establishment.coordinate
        customer_coordinates = order.customer.coordinate
        return self.environment.map.estimated_time(
            establishment_coordinates,
            customer_coordinates,
            self.driver.movement_rate
        )
