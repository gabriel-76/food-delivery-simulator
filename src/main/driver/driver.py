import random
import uuid
from enum import Enum, auto

import simpy

from src.main.driver.capacity import Capacity
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
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
from src.main.trip.route import RouteType
from src.main.trip.trip import Trip


class DriverStatus(Enum):
    WAITING = auto()
    COLLECTING = auto()
    DELIVERING = auto()


class Driver:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
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
        self.collection_distance = 0
        self.delivery_distance = 0
        self.total_distance = 0
        self.current_trip = None
        self.requests = simpy.Store(self.environment)

        self.environment.process(self.process_requests())

    def fits(self, trip: Trip):
        return self.capacity.fits(trip.required_capacity)

    def request_delivery(self, trip: Trip):
        self.requests.put(trip)

    def process_requests(self):
        while True:
            trip = yield self.requests.get()
            if self.accept_trip_condition(trip):
                self.accept_trip(trip)
            else:
                self.reject_trip(trip)

            timeout = self.time_to_accept_or_reject_trip(trip)
            yield self.environment.timeout(timeout)

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
            self.sequential_processor()
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

    def sequential_processor(self):
        if self.current_trip.has_next_route():
            route = self.current_trip.next_route()
            if route.route_type is RouteType.COLLECT:
                self.environment.process(self.start_order_collection(route.order))
            if route.route_type is RouteType.DELIVERY:
                self.environment.process(self.start_order_delivery(route.order))
        else:
            self.current_trip = None

    def reject_trip(self, trip: Trip):
        event = DriverRejectedTrip(
            driver_id=self.driver_id,
            trip_id=self.current_trip.tripe_id,
            distance=self.current_trip.distance,
            time=self.environment.now
        )
        self.environment.add_event(event)
        for route in trip.routes:
            self.environment.add_rejected_delivery_order(route.order)

    def start_order_collection(self, order):
        self.status = DriverStatus.COLLECTING
        event = DriverCollectingOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            distance=self.collection_distance,
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
        self.sequential_processor()
        # self.environment.process(self.start_order_delivery(order))

    def start_order_delivery(self, order: Order):
        self.status = DriverStatus.DELIVERING
        event = DriverDeliveringOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            distance=self.delivery_distance,
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(self.time_to_deliver_order(order))
        self.environment.process(self.wait_client_pick_up_order(order))

    def wait_client_pick_up_order(self, order: Order):
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
        self.collection_distance = 0
        self.delivery_distance = 0
        self.total_distance = 0
        self.status = DriverStatus.WAITING
        self.environment.add_delivered_order(order)
        self.sequential_processor()

    def time_to_accept_or_reject_trip(self, trip: Trip):
        return random.randrange(10, 50)

    def time_to_deliver_order(self, order: Order):
        restaurant_coordinates = order.restaurant.coordinates
        client_coordinates = order.client.coordinates
        return self.environment.map.estimated_time(restaurant_coordinates, client_coordinates, self.movement_rate)

    def time_to_collect_order(self, order: Order):
        return self.environment.map.estimated_time(self.coordinates, order.restaurant.coordinates, self.movement_rate)

    def accept_trip_condition(self, trip: Trip):
        return self.fits(trip) and self.available

    def check_availability(self, trip: Trip):
        return self.fits(trip) and self.available
