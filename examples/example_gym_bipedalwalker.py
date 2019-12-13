import numpy as np
import gym

from sga import population, config, activation, display


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


# Define the configuration file
bipedal_config = config.Config()
bipedal_config.load("BipedalWalkerConfig.cfg")

# Train the population using a Gym environment
env = gym.make('BipedalWalker-v2')
m_population = population.Population(activation_function=activation.tanh, config=bipedal_config)
trained_pop = m_population.run(evaluate_population, save=True, save_interval=50)

# Display the neural network of the best individual
display.display_genome(trained_pop[0], bipedal_config)

# Display the best individual
run_episode(trained_pop[0], episode_len=100000, render=True)
