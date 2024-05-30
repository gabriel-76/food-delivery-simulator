import uuid

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
