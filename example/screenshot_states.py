import gym
import pygame
from PIL import Image

import gym_maze
import numpy as np
import json
from py_image_stitcher import ImageStitch

if __name__ == '__main__':

    env_list = [
        "maze-img-9x9-full-deterministic-v0",
        "maze-img-11x11-full-deterministic-v0",
        "maze-img-13x13-full-deterministic-v0",
        "maze-img-15x15-full-deterministic-v0",
        "maze-img-17x17-full-deterministic-v0",
        "maze-img-19x19-full-deterministic-v0",
        "maze-img-25x25-full-deterministic-v0",
        "maze-img-35x35-full-deterministic-v0",
    ]

    env = gym.make(env_list[0])
    env.reset()

    st = ImageStitch(dimension=(400, 400), rows=2, columns=4)

    for env_name in env_list:
        env = gym.make(env_name)
        s = env.reset()
        env.env.render()
        data = pygame.image.tostring(env.env.surface, 'RGB')
        img = Image.frombytes('RGB', env.env.surface.get_size(), data)
        st.add(img)

    print(st.save("./environments.png"))










