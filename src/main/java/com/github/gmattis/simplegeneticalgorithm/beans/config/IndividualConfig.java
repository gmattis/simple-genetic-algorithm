package com.github.gmattis.simplegeneticalgorithm.beans.config;

public class IndividualConfig {
	
	private int inputNumber;
	private int outputNumber;
	private int maxNodes;
	private InitialGeneration initialGeneration;
	
	public int getInputNumber() {
		return inputNumber;
	}
	
	public void setInputNumber(int inputNumber) {
		this.inputNumber = inputNumber;
	}

	public int getOutputNumber() {
		return outputNumber;
	}

	public void setOutputNumber(int outputNumber) {
		this.outputNumber = outputNumber;
	}

	public int getMaxNodes() {
		return maxNodes;
	}

	public void setMaxNodes(int maxNodes) {
		this.maxNodes = maxNodes;
	}

	public InitialGeneration getInitialGeneration() {
		return initialGeneration;
	}

	public void setInitialGeneration(InitialGeneration initialGeneration) {
		this.initialGeneration = initialGeneration;
	}
}
