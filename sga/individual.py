import random

from .config import Config


class Individual:
    def __init__(self, config: Config, def_act_f, out_act_f=None):
        self.config = config

        # Variables initialization
        self.n_input = config.IND_INP_NUMBER
        self.n_output = config.IND_OUT_NUMBER
        self.max_node = config.IND_MAX_NODES
        self.total_size = self.n_input + self.n_output + self.max_node
        self.def_act_f = def_act_f

        if out_act_f is None:
            self.out_act_f = def_act_f
        else:
            self.out_act_f = out_act_f

        # Genes generation
        self.genes = [["inf" for _ in range(self.total_size)] for _ in range(self.total_size)]
        self.values = ["inf" for _ in range(self.total_size)]
        for i in range(self.n_input + self.max_node, self.total_size):
            for j in range(self.n_input):
                self.genes[i][j] = random.uniform(-1, 1)

    def __available_genes(self):
        """ Returns the list of empty genes """
        available_genes = []
        for i in self.__valid_to_nodes():
            for j in self.__valid_from_nodes():
                if self.genes[i][j] == "inf" and self.genes[j][i] == "inf" and i != j:
                    available_genes.append((i, j))
        return available_genes

    @staticmethod
    def __inf_line(line):
        for x in line:
            if x != "inf":
                return False
        return True

    @staticmethod
    def __inf_column(table, column_ind):
        for i in range(len(table)):
            if table[i][column_ind] != "inf":
                return False
        return True

    @staticmethod
    def __count_occ(table, x):
        count = 0
        for i in table:
            for j in i:
                if j == x:
                    count += 1
        return count

    def __existing_genes(self):
        """ Returns the list of existing genes """
        existing_genes = []
        for i in self.__valid_to_nodes():
            for j in self.__valid_from_nodes():
                if self.genes[i][j] != "inf":
                    existing_genes.append((i, j))
        return existing_genes

    def __valid_from_nodes(self):
        """ Returns the list of nodes usable as input """
        valid_nodes = list(range(self.n_input))
        for i in range(self.n_input, self.n_input + self.max_node):
            if not self.__inf_line(self.genes[i]) and not self.__inf_column(self.genes, i):
                valid_nodes.append(i)
        return valid_nodes

    def __valid_to_nodes(self):
        """ Returns the list of nodes usable as output """
        valid_nodes = list(range(self.n_input + self.max_node, self.total_size))
        for i in range(self.n_input, self.n_input + self.max_node):
            if not self.__inf_line(self.genes[i]) and not self.__inf_column(self.genes, i):
                valid_nodes.append(i)
        return valid_nodes

    def __check_path(self, node: int, already_checked=None):
        """ Checks the network, and removes undesirables genes """
        if already_checked is None:
            already_checked = []
        if not node < self.n_input:
            if node in already_checked:
                self.genes[already_checked[-1]][node] = "inf"

                if self.__inf_column(self.genes, node):
                    for i in range(self.n_input, self.n_input + self.max_node):
                        if self.genes[node][i] != "inf":
                            self.genes[node][i] = "inf"
                            self.__check_path(i)

            if self.__inf_line(self.genes[node]):
                for i in range(self.n_input, self.total_size):
                    if self.genes[i][node] != "inf":
                        self.genes[i][node] = "inf"
                        self.__check_path(i)

            for i in range(self.total_size):
                if self.genes[node][i] != "inf":
                    self.__check_path(i, already_checked + [node])

    def __process(self, node: int):
        """ Predicts the node (i) """
        out = 0
        for i in range(self.n_input + self.max_node):
            if self.genes[node][i] != "inf":
                if self.values[i] == "inf":
                    self.__process(i)
                out += self.values[i] * self.genes[node][i]
        if node < self.n_input + self.max_node:
            self.values[node] = self.def_act_f(out)
        else:
            self.values[node] = self.out_act_f(out)

    def add_gene(self):
        """ Adds a new gene between two existing nodes """
        available_genes = self.__available_genes()
        if len(available_genes) > 0:
            new_gene = random.choice(available_genes)
            self.genes[new_gene[0]][new_gene[1]] = random.uniform(- self.config.WEIGHT_AMP, self.config.WEIGHT_AMP)

    def add_node(self):
        """ Adds a new node in the middle of a gene """
        existing_genes = self.__existing_genes()
        if len(existing_genes) == 0:
            self.add_gene()
            return

        empty_nodes = []
        for i in range(self.n_input, self.n_input + self.max_node):
            if self.__inf_line(self.genes[i]):
                empty_nodes.append(i)

        if len(empty_nodes) > 0 and len(existing_genes) > 0:
            rep_gene = random.choice(existing_genes)
            new_node = random.choice(empty_nodes)
            self.genes[rep_gene[0]][rep_gene[1]] = "inf"
            self.genes[rep_gene[0]][new_node] = random.uniform(- self.config.WEIGHT_AMP, self.config.WEIGHT_AMP)
            self.genes[new_node][rep_gene[1]] = random.uniform(- self.config.WEIGHT_AMP, self.config.WEIGHT_AMP)

    def remove_gene(self):
        """ Removes an existing gene """
        existing_genes = self.__existing_genes()
        if len(existing_genes) > 0:
            selected_gene = random.choice(existing_genes)
            self.genes[selected_gene[0]][selected_gene[1]] = "inf"

    def remove_node(self):
        """ Removes a node and rebuilds the network partially """
        if self.total_size ** 2 - self.__count_occ(self.genes, "inf") < 2:
            self.remove_gene()

        available_nodes = []
        for i in range(self.n_input, self.n_input + self.max_node):
            if self.__count_occ(self.genes[i], "inf") < self.total_size:
                available_nodes.append(i)

        if len(available_nodes) > 0:
            rem_node = random.choice(available_nodes)
            from_nodes, to_nodes = [], []
            for i in range(self.n_input + self.max_node):
                if self.genes[rem_node][i] != "inf":
                    from_nodes.append(i)
                    self.genes[rem_node][i] = "inf"
            for i in range(self.n_input, self.total_size):
                if self.genes[i][rem_node] != "inf":
                    to_nodes.append(i)
                    self.genes[i][rem_node] = "inf"

            for i in to_nodes:
                for j in from_nodes:
                    if self.genes[i][j] == "inf" and random.random() < 0.5:
                        self.genes[i][j] = random.uniform(- self.config.WEIGHT_AMP, self.config.WEIGHT_AMP)

    def mutate(self, rate: float, amp: float):
        """ Mutates the genes """
        for i in range(self.n_input, self.total_size):
            for j in range(self.n_input + self.max_node):
                if random.random() < rate:
                    if self.genes[i][j] != "inf":
                        self.genes[i][j] += random.uniform(-amp, amp)

    def cleanup(self):
        """ Cleans the network by removing undesirables genes """
        for i in range(self.n_input + self.max_node, self.total_size):
            self.__check_path(i)

    def predict(self, inputs):
        """ Returns the prediction of the network """
        self.values = ["inf" for _ in range(self.total_size)]
        self.values[:self.n_input] = inputs
        for i in range(self.n_input + self.max_node, self.total_size):
            self.__process(i)
        return self.values[self.n_input + self.max_node:self.total_size]
