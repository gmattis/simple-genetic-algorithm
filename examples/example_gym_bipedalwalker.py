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
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            break
    return total_reward


def evaluate_population(pop):
    fitness = [0 for _ in range(len(pop))]
    for i in range(len(pop)):
        fitness[i] = run_episode(pop[i])
    return fitness


population.config.IND_INP_NUMBER = 24
population.config.IND_OUT_NUMBER = 4
population.config.IND_MAX_NODES = 10
population.config.GENE_PROB_FACT = 1
population.config.NODE_PROB_FACT = 1
population.config.FITNESS_THRESHOLD = 300
population.config.FITNESS_CRITERION = "max"

# Train the population using a Gym environment
env = gym.make('BipedalWalker-v2')
m_population = population.Population(np.tanh)
m_population.load("sga-state-25.npy")
trained_pop = m_population.run(evaluate_population, save_interval=10)

# Display the best individual
run_episode(trained_pop[0], episode_len=100000, render=True)
