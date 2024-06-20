class FoodDeliveryState:
    def __init__(self):
        self.customers = []
        self.restaurants = []
        self.drivers = []
        self.orders = []

    def add_customers(self, customer):
        self.customers += customer

    def add_restaurants(self, restaurants):
        self.restaurants += restaurants

    def add_drivers(self, drivers):
        self.drivers += drivers
