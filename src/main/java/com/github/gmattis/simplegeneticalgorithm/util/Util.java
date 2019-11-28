package com.github.gmattis.simplegeneticalgorithm.util;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.nd4j.linalg.api.ndarray.INDArray;

public class Util {
	public static List<Integer> listRange(int start, int stop) {
		List<Integer> range = new ArrayList<Integer>();
		for(int i = start; i < stop; i++) {
			range.add(i);
		}
		return range;
	}
	
	public static <T> T rdmChoice(Random rdm, List<T> list) {
		return list.get(rdm.nextInt(list.size()));
	}
	
	public static boolean all(INDArray arr, Double comp){
		for(int i = 0; i < arr.length(); i++) {
			if(arr.getDouble(i) != comp) {
				return false;
			}
		}
		return true;
	}
	
	public static boolean any(INDArray arr, Double comp){
		for(int i = 0; i < arr.length(); i++) {
			if(arr.getDouble(i) == comp) {
				return true;
			}
		}
		return false;
	}
}
