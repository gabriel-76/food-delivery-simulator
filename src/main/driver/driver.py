import random
import uuid

import simpy

from src.main.driver.capacity import Capacity
from src.main.driver.driver_status import DriverStatus
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.driver_accepted_delivery import DriverAcceptedDelivery
from src.main.events.driver_accepted_route import DriverAcceptedRoute
from src.main.events.driver_accepted_route_extension import DriverAcceptedRouteExtension
from src.main.events.driver_arrived_delivery_location import DriverArrivedDeliveryLocation
from src.main.events.driver_picked_up_order import DriverPickedUpOrder
from src.main.events.driver_picking_up_order import DriverPickingUpOrder
from src.main.events.driver_delivered_order import DriverDeliveredOrder
from src.main.events.driver_delivering_order import DriverDeliveringOrder
from src.main.events.driver_rejected_delivery import DriverRejectedDelivery
from src.main.events.driver_rejected_route import DriverRejectedRoute
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus
from src.main.route.route_segment import RouteSegmentType
from src.main.route.route import Route


class Driver:
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            coordinates,
            capacity: Capacity,
            available: bool,
            status: DriverStatus,
            movement_rate
    ):
        self.driver_id = uuid.uuid4()
        self.environment = environment
        self.coordinates = coordinates
        self.capacity = capacity
        self.available = available
        self.status = status
        self.movement_rate = movement_rate
        self.current_route = None
        self.current_route_segment = None
        self.total_distance = 0
        self.delivery_requests = simpy.Store(self.environment)

        self.environment.process(self.process_delivery_requests())
        self.environment.process(self.move())

    def fits(self, route: Route):
        return self.capacity.fits(route.required_capacity)

    def request_delivery(self, route: Route):
        self.delivery_requests.put(route)

    def process_delivery_requests(self):
        while True:
            route = yield self.delivery_requests.get()
            self.process_route(route)
            yield self.environment.timeout(self.time_to_accept_or_reject_route(route))

    def process_route(self, route: Route):
        self.accept_route(route) if self.accept_route_condition(route) else self.reject_route(route)

    def accept_route(self, route: Route):
        if self.current_route is None:
            self.current_route = route
            event = DriverAcceptedRoute(
                driver_id=self.driver_id,
                route_id=self.current_route.route_id,
                distance=self.current_route.distance,
                time=self.environment.now
            )
            self.environment.add_event(event)
            for route_segment in self.current_route.route_segments:
                event = DriverAcceptedDelivery(
                    driver_id=self.driver_id,
                    order_id=route_segment.order.order_id,
                    customer_id=route_segment.order.customer.customer_id,
                    restaurant_id=route_segment.order.restaurant.restaurant_id,
                    distance=self.current_route.distance,
                    time=self.environment.now
                )
                self.environment.add_event(event)
                route_segment.order.update_status(OrderStatus.DRIVER_ACCEPTED)
            self.environment.process(self.sequential_processor())
        else:
            self.accepted_route_extension(route)

    def accepted_route_extension(self, route: Route):
        old_distance = self.current_route.distance
        self.current_route.extend_route(route)
        event = DriverAcceptedRouteExtension(
            driver_id=self.driver_id,
            route_id=self.current_route.route_id,
            old_distance=old_distance,
            distance=self.current_route.distance,
            time=self.environment.now
        )
        self.environment.add_event(event)
        for route_segment in self.current_route.route_segments:
            route_segment.order.update_status(OrderStatus.DRIVER_ACCEPTED)
        for route_segment in route.route_segments:
            event = DriverAcceptedDelivery(
                driver_id=self.driver_id,
                order_id=route_segment.order.order_id,
                customer_id=route_segment.order.customer.customer_id,
                restaurant_id=route_segment.order.restaurant.restaurant_id,
                distance=self.current_route.distance,
                time=self.environment.now
            )
            self.environment.add_event(event)

    def sequential_processor(self):
        if self.current_route_segment is not None and self.current_route_segment.order.status < OrderStatus.READY:
            # print(f"Driver {self.coordinates} is waiting for "
            #       f"order {self.current_segment.coordinates} "
            #       f"status {self.current_segment.order.status.name} "
            #       f"estimated time {self.current_segment.order.estimated_time_to_ready} "
            #       f"ready time {self.current_segments.order.time_it_was_ready} "
            #       f"current time {self.environment.now}")
            yield self.environment.timeout(1)
            self.environment.process(self.sequential_processor())
        elif self.current_route.has_next_segments():
            route_segment = self.current_route.next_segments()
            self.current_route_segment = route_segment
            if route_segment.route_segment_type is RouteSegmentType.PICKUP:
                yield self.environment.timeout(self.time_between_accept_and_start_picking_up(route_segment.order))
                self.environment.process(self.start_picking_up_order(route_segment.order))
            if route_segment.route_segment_type is RouteSegmentType.DELIVERY:
                yield self.environment.timeout(self.time_between_pickup_and_start_delivery(route_segment.order))
                self.environment.process(self.start_order_delivery(route_segment.order))
        else:
            self.current_route = None
            self.current_route_segment = None

    def reject_route(self, route: Route):
        event = DriverRejectedRoute(
            driver_id=self.driver_id,
            route_id=self.current_route.route_id,
            distance=self.current_route.distance,
            time=self.environment.now
        )
        self.environment.add_event(event)
        for route_segment in route.route_segments:
            event = DriverRejectedDelivery(
                driver_id=self.driver_id,
                order_id=route_segment.order.order_id,
                customer_id=route_segment.order.customer.customer_id,
                restaurant_id=route_segment.order.restaurant.restaurant_id,
                time=self.environment.now
            )
            self.environment.add_event(event)
            route_segment.order.update_status(OrderStatus.DRIVER_REJECTED)
            self.environment.add_rejected_delivery(route_segment.order)

    def start_picking_up_order(self, order):
        self.status = DriverStatus.PICKING_UP
        order.update_status(OrderStatus.PICKING_UP)
        self.total_distance += self.environment.map.distance(self.coordinates, order.restaurant.coordinates)
        event = DriverPickingUpOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            distance=self.environment.map.distance(self.coordinates, order.restaurant.coordinates),
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(self.time_to_picking_up_order(order))
        self.finish_order_pickup(order)

    def finish_order_pickup(self, order):
        event = DriverPickedUpOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.coordinates = order.restaurant.coordinates
        self.environment.add_event(event)
        self.environment.process(self.sequential_processor())

    def start_order_delivery(self, order: Order):
        self.status = DriverStatus.DELIVERING
        order.update_status(OrderStatus.DELIVERING)
        self.total_distance += self.environment.map.distance(self.coordinates, order.customer.coordinates)
        event = DriverDeliveringOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            distance=self.environment.map.distance(self.coordinates, order.customer.coordinates),
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(self.time_to_deliver_order(order))
        self.environment.process(self.wait_customer_pick_up_order(order))

    def wait_customer_pick_up_order(self, order: Order):
        order.update_status(OrderStatus.DRIVER_ARRIVED_DELIVERY_LOCATION)
        event = DriverArrivedDeliveryLocation(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.process(order.customer.receive_order(order, self))
        self.finish_order_delivery(order)

    def finish_order_delivery(self, order: Order):
        event = DriverDeliveredOrder(
            order_id=order.order_id,
            customer_id=order.customer.customer_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.coordinates = order.customer.coordinates
        self.environment.add_event(event)
        self.status = DriverStatus.AVAILABLE
        order.update_status(OrderStatus.DELIVERED)
        self.environment.process(self.sequential_processor())

    def move(self):
        while True:
            if self.current_route_segment is not None:
                self.coordinates = self.environment.map.move(
                    origin=self.coordinates,
                    destination=self.current_route_segment.coordinates,
                    rate=self.movement_rate
                )
            yield self.environment.timeout(1)

    def accept_route_condition(self, route: Route):
        return self.fits(route) and self.available

    def check_availability(self, route: Route):
        return self.fits(route) and self.available

    def time_to_accept_or_reject_route(self, route: Route):
        return random.randrange(3, 10)

    def time_between_accept_and_start_picking_up(self, order: Order):
        return random.randrange(0, 3)

    def time_to_picking_up_order(self, order: Order):
        return self.environment.map.estimated_time(self.coordinates, order.restaurant.coordinates, self.movement_rate)

    def time_between_pickup_and_start_delivery(self, order: Order):
        return random.randrange(0, 3)

    def time_to_deliver_order(self, order: Order):
        restaurant_coordinates = order.restaurant.coordinates
        customer_coordinates = order.customer.coordinates
        return self.environment.map.estimated_time(restaurant_coordinates, customer_coordinates, self.movement_rate)
