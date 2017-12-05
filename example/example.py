import gym
import gym_maze
import numpy as np
import json
from example.logger import logger
from example.dqn.dqn_example_4 import DQN

if __name__ == '__main__':

    def preprocess(state, agent):
        new_state = np.zeros(shape=(1, ) + agent.state_size)
        new_state[:1, :state.shape[0], :state.shape[1], :state.shape[2]] = state
        return new_state


    env_list = [
        "maze-arr-9x9-full-deterministic-v0",
        #"maze-arr-11x11-full-deterministic-v0",
        #"maze-arr-13x13-full-deterministic-v0",
        #"maze-arr-15x15-full-deterministic-v0",
        #"maze-arr-17x17-full-deterministic-v0",
        #"maze-arr-19x19-full-deterministic-v0",
        #"maze-arr-25x25-full-deterministic-v0",
        #"maze-arr-35x35-full-deterministic-v0",
        # "maze-arr-55x55-full-deterministic-v0"
    ]

    env = gym.make(env_list[-1])
    env.reset()

    batch_size = 50
    epochs = 500
    train_epochs = 8
    memory_size = 1000
    timeout = 1000
    epsilon_increase = False

    agent = DQN(
        env.observation_space,
        env.action_space,
        memory_size=10000,
        batch_size=64,
        train_epochs=1,
        e_min=0,
        e_max=1.0,
        e_steps=10000,
        lr=1e-6,
        discount=0.95
    )
    agent.model.summary()
    try:
        agent.load("./model_weights.h5")
    except:
        print("cant find weights")

    while True:
        for env_name in env_list:
            print("Creating env %s" % env_name)
            env = gym.make(env_name)
            env.reset()

            victories_before_train = 50
            victories = 0
            perfect_in_row = 0
            perfects_before_next = 10
            agent.epsilon = agent.epsilon_max
            phase = "exploit"
            agent.save("./model_weights.h5")

            epoch = 0
            while epoch < epochs:
                epoch += 1

                # Reset environment
                state = env.reset()
                state = preprocess(state, agent)
                terminal = False
                timestep = 0

                while not terminal:
                    timestep += 1

                    # Draw environment on screen
                    env.render()  # For image you MUST call this

                    # Draw action from distribution
                    action = agent.act(state, force_exploit=True if phase == "exploit" else False)

                    # Perform action in environment
                    next_state, reward, terminal, info = env.step(action)
                    next_state = preprocess(next_state, agent)

                    # Experience replay
                    agent.remember(state, action, reward, next_state, terminal)

                    state = next_state

                    if terminal:
                        # Terminal means victory
                        victories += 1

                        # If it a prefect round, set to test phase
                        if timestep == info["optimal_path"]:
                            phase = "exploit"
                            perfect_in_row += 1
                        else:
                            phase = "explore"
                            perfect_in_row = 0

                        break
                    elif timestep >= timeout:
                        if epsilon_increase:
                            agent.epsilon = min(agent.epsilon_max, agent.epsilon + (agent.epsilon_decay * timestep))
                        phase = "explore"
                        perfect_in_row = 0
                        break

                if len(agent.memory) > agent.batch_size:
                    agent.replay(q_table=env.env.q_table)

                env.render()  # For image you MUST call this
                logger.info(json.dumps({
                    "epoch": epoch,
                    "steps": timestep,
                    "optimal": info["optimal_path"],
                    "epsilon": agent.epsilon,
                    "loss": agent.average_loss(),
                    "terminal": terminal,
                    "replay": len(agent.memory),
                    "perfect_in_row": perfect_in_row,
                    "phase": phase,
                    "env": env_name
                }))

                if perfect_in_row >= perfects_before_next:
                    epoch = epochs



