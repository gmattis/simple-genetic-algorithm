package com.github.gmattis.simplegeneticalgorithm.beans.config;

public class MutationsConfig {
	
	private double addGeneProb;
	private double mutateGeneProb;
	private double removeGeneProb;
	private double addNodeProb;
	private double removeNodeProb;
	private double geneMutationAplitude;
	private double weightsAmplitude;
	private double geneMutationsFactor;
	private double nodeFactor;
	private double geneMutationAplitudeFactor;
	
	public double getAddGeneProb() {
		return addGeneProb;
	}
	
	public void setAddGeneProb(double addGeneProb) {
		this.addGeneProb = addGeneProb;
	}

	public double getMutateGeneProb() {
		return mutateGeneProb;
	}

	public void setMutateGeneProb(double mutateGeneProb) {
		this.mutateGeneProb = mutateGeneProb;
	}

	public double getRemoveGeneProb() {
		return removeGeneProb;
	}

	public void setRemoveGeneProb(double removeGeneProb) {
		this.removeGeneProb = removeGeneProb;
	}

	public double getAddNodeProb() {
		return addNodeProb;
	}

	public void setAddNodeProb(double addNodeProb) {
		this.addNodeProb = addNodeProb;
	}

	public double getRemoveNodeProb() {
		return removeNodeProb;
	}

	public void setRemoveNodeProb(double removeNodeProb) {
		this.removeNodeProb = removeNodeProb;
	}

	public double getGeneMutationAplitude() {
		return geneMutationAplitude;
	}

	public void setGeneMutationAplitude(double geneMutationAplitude) {
		this.geneMutationAplitude = geneMutationAplitude;
	}

	public double getWeightsAmplitude() {
		return weightsAmplitude;
	}

	public void setWeightsAmplitude(double weightsAmplitude) {
		this.weightsAmplitude = weightsAmplitude;
	}

	public double getGeneMutationsFactor() {
		return geneMutationsFactor;
	}

	public void setGeneMutationsFactor(double geneMutationsFactor) {
		this.geneMutationsFactor = geneMutationsFactor;
	}

	public double getNodeFactor() {
		return nodeFactor;
	}

	public void setNodeFactor(double nodeFactor) {
		this.nodeFactor = nodeFactor;
	}

	public double getGeneMutationAplitudeFactor() {
		return geneMutationAplitudeFactor;
	}

	public void setGeneMutationAplitudeFactor(double geneMutationAplitudeFactor) {
		this.geneMutationAplitudeFactor = geneMutationAplitudeFactor;
	}
}
