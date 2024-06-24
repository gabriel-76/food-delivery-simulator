# from typing import List
#
# from src.main.customer.customer import Customer
# from src.main.driver.driver import Driver
# from src.main.order.order import Order
# from src.main.restaurant.restaurant import Restaurant


class FoodDeliveryState:
    def __init__(self):
        self.customers = []
        self.restaurants = []
        self.drivers = []
        self.orders = []

        # self.customers: List[Customer] = []
        # self.restaurants: List[Restaurant] = []
        # self.drivers: List[Driver] = []
        # self.orders: List[Order] = []

    def add_customers(self, customer):
        self.customers += customer

    def add_restaurants(self, restaurants):
        self.restaurants += restaurants

    def add_drivers(self, drivers):
        self.drivers += drivers
