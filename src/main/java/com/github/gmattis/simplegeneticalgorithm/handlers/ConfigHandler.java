package com.github.gmattis.simplegeneticalgorithm.handlers;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;

import com.github.gmattis.simplegeneticalgorithm.beans.config.Config;
import com.google.gson.Gson;
import com.google.gson.JsonIOException;
import com.google.gson.JsonSyntaxException;

public class ConfigHandler {
	
	private static Config config;

	public static Config getConfig() {
		return config;
	}
	
	public static void load() {
		load("sgaConfig.json");
	}

	public static void load(String filename) {
		Gson gson = new Gson();
		
		try {
			BufferedReader reader = new BufferedReader(new FileReader(filename));
			Config uchkConfig = gson.fromJson(reader, Config.class);
			checkConfig(uchkConfig);
			config = uchkConfig;
		} catch (JsonSyntaxException e) {
			throw new IllegalArgumentException("Config file JSON synthax is wrong, please check it.");
		} catch (FileNotFoundException | JsonIOException e) {
			throw new IllegalArgumentException("Config file doesn\'t exist or can\'t be read.");
		}
	}

	private static void checkConfig(Config uConfig) {
		// TODO Finir la fonction checkConfig
	}
		
}
