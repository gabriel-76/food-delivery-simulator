import random
import uuid

import simpy

from src.main.driver.capacity import Capacity
from src.main.driver.driver_status import DriverStatus
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.driver_accepted_delivery import DriverAcceptedDelivery
from src.main.events.driver_accepted_trip import DriverAcceptedTrip
from src.main.events.driver_accepted_trip_extension import DriverAcceptedTripExtension
from src.main.events.driver_arrived_delivery_location import DriverArrivedDeliveryLocation
from src.main.events.driver_collected_order import DriverCollectedOrder
from src.main.events.driver_collecting_order import DriverCollectingOrder
from src.main.events.driver_delivered_order import DriverDeliveredOrder
from src.main.events.driver_delivering_order import DriverDeliveringOrder
from src.main.events.driver_rejected_delivery import DriverRejectedDelivery
from src.main.events.driver_rejected_trip import DriverRejectedTrip
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus
from src.main.trip.route import RouteType
from src.main.trip.trip import Trip


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
        self.current_trip = None
        self.current_route = None
        self.total_distance = 0
        self.requests = simpy.Store(self.environment)

        self.environment.process(self.process_requests())
        self.environment.process(self.move())

    def fits(self, trip: Trip):
        return self.capacity.fits(trip.required_capacity)

    def request_delivery(self, trip: Trip):
        self.requests.put(trip)

    def process_requests(self):
        while True:
            trip = yield self.requests.get()
            self.process_trip(trip)
            yield self.environment.timeout(self.time_to_accept_or_reject_trip(trip))

    def process_trip(self, trip: Trip):
        self.accept_trip(trip) if self.accept_trip_condition(trip) else self.reject_trip(trip)

    def accept_trip(self, trip: Trip):
        if self.current_trip is None:
            self.current_trip = trip
            event = DriverAcceptedTrip(
                driver_id=self.driver_id,
                trip_id=self.current_trip.tripe_id,
                distance=self.current_trip.distance,
                time=self.environment.now
            )
            self.environment.add_event(event)
            for route in self.current_trip.routes:
                event = DriverAcceptedDelivery(
                    driver_id=self.driver_id,
                    order_id=route.order.order_id,
                    client_id=route.order.client.client_id,
                    restaurant_id=route.order.restaurant.restaurant_id,
                    distance=self.current_trip.distance,
                    time=self.environment.now
                )
                self.environment.add_event(event)
                route.order.update_status(OrderStatus.DRIVER_ACCEPTED)
            self.environment.process(self.sequential_processor())
        else:
            self.accepted_trip_extension(trip)

    def accepted_trip_extension(self, trip: Trip):
        old_distance = self.current_trip.distance
        self.current_trip.extend_trip(trip)
        event = DriverAcceptedTripExtension(
            driver_id=self.driver_id,
            trip_id=self.current_trip.tripe_id,
            old_distance=old_distance,
            distance=self.current_trip.distance,
            time=self.environment.now
        )
        self.environment.add_event(event)
        for route in self.current_trip.routes:
            route.order.update_status(OrderStatus.DRIVER_ACCEPTED)
        for route in trip.routes:
            event = DriverAcceptedDelivery(
                driver_id=self.driver_id,
                order_id=route.order.order_id,
                client_id=route.order.client.client_id,
                restaurant_id=route.order.restaurant.restaurant_id,
                distance=self.current_trip.distance,
                time=self.environment.now
            )
            self.environment.add_event(event)

    def sequential_processor(self):
        if self.current_route is not None and self.current_route.order.status < OrderStatus.READY:
            # print(f"Driver {self.coordinates} is waiting for "
            #       f"order {self.current_route.coordinates} "
            #       f"status {self.current_route.order.status.name} "
            #       f"estimated time {self.current_route.order.estimated_time_to_ready} "
            #       f"ready time {self.current_route.order.time_it_was_ready} "
            #       f"current time {self.environment.now}")
            yield self.environment.timeout(1)
            self.environment.process(self.sequential_processor())
        elif self.current_trip.has_next_route():
            route = self.current_trip.next_route()
            self.current_route = route
            if route.route_type is RouteType.COLLECT:
                yield self.environment.timeout(self.time_between_accept_and_start_collection(route.order))
                self.environment.process(self.start_order_collection(route.order))
            if route.route_type is RouteType.DELIVERY:
                yield self.environment.timeout(self.time_between_collection_and_start_delivery(route.order))
                self.environment.process(self.start_order_delivery(route.order))
        else:
            self.current_trip = None
            self.current_route = None

    def reject_trip(self, trip: Trip):
        event = DriverRejectedTrip(
            driver_id=self.driver_id,
            trip_id=self.current_trip.tripe_id,
            distance=self.current_trip.distance,
            time=self.environment.now
        )
        self.environment.add_event(event)
        for route in trip.routes:
            event = DriverRejectedDelivery(
                driver_id=self.driver_id,
                order_id=route.order.order_id,
                client_id=route.order.client.client_id,
                restaurant_id=route.order.restaurant.restaurant_id,
                time=self.environment.now
            )
            self.environment.add_event(event)
            route.order.update_status(OrderStatus.DRIVER_REJECTED)
            self.environment.add_rejected_delivery(route.order)

    def start_order_collection(self, order):
        self.status = DriverStatus.COLLECTING
        order.update_status(OrderStatus.COLLECTING)
        self.total_distance += self.environment.map.distance(self.coordinates, order.restaurant.coordinates)
        event = DriverCollectingOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            distance=self.environment.map.distance(self.coordinates, order.restaurant.coordinates),
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(self.time_to_collect_order(order))
        self.finish_order_collection(order)

    def finish_order_collection(self, order):
        event = DriverCollectedOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
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
        self.total_distance += self.environment.map.distance(self.coordinates, order.client.coordinates)
        event = DriverDeliveringOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            distance=self.environment.map.distance(self.coordinates, order.client.coordinates),
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(self.time_to_deliver_order(order))
        self.environment.process(self.wait_client_pick_up_order(order))

    def wait_client_pick_up_order(self, order: Order):
        order.update_status(OrderStatus.DRIVER_ARRIVED_DELIVERY_LOCATION)
        event = DriverArrivedDeliveryLocation(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.process(order.client.receive_order(order, self))
        self.finish_order_delivery(order)

    def finish_order_delivery(self, order: Order):
        event = DriverDeliveredOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.coordinates = order.client.coordinates
        self.environment.add_event(event)
        self.status = DriverStatus.AVAILABLE
        order.update_status(OrderStatus.DELIVERED)
        self.environment.process(self.sequential_processor())

    def move(self):
        while True:
            if self.current_route is not None:
                self.coordinates = self.environment.map.move(
                    origin=self.coordinates,
                    destination=self.current_route.coordinates,
                    rate=self.movement_rate
                )
            yield self.environment.timeout(1)

    def accept_trip_condition(self, trip: Trip):
        return self.fits(trip) and self.available

    def check_availability(self, trip: Trip):
        return self.fits(trip) and self.available

    def time_to_accept_or_reject_trip(self, trip: Trip):
        return random.randrange(3, 10)
    def time_between_accept_and_start_collection(self, order: Order):
        return random.randrange(0, 3)

    def time_to_collect_order(self, order: Order):
        return self.environment.map.estimated_time(self.coordinates, order.restaurant.coordinates, self.movement_rate)

    def time_between_collection_and_start_delivery(self, order: Order):
        return random.randrange(0, 3)

    def time_to_deliver_order(self, order: Order):
        restaurant_coordinates = order.restaurant.coordinates
        client_coordinates = order.client.coordinates
        return self.environment.map.estimated_time(restaurant_coordinates, client_coordinates, self.movement_rate)