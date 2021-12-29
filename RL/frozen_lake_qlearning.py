import gym
import numpy as np
from QLearningAgent import Agent
import matplotlib.pyplot as plt

env = gym.make('FrozenLake-v0')

n_games = 500000
win_pct = []
scores = []
games_limit = 100

agent = Agent(lr=0.01, gamma=0.9, eps_start=1.0, eps_end=0.01, eps_dec=0.9999995, n_actions=4, n_states=16)

for i in range(n_games):
    done = False
    observation = env.reset()
    score = 0
    while not done:
        action = agent.choose_action(observation)
        next_observation, reward, done, info = env.step(action)
        agent.learn(observation, action, reward, next_observation)
        score += reward
        observation = next_observation
    scores.append(score)

    if i % games_limit == 0:
        average = np.mean(scores[-games_limit:])
        win_pct.append(average)

plt.plot(win_pct)
plt.show()
