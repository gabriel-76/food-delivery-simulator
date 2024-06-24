import numpy as np
from gymnasium import Env
from gymnasium.spaces import Dict, Sequence, Box, Discrete, Tuple

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.order.order_status import OrderStatus
from src.main.route.delivery_route_segment import DeliveryRouteSegment
from src.main.route.pickup_route_segment import PickupRouteSegment
from src.main.route.route import Route


class FoodDeliveryGymTestEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, simpy_env: FoodDeliverySimpyEnv, render_mode=None):
        self.simpy_env = simpy_env
        self.observation_space = Dict({
            'num_drivers': Discrete(10000),  # {0, 1, 2, ..., inf} -> 'num_drivers'
            'drivers': Sequence(
                Dict({
                    'coordinates': Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32),  # (x, y)
                    'available': Discrete(2),  # {0, 1} -> {false or true}
                    'capacity': Discrete(1000000000000),  # {0, 1, 2, ..., inf} -> capacity
                    'status': Discrete(3),  # {0, 1, 2} -> {AVAILABLE, PICKING_UP, DELIVERING}
                    'current_route': Sequence(Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32))
                    # [(x, y), (x, y), ...]
                })
            ),
            'num_orders': Discrete(10000),  # {0, 1, 2, ..., inf} -> 'num_orders
            'orders': Sequence(Dict({
                'pickup_coordinate': Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32),  # (x, y)
                'delivery_coordinate': Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32),  # (x, y)
                'status': Discrete(13),  # {0, 1, 2, ... 12} -> order.status
                'required_capacity': Discrete(1000000000000),  # {0, 1, 2, ..., inf} -> required_capacity
            }))
        })

        self.action_space = Sequence(
            Tuple((
                Discrete(10),  # driver index position
                Sequence(Discrete(100))  # order indexes to add a route
            ))
        )

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def route_to_coordinates(self, route):
        if route is None:
            return []
        return [segment.coordinates for segment in route.route_segments]

    def _get_obs(self):
        ready_orders = [order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY]
        drivers = self.simpy_env.state.drivers
        return {
            'num_drivers': len(drivers),
            'drivers': tuple([
                {
                    'coordinates': np.array(driver.coordinates, dtype=np.float32),
                    'available': int(driver.available),
                    'capacity': int(driver.capacity.value),
                    'status': int(driver.status.value),
                    'current_route': tuple([
                        np.array(segment.coordinates, dtype=np.float32)
                        for segment in driver.current_route.route_segments
                    ]) if driver.current_route is not None else ()
                }
                for driver in drivers
            ]),
            'num_orders': len(ready_orders),
            'orders': tuple([
                {
                    'pickup_coordinate': np.array(order.customer.coordinates, dtype=np.float32),
                    'delivery_coordinate': np.array(order.restaurant.coordinates, dtype=np.float32),
                    'status': int(order.status.value),
                    'required_capacity': int(order.required_capacity.value)
                }
                for order in ready_orders
            ])
        }

    def _get_info(self):
        return self.simpy_env.now

    def action_is_valid(self, action) -> bool:
        ready_orders = [order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY]
        drivers = self.simpy_env.state.drivers
        for driver_index, order_indexes in action:
            # print(f'Driver index: {driver_index}, Order indexes: {order_indexes}')
            if driver_index >= len(drivers):
                # print(f'Driver index {driver_index} is out of bounds')
                # raise ValueError(f'Driver index {driver_index} is out of bounds')
                return False
            for order_index in order_indexes:
                # print(f'\tOrder index: {order_index}')
                if order_index >= len(ready_orders):
                    # print(f'Order index {order_index} is out of bounds')
                    # raise ValueError(f'Order index {order_index} is out of bounds')
                    return False
        return True

    def apply_action(self, action) -> None:
        ready_orders = [order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY]
        drivers = self.simpy_env.state.drivers

        if len(ready_orders) == 0 or action is None:
            return

        for driver_index, order_indexes in action:
            print(f'Driver index: {driver_index}, Order indexes: {order_indexes}')
            driver = drivers[driver_index]
            for order_index in order_indexes:
                order = ready_orders[order_index]
                pickup_segment = PickupRouteSegment(order)
                delivery_segment = DeliveryRouteSegment(order)
                route = Route(self.simpy_env, [pickup_segment, delivery_segment])
                driver.receive_route_requests(route)

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.simpy_env = FoodDeliverySimpyEnv(
            map=self.simpy_env.map,
            generators=self.simpy_env.generators,
            optimizer=self.simpy_env.optimizer,
            view=self.simpy_env.view
        )

        observation = self._get_obs()
        info = self._get_info()

        self.render()

        return observation, {'info': info}

    def step(self, action):
        terminated = False
        truncated = False
        assert self.action_space.contains(action), "A ação gerada não está contida no espaço de ação."
        observation = self._get_obs()
        assert self.observation_space.contains(
            observation), "A observação gerada não está contida no espaço de observação."
        info = self._get_info()

        if self.render_mode == "human":
            truncated = self.simpy_env.view.quited

        reward = 1 if terminated else 0

        return observation, reward, terminated, truncated, info

    def run(self, action):
        assert self.action_space.contains(action), "A ação gerada não está contida no espaço de ação."
        terminated = False
        self.simpy_env.run(until=self.simpy_env.now + 1)

        try:
            self.simpy_env.optimizer.action = action
        except ValueError as e:
            print('Error')
            # print(e)
            # terminated = True

        truncated = False
        observation = self._get_obs()
        assert self.observation_space.contains(
            observation), "A observação gerada não está contida no espaço de observação."
        info = self._get_info()

        if self.render_mode == "human":
            truncated = self.simpy_env.view.quited

        reward = 1 if terminated else 0

        if self.action_is_valid(action):
            print('Action is valid')
            self.apply_action(action)
            terminated = False
            reward = 1
        else:
            terminated = True
            reward = -10

        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            self.simpy_env.render()

    def close(self):
        self.simpy_env.close()
