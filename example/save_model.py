from example.dqn.dqn_example_4 import DQN

agent = DQN(
    (84, 84, 1),
    4,
    memory_size=10000,
    batch_size=64,
    train_epochs=1,
    e_min=0,
    e_max=1.0,
    e_steps=100000,
    lr=1e-6,
    discount=0.95
)


print(agent.model.to_json())