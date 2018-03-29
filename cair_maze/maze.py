# -*- coding: utf-8 -*-
import random
import time
import numpy as np

from .algorithms import recursive_backtracking, randomized_prim


class ActionSpace:

    def __init__(self, seed):
        self.shape = 4
        self._random = random.Random(x=seed)

    def sample(self):
        return self._random.randint(0, self.shape)


class StateSpace:
    def __init__(self, game):
        self.shape = game.grid.shape


class Maze:
    """
    Maze Class, Creates a Maze Instance that contains the internal data of the maze.
    """
    def __init__(self, width=15, height=15, seed_action=time.time(), maze_algorithm="randomized_prim"):
        """
        Maze Instance, Contains maze generator and the data related to it
        :param width: width of the maze in tiles
        :param height: height of the maze in tiles
        :param seed_action: seed of the action sampler
        :param maze_algorithm: the generator algorithm. currently supported: randomized_prim
        """

        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=np.uint8)
        self.action_space = ActionSpace(seed=seed_action)
        self.state_space = StateSpace(self)
        self.maze_algorithm = maze_algorithm

        # Generate the maze structure
        self._generate()

    def _generate(self):
        """
        Generates the maze based on which algorithm was defined in the constructor
        :return: None
        """
        if self.maze_algorithm == "recursive_backtracking":
            recursive_backtracking(self.grid)
        elif self.maze_algorithm == "randomized_prim":
            randomized_prim(self.grid)
        elif self.maze_algorithm == "none":
            pass
        else:
            raise Exception("No maze generation algorithm called %s" % self.maze_algorithm)


