import gym
from gym.envs import register

from cair_maze.maze_game import MazeGame
from cair_maze.mechanics import BaseMazeMechanic


class NoMazeEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    id = "NoMaze-%s-%sx%s-v0"

    class NoMazeMechanic(BaseMazeMechanic):

        def on_start(self):
            pass

        def on_update(self):
            pass

        def on_terminal(self):
            pass

    def __init__(self, width, height, state_type):
        opt = dict(
            algorithm="none",
            disable_target=True
            )
        self.env = MazeGame((width, height), mechanic=NoMazeEnv.NoMazeMechanic, mechanic_args=None, options=opt)

        if state_type == "image":
            self.env.set_preprocess(dict(
                image=dict(),
                #resize=dict(size=(84, 84)),
                #grayscale=dict()
            ))

        self.observation_space = self.env.get_state().shape
        self.action_space = 4

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self, mode='human', close=False):
        if close:
            self.env.quit()
            return None

        return self.env.render()