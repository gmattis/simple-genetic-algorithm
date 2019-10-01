import numpy as np
import gym

from sga import population


def run_episode(ind, episode_len=500, render=False):
    total_reward = 0
    obs = env.reset()
    for t in range(episode_len):
        if render:
            env.render()
        action = ind.predict(obs)
        obs, reward, done, _ = env.step(int(action[0]))
        total_reward += reward
        if done:
            break
    return total_reward


def evaluate_population(pop):
    fitness = [0 for _ in range(len(pop))]
    for i in range(len(pop)):
        fitness[i] = run_episode(pop[i])
    return fitness


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


population.config.IND_INP_NUMBER = 4
population.config.FITNESS_THRESHOLD = 450

# Train the population using a Gym environment
env = gym.make('CartPole-v1')
m_population = population.Population(sigmoid, lambda x: 0 if x < 0.5 else 1)
trained_pop = m_population.run(evaluate_population)

# Display the best individual
run_episode(trained_pop[0], episode_len=100000, render=True)
