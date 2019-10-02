import numpy as np
from typing import Iterable, Callable, Union

from . import config
from .individual import Individual


def save(population: Iterable[Individual], gen: Union[int, str]):
    genes_arrays = np.array([ind.genes for ind in population])
    np.save("sga-state-" + str(gen), genes_arrays)
    print("Saved population state")


def load(path: str, def_act_f: Callable, out_act_f: Callable = None) -> Iterable[Individual]:
    genes_arrays = np.load(path)

    population = np.empty(config.POPULATION_SIZE, dtype=Individual)
    for i in range(len(genes_arrays)):
        population[i] = Individual(def_act_f, out_act_f)
        population[i].genes = genes_arrays[i]
    return population
