from src.main.driver.driver import Driver
from src.main.map.map import Map
from src.main.order.order_status import OrderStatus
from src.main.trip.route import Route
from src.main.trip.route_type import RouteType

WEIGHT_TIME = 1
WEIGHT_DISTANCE = 1
MAX_PENALTY = float('inf')


def penalty(route: Route):
    if route.route_type is RouteType.COLLECT and route.order.status <= OrderStatus.DRIVER_ACCEPTED:
        return 0
    if route.route_type is RouteType.DELIVERY and route.order.status <= OrderStatus.COLLECTED:
        return 0
    return MAX_PENALTY


def delay(map: Map, driver: Driver, route: Route):
    current_delay = 0
    if driver.current_route is not None:
        current_delay = map.estimated_time(
            driver.coordinates,
            driver.current_route.coordinates,
            driver.movement_rate
        )
    new_route_delay = map.estimated_time(
        driver.coordinates,
        route.coordinates,
        driver.movement_rate
    )
    return current_delay + new_route_delay


def distance(map: Map, driver: Driver, route: Route):
    current_distance = 0
    if driver.current_route is not None:
        current_distance = map.distance(
            driver.coordinates,
            driver.current_route.coordinates
        )
    new_route_distance = map.distance(
        driver.coordinates,
        route.coordinates
    )
    return current_distance + new_route_distance


def cost(map: Map, driver: Driver, route: Route):
    value = WEIGHT_TIME * delay(map, driver, route) + WEIGHT_DISTANCE * distance(map, driver, route) + penalty(route)
    # print(f"Cost: {value}")
    return value
