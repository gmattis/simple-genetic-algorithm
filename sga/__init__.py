# ToDo: More explicit variables names
# ToDo: Show more statistics about generations
# ToDo: Write a real introduction for all the scripts
# ToDo: Add a license
# ToDo: Adapt GENE_PROB_FACT, NODE_PROB_FACT and AMP_MU_FACT to take account of the fitness
# ToDo: Verify the settings are correct when loading a state

from . import config

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

if not 0 <= config.ADD_GENE_PROB <= 1:
    _warning_stack.append("ADD_GENE_RATE should be between 0 and 1")
if not 0 <= config.MUT_GENE_PROB <= 1:
    _warning_stack.append("MUT_GENE_RATE should be between 0 and 1")
if not 0 <= config.REM_GENE_PROB <= 1:
    _warning_stack.append("REM_GENE_RATE should be between 0 and 1")

if not 0 <= config.ADD_NODE_PROB <= 1:
    _warning_stack.append("ADD_NODE_RATE should be between 0 and 1")
if not 0 <= config.REM_NODE_PROB <= 1:
    _warning_stack.append("REM_NODE_RATE should be between 0 and 1")

if not 0 < config.GENE_PROB_FACT <= 1:
    _warning_stack.append("GENE_PROB_FACT must be between 0 and 1")
if not 0 < config.NODE_PROB_FACT <= 1:
    _warning_stack.append("NODE_PROB_FACT must be between 0 and 1")
if not 0 != config.AMP_MUT_FACT:
    _warning_stack.append("AMP_MUT_FACT should be different than 0")

if not 0 <= config.ELITISM_RATE <= 1:
    _warning_stack.append("ELITISM_RATE should be between 0 and 1")
if not 0 <= config.EXTINCTION_RATE <= 1:
    _warning_stack.append("EXTINCTION_RATE should be between 0 and 1")

if config.FITNESS_CRITERION not in ["min", "avg", "max"]:
    _warning_stack.append("Invalid value for FITNESS_CRITERION. Should be min, avg or max")

# Print the warnings
if len(_warning_stack) > 0:
    print("WARNING: Some parameters in the config file are invalid:")
    for message in _warning_stack:
        print("-", message)
    print()
