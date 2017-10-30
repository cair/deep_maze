import json
from collections import deque

import pyximport;

from gym_maze.envs import logger

pyximport.install()
from gym_maze.envs.maze import MazeGame
from dqn.dqn import DQN

if __name__ == '__main__':
    width = 4
    height = 4

    env = MazeGame(width, height, no_random=True, change_map_after=9999999999, state_representation="image", funny=False)
    env.render()

    agent = DQN(env.state_space.shape, env.action_space.shape)
    batch_size = 32

    # Temporary memory
    temporary_memory = []

    temporary_memory_max_steps = 30
    timeout = 50

    # 7x7
    #temporary_memory_max_steps = 200
    #timeout = 2000

    # Failure compensation
    recent_games = deque(maxlen=10)
    maximum_loss_rate = .5
    epsilon_boost = .05

    while True:

        # Reset environment
        s = env.reset()

        # Set terminal state to false
        terminal = False

        # Step counter (Increased per action)
        step_counter = 0

        # Reset Temporary memory
        temporary_memory.clear()

        while not terminal:
            # Draw environment on screen
            env.render()  # For image you MUST call this

            # Draw action from distribution
            a = agent.act(s)

            # Perform action in environment
            s1, r, t, _ = env.step(a)
            terminal = t

            # Temporary Experience replay
            temporary_memory.append((s, a, r, s1, t))

            step_counter += 1

            # Just give up on when failing horribly
            if step_counter >= timeout:

                # Add a loss
                recent_games.append(False)

                # Also boost epsilon if the AI is failing horribly (Need more good experiences)
                if len(recent_games) > 1:
                    loss_rate = recent_games.count(False) / len(recent_games)
                    if loss_rate > maximum_loss_rate:
                        agent.epsilon = min(1.0, agent.epsilon + epsilon_boost)

                break

            s = s1

        # Evaluate how good this round was
        if step_counter < temporary_memory_max_steps:
            # Add a victory
            recent_games.append(True)

        for experience in temporary_memory:
                agent.remember(*experience)

        # Train
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        env.render()

        logger.logger.info(json.dumps({
            "steps": step_counter,
            "epsilon": agent.epsilon,
            "loss": agent.average_loss(),
            "terminal": terminal,
            "loss_rate": recent_games.count(False) / (len(recent_games)+0.0001)
        }))



