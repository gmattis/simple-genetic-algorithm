package com.github.gmattis.simplegeneticalgorithm.beans.algo;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.cpu.nativecpu.NDArray;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.indexing.INDArrayIndex;
import org.nd4j.linalg.indexing.NDArrayIndex;

import com.github.gmattis.simplegeneticalgorithm.beans.config.Config;
import com.github.gmattis.simplegeneticalgorithm.beans.config.IndividualConfig;
import com.github.gmattis.simplegeneticalgorithm.beans.config.MutationsConfig;
import com.github.gmattis.simplegeneticalgorithm.util.Activation;
import com.github.gmattis.simplegeneticalgorithm.util.Util;

public class Individual {

	private IndividualConfig indivConfig;
	private MutationsConfig mutConfig;

	private int nInput;
	private int nOutput;
	private int maxNode;
	private int totalSize;
	private Activation activation;
	private Activation outActivation;

	private INDArray genes;
	private INDArray values;
	private Random rdm;

	public Individual(Config config, Activation activation, Activation outActivation,
			boolean generateNetwork) {
		this.rdm = new Random();
		//rdm.setSeed(System.currentTimeMillis());
		
		this.indivConfig = config.getIndividual();
		this.mutConfig = config.getMutations();

		// Variables init
		this.nInput = indivConfig.getInputNumber();
		this.nOutput = indivConfig.getOutputNumber();
		this.maxNode = indivConfig.getMaxNodes();
		this.totalSize = nInput + nOutput + maxNode;
		this.activation = activation;
		this.outActivation = outActivation;

		// Genes generation
		this.genes = Nd4j.zeros(totalSize, totalSize).addi(Double.POSITIVE_INFINITY);
		this.values = Nd4j.zeros(totalSize).addi(Double.POSITIVE_INFINITY);

		if (generateNetwork) {
			switch (indivConfig.getInitialGeneration()) {
			case FULL:
				for (int i = nInput + maxNode; i < totalSize; i++) {
					for (int j = 0; j < nInput; j++) {
						genes.putScalar(i, j, 2. * rdm.nextDouble() - 1.);
					}
				}
				break;
			case RANDOM:
				for (int i = nInput + maxNode; i < totalSize; i++) {
					for (int j = 0; j < nInput; j++) {
						if (rdm.nextDouble() < 0.5) {
							genes.putScalar(i, j, 2. * rdm.nextDouble() - 1.);
						}
					}
				}
				break;
			case RANDOM_NODES:
				for (int i = nInput + maxNode; i < totalSize; i++) {
					for (int j = 0; j < nInput; j++) {
						genes.putScalar(i, j, 2 * rdm.nextDouble() - 1);
					}
				}

				for (int i = nInput; i < nInput + maxNode; i++) {
					if (rdm.nextDouble() < 0.5) {
						this.addNode();
					}
				}

				for (int i = nInput; i < nInput + maxNode; i++) {
					if (rdm.nextDouble() < 0.5) {
						this.addGene();
					}
				}
				break;
			default:
				throw new IllegalArgumentException("Initial Generation must be `FULL`, `RANDOM`, or `RANDOM_NODES`");
			}
		}
	}

	private List<int[]> availableGenes() {
		List<int[]> availableGenes = new ArrayList<int[]>();
		for (int i : validToNodes()) {
			for (int j : validFromNodes()) {
				if (genes.getDouble(i, j) == Double.POSITIVE_INFINITY
						&& genes.getDouble(j, i) == Double.POSITIVE_INFINITY && j != i) {
					availableGenes.add(new int[] { i, j });
				}
			}
		}
		return availableGenes;
	}

	private List<int[]> existingGenes() {
		List<int[]> existingGenes = new ArrayList<int[]>();
		for (int i : validToNodes()) {
			for (int j : validFromNodes()) {
				if (genes.getDouble(i, j) != Double.POSITIVE_INFINITY) {
					existingGenes.add(new int[] { i, j });
				}
			}
		}
		return existingGenes;
	}

	private List<Integer> validFromNodes() {
		List<Integer> validNodes = Util.listRange(0, nInput);
		for (int i = nInput; i < nInput + maxNode; i++) {
			if (!Util.all(genes.slice(i, 0).reshape(totalSize), Double.POSITIVE_INFINITY)
					&& !Util.all(genes.slice(i, 1).reshape(totalSize), Double.POSITIVE_INFINITY)) {
				validNodes.add(i);
			}
		}
		return validNodes;
	}

	private List<Integer> validToNodes() {
		List<Integer> validNodes = Util.listRange(nInput + maxNode, totalSize);
		for (int i = nInput; i < nInput + maxNode; i++) {
			if (!Util.all(genes.slice(i, 0).reshape(totalSize), Double.POSITIVE_INFINITY)
					&& !Util.all(genes.slice(i, 1).reshape(totalSize), Double.POSITIVE_INFINITY)) {
				validNodes.add(i);
			}
		}
		return validNodes;
	}

	private void checkPath(int node, List<Integer> alreadyChecked) {
		if (!(node < nInput)) {
			if (alreadyChecked.contains(node)) {
				genes.putScalar(alreadyChecked.get(alreadyChecked.size() - 1), node, Double.POSITIVE_INFINITY);

				if (Util.all(genes.slice(node, 1).reshape(totalSize), Double.POSITIVE_INFINITY)) {
					for (int i = nInput; i < nInput + maxNode; i++) {
						if (genes.getDouble(node, i) != Double.POSITIVE_INFINITY) {
							genes.putScalar(node, i, Double.POSITIVE_INFINITY);
							checkPath(i, new ArrayList<Integer>());
						}
					}
				}
			}

			if (Util.all(genes.slice(node, 0).reshape(totalSize), Double.POSITIVE_INFINITY)) {
				for (int i = nInput; i < totalSize; i++) {
					if (genes.getDouble(i, node) != Double.POSITIVE_INFINITY) {
						genes.putScalar(i, node, Double.POSITIVE_INFINITY);
						checkPath(i, new ArrayList<Integer>());
					}
				}
			}

			for (int i = 0; i < totalSize; i++) {
				if (genes.getDouble(node, i) != Double.POSITIVE_INFINITY) {
					List<Integer> pathCopy = new ArrayList<Integer>(alreadyChecked);
					pathCopy.add(i);
					checkPath(i, pathCopy);
				}
			}
		}
	}

	private void process(int node) {
		double out = 0.;
		for (int i = 0; i < nInput + maxNode; i++) {
			if (genes.getDouble(node, i) != Double.POSITIVE_INFINITY) {
				if (values.getDouble(i) == Double.POSITIVE_INFINITY) {
					process(i);
				}
				out += values.getDouble(i) * genes.getDouble(node, i);
			}
		}
		try {
			if (node < nInput + maxNode) {
				Method act = Activation.class.getMethod(activation.getName(), double.class);
				values.putScalar(node, (double) act.invoke(null, out));
			} else {
				Method act = Activation.class.getMethod(outActivation.getName(), double.class);
				values.putScalar(node, (double) act.invoke(null, out));
			}
		} catch (IllegalAccessException | IllegalArgumentException | InvocationTargetException | NoSuchMethodException | SecurityException e) {
			throw new InternalError();
		}
	}

	public void addGene() {
		List<int[]> availableGenes = availableGenes();
		if(!availableGenes.isEmpty()) {
			int[] newGene = Util.rdmChoice(rdm, availableGenes);
			genes.putScalar(newGene[0], newGene[1], mutConfig.getWeightsAmplitude()*(2*rdm.nextDouble() - 1));
		}
	}

	public void addNode() {
		List<int[]> existingGenes = existingGenes();
		if (existingGenes.isEmpty()) {
			addGene();
			return;
		}
		
		List<Integer> emptyNodes = new ArrayList<Integer>();
		for(int i = nInput; i < nInput + maxNode; i++) {
			if(Util.all(genes.slice(i, 0).reshape(totalSize), Double.POSITIVE_INFINITY)) {
				emptyNodes.add(i);
			}
		}
		
		if(!emptyNodes.isEmpty()) {
			int[] repGene = Util.rdmChoice(rdm, existingGenes);
			int newNode = Util.rdmChoice(rdm, emptyNodes);
			
			genes.putScalar(repGene[0], repGene[1], Double.POSITIVE_INFINITY);
			genes.putScalar(repGene[0], newNode, mutConfig.getWeightsAmplitude()*(2*rdm.nextDouble() - 1));
			genes.putScalar(newNode, repGene[1], mutConfig.getWeightsAmplitude()*(2*rdm.nextDouble() - 1));
		}
	}
	
	public void removeGene() {
		List<int[]> existingGenes = existingGenes();
		if(existingGenes.size() > 1) {
			int[] selectedGene = Util.rdmChoice(rdm, existingGenes);
			genes.putScalar(selectedGene[0], selectedGene[1], Double.POSITIVE_INFINITY);
		}
	}
	
	public void removeNodes() {
		List<Integer> existingNodes = new ArrayList<Integer>();
		for(int i = nInput; i < nInput + maxNode; i++) {
			if(!Util.all(genes.slice(i, 0).reshape(totalSize), Double.POSITIVE_INFINITY)) {
				existingNodes.add(i);
			}
		}
		
		if(!existingNodes.isEmpty()) {
			int remNode = Util.rdmChoice(rdm, existingNodes);
			List<Integer> fromNodes = new ArrayList<Integer>(), toNodes = new ArrayList<Integer>();
			
			for(int i = 0; i < nInput + maxNode; i++) {
				if(genes.getDouble(remNode, i) != Double.POSITIVE_INFINITY) {
					fromNodes.add(i);
					genes.put(remNode, i, Double.POSITIVE_INFINITY);
				}
			}
			
			for(int i = nInput; i < totalSize; i++) {
				if(genes.getDouble(i, remNode) != Double.POSITIVE_INFINITY) {
					toNodes.add(i);
					genes.put(i, remNode, Double.POSITIVE_INFINITY);
				}
			}
			
			for(int i : toNodes) {
				for(int j : fromNodes) {
					if (genes.getDouble(i, j) != Double.POSITIVE_INFINITY && rdm.nextDouble() < 0.5) {
						genes.putScalar(i, j, mutConfig.getWeightsAmplitude()*(2*rdm.nextDouble() - 1));
					}
				}
			}
		}
	}
	
	public void mutate(double rate, double amplitude) {
		for(int i = nInput; i < totalSize; i++) {
			for(int j = 0; j < nInput + maxNode; j++) {
				if(rdm.nextDouble() < rate && genes.getDouble(i, j) != Double.POSITIVE_INFINITY) {
					genes.putScalar(i, j, genes.getDouble(i, j) + amplitude*(2*rdm.nextDouble() - 1));
				}
			}
		}
	}
	
	public void cleanup() {
		for(int i = nInput + maxNode; i < totalSize; i++) {
			checkPath(i, new ArrayList<Integer>());
		}
	}
	
	public INDArray predict(INDArray inputs) {
		values.addi(Double.POSITIVE_INFINITY);
		INDArrayIndex[] indices = new INDArrayIndex[] {NDArrayIndex.interval(0, nInput)};
		values.put(indices, inputs);
		
		for(int i = nInput + maxNode; i < totalSize; i++) {
			process(i);
		}
		
		return values.get(NDArrayIndex.interval(nInput + maxNode, totalSize));
	}
}
