"""
A basic example of using the library to train a population with the XOR gate
"""
from sga import population, activation, display


xor_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
xor_outputs = [0, 1, 1, 0]


# Evaluation function, basically test 100 times each network
# It takes an array as parameter, and returns an array of the same size for the fitness of the networks.
# The higher the fitness, the better the network is
def f_eval(pop):
    fitness = [4 for _ in range(len(pop))]
    for i in range(len(pop)):
        for xi, xo in zip(xor_inputs, xor_outputs):
            fitness[i] -= (xo - pop[i].predict(xi)[0]) ** 2
    return fitness


# Instantiate the population
m_population = population.Population(activation_function=activation.sigmoid)

# Run the training for 500 generations
ind = m_population.run(f_eval, 500)[0]

# Display the neural network of the best individual
display.display_genome(ind, m_population.config, display=True)
