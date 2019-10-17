import configparser
from os.path import dirname, join

default_config_file = join(dirname(__file__), "DefaultConfig.cfg")


class Config:
    def __init__(self):
        self.config_file = configparser.ConfigParser()
        self.load()

    def __check_config(self):
        _warning_stack = []

        # Check the validity of the config file
        if not 0 < self.POPULATION_SIZE:
            _warning_stack.append("POPULATION_SIZE must be greater than 0")

        if not 0 < self.IND_INP_NUMBER:
            _warning_stack.append("IND_INP_NUMBER must be greater than 0")
        if not 0 < self.IND_OUT_NUMBER:
            _warning_stack.append("IND_OUT_NUMBER must be greater than 0")
        if not 0 <= self.IND_MAX_NODES:
            _warning_stack.append("IND_MAX_NODES must be positive")

        if not 0 <= self.ADD_GENE_PROB <= 1:
            _warning_stack.append("ADD_GENE_RATE should be between 0 and 1")
        if not 0 <= self.MUT_GENE_PROB <= 1:
            _warning_stack.append("MUT_GENE_RATE should be between 0 and 1")
        if not 0 <= self.REM_GENE_PROB <= 1:
            _warning_stack.append("REM_GENE_RATE should be between 0 and 1")

        if not 0 <= self.ADD_NODE_PROB <= 1:
            _warning_stack.append("ADD_NODE_RATE should be between 0 and 1")
        if not 0 <= self.REM_NODE_PROB <= 1:
            _warning_stack.append("REM_NODE_RATE should be between 0 and 1")

        if not 0 < self.GENE_PROB_FACT <= 1:
            _warning_stack.append("GENE_PROB_FACT must be between 0 and 1")
        if not 0 < self.NODE_PROB_FACT <= 1:
            _warning_stack.append("NODE_PROB_FACT must be between 0 and 1")
        if not 0 != self.AMP_MUT_FACT:
            _warning_stack.append("AMP_MUT_FACT should be different than 0")

        if not 0 <= self.ELITISM_NUMBER:
            _warning_stack.append("ELITISM_RATE should be positive")
        if not 0 <= self.EXTINCTION_NUMBER:
            _warning_stack.append("EXTINCTION_RATE should be positive")

        if self.FITNESS_CRITERION not in ["min", "avg", "max"]:
            _warning_stack.append("Invalid value for FITNESS_CRITERION. Should be min, avg or max")

        # Print the warnings
        if len(_warning_stack) > 0:
            print("WARNING: Some parameters in the config file are invalid:")
            for message in _warning_stack:
                print("-", message)
            print()

    # noinspection PyAttributeOutsideInit
    def load(self, filename: str = default_config_file):
        """ Loads a specific config file, or the default one if none is specified """
        self.config_file.read(filename)

        # Population
        self.POPULATION_SIZE = self.config_file.getint('Population', 'POPULATION_SIZE')

        # Individuals characteristics
        self.IND_INP_NUMBER = self.config_file.getint('Individual', 'IND_INP_NUMBER')
        self.IND_OUT_NUMBER = self.config_file.getint('Individual', 'IND_OUT_NUMBER')
        self.IND_MAX_NODES = self.config_file.getint('Individual', 'IND_MAX_NODES')

        # Genes mutations
        self.ADD_GENE_PROB = self.config_file.getfloat('Mutations', 'ADD_GENE_PROB')
        self.MUT_GENE_PROB = self.config_file.getfloat('Mutations', 'MUT_GENE_PROB')
        self.REM_GENE_PROB = self.config_file.getfloat('Mutations', 'REM_GENE_PROB')

        self.ADD_NODE_PROB = self.config_file.getfloat('Mutations', 'ADD_NODE_PROB')
        self.REM_NODE_PROB = self.config_file.getfloat('Mutations', 'REM_NODE_PROB')

        self.MUT_GENE_AMP = self.config_file.getfloat('Mutations', 'MUT_GENE_AMP')
        self.WEIGHT_AMP = self.config_file.getfloat('Mutations', 'WEIGHT_AMP')

        self.GENE_PROB_FACT = self.config_file.getfloat('Mutations', 'GENE_PROB_FACT')
        self.NODE_PROB_FACT = self.config_file.getfloat('Mutations', 'NODE_PROB_FACT')
        self.AMP_MUT_FACT = self.config_file.getfloat('Mutations', 'AMP_MUT_FACT')

        # Elitism and extinction
        self.ELITISM_NUMBER = self.config_file.getint('Crossover', 'ELITISM_NUMBER')
        self.EXTINCTION_NUMBER = self.config_file.getint('Crossover', 'EXTINCTION_NUMBER')

        # Training conditions
        self.FITNESS_CRITERION = self.config_file.get('Training', 'FITNESS_CRITERION')
        self.FITNESS_THRESHOLD = self.config_file.getfloat('Training', 'FITNESS_THRESHOLD')

        # Check the loaded configuration
        self.__check_config()
