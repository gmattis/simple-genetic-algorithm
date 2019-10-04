import numpy as np

from typing import Iterable, List, Tuple

from . import config


class Tracker:
    def __init__(self):
        # Variables initialization
        self.raw_fitness_tracking = []
        self.avg_fitness_tracking = []
        self.min_fitness_tracking = []
        self.max_fitness_tracking = []

    def append(self, fitness: Iterable[float]):
        """ Adds new values to the tracking lists """
        self.raw_fitness_tracking.append(fitness)
        self.avg_fitness_tracking.append(np.average(fitness))
        self.min_fitness_tracking.append(np.min(fitness))
        self.max_fitness_tracking.append(np.max(fitness))

    def get_raw(self) -> List[Iterable[float]]:
        """ Returns the list of raw fitness """
        return self.raw_fitness_tracking

    def get_avg(self) -> List[float]:
        """ Returns the list of average fitness """
        return self.avg_fitness_tracking

    def get_min(self) -> List[float]:
        """ Returns the list of minimum fitness """
        return self.min_fitness_tracking

    def get_max(self) -> List[float]:
        """ Return the list of maximum fitness """
        return self.max_fitness_tracking

    def get_last_stats(self) -> Tuple[float, float, float]:
        """ Returns the average, minimum and maximum fitness for the last generation """
        if self.raw_fitness_tracking:
            return self.avg_fitness_tracking[-1], self.min_fitness_tracking[-1], self.max_fitness_tracking[-1]

    def get_last_percentages(self) -> Tuple[float, float, float]:
        """ Returns the progression in percent for the last generation """
        if len(self.raw_fitness_tracking) > 1:
            avg_percentage = (self.avg_fitness_tracking[-1] - self.avg_fitness_tracking[-2]) * 100 / config.FITNESS_THRESHOLD
            min_percentage = (self.min_fitness_tracking[-1] - self.min_fitness_tracking[-2]) * 100 / config.FITNESS_THRESHOLD
            max_percentage = (self.max_fitness_tracking[-1] - self.max_fitness_tracking[-2]) * 100 / config.FITNESS_THRESHOLD
        else:
            avg_percentage = self.avg_fitness_tracking[-1] * 100 / config.FITNESS_THRESHOLD
            min_percentage = self.min_fitness_tracking[-1] * 100 / config.FITNESS_THRESHOLD
            max_percentage = self.max_fitness_tracking[-1] * 100 / config.FITNESS_THRESHOLD
        return avg_percentage, min_percentage, max_percentage

    def print_stats(self):
        """ Prints the statistics for the last generation """
        avg_fitness, min_fitness, max_fitness = self.get_last_stats()
        avg_percent, min_percent, max_percent = self.get_last_percentages()

        stats_len = str(int(np.log10(max(abs(avg_fitness), abs(min_fitness), abs(max_fitness)) * 10000000)) + 1)
        percent_len = str(int(np.log10(max(abs(avg_percent), abs(min_percent), abs(max_percent)) * 10000000)) + 1)

        print("- avg. fitness: {:{}.5f} [ {:{}.5f}% ]".format(avg_fitness, stats_len, avg_percent, percent_len))
        print("- min. fitness: {:{}.5f} [ {:{}.5f}% ]".format(min_fitness, stats_len, min_percent, percent_len))
        print("- max. fitness: {:{}.5f} [ {:{}.5f}% ]".format(max_fitness, stats_len, max_percent, percent_len))

    def reset(self):
        """ Resets the fitness trackers """
        self.raw_fitness_tracking = []
        self.avg_fitness_tracking = []
        self.min_fitness_tracking = []
        self.max_fitness_tracking = []
