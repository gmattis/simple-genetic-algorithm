package com.github.gmattis.simplegeneticalgorithm.beans.config;

public class TrainingConfig {
	
	private FitnessCriterion fitnessCriterion;
	private double fitnessThreshold;
	
	public FitnessCriterion getFitnessCriterion() {
		return fitnessCriterion;
	}
	
	public void setFitnessCriterion(FitnessCriterion fitnessCriterion) {
		this.fitnessCriterion = fitnessCriterion;
	}

	public double getFitnessThreshold() {
		return fitnessThreshold;
	}

	public void setFitnessThreshold(double fitnessThreshold) {
		this.fitnessThreshold = fitnessThreshold;
	}
}
