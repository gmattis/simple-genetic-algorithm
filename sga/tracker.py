from .config import Config


class Tracker:
    def __init__(self, config: Config):
        self.config = config

        # Variables initialization
        self.raw_fitness_tracking = []
        self.avg_fitness_tracking = []
        self.min_fitness_tracking = []
        self.max_fitness_tracking = []

    def append(self, fitness):
        """ Adds new values to the tracking lists """
        self.raw_fitness_tracking.append(fitness)
        self.avg_fitness_tracking.append(sum(fitness) / len(fitness))
        self.min_fitness_tracking.append(min(fitness))
        self.max_fitness_tracking.append(max(fitness))

    def get_raw(self):
        """ Returns the list of raw fitness """
        return self.raw_fitness_tracking

    def get_avg(self):
        """ Returns the list of average fitness """
        return self.avg_fitness_tracking

    def get_min(self):
        """ Returns the list of minimum fitness """
        return self.min_fitness_tracking

    def get_max(self):
        """ Return the list of maximum fitness """
        return self.max_fitness_tracking

    def get_last_stats(self):
        """ Returns the average, minimum and maximum fitness for the last generation """
        if self.raw_fitness_tracking:
            return self.avg_fitness_tracking[-1], self.min_fitness_tracking[-1], self.max_fitness_tracking[-1]

    def get_last_percentages(self):
        """ Returns the progression in percent for the last generation """
        if len(self.raw_fitness_tracking) > 1:
            avg_percentage = (self.avg_fitness_tracking[-1] - self.avg_fitness_tracking[-2]) * \
                100 / self.config.FITNESS_THRESHOLD
            min_percentage = (self.min_fitness_tracking[-1] - self.min_fitness_tracking[-2]) * \
                100 / self.config.FITNESS_THRESHOLD
            max_percentage = (self.max_fitness_tracking[-1] - self.max_fitness_tracking[-2]) * \
                100 / self.config.FITNESS_THRESHOLD
        else:
            avg_percentage = self.avg_fitness_tracking[-1] * 100 / self.config.FITNESS_THRESHOLD
            min_percentage = self.min_fitness_tracking[-1] * 100 / self.config.FITNESS_THRESHOLD
            max_percentage = self.max_fitness_tracking[-1] * 100 / self.config.FITNESS_THRESHOLD
        return avg_percentage, min_percentage, max_percentage

    def print_stats(self):
        """ Prints the statistics for the last generation """
        avg_fitness, min_fitness, max_fitness = self.get_last_stats()
        avg_percent, min_percent, max_percent = self.get_last_percentages()

        print("- avg. fitness: {:.5f} [ {:.5f}% ]".format(avg_fitness, avg_percent))
        print("- min. fitness: {:.5f} [ {:.5f}% ]".format(min_fitness, min_percent))
        print("- max. fitness: {:.5f} [ {:.5f}% ]".format(max_fitness, max_percent))

    def reset(self):
        """ Resets the fitness trackers """
        self.raw_fitness_tracking = []
        self.avg_fitness_tracking = []
        self.min_fitness_tracking = []
        self.max_fitness_tracking = []
