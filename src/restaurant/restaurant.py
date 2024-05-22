from simpy import Environment


class Restaurant:
    def __init__(
            self,
            environment: Environment,
            name: str,
            coordinates,
            available: bool
    ):
        self.environment = environment
        self.name = name
        self.coordinates = coordinates
        self.available = available

    def receive_order(self, order):
        preparation_time = self.preparation_time(order)
        print(f"The {self.name} is preparing the order {order.order_id} for the {order.client.name} in {preparation_time}m")
        yield self.environment.timeout(preparation_time)


    def preparation_time(self, order):
        return 2

