import simpy

from src.main.map.map import Map


class FoodDeliveryEnvironment(simpy.Environment):
    def __init__(self, map: Map):
        super().__init__()
        self.map = map
        self.clients = []
        self.restaurants = []
        self.drivers = []
        self.events = simpy.Store(self)
        # Orders ready for collection
        self.ready_orders = simpy.Store(self)
        # Order deliveries rejected by driver
        self.rejected_delivery_orders = simpy.Store(self)
        # Orders delivered by drivers
        self.delivered_orders = simpy.Store(self)

    def add_clients(self, clients):
        self.clients += clients

    def add_restaurants(self, restaurants):
        self.restaurants += restaurants

    def add_drivers(self, drivers):
        self.drivers += drivers

    def add_ready_order(self, order):
        self.ready_orders.put(order)

    def get_ready_order(self):
        return self.ready_orders.get()

    def count_ready_orders(self):
        return len(self.ready_orders.items)

    def add_rejected_delivery_order(self, order):
        self.rejected_delivery_orders.put(order)

    def get_rejected_delivery_order(self):
        return self.rejected_delivery_orders.get()

    def count_rejected_delivery_orders(self):
        return len(self.rejected_delivery_orders.items)

    def add_delivered_order(self, order):
        self.delivered_orders.put(order)

    def get_delivered_order(self):
        self.delivered_orders.get()

    def count_delivered_orders(self):
        return len(self.delivered_orders.items)

    def add_event(self, event):
        self.events.put(event)

    def get_event(self):
        return self.events.get()

    def count_event(self):
        return len(self.events.items)

    def debug(self):
        print()
        for order in self.ready_orders.items:
            print(f"==============> order {order.order_id}")
        print()
        #
        # for driver in self.drivers:
        #     print(f"================ driver {driver.driver_id}")

        for order in self.delivered_orders.items:
            print(f"==============> order {order.order_id}")
        print()

        print(len(self.delivered_orders.items))
