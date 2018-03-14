from queue import PriorityQueue
import numpy as np
import pygame
from maze import Maze


class Sprite(pygame.sprite.DirtySprite):
    def __init__(self, color, x, y, w, h):
        pygame.sprite.DirtySprite.__init__(self)
        self.w = w
        self.h = h
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.move(x, y)

    def update(self, *args):
        self.dirty = 1

    def set_color(self, color):
        pass

    def move(self, x, y):
        self.rect.move_ip(x * self.w, y * self.h)


class MazeGame:

    def __init__(self, maze_size, screen_size=(640, 480), custom_mechanics=None):

        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("DeepMaze")

        self.width, self.height = maze_size
        self.tile_width, self.tile_height = int(screen_size[0] / maze_size[0]), int(screen_size[1] / maze_size[1])

        self.font = pygame.font.SysFont("Arial", size=16)
        self.screen = pygame.display.set_mode(screen_size, 0, 32)

        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.sprite_maze = [Sprite(color=(255, 0, 255), x=x, w=self.tile_width, y=y, h=self.tile_height) for x in range(self.width) for y in range(self.height)]
        self.sprite_player = Sprite(color=(0, 255, 0), x=0, y=0, w=self.tile_width, h=self.tile_height)
        self.sprite_target = Sprite(color=(255, 0, 0), x=0, y=0, w=self.tile_width, h=self.tile_height)
        self.sprites = pygame.sprite.LayeredDirty(self.sprite_maze, [self.sprite_player, self.sprite_target])

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

        # Update sprite color reflecting the maze state
        for i in range(self.width * self.height):
            x = i % self.width
            y = int((i - x) / self.width)

            val = self.maze.grid[x, y]

            if val == 0:
                self.sprites.get_sprite(i).image.fill(color=(255, 255, 255))
            elif val == 1:
                self.sprites.get_sprite(i).image.fill(color=(0, 0, 0))

        # Set player positions
        self.player, self.target = self.spawn_players()

        # Update player sprites
        self.sprite_player.move(*self.player)
        self.sprite_target.move(*self.target)

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
        rectangles = self.sprites.draw(self.surface)
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update(rectangles)

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

