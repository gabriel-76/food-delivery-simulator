import random
import uuid

from src.driver.driver import Driver
from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.order.order import Order
from src.restaurant.restaurant import Restaurant


class Client:
    def __init__(self, environment: FoodDeliveryEnvironment, coordinates, available: bool):
        self.client_id = uuid.uuid4()
        self.environment = environment
        self.coordinates = coordinates
        self.available = available

    def place_order(self, order: Order, restaurant: Restaurant):
        print(f"Client {self.client_id} placed an order {order.order_id} to restaurant {restaurant.restaurant_id} in time {self.environment.now}")
        restaurant.receive_orders([order])

    def receive_order(self, order: Order, driver: Driver):
        yield self.environment.timeout(self.time_to_receive_order(order))
        print(f"Client {self.client_id} picked up the order {order.order_id} with driver {driver.driver_id} from restaurant {order.restaurant.restaurant_id} in time {self.environment.now}")

    def time_to_receive_order(self, order: Order):
        return random.randrange(0, 3)

