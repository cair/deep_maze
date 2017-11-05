# -*- coding: utf-8 -*-
import random
from queue import PriorityQueue

import pygame
import numpy as np
import scipy.misc



class Maze(object):
    def __init__(self, width=15, height=15, complexity=1, density=1, np_rng=np.random.RandomState(), rng=random.Random()):
        """
        Creates a new maze with the given sizes, with all walls standing.
        """
        self.np_rng = np_rng
        self.rng = rng

        self.maze = self.generate(width, height, complexity, density)
        self.maze = self.maze.reshape((self.maze.shape[0], self.maze.shape[1], 1))
        self.width = self.maze.shape[0]
        self.height = self.maze.shape[1]

    def generate(self, width=10, height=10, complexity=.75, density=.50):
        # Only odd shapes
        shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)

        # Adjust complexity and density relative to maze size
        complexity = int(complexity * (5 * (shape[0] + shape[1])))
        density = int(density * ((shape[0] // 2) * (shape[1] // 2)))

        # Build actual maze
        Z = np.zeros(shape, dtype=np.int8)

        # Fill borders
        Z[0, :] = Z[-1, :] = 1
        Z[:, 0] = Z[:, -1] = 1

        # Make aisles
        for i in range(density):
            x, y = self.np_rng.random_integers(0, shape[1] // 2) * 2, self.np_rng.random_integers(0, shape[0] // 2) * 2
            Z[y, x] = 1

            for j in range(complexity):
                neighbours = []
                if x > 1:
                    neighbours.append((y, x - 2))
                if x < shape[1] - 2:
                    neighbours.append((y, x + 2))
                if y > 1:
                    neighbours.append((y - 2, x))
                if y < shape[0] - 2:
                    neighbours.append((y + 2, x))
                if len(neighbours):
                    y_, x_ = neighbours[self.np_rng.random_integers(0, len(neighbours) - 1)]

                    if Z[y_, x_] == 0:
                        Z[y_, x_] = 1
                        Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                        x, y = x_, y_
        return Z


class ActionSpace:
    def __init__(self):
        self.shape = 4

    @staticmethod
    def sample():
        return random.randint(0, 3)


class StateSpace:
    def __init__(self, game):
        self.shape = game._get_state().shape


class MazeGame(object):
    """
    Class for interactively playing random maze games.
    """

    def __init__(self,
                 width,
                 height,
                 screen_width=640,
                 screen_height=480,
                 state_representation="image",
                 image_state_width=80,
                 image_state_height=80,
                 seed=None,
                 seed_both=False
                 ):

        # Pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("DeepMaze")
        self.font = pygame.font.SysFont("Arial", size=16)
        self.screen = pygame.display.set_mode((screen_width + 5, screen_height + 5), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((255, 255, 255))
        self.txt_up = self.font.render("U", False, (0, 0, 0))
        self.txt_down = self.font.render("D", False, (0, 0, 0))
        self.txt_left = self.font.render("L", False, (0, 0, 0))
        self.txt_right = self.font.render("R", False, (0, 0, 0))
        self.tile_w = (screen_width + 5) / width
        self.tile_h = (screen_height + 5) / height

        # Game Parameters
        self.width = width
        self.height = height
        self.terminal = False

        # State Definition
        self.state_representation = state_representation
        self.image_state_size = (image_state_width, image_state_height)

        # Random Seeding
        self.seed = seed
        self.seed_both = seed_both

        self.rng = random.Random(self.seed if self.seed_both else None)
        self.np_rng = np.random.RandomState(self.seed)

        # Maze Generation
        self.maze = None
        self.optimal_path = None
        self.optimal_path_length = None

        # Players
        self.player, self.target = None, None

        # Reset
        self.reset()

        # q-stuff
        self.q_table = np.zeros(shape=(self.maze.maze.shape[0], self.maze.maze.shape[1]), dtype=np.int8)
        self.q_table.fill(-1)


    @staticmethod
    def rgb2gray(rgb):
        return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])

    def get_state(self):

        if self.state_representation == "image":
            arr = pygame.surfarray.array3d(self.screen)
            arr = scipy.misc.imresize(arr, self.image_state_size)
            arr = arr / 255
            arr = np.expand_dims(arr, axis=0)
            return arr

        elif self.state_representation == "image_gray":
            arr = pygame.surfarray.array3d(self.screen)
            arr = scipy.misc.imresize(arr, self.image_state_size)
            arr = MazeGame.rgb2gray(arr)
            arr = arr.reshape(*arr.shape, 1)
            arr = np.expand_dims(arr, axis=0)
            return arr

        elif self.state_representation == "array":
            state = np.array(self.maze.maze, copy=True)
            state[self.player[0], self.player[1], 0] = 2
            state[self.target[0], self.target[1], 0] = 3
            return state

    def reset(self):
        # Reinitialize RNG
        self.rng = random.Random(self.seed if self.seed_both else None)
        self.np_rng = np.random.RandomState(self.seed)

        # Reset terminal state
        self.terminal = False

        # Create new maze
        self.maze = Maze(self.width, self.height, np_rng=self.np_rng, rng=self.rng)

        # Set player positions
        self.player, self.target = self.spawn_players()

        # Return state
        return self.get_state()

    def _draw(self):

        self.surface.fill((0, 0, 0))

        for (x, y, z), value in np.ndenumerate(self.maze.maze):
            pos = (x * self.tile_w, y * self.tile_h, self.tile_w + 1, self.tile_h + 1)
            color = 0xFFFFFF
            if value == 1:
                color = 0x000000
            pygame.draw.rect(self.surface, color, pos)

            if value == 0:

                txt_type = self.q_table[x, y]
                if txt_type == 1:
                    self.surface.blit(self.txt_down, (pos[0] + 8, pos[1] + 8))  # Down
                if txt_type == 2:
                    self.surface.blit(self.txt_up, (pos[0] + 8, pos[1] + 8))  # Up
                if txt_type == 3:
                    self.surface.blit(self.txt_left, (pos[0] + 8, pos[1] + 8))  # Left
                if txt_type == 4:
                    self.surface.blit(self.txt_right, (pos[0] + 8, pos[1] + 8))  # Right

        pygame.draw.rect(self.surface, 0x00FF00,
                         (self.player[0] * self.tile_w, self.player[1] * self.tile_h, self.tile_w, self.tile_h))
        pygame.draw.rect(self.surface, 0xFF0000,
                         (self.target[0] * self.tile_w, self.target[1] * self.tile_h, self.tile_w, self.tile_h))

        self.screen.blit(self.surface, (0, 0))

        pygame.display.flip()

    def dfs(self, start, goal):
        stack = [(start, [start])]

        possible_path = PriorityQueue()


        while stack:
            (vertex, path) = stack.pop()
            legal_cells = set(self.legal_directions(*vertex)) - set(path)
            for next in legal_cells:
                if next == goal:
                    full_path = path + [next]
                    length = len(path)
                    possible_path.put((length, full_path))
                else:
                    stack.append((next, path + [next]))

        return possible_path.get()

    def spawn_players(self):
        """
        Returns a random position on the maze.
        """
        non_walls = np.where(self.maze.maze == 0)
        non_walls = np.array([(non_walls[0][i], non_walls[1][i]) for i in range(len(non_walls[0]))])


        target_spawn = tuple(self.rng.choice(non_walls))
        while True:  # todo xd
            player_spawn = tuple(self.rng.choice(non_walls))

            if target_spawn != player_spawn:
                break

        self.optimal_path_length, self.optimal_path = self.dfs(player_spawn, target_spawn)


        return player_spawn, target_spawn

    def render(self):
        try:
            self._draw()
        except:
            pass

    def on_return(self, reward):
        return self.get_state(), reward, self.terminal, {
            "optimal_path": self.optimal_path_length
        }

    def step(self, a):
        if self.terminal:
            return self.on_return(1)

        a_vec = self.to_action(a)
        posx, posy = self.player
        nextx, nexty = posx + a_vec[0], posy + a_vec[1]

        if self.is_legal(nextx, nexty):
            self.player = (nextx, nexty)

        if self.player == self.target:
            self.terminal = True
            return self.on_return(1)

        return self.on_return(-0.01)

    def quit(self):
        try:
            pass
            #pygame.display.quit()
            #pygame.quit()
        except:
            pass

    def to_action(self, a):
        if a == 0:
            return 0, 1
        elif a == 1:
            return 0, -1
        elif a == 2:
            return -1, 0
        elif a == 3:
            return 1, 0

    def legal_directions(self, posx, posy):
        legal = []

        possible_moves = [
            (posx + 0, posy + 1),  # Down
            (posx + 0, posy - 1),  # Up
            (posx + 1, posy + 0),  # Left
            (posx - 1, posy + 0)  # Right
        ]

        for possible_move in possible_moves:

            type = self.maze.maze[possible_move[0], possible_move[1], 0]
            if type == 0:
                legal.append(possible_move)

        return legal

    def is_legal(self, nextx, nexty):
        return True if self.maze.maze[nextx, nexty, 0] == 0 else False
