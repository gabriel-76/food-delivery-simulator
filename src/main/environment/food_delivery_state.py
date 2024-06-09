class FoodDeliveryState:
    def __init__(self):
        self.clients = []
        self.restaurants = []
        self.drivers = []
        self.orders = []

    def add_clients(self, clients):
        self.clients += clients

    def add_restaurants(self, restaurants):
        self.restaurants += restaurants

    def add_drivers(self, drivers):
        self.drivers += drivers
