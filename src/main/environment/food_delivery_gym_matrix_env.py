import numpy as np
from gymnasium import Env
from gymnasium.spaces import Dict, Sequence, Box, Discrete, Tuple, MultiDiscrete

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.order.order_status import OrderStatus
from src.main.route.delivery_route_segment import DeliveryRouteSegment
from src.main.route.pickup_route_segment import PickupRouteSegment
from src.main.route.route import Route


class FoodDeliveryGymMatrixEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, simpy_env: FoodDeliverySimpyEnv, num_drivers, num_orders, render_mode=None):
        self.num_drivers = num_drivers
        self.num_orders = num_orders
        self.simpy_env = simpy_env
        self.observation_space = Dict({
            'num_drivers': Discrete(self.num_drivers + 1),
            'drivers': Box(low=-np.inf, high=np.inf, shape=(self.num_drivers, 6), dtype=np.float32),
            # (x, y, available, capacity, status, current_route_size)
            'num_orders': Discrete(self.num_orders + 1),
            'orders': Box(low=-np.inf, high=np.inf, shape=(self.num_orders, 6), dtype=np.float32),
            # (pickup_x, pickup_y, delivery_x, delivery_y, status, required_capacity)
        })

        low = np.array([-1] + [-1] * self.num_orders, dtype=np.int64)
        high = np.array([self.num_drivers - 1] + [self.num_orders - 1] * self.num_orders, dtype=np.int64)
        low_matrix = np.array([low] * self.num_drivers, dtype=np.int64)
        high_matrix = np.array([high] * self.num_drivers, dtype=np.int64)

        self.action_space = Box(
            low=low_matrix,
            high=high_matrix,
            # shape=(2 * self.num_drivers, 2 + self.num_orders),
            dtype=np.float32
        )

        # low = np.array([-1] + [-1] + [-1] * self.num_orders, dtype=np.int64)
        # high = np.array([self.num_drivers - 1] + [1] + [self.num_orders - 1] * self.num_orders, dtype=np.int64)
        # low_matrix = np.array([low] * self.num_drivers, dtype=np.int64)
        # high_matrix = np.array([high] * self.num_drivers, dtype=np.int64)
        #
        # self.action_space = Box(
        #     low=low_matrix,
        #     high=high_matrix,
        #     # shape=(2 * self.num_drivers, 2 + self.num_orders),
        #     dtype=np.float32
        # )

        # # Defina os limites inferiores e superiores
        # low = [-1, 0] + [0] * self.num_orders
        # high = [self.num_drivers - 1, 1] + [self.num_orders - 1] * self.num_orders
        # vec = [high[i] - low[i] + 1 for i in range(len(low))]
        #
        # # Crie o espaço MultiDiscrete
        # nvec = np.array(vec * self.num_drivers, dtype=np.int32)
        # print('nvec', nvec)
        # self.action_space = MultiDiscrete(nvec)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def route_to_coordinates(self, route):
        if route is None:
            return []
        return [segment.coordinates for segment in route.route_segments]

    def _get_obs(self):
        ready_orders = [order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY]
        drivers = self.simpy_env.state.drivers
        final_driver_matrix = np.zeros((self.num_drivers, 6), dtype=np.float32)
        driver_matrix = np.array([
            np.array([
                driver.coordinates[0],
                driver.coordinates[1],
                driver.available,
                driver.capacity.value,
                driver.status.value,
                len(driver.current_route.route_segments) if driver.current_route is not None else 0
            ], dtype=np.float32)
            for driver in drivers
        ])

        if len(driver_matrix) > 0:
            final_driver_matrix[:driver_matrix.shape[0], :driver_matrix.shape[1]] = driver_matrix

        final_order_matrix = np.zeros((self.num_orders, 6), dtype=np.float32)
        order_matrix = np.array([
            np.array([
                order.customer.coordinates[0],
                order.customer.coordinates[1],
                order.restaurant.coordinates[0],
                order.restaurant.coordinates[1],
                order.status.value,
                order.required_capacity.value
            ], dtype=np.float32)
            for order in ready_orders
        ])
        if len(order_matrix) > 0:
            final_order_matrix[:order_matrix.shape[0], :order_matrix.shape[1]] = order_matrix

        obs = {
            'num_drivers': len(drivers),
            'drivers': final_driver_matrix,
            'num_orders': len(ready_orders),
            'orders': final_order_matrix
        }
        # print(obs)

        return obs

    def _get_info(self):
        return {'info': self.simpy_env.now}

    def action_is_valid(self, action) -> bool:
        # print(action)
        # ready_orders = [order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY]
        # num_ready_orders = len(ready_orders)
        # for lines in action:
        #     if lines[0] >= self.num_drivers:
        #         return False
        #     if lines[1] >= 2:
        #         return False
        #     for order_index in lines[2:]:
        #         if order_index >= num_ready_orders:
        #             return False
        #
        # return True

        ready_orders = [order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY]
        num_ready_orders = len(ready_orders)
        for lines in action:
            if lines[0] >= self.num_drivers:
                return False
            for order_index in lines[1:]:
                if order_index >= num_ready_orders:
                    return False

        return True

        # for i in range(len(action)):
        #     for j in range(len(action[i])):
        #         driver_index = action[i][0]
        #         rout_segment_type = action[i][1]
        #         order_indexes = list(filter(lambda index: -1 < index < self.num_orders, action[i][2:]))
        #         if driver_index >= self.num_drivers:
        #             return False
        #         if rout_segment_type >= 2:
        #             return False
        #         if len(order_indexes) > 0:
        #             for order_index in order_indexes:
        #                 if order_index >= num_ready_orders:
        #                     return False
        #
        #         if driver_index > -1 and rout_segment_type == 0:



        return True


    def apply_action(self, action) -> None:
        # print(action)
        ready_orders = [order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY]
        drivers = self.simpy_env.state.drivers

        if len(ready_orders) == 0 or action is None:
            return

        for line in action:
            if -1 < line[0] < self.num_drivers and -1 < line[1] < 2:
                driver_index = line[0]
                order_indexes = list(filter(lambda index: -1 < index < self.num_orders, line[1:]))
                if len(order_indexes) > 0:
                    driver = drivers[driver_index]
                    for order_index in order_indexes:
                        order = ready_orders[order_index]
                        pickup_segment = PickupRouteSegment(order)
                        delivery_segment = DeliveryRouteSegment(order)
                        route = Route(self.simpy_env, [pickup_segment, delivery_segment])
                        driver.receive_route_requests(route)

        # for line in action:
        #     if -1 < line[0] < self.num_drivers and -1 < line[1] < 2:
        #         driver_index = line[0]
        #         rout_segment_type = line[1]
        #         order_indexes = list(filter(lambda index: -1 < index < self.num_orders, line[2:]))
        #         if len(order_indexes) > 0:
        #             driver = drivers[driver_index]
        #             for order_index in order_indexes:
        #                 order = ready_orders[order_index]
        #                 pickup_segment = PickupRouteSegment(order)
        #                 delivery_segment = DeliveryRouteSegment(order)
        #                 route = Route(self.simpy_env, [pickup_segment, delivery_segment])
        #                 driver.receive_route_requests(route)
                        # if rout_segment_type == 0:
                        #     pickup_segment = PickupRouteSegment(order)
                        #     route = Route(self.simpy_env, [pickup_segment])
                        #     driver.receive_route_requests(route)
                        # elif rout_segment_type == 1:
                        #     delivery_segment = DeliveryRouteSegment(order)
                        #     route = Route(self.simpy_env, [delivery_segment])
                        #     driver.receive_route_requests(route)

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

        return observation, info

    def step(self, action):
        action = np.round(action).astype(np.int32)
        return self.run(action)

    def run(self, action):
        # assert self.action_space.contains(action), "A ação gerada não está contida no espaço de ação."
        terminated = False
        self.simpy_env.run(until=self.simpy_env.now + 1)

        truncated = False
        observation = self._get_obs()
        assert self.observation_space.contains(
            observation), "A observação gerada não está contida no espaço de observação."
        info = self._get_info()

        if self.render_mode == "human":
            truncated = self.simpy_env.view.quited

        if self.action_is_valid(action):
            # print('Action is valid')
            self.apply_action(action)
            terminated = False
            num_delivered = len(list(filter(lambda order: order.status == OrderStatus.DELIVERED, self.simpy_env.state.orders)))
            reward = 1 + num_delivered
        else:
            terminated = True
            reward = -2

        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            self.simpy_env.render()

    def close(self):
        self.simpy_env.close()
