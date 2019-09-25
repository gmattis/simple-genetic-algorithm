"""
it just works.
"""
import numpy as np
import random
import time

# PARAMETERS

ADD_GENE_RATE = 0.3  # Probability to add a new gene
MUT_GENE_RATE = 0.4  # Probability to mutate a gene
REM_GENE_RATE = 0.3  # Probability to remove a gene

ADD_NODE_RATE = 0.15  # Probability to add a new node
REM_NODE_RATE = 0.15  # Probability to remove a node

MUT_GENE_AMP = 0.2  # Gene mutation amplitude
WEIGHT_AMP = 1  # Default weights amplitude

MIN_FIT_TRHS = np.inf  # Minimum fitness threshold for stopping training
AVG_FIT_TRHS = 95  # Average fitness threshold for stopping training
MAX_FIT_TRHS = np.inf  # Maximum fitness threshold for stopping training


class Individual:
    def __init__(self, n_input, n_output, max_node, def_act_f, out_act_f=None):
        # Variables initialization
        self.n_input = n_input
        self.n_output = n_output
        self.max_node = max_node
        self.total_size = n_input + max_node + n_output
        self.def_act_f = def_act_f

        if out_act_f is None:
            self.out_act_f = def_act_f
        else:
            self.out_act_f = out_act_f

        # Genes generation
        self.genes = np.full((self.total_size, self.total_size), np.inf)
        self.values = np.full(self.total_size, np.inf)
        for i in range(n_input + max_node, self.total_size):
            for j in range(n_input):
                self.genes[i, j] = random.uniform(-1, 1)

    def __available_genes(self):  # Return the list of empty genes
        available_genes = []
        for i in self.__valid_to_nodes():
            for j in self.__valid_from_nodes():
                if self.genes[i, j] == np.inf and self.genes[j, i] == np.inf and i != j:
                    available_genes.append((i, j))
        return available_genes

    def __existing_genes(self):  # Return the list of existing genes
        existing_genes = []
        for i in self.__valid_to_nodes():
            for j in self.__valid_from_nodes():
                if self.genes[i, j] != np.inf:
                    existing_genes.append((i, j))
        return existing_genes

    def __valid_from_nodes(self) -> list:  # Return the list of nodes usable as input
        valid_nodes = list(range(self.n_input))
        for i in range(self.n_input, self.n_input + self.max_node):
            if not (self.genes[i] == np.inf).all() and not (self.genes[:, i] == np.inf).all():
                valid_nodes.append(i)
        return valid_nodes

    def __valid_to_nodes(self) -> list:  # Return the list of nodes usable as output
        valid_nodes = list(range(self.n_input + self.max_node, self.total_size))
        for i in range(self.n_input, self.n_input + self.max_node):
            if not (self.genes[i] == np.inf).all() and not (self.genes[:, i] == np.inf).all():
                valid_nodes.append(i)
        return valid_nodes

    def __check_path(self, node, already_checked=[]):  # Check the network, and remove undesirables genes
        if not node < self.n_input:
            if node in already_checked:
                self.genes[already_checked[-1], node] = np.inf

                if (self.genes[:, node] == np.inf).all():
                    for i in range(self.n_input, self.n_input + self.max_node):
                        if self.genes[node, i] != np.inf:
                            self.genes[node, i] = np.inf
                            self.__check_path(i)

            if (self.genes[node] == np.inf).all():
                for i in range(self.n_input, self.total_size):
                    if self.genes[i, node] != np.inf:
                        self.genes[i, node] = np.inf
                        self.__check_path(i)

            for i in range(self.total_size):
                if self.genes[node, i] != np.inf:
                    self.__check_path(i, already_checked + [node])

    def __process(self, node):  # Predict the node (i)
        out = 0
        for i in range(self.n_input + self.max_node):
            if self.genes[node, i] != np.inf:
                if self.values[i] == np.inf:
                    self.__process(i)
                out += self.values[i] * self.genes[node, i]
        if node < self.n_input + self.max_node:
            self.values[node] = self.def_act_f(out)
        else:
            self.values[node] = self.out_act_f(out)

    def add_gene(self):  # Add a new gene between two existing nodes
        available_genes = self.__available_genes()
        if len(available_genes) > 0:
            new_gene = available_genes[random.randrange(0, len(available_genes))]
            self.genes[new_gene[0], new_gene[1]] = random.uniform(-WEIGHT_AMP, WEIGHT_AMP)

    def add_node(self):  # Add a new node in the middle of a gene
        if (self.genes != np.inf).sum() == 0:
            self.add_gene()
            return

        empty_nodes = []
        for i in range(self.n_input, self.n_input + self.max_node):
            if (self.genes[i] == np.inf).all():
                empty_nodes.append(i)

        if len(empty_nodes) > 0:
            existing_genes = self.__existing_genes()
            rep_gene = existing_genes[random.randrange(0, len(existing_genes))]
            new_node = np.random.choice(empty_nodes)
            self.genes[rep_gene[0], rep_gene[1]] = np.inf
            self.genes[rep_gene[0], new_node] = random.uniform(-WEIGHT_AMP, WEIGHT_AMP)
            self.genes[new_node, rep_gene[1]] = random.uniform(-WEIGHT_AMP, WEIGHT_AMP)

    def remove_gene(self):  # Remove an existing gene
        if (self.genes != np.inf).sum() > 0:
            existing_genes = self.__existing_genes()
            selected_gene = existing_genes[random.randrange(0, len(existing_genes))]
            self.genes[selected_gene[0], selected_gene[1]] = np.inf

    def remove_node(self):  # Remove a node and rebuild the network partially
        if (self.genes != np.inf).sum() < 2:
            self.remove_gene()
            pass

        available_nodes = []
        for i in range(self.n_input, self.n_input + self.max_node):
            if (self.genes[i] != np.inf).any():
                available_nodes.append(i)

        if len(available_nodes) > 0:
            rem_node = np.random.choice(available_nodes)
            from_nodes, to_nodes = [], []
            for i in range(self.n_input + self.max_node):
                if self.genes[rem_node, i] != np.inf:
                    from_nodes.append(i)
                    self.genes[rem_node, i] = np.inf
            for i in range(self.n_input, self.total_size):
                if self.genes[i, rem_node] != np.inf:
                    to_nodes.append(i)
                    self.genes[i, rem_node] = np.inf

            for i in to_nodes:
                for j in from_nodes:
                    if self.genes[i, j] == np.inf and random.random() < 0.5:
                        self.genes[i, j] = random.uniform(-WEIGHT_AMP, WEIGHT_AMP)

    def mutate(self, rate, amp):  # Mutate the genes
        for i in range(self.n_input, self.total_size):
            for j in range(self.n_input + self.max_node):
                if random.random() < rate:
                    if self.genes[i, j] != np.inf:
                        self.genes[i, j] += random.uniform(-amp, amp)

    def cleanup(self):  # Clean the network of undesirable genes
        for i in range(self.n_input + self.max_node, self.total_size):
            self.__check_path(i)

    def predict(self, inputs) -> np.ndarray:  # Return the prediction of the network
        self.values.fill(np.inf)
        self.values[:self.n_input] = inputs
        for i in range(self.n_input + self.max_node, self.total_size):
            self.__process(i)
        return self.values[self.n_input + self.max_node:self.total_size]


class Population:
    def __init__(self, n_pop, n_input, n_output, max_node, def_act_f, out_act_f=None):
        self.n_pop = n_pop
        self.n_input = n_input
        self.n_output = n_output
        self.max_node = max_node
        self.def_act_f = def_act_f
        self.out_act_f = out_act_f
        self.population = np.array([Individual(n_input, n_output, max_node, def_act_f, out_act_f) for i in range(n_pop)])

    def __mix_genes(self, genes_a, genes_b) -> np.ndarray:
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

    def __crossover(self, fitness):
        new_population = np.empty(self.n_pop, dtype=Individual)
        for i in range(self.n_pop):
            parent_a = np.random.choice(self.population, p=fitness)
            parent_b = np.random.choice(self.population, p=fitness)
            new_population[i] = Individual(self.n_input, self.n_output, self.max_node, self.def_act_f, self.out_act_f)
            new_population[i].genes = self.__mix_genes(parent_a.genes, parent_b.genes)
        self.population = new_population

    def __mutate(self):
        for i in range(self.n_pop):
            random.seed()

            if random.random() < REM_NODE_RATE:
                self.population[i].remove_node()
            if random.random() < REM_GENE_RATE:
                self.population[i].remove_gene()

            self.population[i].mutate(MUT_GENE_RATE, MUT_GENE_AMP)

            if random.random() < ADD_NODE_RATE:
                self.population[i].add_node()
            if random.random() < ADD_GENE_RATE:
                self.population[i].add_gene()

            self.population[i].cleanup()

    def run(self, eval_f, n_gen=1000):
        print("Beginning training!")
        start_time = time.time()
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
            if i < n_gen and min_fit < MIN_FIT_TRHS and avg_fit < AVG_FIT_TRHS and max_fit < MAX_FIT_TRHS:
                self.__crossover(np.array(fitness) / np.sum(fitness))
                self.__mutate()
            else:
                break
        print("======[", "END".center(n_digit + 5), "]======")
        print("Training ended in", format(time.time() - start_time, '.2f'), "s")
        return sorted([(self.population[i], fitness[i]) for i in range(self.n_pop)], key=(lambda x: x[1]), reverse=True)
