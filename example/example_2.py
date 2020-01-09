
import gym
import random

import time

import gym_maze
import pygame

from cair_maze.maze_game import MazeGame

if __name__ == "__main__":

    env = gym.make("Maze-11x11-NormalMaze-v0")

    while False:
        a = random.randint(0, 3)

        s, r, t, info = env.step(a)
        env.render()

        if t:
            env.reset()

    # Direct initialization
    m = MazeGame((32, 32), mechanic=MazeGame.NormalMaze, mechanic_args=dict(vision=3))
    path = list(reversed(m.maze_optimal_path[1]))

    fps = 0
    path.pop()

    while True:
        nx, ny = path.pop()
        px, py = m.player
        dx, dy = nx - px, ny - py

        if dx == 1:
            a = 3
        elif dx == -1:
            a = 2
        elif dy == 1:
            a = 0
        elif dy == -1:
            a = 1
        else:
            Exception("omg")

        m.render()
        data = m.step(a)
        m.render()
        if m.terminal:
            m.reset()
            path = list(reversed(m.maze_optimal_path[1]))

            path.pop()

