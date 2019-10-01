# Population
POPULATION_SIZE = 100  # Number of individuals in the population

# Individuals characteristics
IND_INP_NUMBER = 2  # Number of inputs
IND_OUT_NUMBER = 1  # Number of outputs
IND_MAX_NODES = 2  # Maximum number of nodes

# Genes mutations
ADD_GENE_RATE = 0.3  # Probability to add a new gene
MUT_GENE_RATE = 0.5  # Probability to mutate a gene
REM_GENE_RATE = 0.3  # Probability to remove a gene

ADD_NODE_RATE = 0.15  # Probability to add a new node
REM_NODE_RATE = 0.15  # Probability to remove a node

MUT_GENE_AMP = 0.2  # Gene mutation amplitude
WEIGHT_AMP = 1  # Default weights amplitude

# Generations mutations
ELITISM_RATE = 0.1  # Percent of best individuals kept without mutations

# Training conditions
FITNESS_CRITERION = "avg"  # Fitness threshold criterion to stop training. Valid values are [min, avg, max]
FITNESS_THRESHOLD = 3.5  # Fitness threshold for the specified criterion
