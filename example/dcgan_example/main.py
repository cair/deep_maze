from collections import namedtuple

import gym
import gym_maze
import random
import numpy as np
from example.dcgan_example.explore.dream import Dream
from example.dcgan_example.memory import ReplayMemory

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


if __name__ == "__main__":


    config = config_class(
        history_length=1,
        batch_size=16,
        screen_width=84,
        screen_height=84,
        screen_dim=1,
        action_size=4,
        cnn_format="N/A",
        memory_size=1000
    )

    memory = ReplayMemory(config)

    dream = Dream(config, memory)

    env = gym.make("NoMaze-Img-4x4-v0")
    s = env.reset()
    for step in range(0, 1000000000000):
        a = random.randint(0, 3)
        s1, r, terminal, info = env.step(a)
        env.render()
        s1 = np.expand_dims(rgb2gray(s1), 2)

        # Add sample to replay buffer
        memory.add(s1, r, a, terminal)

        if step > 50:
            dream.train()

        if step > 50 and step % 500 == 0:
            dream.test()

        s = s1
        if terminal:
            s = env.reset()
