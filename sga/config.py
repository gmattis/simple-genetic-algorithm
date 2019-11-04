class Config:
    def __init__(self):
        """ Initialize the configuration """
        # Population
        self.POPULATION_SIZE = 100

        # Individuals characteristics
        self.IND_INP_NUMBER = 2
        self.IND_OUT_NUMBER = 1
        self.IND_MAX_NODES = 2

        # Genes mutations
        self.ADD_GENE_PROB = 0.3
        self.MUT_GENE_PROB = 0.5
        self.REM_GENE_PROB = 0.3

        self.ADD_NODE_PROB = 0.15
        self.REM_NODE_PROB = 0.15

        self.MUT_GENE_AMP = 0.2
        self.WEIGHT_AMP = 1

        self.GENE_PROB_FACT = 1
        self.NODE_PROB_FACT = 1
        self.AMP_MUT_FACT = 1

        # Elitism and extinction
        self.ELITISM_NUMBER = 10
        self.EXTINCTION_NUMBER = 10

        # Training conditions
        self.FITNESS_CRITERION = "avg"
        self.FITNESS_THRESHOLD = 3.5
