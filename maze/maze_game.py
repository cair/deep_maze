import random
from queue import PriorityQueue

import numpy as np
import scipy.misc
import pygame

from maze import Maze


class MazeGame:

    def __init__(self, maze_size, screen_size=(640, 480), custom_mechanics=None):

        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("DeepMaze")

        self.width, self.height = maze_size

        self.font = pygame.font.SysFont("Arial", size=16)
        self.screen = pygame.display.set_mode(screen_size, 0, 32)


        self.surface_maze = pygame.Surface(self.screen.get_size()).convert()
        self.surface_player = pygame.Surface(self.screen.get_size()).convert()

        # Maze
        self.maze = None

        # Player
        self.player, self.target = None, None

        # Reset the game
        self.reset()

    def get_state(self):
        pass

    def reset(self):

        # Create new maze
        self.maze = Maze(width=self.width, height=self.height)

        # Set player positions
        self.player, self.target = self.spawn_players()

        # Return state
        return self.get_state()



    def spawn_players(self):
        """
        Returns a random position on the maze.
        """
        start_positions = []
        for start_position in [(0, 0), (self.width - 1, self.height - 1)]:
            visited, queue = set(), [start_position]
            while queue:
                vertex = queue.pop(0)

                if self.maze.grid[vertex[0], vertex[1]] == 0:
                    start_positions.append(vertex)
                    queue.clear()
                    continue
                if vertex not in visited:
                    visited.add(vertex)
                    queue.extend(self.maze.grid[vertex[0], vertex[1]] - visited)

        return start_positions

    def _draw(self):

        self.surface.fill((0, 0, 0))

        for (x, y), value in np.ndenumerate(self.maze.grid):
            pos = (x * self.tile_w, y * self.tile_h, self.tile_w + 1, self.tile_h + 1)
            color = 0xFFFFFF
            if value == 1:
                color = 0x000000
            pygame.draw.rect(self.surface, color, pos)

            if value == 0:

                """txt_type = self.q_table[x, y]
                if txt_type == 1:
                    self.surface.blit(self.txt_down, (pos[0] + 8, pos[1] + 8))  # Down
                if txt_type == 2:
                    self.surface.blit(self.txt_up, (pos[0] + 8, pos[1] + 8))  # Up
                if txt_type == 3:
                    self.surface.blit(self.txt_left, (pos[0] + 8, pos[1] + 8))  # Left
                if txt_type == 4:
                    self.surface.blit(self.txt_right, (pos[0] + 8, pos[1] + 8))  # Right"""

        """pygame.draw.rect(self.surface, 0x00FF00,
                         (self.player[0] * self.tile_w, self.player[1] * self.tile_h, self.tile_w, self.tile_h))
        pygame.draw.rect(self.surface, 0xFF0000,
                         (self.target[0] * self.tile_w, self.target[1] * self.tile_h, self.tile_w, self.tile_h))
        """
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



    def render(self):

        self._draw()


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

            type = self.maze.grid[possible_move[0], possible_move[1]]
            if type == 0:
                legal.append(possible_move)

        return legal

    def is_legal(self, nextx, nexty):
        return True if self.maze.maze[nextx, nexty, 0] == 0 else False

