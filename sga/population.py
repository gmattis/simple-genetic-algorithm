import numpy as np
import random
import time

from . import config
from .individual import Individual


class Population:
    def __init__(self, def_act_f, out_act_f=None):
        self.def_act_f = def_act_f
        self.out_act_f = out_act_f
        self.population = np.array([Individual(def_act_f, out_act_f) for _ in range(config.POPULATION_SIZE)])
        self.n_elite = int(config.ELITISM_RATE * config.POPULATION_SIZE)
        self.gene_prob_factor = 1
        self.node_prob_factor = 1
        self.amp_mut_factor = 1

    @staticmethod
    def __check_criterion(min_fit, avg_fit, max_fit):
        if config.FITNESS_CRITERION == "min":
            return config.FITNESS_THRESHOLD <= min_fit
        elif config.FITNESS_CRITERION == "max":
            return config.FITNESS_THRESHOLD <= max_fit
        else:
            return config.FITNESS_THRESHOLD <= avg_fit

    @staticmethod
    def __mix_genes(genes_a, genes_b) -> np.ndarray:  # Mix genes of individuals
        shape = np.shape(genes_a)
        mixed_genes = np.full(shape, np.inf)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if genes_a[i, j] != np.inf:
                    if genes_b[i, j] != np.inf:
                        if random.random() < 0.5:
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
    def __sort_population(fitness) -> list:  # Return the index of the individuals sorted by decreasing fitness
        fitness_copy, index_list = fitness.copy(), []
        for i in range(len(fitness)):
            index_max = np.argmax(fitness_copy)
            fitness_copy[index_max] = - np.inf
            index_list.append(index_max)
        return index_list

    def __crossover(self, fitness):  # Do the crossover between individuals
        new_population = np.empty(config.POPULATION_SIZE, dtype=Individual)

        sorted_index = self.__sort_population(fitness)
        for i in range(self.n_elite):
            new_population[i] = self.population[sorted_index[i]]

        for i in range(self.n_elite, config.POPULATION_SIZE):
            parent_a = np.random.choice(self.population, p=fitness)
            parent_b = np.random.choice(self.population, p=fitness)
            new_population[i] = Individual(self.def_act_f, self.out_act_f)
            new_population[i].genes = self.__mix_genes(parent_a.genes, parent_b.genes)
        self.population = new_population

    def __mutate(self):  # Mutate each individuals
        for i in range(config.POPULATION_SIZE):
            random.seed()

            if random.random() < config.REM_NODE_PROB * self.node_prob_factor:
                self.population[i].remove_node()
            if random.random() < config.REM_GENE_PROB * self.gene_prob_factor:
                self.population[i].remove_gene()

            self.population[i].mutate(config.MUT_GENE_PROB * self.gene_prob_factor, config.MUT_GENE_AMP * self.amp_mut_factor)

            if random.random() < config.ADD_NODE_PROB * self.node_prob_factor:
                self.population[i].add_node()
            if random.random() < config.ADD_GENE_PROB * self.gene_prob_factor:
                self.population[i].add_gene()

            self.population[i].cleanup()

    def run(self, eval_f, n_gen=1000):  # Main loop
        print("Beginning training!")
        start_time = time.time()
        fitness = []
        n_digit = int(np.log10(n_gen)) + 1
        for i in range(1, n_gen + 1):
            print("======[ GEN.", str(i).zfill(n_digit), "]======")
            gen_time = time.time()
            fitness = eval_f(self.population)
            print("Done in", format(time.time() - gen_time, '.2f'), "s.")

            print("STATS:")
            min_fit = np.min(fitness)
            max_fit = np.max(fitness)
            avg_fit = np.average(fitness)
            print("- min. fitness:", min_fit)
            print("- max. fitness:", max_fit)
            print("- avg. fitness:", avg_fit)

            if i < n_gen and not self.__check_criterion(min_fit, avg_fit, max_fit):
                self.__crossover(np.array(fitness) / np.sum(fitness))
                self.__mutate()

                self.gene_prob_factor *= config.GENE_PROB_FACT
                self.node_prob_factor *= config.NODE_PROB_FACT
                self.amp_mut_factor *= config.AMP_MUT_FACT
            else:
                break
        print("======[", "END".center(n_digit + 5), "]======")
        print("Training ended in", format(time.time() - start_time, '.2f'), "s")
        return [self.population[i] for i in self.__sort_population(fitness)]
