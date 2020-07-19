package com.tcs.hackathon.entity;

public class Customer {

	@Override
	public String toString() {
		return "Customer [id=" + id + ", firstName=" + firstName + ", lastName=" + lastName + ", campaignResponse="
				+ campaignResponse + ", timeSpentOnCompanySite=" + timeSpentOnCompanySite + ", visitsToCompanySite="
				+ visitsToCompanySite + ", sportsScore=" + sportsScore + ", moviesScore=" + moviesScore
				+ ", technologyScore=" + technologyScore + ", financeScore=" + financeScore + ", politicsScore="
				+ politicsScore + ", travelScore=" + travelScore + ", businessScore=" + businessScore
				+ ", internationalScore=" + internationalScore + ", age=" + age + ", gender=" + gender + ", relation="
				+ relation + ", familySize=" + familySize + ", jobLevel=" + jobLevel + ", income=" + income
				+ ", ownedVehicles=" + ownedVehicles + ", sale=" + sale + "]";
	}

	private long id;

	private String firstName;

	private String lastName;

	private String campaignResponse;

	private String timeSpentOnCompanySite;

	private String visitsToCompanySite;

	private int sportsScore;

	private int moviesScore;

	private int technologyScore;

	private int financeScore;

	private int politicsScore;

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public String getFirstName() {
		return firstName;
	}

	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}

	public String getLastName() {
		return lastName;
	}

	public void setLastName(String lastName) {
		this.lastName = lastName;
	}

	public String getCampaignResponse() {
		return campaignResponse;
	}

	public void setCampaignResponse(String campaignResponse) {
		this.campaignResponse = campaignResponse;
	}

	public String getTimeSpentOnCompanySite() {
		return timeSpentOnCompanySite;
	}

	public void setTimeSpentOnCompanySite(String timeSpentOnCompanySite) {
		this.timeSpentOnCompanySite = timeSpentOnCompanySite;
	}

	public String getVisitsToCompanySite() {
		return visitsToCompanySite;
	}

	public void setVisitsToCompanySite(String visitsToCompanySite) {
		this.visitsToCompanySite = visitsToCompanySite;
	}

	public int getSportsScore() {
		return sportsScore;
	}

	public void setSportsScore(int sportsScore) {
		this.sportsScore = sportsScore;
	}

	public int getMoviesScore() {
		return moviesScore;
	}

	public void setMoviesScore(int moviesScore) {
		this.moviesScore = moviesScore;
	}

	public int getTechnologyScore() {
		return technologyScore;
	}

	public void setTechnologyScore(int technologyScore) {
		this.technologyScore = technologyScore;
	}

	public int getFinanceScore() {
		return financeScore;
	}

	public void setFinanceScore(int financeScore) {
		this.financeScore = financeScore;
	}

	public int getPoliticsScore() {
		return politicsScore;
	}

	public void setPoliticsScore(int politicsScore) {
		this.politicsScore = politicsScore;
	}

	public int getTravelScore() {
		return travelScore;
	}

	public void setTravelScore(int travelScore) {
		this.travelScore = travelScore;
	}

	public int getBusinessScore() {
		return businessScore;
	}

	public void setBusinessScore(int businessScore) {
		this.businessScore = businessScore;
	}

	public int getInternationalScore() {
		return internationalScore;
	}

	public void setInternationalScore(int internationalScore) {
		this.internationalScore = internationalScore;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public String getGender() {
		return gender;
	}

	public void setGender(String gender) {
		this.gender = gender;
	}

	public String getRelation() {
		return relation;
	}

	public void setRelation(String relation) {
		this.relation = relation;
	}

	public int getFamilySize() {
		return familySize;
	}

	public void setFamilySize(int familySize) {
		this.familySize = familySize;
	}

	public String getJobLevel() {
		return jobLevel;
	}

	public void setJobLevel(String jobLevel) {
		this.jobLevel = jobLevel;
	}

	public String getIncome() {
		return income;
	}

	public void setIncome(String income) {
		this.income = income;
	}

	public int getOwnedVehicles() {
		return ownedVehicles;
	}

	public void setOwnedVehicles(int ownedVehicles) {
		this.ownedVehicles = ownedVehicles;
	}

	public Sale getSale() {
		return sale;
	}

	public void setSale(Sale sale) {
		this.sale = sale;
	}

	private int travelScore;

	private int businessScore;

	private int internationalScore;

	private int age;

	private String gender;

	private String relation;

	private int familySize;

	private String jobLevel;

	private String income;

	private int ownedVehicles;

	private Sale sale;

}
