from math import tanh

import matplotlib.pyplot as plt

from src.main.driver.driver_status import DriverStatus
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment

plt.ion()
fig, ax = plt.subplots()


class GridView:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def extract_coordinates(self, objects):
        x = [obj.coordinates[0] for obj in objects]
        y = [obj.coordinates[1] for obj in objects]
        return x, y

    def view(self):
        x_clients, y_clients = self.extract_coordinates(self.environment.state.clients)
        x_restaurants, y_restaurants = self.extract_coordinates(self.environment.state.restaurants)
        x_drivers, y_drivers = self.extract_coordinates(self.environment.state.drivers)

        ax.clear()

        for driver in self.environment.state.drivers:
            if driver.status in [DriverStatus.COLLECTING, DriverStatus.DELIVERING]:
                x, y = driver.coordinates
                route_x, route_y = driver.current_route.coordinates
                dx, dy = route_x - x, route_y - y
                scale = tanh(driver.movement_rate)
                ax.quiver(x, y, dx, dy, angles='xy', scale_units='xy', scale=scale, color='red', width=0.003)

        # Criar o gráfico de dispersão
        ax.scatter(x_clients, y_clients, color='blue', label='Clients', marker="x", s=6)
        ax.scatter(x_restaurants, y_restaurants, color='green', label='Restaurants', marker="s", s=6)
        ax.scatter(x_drivers, y_drivers, color='red', label='Drivers', marker="o", s=4)

        # Adicionar títulos e rótulos
        ax.set_title('Scatter Plot of Coordinates')
        ax.set_xlabel('X coordinates')
        ax.set_ylabel('Y coordinates')

        # Mostrar o gráfico
        plt.show()
