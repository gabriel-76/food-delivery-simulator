import bisect


class Simulator:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        bisect.insort(self.events, event)

    def remove_event(self, event):
        pass
