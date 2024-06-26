import pygame

from src.main.driver.driver_status import DriverStatus
from src.main.view.food_delivery_view import FoodDeliveryView

# Definindo cores
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


def map_coordinate(value, min_val, max_val, min_screen, max_screen):
    return min_screen + (value - min_val) * (max_screen - min_screen) / (max_val - min_val)


class GridViewPygame(FoodDeliveryView):

    def __init__(self, window_size=(800, 600), fps=30):
        super().__init__(window_size, fps)
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Map of Establishments, Customers and Drivers')

    def coordinate(self, coordinate):
        return (map_coordinate(coordinate[0], self.min_x, self.max_x, 0, self.window_size[0]),
                map_coordinate(coordinate[1], self.min_y, self.max_y, 0, self.window_size[1]))

    def render(self, environment):

        self.quited = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quited = True

        if self.quited:
            return

        canvas = pygame.Surface(self.window_size)

        canvas.fill(WHITE)

        for customer in environment.state.customers:
            mapped_x, mapped_y = self.coordinate(customer.coordinate)
            pygame.draw.circle(canvas, BLUE, (int(mapped_x), int(mapped_y)), 5)

        for establishment in environment.state.establishments:
            mapped_x, mapped_y = self.coordinate(establishment.coordinate)
            pygame.draw.circle(canvas, GREEN, (int(mapped_x), int(mapped_y)), 5)

            if hasattr(establishment, "operating_radius"):
                operating_radius_mapped = map_coordinate(establishment.operating_radius, 0, 100, 0, min(self.window_size))
                pygame.draw.circle(canvas, GREEN, (int(mapped_x), int(mapped_y)), int(operating_radius_mapped), 1)

        for driver in environment.state.drivers:
            mapped_x, mapped_y = self.coordinate(driver.coordinate)
            pygame.draw.circle(canvas, RED, (int(mapped_x), int(mapped_y)), 5)
            if driver.status in [DriverStatus.PICKING_UP, DriverStatus.DELIVERING]:
                target_mapped_x, target_mapped_y = self.coordinate(driver.current_route_segment.coordinate)
                pygame.draw.line(canvas, RED, (mapped_x, mapped_y), (target_mapped_x, target_mapped_y), 2)

        self.screen.blit(canvas, canvas.get_rect())
        # pygame.event.pump()
        pygame.display.update()
        self.clock.tick(self.fps)

    def quit(self):
        pygame.display.quit()
        pygame.quit()
