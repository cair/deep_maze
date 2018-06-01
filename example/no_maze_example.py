
import gym
import random

import time

import gym_maze
import pygame
if __name__ == "__main__":
    env = gym.make("NoMaze-Img-4x4-v0")
    while True:
        a = random.randint(0, 3)
        print("Gonna do action " + str(a))
        time.sleep(5)

        s, r, t, info = env.step(a)
        env.render()


        if t:
            env.reset()

    # Direct initialization
    m = MazeGame((11, 11), mechanic=MazeGame.POMDPMaze, mechanic_args=dict(vision=3))
    m.set_preprocess(dict(
        image=dict(),
        #resize=dict(size=(84, 84)),
        #grayscale=dict()
    ))

    fps = 0
    now = time.time()
    while True:
        a = random.randint(0, 3)
        print("Gonna do action " + str(a))
        time.sleep(5)

        data = m.step(a)
        m.render()


        if m.terminal:
            m.reset()

        if time.time() >= now + 1:
            print(fps)
            fps = 0
            now = time.time()

        fps += 1

