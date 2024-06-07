from uuid import uuid4


class Event:
    def __init__(self, time, event_type):
        self.event_id = uuid4()
        self.time = time
        self.event_type = event_type

    # def __lt__(self, other):
    #     return self.creation_date < other.creation_date
