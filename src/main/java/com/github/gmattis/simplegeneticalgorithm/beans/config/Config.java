package com.github.gmattis.simplegeneticalgorithm.beans.config;

public class Config {
	
	private PopulationConfig population;
	private IndividualConfig individual;
	private CrossoverConfig crossover;
	private TrainingConfig training;
	private MutationsConfig mutations;
	
	public PopulationConfig getPopulation() {
		return population;
	}
	
	public void setPopulation(PopulationConfig population) {
		this.population = population;
	}

	public IndividualConfig getIndividual() {
		return individual;
	}

	public void setIndividual(IndividualConfig individual) {
		this.individual = individual;
	}

	public CrossoverConfig getCrossover() {
		return crossover;
	}

	public void setCrossover(CrossoverConfig crossover) {
		this.crossover = crossover;
	}

	public TrainingConfig getTraining() {
		return training;
	}

	public void setTraining(TrainingConfig training) {
		this.training = training;
	}

	public MutationsConfig getMutations() {
		return mutations;
	}

	public void setMutations(MutationsConfig mutations) {
		this.mutations = mutations;
	}
}
