# ToDo: Mutation rates and amplitude factor
# ToDo: More explicit variables names
# ToDo: Possibility to save the population and restart the training from a certain state
# ToDo: Automatic saving
# ToDo: Show more statistics about generations
# ToDo: Comment
# ToDo: Input variables typing
# ToDo: Write a real introduction for all the scripts

from . import config, individual, population

_warning_stack = []

# Check the validity of the config file
if not 0 < config.POPULATION_SIZE:
    _warning_stack.append("POPULATION_SIZE must be greater than 0")

if not 0 < config.IND_INP_NUMBER:
    _warning_stack.append("IND_INP_NUMBER must be greater than 0")
if not 0 < config.IND_OUT_NUMBER:
    _warning_stack.append("IND_OUT_NUMBER must be greater than 0")
if not 0 <= config.IND_MAX_NODES:
    _warning_stack.append("IND_MAX_NODES must be positive")

if not 0 <= config.ADD_GENE_RATE <= 1:
    _warning_stack.append("ADD_GENE_RATE should be between 0 and 1")
if not 0 <= config.MUT_GENE_RATE <= 1:
    _warning_stack.append("MUT_GENE_RATE should be between 0 and 1")
if not 0 <= config.REM_GENE_RATE <= 1:
    _warning_stack.append("REM_GENE_RATE should be between 0 and 1")

if not 0 <= config.ADD_NODE_RATE <= 1:
    _warning_stack.append("ADD_NODE_RATE should be between 0 and 1")
if not 0 <= config.REM_NODE_RATE <= 1:
    _warning_stack.append("REM_NODE_RATE should be between 0 and 1")

if not 0 <= config.ELITISM_RATE <= 1:
    _warning_stack.append("ELITISM_RATE should be between 0 and 1")

if config.FITNESS_CRITERION not in ["min", "avg", "max"]:
    _warning_stack.append("Invalid value for FITNESS_CRITERION. Should be min, avg or max")

# Print the warnings
if len(_warning_stack) > 0:
    print("WARNING: Some parameters in the config file are invalid:")
    for message in _warning_stack:
        print("-", message)
    print()
