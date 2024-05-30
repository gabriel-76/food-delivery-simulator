import random
import uuid

from src.driver.driver import Driver
from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.events.client_placed_order import ClientPlacedOrder
from src.events.client_received_order import ClientReceivedOrder
from src.order.order import Order
from src.restaurant.restaurant import Restaurant


class Client:
    def __init__(self, environment: FoodDeliveryEnvironment, coordinates, available: bool):
        self.client_id = uuid.uuid4()
        self.environment = environment
        self.coordinates = coordinates
        self.available = available

    def place_order(self, order: Order, restaurant: Restaurant):
        event = ClientPlacedOrder(
            order_id=order.order_id,
            client_id=self.client_id,
            restaurant_id=restaurant.restaurant_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        restaurant.receive_orders([order])

    def receive_order(self, order: Order, driver: Driver):
        yield self.environment.timeout(self.time_to_receive_order(order))
        event = ClientReceivedOrder(
            order_id=order.order_id,
            client_id=self.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=driver.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)

    def time_to_receive_order(self, order: Order):
        return random.randrange(1, 5)

