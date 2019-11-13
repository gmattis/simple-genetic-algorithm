import math
import numpy as np
import random
import time

from typing import Callable, List, Optional

from . import saveload, tracker, activation
from .individual import Individual
from .config import Config


class Population:
    def __init__(self, activation_function: str, out_activation_function: Optional[str] = None, config: Config = None):
        if out_activation_function is None:
            out_activation_function = activation_function

        if config is None:
            self.config = Config()
        else:
            self.config = config

        # Activation functions
        self.activation_function = activation.get_function(activation_function)
        self.out_activation_function = activation.get_function(out_activation_function)

        # Mutations probabilities and amplitude factor
        self.gene_probability_factor = 1
        self.node_probability_factor = 1
        self.amplitude_factor = 1

        # Tracker / Statistics printer
        self.tracker = tracker.Tracker(self.config)

        # Population
        self.population = np.array([Individual(self.config, self.activation_function, self.out_activation_function)
                                    for _ in range(self.config.POPULATION_SIZE)])

    @staticmethod
    def __mix_genes(genes_a: np.ndarray, genes_b: np.ndarray) -> np.ndarray:
        """ Mixes the genes of two individuals """
        shape = np.shape(genes_a)
        mixed_genes = np.full(shape, np.inf)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if genes_a[i, j] != np.inf:
                    if genes_b[i, j] != np.inf:
                        if random.random() < .5:
                            mixed_genes[i, j] = genes_a[i, j]
                        else:
                            mixed_genes[i, j] = genes_b[i, j]
                    else:
                        mixed_genes[i, j] = genes_a[i, j]
                else:
                    if genes_b[i, j] != np.inf:
                        mixed_genes[i, j] = genes_b[i, j]
        return mixed_genes

    @staticmethod
    def __normalize_fitness(fitness: List[float]) -> list:
        """ Makes all the fitness positive and the sum equal to 1 """
        minimum_fitness = min(fitness)
        normalized_fitness = [fit + minimum_fitness for fit in fitness]
        fitness_sum = sum(normalized_fitness)
        return [fit / fitness_sum for fit in normalized_fitness]

    @staticmethod
    def __sort_population(fitness: List[float]) -> list:
        """ Returns the indexes of the individuals sorted by decreasing fitness """
        fitness_copy, index_list = fitness.copy(), []
        for i in range(len(fitness)):
            index_max = np.argmax(fitness_copy)
            fitness_copy[index_max] = np.NINF
            index_list.append(index_max)
        return index_list

    def __check_criterion(self, min_fit: float, avg_fit: float, max_fit: float) -> bool:
        """ Checks if the criterion for stopping the training is verified """
        if self.config.FITNESS_CRITERION == "min":
            return self.config.FITNESS_THRESHOLD <= min_fit
        elif self.config.FITNESS_CRITERION == "max":
            return self.config.FITNESS_THRESHOLD <= max_fit
        else:
            return self.config.FITNESS_THRESHOLD <= avg_fit

    def __crossover(self, fitness: List[float]):
        """ Do the crossover between individuals """
        new_population = np.empty(self.config.POPULATION_SIZE, dtype=Individual)

        sorted_index = self.__sort_population(fitness)
        normalized_fitness = self.__normalize_fitness(
            [fitness[i] for i in sorted_index[:self.config.EXTINCTION_NUMBER]])

        # Elite individuals
        for i in range(self.config.ELITISM_NUMBER):
            new_population[i] = self.population[sorted_index[i]]

        # Crossover between individuals
        for i in range(self.config.ELITISM_NUMBER, self.config.POPULATION_SIZE - self.config.EXTINCTION_NUMBER):
            parent_a, parent_b = random.choices(self.population[:self.config.EXTINCTION_NUMBER],
                                                weights=normalized_fitness, k=2)
            new_population[i] = Individual(self.config, self.activation_function, self.out_activation_function,
                                           generate_network=False)
            new_population[i].genes = self.__mix_genes(parent_a.genes, parent_b.genes)

        # New individuals replacing the extincted ones
        for i in range(self.config.POPULATION_SIZE - self.config.EXTINCTION_NUMBER, self.config.POPULATION_SIZE):
            new_population[i] = Individual(self.config, self.activation_function, self.out_activation_function)

        self.population = new_population

    def __mutate(self):
        """ Makes each individual mutate """
        for i in range(self.config.ELITISM_NUMBER, self.config.POPULATION_SIZE):
            random.seed()

            if random.random() < self.config.REM_NODE_PROB * self.node_probability_factor:
                self.population[i].remove_node()
            if random.random() < self.config.REM_GENE_PROB * self.gene_probability_factor:
                self.population[i].remove_gene()

            self.population[i].mutate(self.config.MUT_GENE_PROB * self.gene_probability_factor,
                                      self.config.MUT_GENE_AMP * self.amplitude_factor)

            if random.random() < self.config.ADD_NODE_PROB * self.node_probability_factor:
                self.population[i].add_node()
            if random.random() < self.config.ADD_GENE_PROB * self.gene_probability_factor:
                self.population[i].add_gene()

            self.population[i].cleanup()

    def load(self, path: str):
        """ Loads a saved state """
        self.population = saveload.load(path, self.config, self.activation_function, self.out_activation_function)

    def run(self, evaluation_function: Callable, n_gen: Optional[int] = 500,
            save: Optional[bool] = False, save_interval: Optional[int] = None) -> list:
        """ Training loop """
        print("Beginning training!")

        self.tracker.reset()

        start_time = time.time()
        fitness = np.zeros(self.config.POPULATION_SIZE)
        n_digit = int(math.log10(n_gen)) + 1

        for gen in range(1, n_gen + 1):
            print("======[ GEN.", str(gen).zfill(n_digit), "]======")
            gen_time = time.time()
            fitness = evaluation_function(self.population)
            print("Done in", format(time.time() - gen_time, '.2f'), "s.")

            print("STATS:")
            self.tracker.append(fitness)
            self.tracker.print_stats()

            avg_fitness, min_fitness, max_fitness = self.tracker.get_last_stats()

            if gen < n_gen and not self.__check_criterion(min_fitness, avg_fitness, max_fitness):
                if save and save_interval is not None and gen % save_interval == 0:
                    saveload.save([self.population[i] for i in self.__sort_population(fitness)], gen)

                self.__crossover(fitness)
                self.__mutate()

                self.gene_probability_factor *= self.config.GENE_PROB_FACT
                self.node_probability_factor *= self.config.NODE_PROB_FACT
                self.amplitude_factor *= self.config.AMP_MUT_FACT
            else:
                break

        print("======[", "END".center(n_digit + 5), "]======")
        print("Training ended in", format(time.time() - start_time, '.2f'), "s")

        if save:
            saveload.save([self.population[i] for i in self.__sort_population(fitness)], "end")

        return [self.population[i] for i in self.__sort_population(fitness)]
