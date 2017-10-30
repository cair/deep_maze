import gym
import os
from gym import error, spaces, utils
from gym.utils import seeding

from gym_maze.envs.maze import MazeGame


class MazeEnv(gym.Env):
    metadata = {'render.modes': ['array', 'array_flat', 'image', 'image_gray', 'human']}

    def __init__(self):

        self.game = MazeGame(
            int(os.getenv("gym_maze_width", 5)),
            int(os.getenv("gym_maze_height", 5)),
            int(os.getenv("gym_maze_screen_width", 640)),
            int(os.getenv("gym_maze_screen_height", 480)),
            bool(os.getenv("gym_maze_no_random", 0)),
            int(os.getenv("gym_maze_change_map_after", 10)),
            os.getenv("gym_maze_state_representation", "image"),
            bool(os.getenv("gym_maze_funny", 0)),
            int(os.getenv("image_state_width", 80)),
            int(os.getenv("image_state_height", 80))
        )

        self.observation_space = self.game.state_space
        self.action_space = self.game.action_space

    def _step(self, action):
        return self.game.step(action)

    def _reset(self):
        return self.game.reset()

    def _render(self, mode='image', close=False):
        if mode == "human":
            mode = "image"
        self.game.state_representation = mode
        return self.game.render()
