from gymnasium import Env, spaces

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv


class FoodDeliveryGymEnv(Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, simpy_env: FoodDeliverySimpyEnv, render_mode=None):
        self.simpy_env = simpy_env
        self.observation_space = spaces.Discrete(1)
        self.action_space = spaces.Discrete(1)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):
        return self.simpy_env.count_ready_orders()

    def _get_info(self):
        return self.simpy_env.now

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
        self.simpy_env.step()
        terminated = False
        truncated = False
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            truncated = self.simpy_env.view.quited

        reward = 1 if terminated else 0

        return observation, reward, terminated, truncated, info

    def run(self, action):
        terminated = False
        truncated = False
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            truncated = self.simpy_env.view.quited

        reward = 1 if terminated else 0

        self.simpy_env.run(until=self.simpy_env.now + 1)
        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            self.simpy_env.render()

    def close(self):
        self.simpy_env.close()

