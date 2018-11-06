package com.tcs.hackathon.entity;

public class Sale {

	@Override
	public String toString() {
		return "Sale [saleDate=" + saleDate + ", model=" + model + ", color=" + color + ", panaromicRoof="
				+ panaromicRoof + ", blackBody=" + blackBody + ", hyperblackAluminiumWheel=" + hyperblackAluminiumWheel
				+ ", cruiseControl=" + cruiseControl + ", metallicCoat=" + metallicCoat + ", leatherTrimmedHeat="
				+ leatherTrimmedHeat + ", VentSportSeat=" + VentSportSeat + "]";
	}

	private String saleDate;
	
	private String model;
	
	private String color;
	
	private int panaromicRoof;
	
	private int blackBody;
	
	private int hyperblackAluminiumWheel;
	
	private int cruiseControl;
	
	private int metallicCoat;
	
	private int leatherTrimmedHeat;
	
	private int VentSportSeat;

	public String getSaleDate() {
		return saleDate;
	}

	public void setSaleDate(String saleDate) {
		this.saleDate = saleDate;
	}

	public String getModel() {
		return model;
	}

	public void setModel(String model) {
		this.model = model;
	}

	public String getColor() {
		return color;
	}

	public void setColor(String color) {
		this.color = color;
	}

	public int getPanaromicRoof() {
		return panaromicRoof;
	}

	public void setPanaromicRoof(int panaromicRoof) {
		this.panaromicRoof = panaromicRoof;
	}

	public int getBlackBody() {
		return blackBody;
	}

	public void setBlackBody(int blackBody) {
		this.blackBody = blackBody;
	}

	public int getHyperblackAluminiumWheel() {
		return hyperblackAluminiumWheel;
	}

	public void setHyperblackAluminiumWheel(int hyperblackAluminiumWheel) {
		this.hyperblackAluminiumWheel = hyperblackAluminiumWheel;
	}

	public int getCruiseControl() {
		return cruiseControl;
	}

	public void setCruiseControl(int cruiseControl) {
		this.cruiseControl = cruiseControl;
	}

	public int getMetallicCoat() {
		return metallicCoat;
	}

	public void setMetallicCoat(int metallicCoat) {
		this.metallicCoat = metallicCoat;
	}

	public int getLeatherTrimmedHeat() {
		return leatherTrimmedHeat;
	}

	public void setLeatherTrimmedHeat(int leatherTrimmedHeat) {
		this.leatherTrimmedHeat = leatherTrimmedHeat;
	}

	public int getVentSportSeat() {
		return VentSportSeat;
	}

	public void setVentSportSeat(int ventSportSeat) {
		VentSportSeat = ventSportSeat;
	}
	
}
