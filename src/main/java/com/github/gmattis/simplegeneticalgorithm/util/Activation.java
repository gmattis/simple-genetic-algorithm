package com.github.gmattis.simplegeneticalgorithm.util;

public enum Activation {
	
	IDENTITY("identity"),
	HEAVISIDE("heaviside"),
	SIGMOID("sigmoid"),
	RELU("relu"),
	SOFTPLUS("softplus"),
	GAUSS("gauss");
	
	private String name;

	Activation(String name) {
		this.name = name;
	}
	
	public String getName() {
		return name;
	}
	
	//////////////////////////
	// Activation Functions //
	//////////////////////////

	public static Double identity(Double x) {
		return x;
	}
	
	public static Double heaviside(Double x) {
		if (x >= 0) {
			return 1.;
		} else {
			return 0.;
		}
	}
	
	public static Double sigmoid(Double x) {
		return 1. / (1. + Math.exp(x));
	}
	
	public static Double relu(Double x) {
		return Math.max(0., x);
	}
	
	public static Double softplus(Double x) {
		return Math.log(1. + Math.exp(x));
	}
	
	public static Double gauss(Double x) {
		return Math.exp(-(x*x));
	}
}
