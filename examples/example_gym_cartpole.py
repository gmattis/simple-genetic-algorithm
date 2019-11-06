import gym

from sga import population, config, display


def normalize_output(x):
    return 1 if x > 0.5 else 0


def run_episode(ind, episode_len=500, render=False):
    total_reward = 0
    obs = env.reset()
    for t in range(episode_len):
        if render:
            env.render()
        action = ind.predict(obs)
        obs, reward, done, _ = env.step(int(normalize_output(action[0])))
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
cartpole_config = config.Config()
cartpole_config.load("CartpoleConfig.cfg")

# Train the population using a Gym environment
env = gym.make('CartPole-v1')
m_population = population.Population(activation_function="sigmoid",
                                     out_activation_function="identity",
                                     config=cartpole_config)
trained_pop = m_population.run(evaluate_population, save=True, save_interval=50)

# Display the neural network of the best individual
display.display_genome(trained_pop[0], cartpole_config)

# Display the best individual
run_episode(trained_pop[0], episode_len=100000, render=True)
