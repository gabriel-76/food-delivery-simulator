from math import tanh

import matplotlib.pyplot as plt

from src.main.driver.driver_status import DriverStatus
from src.main.view.food_delivery_view import FoodDeliveryView


def extract_coordinates(objects):
    x = [obj.coordinates[0] for obj in objects]
    y = [obj.coordinates[1] for obj in objects]
    return x, y


class GridViewMatplotlib(FoodDeliveryView):
    def __init__(self):
        super().__init__()
        plt.ion()
        self.fig, self.ax = plt.subplots()

    def render(self, environment):
        self.quited = False

        self.fig.canvas.mpl_connect('close_event', lambda evt: self.quit())
        if self.quited:
            return

        x_restaurants, y_restaurants = extract_coordinates(environment.state.restaurants)
        x_clients, y_clients = extract_coordinates(environment.state.clients)
        x_drivers, y_drivers = extract_coordinates(environment.state.drivers)

        self.ax.clear()
        circles = []
        for restaurant in environment.state.restaurants:
            if hasattr(restaurant, "operating_radius"):
                circle = plt.Circle(restaurant.coordinates, restaurant.operating_radius, color='green', fill=False)
                circles.append(circle)

        for driver in environment.state.drivers:
            if driver.status in [DriverStatus.COLLECTING, DriverStatus.DELIVERING]:
                x, y = driver.coordinates
                segment_x, segment_y = driver.current_segment.coordinates
                dx, dy = segment_x - x, segment_y - y
                scale = tanh(driver.movement_rate)
                self.ax.quiver(x, y, dx, dy, angles='xy', scale_units='xy', scale=scale, color='red', width=0.003)

        # Criar o gráfico de dispersão
        self.ax.scatter(x_clients, y_clients, color='blue', label='Clients', marker="x", s=10)
        self.ax.scatter(x_restaurants, y_restaurants, color='green', label='Restaurants', marker="s", s=20)
        self.ax.scatter(x_drivers, y_drivers, color='red', label='Drivers', marker="o", s=10)

        for circle in circles:
            self.ax.add_artist(circle)

        # Adicionar títulos e rótulos
        self.ax.set_title('Scatter Plot of Coordinates')
        self.ax.set_xlabel('X coordinates')
        self.ax.set_ylabel('Y coordinates')

        self.ax.set_xlim(0, environment.map.size)
        self.ax.set_ylim(0, environment.map.size)

        plt.pause(self.fps / 1000)

        plt.show()

    def quit(self):
        self.quited = True
        plt.ioff()
