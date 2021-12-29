import gym
import numpy as np
import matplotlib.pyplot as plt

env = gym.make('FrozenLake-v0')

n_games = 1000
win_pct = []
scores = []

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3
policy = {0: DOWN, 1: RIGHT, 2: DOWN, 3: LEFT, 4: DOWN, 6: DOWN, 8: RIGHT, 9: DOWN, 10: DOWN, 13: RIGHT, 14: RIGHT}
for i in range(n_games):
    done = False
    obs = env.reset()
    score = 0
    while not done:
        action = policy[obs]
        obs, reward, done, info = env.step(action)
        score += reward
    scores.append(score)

    if i % 10 == 0:
        average = np.mean(scores[-10:])
        win_pct.append(average)

plt.plot(win_pct)
plt.show()
