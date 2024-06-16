from abc import ABC, abstractmethod


class FoodDeliveryView(ABC):

    def __init__(self, window_size=(800, 600), fps=30):
        self.window_size = window_size
        self.fps = fps
        self.min_x = 0
        self.max_x = 100
        self.min_y = 0
        self.max_y = 100
        self.quited = False

    @abstractmethod
    def render(self, environment) -> bool: pass

    @abstractmethod
    def quit(self): pass
