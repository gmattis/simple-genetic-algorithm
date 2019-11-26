package com.github.gmattis.simplegeneticalgorithm.beans.config;

public class CrossoverConfig {
	
	private int elitismNumber;
	private int extinctionNumber;
	
	public int getElitismNumber() {
		return elitismNumber;
	}
	
	public void setElitismNumber(int elitismNumber) {
		this.elitismNumber = elitismNumber;
	}

	public int getExtinctionNumber() {
		return extinctionNumber;
	}

	public void setExtinctionNumber(int extinctionNumber) {
		this.extinctionNumber = extinctionNumber;
	}
}
