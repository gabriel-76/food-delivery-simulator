from typing import List

from src.main.order.order import Order


class FoodDeliveryState:
    def __init__(self):
        self.customers = []
        self.restaurants = []
        self.drivers = []
        self.orders = []

        # Orders ready for picking up
        self.orders_awaiting_delivery: List[Order] = []

        self.events = []

    def add_customers(self, customer):
        self.customers += customer

    def add_restaurants(self, restaurants):
        self.restaurants += restaurants

    def add_drivers(self, drivers):
        self.drivers += drivers

    def add_event(self, event):
        self.events.append(event)

    def log_events(self):
        for event in self.events:
            print(event)
