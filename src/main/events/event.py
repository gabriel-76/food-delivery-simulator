class Event:
    def __init__(self, order_id, client_id, restaurant_id, time):
        self.order_id = order_id
        self.client_id = client_id
        self.restaurant_id = restaurant_id
        self.time = time

    # def __lt__(self, other):
    #     return self.creation_date < other.creation_date
