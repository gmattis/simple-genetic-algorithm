import math
import random

import tracker
from config import Config
from individual import Individual


class Population:
    def __init__(self, def_act_f, out_act_f=None, config: Config = None):
        if config is None:
            self.config = Config()
        else:
            self.config = config

        # Activation functions
        self.def_act_f = def_act_f
        self.out_act_f = out_act_f

        # Mutations probabilities and amplitude factor
        self.gene_prob_factor = 1
        self.node_prob_factor = 1
        self.amp_mut_factor = 1

        # Tracker / Statistics printer
        self.tracker = tracker.Tracker(self.config)

        # Population
        self.population = [Individual(self.config, def_act_f, out_act_f) for _ in range(self.config.POPULATION_SIZE)]

    @staticmethod
    def __argmax(iterable):
        ind_max = 0
        for i in range(1, len(iterable)):
            if iterable[i] > iterable[ind_max]:
                ind_max = i
        return ind_max

    @staticmethod
    def __mix_genes(genes_a, genes_b):
        """ Mixes the genes of two individuals """
        shape = len(genes_a), len(genes_a[0])
        mixed_genes = [["inf" for _ in range(shape[1])] for _ in range(shape[0])]
        for i in range(shape[0]):
            for j in range(shape[1]):
                if genes_a[i][j] != "inf":
                    if genes_b[i][j] != "inf":
                        if random.random() < 0.5:
                            mixed_genes[i][j] = genes_a[i][j]
                        else:
                            mixed_genes[i][j] = genes_b[i][j]
                    else:
                        mixed_genes[i][j] = genes_a[i][j]
                else:
                    if genes_b[i][j] != "inf":
                        mixed_genes[i][j] = genes_b[i][j]
        return mixed_genes

    @staticmethod
    def __normalize_fitness(fitness):
        """ Applies the softmax function to the fitness """
        normalized_fitness = [math.exp(x) for x in fitness]
        return [x / sum(normalized_fitness) for x in normalized_fitness]

    def __sort_population(self, fitness) -> list:
        """ Returns the indexes of the individuals sorted by decreasing fitness """
        fitness_copy, index_list = fitness.copy(), []
        for i in range(len(fitness)):
            index_max = self.__argmax(fitness_copy)
            fitness_copy[index_max] = -100000
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

    def __crossover(self, fitness):
        """ Do the crossover between individuals """
        new_population = [None for _ in range(self.config.POPULATION_SIZE)]

        sorted_index = self.__sort_population(fitness)
        normalized_fitness = self.__normalize_fitness(
            [fitness[i] for i in sorted_index[:self.config.EXTINCTION_NUMBER]])

        # Elite individuals
        for i in range(self.config.ELITISM_NUMBER):
            new_population[i] = self.population[sorted_index[i]]

        # Crossover between individuals
        for i in range(self.config.ELITISM_NUMBER, self.config.POPULATION_SIZE - self.config.EXTINCTION_NUMBER):
            parent_a = random.choices(self.population[:self.config.EXTINCTION_NUMBER], weights=normalized_fitness)[0]
            parent_b = random.choices(self.population[:self.config.EXTINCTION_NUMBER], weights=normalized_fitness)[0]
            new_population[i] = Individual(self.config, self.def_act_f, self.out_act_f)
            new_population[i].genes = self.__mix_genes(parent_a.genes, parent_b.genes)

        # New individuals replacing the extincted ones
        for i in range(self.config.POPULATION_SIZE - self.config.EXTINCTION_NUMBER, self.config.POPULATION_SIZE):
            new_population[i] = Individual(self.config, self.def_act_f, self.out_act_f)

        self.population = new_population

    def __mutate(self):
        """ Makes each individual mutate """
        for i in range(self.config.ELITISM_NUMBER, self.config.POPULATION_SIZE):
            random.seed()

            if random.random() < self.config.REM_NODE_PROB * self.node_prob_factor:
                self.population[i].remove_node()
            if random.random() < self.config.REM_GENE_PROB * self.gene_prob_factor:
                self.population[i].remove_gene()

            self.population[i].mutate(self.config.MUT_GENE_PROB * self.gene_prob_factor,
                                      self.config.MUT_GENE_AMP * self.amp_mut_factor)

            if random.random() < self.config.ADD_NODE_PROB * self.node_prob_factor:
                self.population[i].add_node()
            if random.random() < self.config.ADD_GENE_PROB * self.gene_prob_factor:
                self.population[i].add_gene()

            self.population[i].cleanup()

    def run(self, eval_f, n_gen=500) -> list:
        """ Training loop """
        print("Beginning training!")

        self.tracker.reset()

        fitness = [0 for _ in range(self.config.POPULATION_SIZE)]

        for gen in range(1, n_gen + 1):
            print("======[ GEN.", str(gen), "]======")

            fitness = eval_f(self.population)
            print("Done!")

            print("STATS:")
            self.tracker.append(fitness)
            self.tracker.print_stats()

            avg_fitness, min_fitness, max_fitness = self.tracker.get_last_stats()

            if gen < n_gen and not self.__check_criterion(min_fitness, avg_fitness, max_fitness):
                self.__crossover(fitness)
                self.__mutate()

                self.gene_prob_factor *= self.config.GENE_PROB_FACT
                self.node_prob_factor *= self.config.NODE_PROB_FACT
                self.amp_mut_factor *= self.config.AMP_MUT_FACT
            else:
                break

        print("======[   END   ]======")

        return [self.population[i] for i in self.__sort_population(fitness)]
