# -*- coding: utf-8 -*-
import random
import numpy as np

from algorithms import recursive_backtracking, randomized_prim




class ActionSpace:
    def __init__(self, seed):
        self.shape = 4
        self._random = random.Random(x=seed)

    def sample(self):
        return self._random.randint(0, self.shape)


class StateSpace:
    def __init__(self, game):
        self.shape = game.get_shape().shape


class Maze:
    def __init__(self,
                 width=15,
                 height=15,
                 complexity=1,
                 density=1,
                 seed_action=1337,
                 maze_algorithm="randomized_prim"):

        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=np.uint8)
        self.action_space = ActionSpace(seed=seed_action)
        #self.state_space = StateSpace(self)
        self.maze_algorithm = maze_algorithm

        # Generate the maze structure
        self._generate()

    def _generate(self):
        if self.maze_algorithm == "recursive_backtracking":
            recursive_backtracking(self.grid)
        if self.maze_algorithm == "randomized_prim":
            randomized_prim(self.grid)


