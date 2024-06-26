import uuid


class Driver:
    def __init__(self, coordinate, capacity, available, status, movement_rate):
        self.driver_id = uuid.uuid4()
        self.coordinate = coordinate
        self.capacity = capacity
        self.available = available
        self.status = status
        self.movement_rate = movement_rate

