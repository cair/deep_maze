# -*- coding: utf-8 -*-
import random
import pygame
import base64
import numpy as np
import scipy.misc
from io import BytesIO

from PIL import Image

pygame.init()

# Easy to read representation for each cardinal direction.
N, S, W, E = ('n', 's', 'w', 'e')


class Cell(object):
    """
    Maze class containing full board and maze generation algorithms.
    """
    CELL_TYPES = {(E, N, S, W): 15,
                  (E, N, S): 14,
                  (E, N, W): 13,
                  (E, S, W): 12,
                  (E, S): 11,
                  (E, N): 10,
                  (E, W): 9,
                  (E,): 8,
                  (N, S, W): 7,
                  (N, S): 6,
                  (N, W): 5,
                  (S, W): 4,
                  (S,): 3,
                  (N,): 2,
                  (W,): 1,
                  (): 0,
                  }

    """
    Class for each individual cell. Knows only its position and which walls are
    still standing.
    """

    def __init__(self, x, y, walls):
        self.x = x
        self.y = y
        self.walls = set(walls)
        self.legal_moves = None
        self.type = None

    def done(self):
        self.legal_moves = list({N, S, W, E} - self.walls)
        self.type = Cell.CELL_TYPES[tuple(sorted(self.walls))]  # inefficient TODO

    def legal_directions(self):
        return self.legal_moves

    def is_full(self):
        """
        Returns True if all walls are still standing.
        """
        return len(self.walls) == 4

    def _wall_to(self, other):
        """
        Returns the direction to the given cell from the current one.
        Must be one cell away only.
        """
        assert abs(self.x - other.x) + abs(self.y - other.y) == 1, '{}, {}'.format(self, other)
        if other.y < self.y:
            return N
        elif other.y > self.y:
            return S
        elif other.x < self.x:
            return W
        elif other.x > self.x:
            return E
        else:
            assert False

    def connect(self, other):
        """
        Removes the wall between two adjacent cells.
        """
        other.walls.remove(other._wall_to(self))
        self.walls.remove(self._wall_to(other))


class Maze(object):
    def __init__(self, width=20, height=10):
        """
        Creates a new maze with the given sizes, with all walls standing.
        """
        self.width = width
        self.height = height
        self.cells = []

        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(Cell(x, y, [N, S, E, W]))

    def __getitem__(self, index):
        """
        Returns the cell at index = (x, y).
        """
        x, y = index
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x + y * self.width]
        else:
            return None

    def state(self):
        _state = np.zeros(shape=(self.width, self.height, 2), dtype=np.float)
        for cell in self.cells:
            _state[cell.x, cell.y, 0] = cell.type
        return _state

    def state_flat(self):
        return [cell.type for cell in self.cells]

    def neighbors(self, cell):
        """
        Returns the list of neighboring cells, not counting diagonals. Cells on
        borders or corners may have less than 4 neighbors.
        """
        x = cell.x
        y = cell.y
        for new_x, new_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            neighbor = self[new_x, new_y]
            if neighbor is not None:
                yield neighbor

    def randomize(self):
        """
        Knocks down random walls to build a random perfect maze.

        Algorithm from http://mazeworks.com/mazegen/mazetut/index.htm
        """
        cell_stack = []
        cell = random.choice(self.cells)
        n_visited_cells = 1

        while n_visited_cells < len(self.cells):
            neighbors = [c for c in self.neighbors(cell) if c.is_full()]
            if len(neighbors):
                neighbor = random.choice(neighbors)
                cell.connect(neighbor)
                cell_stack.append(cell)
                cell = neighbor
                n_visited_cells += 1
            else:
                cell = cell_stack.pop()

        for cell in self.cells:
            cell.done()

    @staticmethod
    def generate(width=20, height=10):
        """
        Returns a new random perfect maze with the given sizes.
        """
        m = Maze(width, height)
        m.randomize()
        return m


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

    def __init__(self, width, height, screen_width=640, screen_height=480, no_random=0, change_map_after=10,
                 state_representation="image", funny=0, image_state_width=80, image_state_height=80):
        self.w, self.h = width, height
        self.maze = Maze.generate(width, height)
        self.player = self._get_random_position()
        self.target = self._get_random_position()
        pygame.display.set_caption("DeepMaze")
        self.screen = pygame.display.set_mode((screen_width + 5, screen_height + 5), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.maze_surface = pygame.Surface(self.screen.get_size())
        self.surface.fill((255, 255, 255))
        self.image_state_size = (image_state_width, image_state_height)
        self.tile_w = (screen_width+5) / width
        self.tile_h = (screen_height+5) / height

        if funny == 1:
            self.base_trump = b'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'
            self.base_kim = b'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'

            self.img_trump = pygame.image.load(BytesIO(base64.b64decode(self.base_trump)))
            self.img_trump = pygame.transform.scale(self.img_trump, (int(self.tile_w), int(self.tile_h)))

            self.img_kim = pygame.image.load(BytesIO(base64.b64decode(self.base_kim)))
            self.img_kim = pygame.transform.scale(self.img_kim, (int(self.tile_w), int(self.tile_h)))
        else:
            self.img_kim = pygame.Surface((int(self.tile_w), int(self.tile_h) - 5))
            self.img_trump = pygame.Surface((int(self.tile_w), int(self.tile_h) - 5))
            self.img_kim.fill((255, 0, 0))
            self.img_trump.fill((0, 255, 0))

        self.actions = {0: N, 1: S, 2: E, 3: W}
        self.action_direction = {
            N: (0, -1),
            S: (0, 1),
            E: (1, 0),
            W: (-1, 0)
        }
        self.terminal = False
        self.change_map_counter = 0
        self.no_random = no_random
        self.change_map_after = change_map_after
        self.seed = "This is a awesome seed!!!!"
        self.state_representation = state_representation

        self.action_space = ActionSpace()
        self.state_space = StateSpace(self)

    @staticmethod
    def rgb2gray(rgb):
        return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])

    def _get_state(self):
        if self.state_representation == "image":
            arr = pygame.surfarray.array3d(self.screen)
            arr = scipy.misc.imresize(arr, self.image_state_size)
            arr = arr / 255

            #im = Image.fromarray(np.uint8(arr*255))
            #im.save("test.png")

            arr = np.expand_dims(arr, axis=0)
            return arr
        elif self.state_representation == "image_gray":
            arr = pygame.surfarray.array3d(self.screen)
            arr = scipy.misc.imresize(arr, self.image_state_size)
            #arr /= 255
            arr = MazeGame.rgb2gray(arr)
            arr = arr.reshape(*arr.shape, 1)
            arr = np.expand_dims(arr, axis=0)
            return arr
        elif self.state_representation == "array":
            state = self.maze.state()
            state[self.player[0], self.player[1], 1] = 1
            state[self.target[0], self.target[1], 1] = 2
            return np.expand_dims(state, axis=0)
        elif self.state_representation == "array_flat":
            state = np.array(self.maze.state_flat())
            return np.expand_dims(state, axis=0)
        elif self.state_representation == "array_3d":
            state = np.zeros(shape=(1, self.w, self.h, 4))
            for cell in self.maze.cells:
                if 'n' in cell.walls:
                    state[0, cell.x, cell.y, 0] = 1
                if 's' in cell.walls:
                    state[0, cell.x, cell.y, 1] = 1
                if 'e' in cell.walls:
                    state[0, cell.x, cell.y, 2] = 1
                if 'w' in cell.walls:
                    state[0, cell.x, cell.y, 3] = 1
            return state

    def reset(self):
        self.change_map_counter += 1
        if not self.no_random == 0 and self.change_map_counter > self.change_map_after:
            self.seed += "!"
            self.change_map_counter = 0
        random.seed(self.seed)

        self.maze = Maze.generate(self.w, self.h)
        self.player = self._get_random_position()
        self.target = self._get_random_position()
        self.terminal = False

        return self._get_state()

    def _draw(self):

        self.maze_surface.fill((0, 0, 0))

        for cell in self.maze.cells:
            x = (cell.x * self.tile_w)
            y = (cell.y * self.tile_h)

            if N in cell.walls:
                start = [x, y]
                end = [x + self.tile_w, y]
                pygame.draw.line(self.maze_surface, 0xFFFFFF, start, end, 5)
            if S in cell.walls:
                start = [x, y + self.tile_h]
                end = [x + self.tile_w, y + self.tile_h]
                pygame.draw.line(self.maze_surface, 0xFFFFFF, start, end, 5)
            if W in cell.walls:
                start = [x, y]
                end = [x, y + self.tile_h]
                pygame.draw.line(self.maze_surface, 0xFFFFFF, start, end, 5)
            if E in cell.walls:
                start = [x + self.tile_w, y]
                end = [x + self.tile_w, y + self.tile_h]
                pygame.draw.line(self.maze_surface, 0xFFFFFF, start, end, 5)

        # Draw target
        pygame.Surface.blit(self.maze_surface, self.img_trump, (
            (self.player[0] * self.tile_w) + 3,
            (self.player[1] * self.tile_h) + 3
        ))

        # Draw target
        pygame.Surface.blit(self.maze_surface, self.img_kim, (
            (self.target[0] * self.tile_w) + 3,
            (self.target[1] * self.tile_h) + 3
        ))

        self.surface.blit(self.maze_surface, (0, 0))
        self.screen.blit(self.surface, (0, 0))

        pygame.display.flip()

    def _get_random_position(self):
        """
        Returns a random position on the maze.
        """
        return (random.randrange(0, self.maze.width),
                random.randrange(0, self.maze.height))

    def render(self):
        self._draw()

    def step(self, a):
        if self.terminal:
            return self._get_state(), 1, self.terminal, {}

        current_cell = self.maze[self.player]
        a_str = self.actions[a]
        a_dx, a_dy = self.action_direction[a_str]

        if a_str not in current_cell.legal_directions():
            return self._get_state(), -1, self.terminal, {}

        self.player = (self.player[0] + a_dx, self.player[1] + a_dy)

        if self.player == self.target:
            self.terminal = True
            return self._get_state(), 1, self.terminal, {}

        return self._get_state(), -1, self.terminal, {}

    def next_level(self):
        self.seed += "!"
