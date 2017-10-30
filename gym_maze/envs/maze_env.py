import gym
from gym_maze.envs.maze import MazeGame


class MazeEnv(gym.Env):
    metadata = {'render.modes': ['array', 'array_flat', 'image', 'image_gray']}

    def __init__(self, width, height, screen_width=640, screen_height=480, no_random=False, change_map_after=10,
                 state_representation="image", funny=False, image_state_size=(80, 80)):

        self.game = MazeGame(
            width,
            height,
            screen_width,
            screen_height,
            no_random,
            change_map_after,
            state_representation,
            funny,
            image_state_size
        )

        self.action_space = self.game.action_space
        self.observation_space = self.game.state_space

    def _step(self, action):
        return self.game.step(action)

    def _reset(self):
        return self.game.reset()

    def _render(self, mode='image', close=False):
        if close:
            return

        self.game.state_representation = mode
        return self.game.render()
