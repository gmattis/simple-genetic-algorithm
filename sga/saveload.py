import numpy as np

from typing import Callable, Iterable, Optional, Union

from .config import Config
from .individual import Individual


def save(population: Iterable[Individual], gen: Union[int, str]):
    """ Saves the population's genes """
    genes_arrays = np.array([ind.genes for ind in population])
    np.save("sga-state-" + str(gen), genes_arrays)
    print("Saved population state")


def load(path: str, config: Config, def_act_f: Callable, out_act_f: Optional[Callable] = None) -> Iterable[Individual]:
    """ Returns the population from a saved state """
    genes_arrays = np.load(path)
    population = np.empty(config.POPULATION_SIZE, dtype=Individual)
    for i in range(len(genes_arrays)):
        population[i] = Individual(config, def_act_f, out_act_f)
        population[i].genes = genes_arrays[i]
    return population
