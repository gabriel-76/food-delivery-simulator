import random
import uuid

from src.main.driver.driver import Driver
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.customer_placed_order import CustomerPlacedOrder
from src.main.events.customer_received_order import CustomerReceivedOrder
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus
from src.main.restaurant.restaurant import Restaurant


class Customer:
    def __init__(self, environment: FoodDeliverySimpyEnv, coordinates, available: bool):
        self.customer_id = uuid.uuid4()
        self.environment = environment
        self.coordinates = coordinates
        self.available = available

    def place_order(self, order: Order, restaurant: Restaurant):
        event = CustomerPlacedOrder(
            order_id=order.order_id,
            customer_id=self.customer_id,
            restaurant_id=restaurant.restaurant_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        restaurant.receive_orders([order])
        order.update_status(OrderStatus.PLACED)

    def receive_order(self, order: Order, driver: Driver):
        yield self.environment.timeout(self.time_to_receive_order(order))
        event = CustomerReceivedOrder(
            order_id=order.order_id,
            customer_id=self.customer_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=driver.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        order.update_status(OrderStatus.RECEIVED)

    def time_to_receive_order(self, order: Order):
        return random.randrange(2, 10)

