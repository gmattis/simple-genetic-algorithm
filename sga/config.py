# Population
POPULATION_SIZE = 100  # Number of individuals in the population

# Individuals characteristics
IND_INP_NUMBER = 2  # Number of inputs
IND_OUT_NUMBER = 1  # Number of outputs
IND_MAX_NODES = 2  # Maximum number of nodes

# Genes mutations
ADD_GENE_PROB = 0.3  # Probability to add a new gene
MUT_GENE_PROB = 0.5  # Probability to mutate a gene
REM_GENE_PROB = 0.3  # Probability to remove a gene

ADD_NODE_PROB = 0.15  # Probability to add a new node
REM_NODE_PROB = 0.15  # Probability to remove a node

MUT_GENE_AMP = 0.2  # Gene mutation amplitude
WEIGHT_AMP = 1  # Default weights amplitude

GENE_PROB_FACT = 0.99  # Each generation, multiply the gene mutations probability by this factor
NODE_PROB_FACT = 0.99  # Each generation, multiply the node mutations probability by this factor
AMP_MUT_FACT = 1  # Each generation, multiply the gene mutation amplitude by this factor

# Elitism and extinction
ELITISM_NUMBER = 5  # Number of best individuals kept without mutations nor crossover
EXTINCTION_NUMBER = 2  # Number of worst individuals who will not crossover

# Training conditions
FITNESS_CRITERION = "avg"  # Fitness threshold criterion to stop training. Valid values are [min, avg, max]
FITNESS_THRESHOLD = 3.5  # Fitness threshold for the specified criterion
