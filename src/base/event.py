class Event:
    def __init__(self, creation_date, event_type):
        self.creation_date = creation_date
        self.event_type = event_type

    def __lt__(self, other):
        return self.creation_date < other.creation_date
