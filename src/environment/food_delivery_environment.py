import simpy


class FoodDeliveryEnvironment(simpy.Environment):
    def __init__(self):
        super().__init__()
        # Orders ready for collection
        self.ready_orders = simpy.Store(self)
        # Order deliveries rejected by driver
        self.rejected_delivery_orders = simpy.Store(self)
        # Orders in the delivery process
        self.orders_in_transit = simpy.Store(self)
        # Orders delivered by drivers
        self.delivered_orders = simpy.Store(self)

    def add_ready_order(self, order):
        self.ready_orders.put(order)

    def get_ready_order(self):
        return self.ready_orders.get()

    def count_ready_orders(self):
        return len(self.ready_orders.items)
