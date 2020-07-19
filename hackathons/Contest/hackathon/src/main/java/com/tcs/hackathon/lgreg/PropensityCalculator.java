package com.tcs.hackathon.lgreg;

import Jama.Matrix;

public class PropensityCalculator {

	Matrix factorMatrix = null;

	public void calculateLead(double[][] features, double[][] existingSales) {

		Matrix leadsMatrix = new Matrix(features);
		Matrix salesMatrix = new Matrix(existingSales);
		Matrix invertedMatrix = (leadsMatrix.transpose().times(leadsMatrix)).inverse();
		factorMatrix = (invertedMatrix.times(leadsMatrix.transpose())).times(salesMatrix);
		
	}

	public double[][] calculatePropensity(double[][] newLeads) {
		Matrix leadsMatrix = new Matrix(newLeads);
		double[][] resultArray = new double[leadsMatrix.getRowDimension()][2];
		Matrix result = leadsMatrix.times(factorMatrix);
		for (int rowIndex = 0; rowIndex < result.getRowDimension(); rowIndex++) {
			for (int colIndex = 0; colIndex < result.getColumnDimension(); colIndex++) {
				resultArray[rowIndex][colIndex] = result.get(rowIndex, colIndex);
			}
		}
		return resultArray;
	}

}
