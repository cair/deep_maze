import gym
import gym_maze
import numpy as np
import os
import json
from collections import deque

from example.logger import logger
from example.dqn.dqn_example_4 import DQN

if __name__ == '__main__':
    width = 4
    height = 4

    os.environ["gym_maze_width"] = str(5)
    os.environ["gym_maze_height"] = str(5)
    os.environ["gym_maze_screen_width"] = str(640)
    os.environ["gym_maze_screen_height"] = str(480)
    os.environ["gym_maze_no_random"] = str(0)
    os.environ["gym_maze_change_map_after"] = str(10000000000000)
    os.environ["gym_maze_state_representation"] = "array_3d"
    os.environ["gym_maze_funny"] = str(1)
    os.environ["image_state_width"] = str(80)
    os.environ["image_state_height"] = str(80)

    env = gym.make("maze-v0")
    env.render()

    batch_size = 50
    max_timesteps = 500
    epochs = 15000
    train_epochs = 8
    memory_size = 1000

    agent = DQN(
        env.observation_space.shape,
        env.action_space.shape,
        batch_size=50,
        memory_size=1000,
        train_epochs=8
    )

    _s_l = env.observation_space.shape[1]

    for epoch in range(epochs):

        # Reset environment
        state = env.reset()

        # Set terminal state to false
        terminal = False

        # Score
        epoch_score = 0

        actions = [0, 0, 0, 0]

        for timestep in range(max_timesteps):
            # Draw environment on screen
            #env.render()  # For image you MUST call this

            # Draw action from distribution
            action = agent.act(state)
            actions[action] += 1

            # Perform action in environment
            next_state, reward, terminal, _ = env.step(action)

            epoch_score += reward

            # Temporary Experience replay
            agent.remember(state, action, reward, next_state, terminal)

            if terminal:
                break

        if len(agent.memory) > batch_size:
            agent.replay()

        logger.info(json.dumps({
            "epoch": epoch,
            "score": epoch_score,
            "epsilon": agent.epsilon,
            "loss": agent.average_loss(),
            "terminal": terminal,
            "replay": len(agent.memory),
            "actions": [x / timestep for x in actions]
        }))


