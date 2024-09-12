import pettingzoo.butterfly.knights_archers_zombies_v10 as kaz
from flexibuff import FlexibleBuffer
import random
import math
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import matplotlib.pyplot as plt

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)

# Create the environment
env = kaz.env(render_mode="human")
# Reset the environment
observations = env.reset()


# Set up the memory buffer for use with one agent,
# global reward and one discrete action output
memory = FlexibleBuffer(
    num_steps=10000,
    obs_size=4,
    discrete_action_cardinalities=[2],
    path="./test_save/",
    name="all_attributes",
    n_agents=1,
    global_reward=True,
)

# Run an episode
terminated = {agent: False for agent in env.agents}
while not all(terminated.values()):
    for agent in env.agent_iter():
        if terminated[agent]:
            continue

        observation = observations[agent]
        action = agent.act(observation)

        env.step(action)
        env.render()  # Add this line to render the environment
        next_observation = env.observe(agent)
        reward = env.rewards[agent]
        terminated[agent] = env.dones[agent]

        if agent == "agent1":
            agent1.learn(
                observation, action, reward, next_observation, terminated[agent]
            )
        else:
            agent2.learn(
                observation, action, reward, next_observation, terminated[agent]
            )

        observations[agent] = next_observation

# Close the environment
env.close()
