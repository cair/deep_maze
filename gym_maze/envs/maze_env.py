import gym
import os
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random
from gym_maze.envs.maze import MazeGame


class MazeEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    id = "maze-v0"

    def __init__(self, width, height, state_type, seed=None, full_deterministic=False):

        self.env = MazeGame(
            width, height, 640, 480, state_type, 80, 80, seed=seed, seed_both=full_deterministic
        )

        self.observation_space = self.env.get_state().shape
        self.action_space = 4

    def _step(self, action):
        return self.env.step(action)

    def _reset(self):
        return self.env.reset()

    def _render(self, mode='human', close=False):
        if close:
            self.env.quit()
            return None

        return self.env.render()


class MazeArr9x9Env(MazeEnv):
    id = "maze-arr-9x9-deterministic-v0"

    def __init__(self):
        super(MazeArr9x9Env, self).__init__(9, 9, "array", 1337)


class MazeImg9x9Env(MazeEnv):
    id = "maze-img-9x9-deterministic-v0"

    def __init__(self):
        super(MazeImg9x9Env, self).__init__(9, 9, "image", 1337)


class MazeArr11x11Env(MazeEnv):
    id = "maze-arr-11x11-deterministic-v0"

    def __init__(self):
        super(MazeArr11x11Env, self).__init__(11, 11, "array", 1337)


class MazeImg11x11Env(MazeEnv):
    id = "maze-img-11x11-deterministic-v0"

    def __init__(self):
        super(MazeImg11x11Env, self).__init__(11, 11, "image", 1337)


class MazeArr13x13Env(MazeEnv):
    id = "maze-arr-13x13-deterministic-v0"

    def __init__(self):
        super(MazeArr13x13Env, self).__init__(13, 13, "array", 1337)


class MazeImg13x13Env(MazeEnv):
    id = "maze-img-13x13-deterministic-v0"

    def __init__(self):
        super(MazeImg13x13Env, self).__init__(13, 13, "image", 1337)


class MazeArr15x15Env(MazeEnv):
    id = "maze-arr-15x15-deterministic-v0"

    def __init__(self):
        super(MazeArr15x15Env, self).__init__(15, 15, "array", 1337)


class MazeImg15x15Env(MazeEnv):
    id = "maze-img-15x15-deterministic-v0"

    def __init__(self):
        super(MazeImg15x15Env, self).__init__(15, 15, "image", 1337)


class MazeArr17x17Env(MazeEnv):
    id = "maze-arr-17x17-deterministic-v0"

    def __init__(self):
        super(MazeArr17x17Env, self).__init__(17, 17, "array", 1337)


class MazeImg17x17Env(MazeEnv):
    id = "maze-img-17x17-deterministic-v0"

    def __init__(self):
        super(MazeImg17x17Env, self).__init__(17, 17, "image", 1337)


class MazeArr19x19Env(MazeEnv):
    id = "maze-arr-19x19-deterministic-v0"

    def __init__(self):
        super(MazeArr19x19Env, self).__init__(19, 19, "array", 1337)


class MazeImg19x19Env(MazeEnv):
    id = "maze-img-19x19-deterministic-v0"

    def __init__(self):
        super(MazeImg19x19Env, self).__init__(19, 19, "image", 1337)


class MazeArr25x25Env(MazeEnv):
    id = "maze-arr-25x25-deterministic-v0"

    def __init__(self):
        super(MazeArr25x25Env, self).__init__(25, 25, "array", 1337)


class MazeImg25x25Env(MazeEnv):
    id = "maze-img-25x25-deterministic-v0"

    def __init__(self):
        super(MazeImg25x25Env, self).__init__(25, 25, "image", 1337)


class MazeArr35x35Env(MazeEnv):
    id = "maze-arr-35x35-deterministic-v0"

    def __init__(self):
        super(MazeArr35x35Env, self).__init__(35, 35, "array", 1337)


class MazeImg35x35Env(MazeEnv):
    id = "maze-img-35x35-deterministic-v0"

    def __init__(self):
        super(MazeImg35x35Env, self).__init__(35, 35, "image", 1337)


class MazeArr55x55Env(MazeEnv):
    id = "maze-arr-55x55-deterministic-v0"

    def __init__(self):
        super(MazeArr55x55Env, self).__init__(55, 55, "array", 1337)


class MazeImg55x55Env(MazeEnv):
    id = "maze-img-55x55-deterministic-v0"

    def __init__(self):
        super(MazeImg55x55Env, self).__init__(55, 55, "image", 1337)













class MazeArrFullDet9x9Env(MazeEnv):
    id = "maze-arr-9x9-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet9x9Env, self).__init__(9, 9, "array", 1337, full_deterministic=True)


class MazeImgFullDet9x9Env(MazeEnv):
    id = "maze-img-9x9-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet9x9Env, self).__init__(9, 9, "image", 1337, full_deterministic=True)


class MazeArrFullDet11x11Env(MazeEnv):
    id = "maze-arr-11x11-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet11x11Env, self).__init__(11, 11, "array", 1337, full_deterministic=True)


class MazeImgFullDet11x11Env(MazeEnv):
    id = "maze-img-11x11-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet11x11Env, self).__init__(11, 11, "image", 1337, full_deterministic=True)


class MazeArrFullDet13x13Env(MazeEnv):
    id = "maze-arr-13x13-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet13x13Env, self).__init__(13, 13, "array", 1337, full_deterministic=True)


class MazeImgFullDet13x13Env(MazeEnv):
    id = "maze-img-13x13-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet13x13Env, self).__init__(13, 13, "image", 1337, full_deterministic=True)


class MazeArrFullDet15x15Env(MazeEnv):
    id = "maze-arr-15x15-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet15x15Env, self).__init__(15, 15, "array", 1337, full_deterministic=True)


class MazeImgFullDet15x15Env(MazeEnv):
    id = "maze-img-15x15-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet15x15Env, self).__init__(15, 15, "image", 1337, full_deterministic=True)


class MazeArrFullDet17x17Env(MazeEnv):
    id = "maze-arr-17x17-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet17x17Env, self).__init__(17, 17, "array", 1337, full_deterministic=True)


class MazeImgFullDet17x17Env(MazeEnv):
    id = "maze-img-17x17-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet17x17Env, self).__init__(17, 17, "image", 1337, full_deterministic=True)


class MazeArrFullDet19x19Env(MazeEnv):
    id = "maze-arr-19x19-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet19x19Env, self).__init__(19, 19, "array", 1337, full_deterministic=True)


class MazeImgFullDet19x19Env(MazeEnv):
    id = "maze-img-19x19-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet19x19Env, self).__init__(19, 19, "image", 1337, full_deterministic=True)


class MazeArrFullDet25x25Env(MazeEnv):
    id = "maze-arr-25x25-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet25x25Env, self).__init__(25, 25, "array", 1337, full_deterministic=True)


class MazeImgFullDet25x25Env(MazeEnv):
    id = "maze-img-25x25-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet25x25Env, self).__init__(25, 25, "image", 1337, full_deterministic=True)


class MazeArrFullDet35x35Env(MazeEnv):
    id = "maze-arr-35x35-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet35x35Env, self).__init__(35, 35, "array", 1337, full_deterministic=True)


class MazeImgFullDet35x35Env(MazeEnv):
    id = "maze-img-35x35-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet35x35Env, self).__init__(35, 35, "image", 1337, full_deterministic=True)


class MazeArrFullDet55x55Env(MazeEnv):
    id = "maze-arr-55x55-full-deterministic-v0"

    def __init__(self):
        super(MazeArrFullDet55x55Env, self).__init__(55, 55, "array", 1337, full_deterministic=True)


class MazeImgFullDet55x55Env(MazeEnv):
    id = "maze-img-55x55-full-deterministic-v0"

    def __init__(self):
        super(MazeImgFullDet55x55Env, self).__init__(55, 55, "image", 1337, full_deterministic=True)


















class MazeArrRnd9x9Env(MazeEnv):
    id = "maze-arr-9x9-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd9x9Env, self).__init__(9, 9, "array", None)


class MazeImgRnd9x9Env(MazeEnv):
    id = "maze-img-9x9-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd9x9Env, self).__init__(9, 9, "image", None)


class MazeArrRnd11x11Env(MazeEnv):
    id = "maze-arr-11x11-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd11x11Env, self).__init__(11, 11, "array", None)


class MazeImgRnd11x11Env(MazeEnv):
    id = "maze-img-11x11-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd11x11Env, self).__init__(11, 11, "image", None)


class MazeArrRnd13x13Env(MazeEnv):
    id = "maze-arr-13x13-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd13x13Env, self).__init__(13, 13, "array", None)


class MazeImgRnd13x13Env(MazeEnv):
    id = "maze-img-13x13-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd13x13Env, self).__init__(13, 13, "image", None)


class MazeArrRnd15x15Env(MazeEnv):
    id = "maze-arr-15x15-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd15x15Env, self).__init__(15, 15, "array", None)


class MazeImgRnd15x15Env(MazeEnv):
    id = "maze-img-15x15-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd15x15Env, self).__init__(15, 15, "image", None)


class MazeArrRnd17x17Env(MazeEnv):
    id = "maze-arr-17x17-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd17x17Env, self).__init__(17, 17, "array", None)


class MazeImgRnd17x17Env(MazeEnv):
    id = "maze-img-17x17-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd17x17Env, self).__init__(17, 17, "image", None)


class MazeArrRnd19x19Env(MazeEnv):
    id = "maze-arr-19x19-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd19x19Env, self).__init__(19, 19, "array", None)


class MazeImgRnd19x19Env(MazeEnv):
    id = "maze-img-19x19-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd19x19Env, self).__init__(19, 19, "image", None)


class MazeArrRnd25x25Env(MazeEnv):
    id = "maze-arr-25x25-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd25x25Env, self).__init__(25, 25, "array", None)


class MazeImgRnd25x25Env(MazeEnv):
    id = "maze-img-25x25-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd25x25Env, self).__init__(25, 25, "image", None)


class MazeArrRnd35x35Env(MazeEnv):
    id = "maze-arr-35x35-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd35x35Env, self).__init__(35, 35, "array", None)


class MazeImgRnd35x35Env(MazeEnv):
    id = "maze-img-35x35-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd35x35Env, self).__init__(35, 35, "image", None)


class MazeArrRnd55x55Env(MazeEnv):
    id = "maze-arr-55x55-stochastic-v0"

    def __init__(self):
        super(MazeArrRnd55x55Env, self).__init__(55, 55, "array", None)


class MazeImgRnd55x55Env(MazeEnv):
    id = "maze-img-55x55-stochastic-v0"

    def __init__(self):
        super(MazeImgRnd55x55Env, self).__init__(55, 55, "image", None)
