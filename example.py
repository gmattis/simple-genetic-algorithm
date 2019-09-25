"""
A basic example of using the library to train a population with the XOR gate
"""
import simple_genetic_algorithm as sga
import random
import numpy


# Sigmoid function, used as activation function
def sigmoid(x):
    return 1 / (1 + numpy.exp(-x))


# Evaluation function, basically test 100 times each network
# It must takes an array as parameter, and returns an array of the same size for the fitness of the networks.
# The higher the fitness, the better the network is
def f_eval(population):
    fitness = [0 for i in range(len(population))]
    for i in range(len(population)):
        for j in range(100):
            rand1, rand2 = random.randint(0, 1), random.randint(0, 1)
            if numpy.bitwise_xor(rand1, rand2) - population[i].predict(numpy.array([rand1, rand2])) < 0.1:
                fitness[i] += 1
    return fitness


# Instantiate the population
pop = sga.Population(50, 2, 1, 2, sigmoid)

# Run the training for 50 generations
# Returns the network and their fitness after the last generation sorted by decreasing fitness
pop.run(f_eval, 500)
