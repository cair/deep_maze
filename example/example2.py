import gym
import gym_maze


import os
import json
from collections import deque

from example.logger import logger
from example.dqn.dqn import DQN

if __name__ == '__main__':
    width = 4
    height = 4

    os.environ["gym_maze_width"] = str(6)
    os.environ["gym_maze_height"] = str(6)
    os.environ["gym_maze_screen_width"] = str(640)
    os.environ["gym_maze_screen_height"] = str(480)
    os.environ["gym_maze_no_random"] = str(0)
    os.environ["gym_maze_change_map_after"] = str(10000000000000)
    os.environ["gym_maze_state_representation"] = "array_3d"
    os.environ["gym_maze_funny"] = str(0)
    os.environ["image_state_width"] = str(80)
    os.environ["image_state_height"] = str(80)

    env = gym.make("maze-v0")
    env.render()

    agent = DQN(env.observation_space.shape, env.action_space.shape)
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

    action_distrib = [0, 0, 0, 0]

    while True:

        # Reset environment
        s = env.reset()

        # Set terminal state to false
        terminal = False

        # Step counter (Increased per action)
        step_counter = 0

        # Reset Temporary memory
        temporary_memory.clear()

        # Reset action distrib
        action_distrib = [0, 0, 0, 0]

        while not terminal:
            # Draw environment on screen
            #env.render()  # For image you MUST call this

            # Draw action from distribution
            a = agent.act(s)
            action_distrib[a] += 1

            # Perform action in environment
            s1, r, t, _ = env.step(a)
            terminal = t

            if not t:
                print(r)



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

        logger.info(json.dumps({
            "steps": step_counter,
            "epsilon": agent.epsilon,
            "loss": agent.average_loss(),
            "terminal": terminal,
            "loss_rate": recent_games.count(False) / (len(recent_games)+0.0001),
            "action_distrib": action_distrib,
            "replay": len(agent.memory)
        }))


