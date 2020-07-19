package com.tcs.hackathon;

import java.io.File;
import java.io.FileInputStream;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;

import com.tcs.hackathon.entity.Customer;
import com.tcs.hackathon.entity.Sale;
import com.tcs.hackathon.lgreg.PropensityCalculator;

/**
 * Main program for executing the job
 * 
 * @author Raja
 *
 */
public class InputParser {
	/**
	 * @param args
	 */
	public static void main(String[] args) {

		PropensityCalculator propensity = new PropensityCalculator();

		try {

			if (args.length != 1) {
				System.out.println("Please provide the filename");
				System.exit(0);
			} else {
				FileInputStream file = new FileInputStream(new File(args[0]));
				Workbook workbook = WorkbookFactory.create(file);
				Map<Long, Customer> customerMap = new LinkedHashMap<Long, Customer>();
				Map<String, Integer> colorMap = new HashMap<String, Integer>();
				Map<String, Integer> typeMap = new HashMap<String, Integer>();
				Map<Long, Customer> newLeadsMap = new LinkedHashMap<Long, Customer>();

				// Sales Block
				extractSales(workbook, customerMap, colorMap, typeMap);

				// Old Leads block
				extractLeads(workbook, customerMap, 1);

				// new Leads block
				extractLeads(workbook, newLeadsMap, 3);

				double[][] features = new double[customerMap.size()][19];
				double[][] sales = new double[customerMap.size()][2];
				extractFeatureSales(customerMap, colorMap, typeMap, features, sales);
				propensity.calculateLead(features, sales);

				features = new double[newLeadsMap.size()][19];
				sales = new double[newLeadsMap.size()][2];
				extractFeatureSales(newLeadsMap, colorMap, typeMap, features, sales);

				sales = propensity.calculatePropensity(features);

				colorMap = sortMapByValue(colorMap);
				typeMap = sortMapByValue(typeMap);
				List<Long> newLeadsKeySet = new ArrayList<Long>(newLeadsMap.keySet());
				for (int rowIndex = 0; rowIndex < newLeadsMap.size(); rowIndex++) {
					double modelScore = sales[rowIndex][0];
					double colorScore = sales[rowIndex][1];
					Customer customer = newLeadsMap.get(newLeadsKeySet.get(rowIndex));
					StringBuilder message = new StringBuilder("Propensity of Customer ");
					message.append(customer.getFirstName());
					message.append(" ");
					message.append(customer.getLastName());
					message.append(" = ");

					for (Entry<String, Integer> entry : typeMap.entrySet()) {
						double percent = ((Math.abs(modelScore - entry.getValue())) / modelScore) * 100;
						message.append(" " + entry.getKey());
						message.append("-");
						message.append(roundValue(percent));
						message.append("%");
					}
					for (Entry<String, Integer> entry : colorMap.entrySet()) {
						double percent = ((Math.abs(colorScore - entry.getValue())) / colorScore) * 100;
						message.append(" " + entry.getKey());
						message.append("-");
						message.append(roundValue(percent));
						message.append("%");
					}
					System.out.println(message);
				}

			}
		} catch (Exception e) {
			System.out.println("Error in Main Program" + e);
			e.printStackTrace();
		}
	}

	private static double roundValue(double value) {
		BigDecimal bd = new BigDecimal(value);
		bd = bd.setScale(3, RoundingMode.HALF_UP);
		return bd.doubleValue();
	}

	private static Map<String, Integer> sortMapByValue(Map<String, Integer> map) {
		Map<String, Integer> output = new LinkedHashMap<String, Integer>();
		List<Integer> valueList = new ArrayList<>(map.values());
		Collections.sort(valueList);
		for (Integer value : valueList) {
			for (Entry<String, Integer> entry : map.entrySet()) {
				if (entry.getValue() == value) {
					output.put(entry.getKey(), entry.getValue());
					break;
				}
			}
		}

		return output;
	}

	private static void extractFeatureSales(Map<Long, Customer> customerMap, Map<String, Integer> colorMap,
			Map<String, Integer> typeMap, double[][] features, double[][] sales) {
		int featureRow = 0;
		for (Customer customer : customerMap.values()) {
			int column = 0;
			features[featureRow][column++] = 1;
			features[featureRow][column++] = "No".equals(customer.getCampaignResponse()) ? 1
					: "NA".equals(customer.getCampaignResponse()) ? 2 : 0;
			features[featureRow][column++] = "NA".equals(customer.getTimeSpentOnCompanySite()) ? 0
					: Double.valueOf(customer.getTimeSpentOnCompanySite());
			features[featureRow][column++] = "NA".equals(customer.getVisitsToCompanySite()) ? 0
					: Double.valueOf(customer.getVisitsToCompanySite());
			features[featureRow][column++] = customer.getSportsScore();
			features[featureRow][column++] = customer.getMoviesScore();
			features[featureRow][column++] = customer.getTechnologyScore();
			features[featureRow][column++] = customer.getFinanceScore();
			features[featureRow][column++] = customer.getPoliticsScore();
			features[featureRow][column++] = customer.getTravelScore();
			features[featureRow][column++] = customer.getBusinessScore();
			features[featureRow][column++] = customer.getInternationalScore();
			features[featureRow][column++] = customer.getAge();
			features[featureRow][column++] = "Male".equals(customer.getGender()) ? 1
					: "Female".equals(customer.getGender()) ? 2 : 0;
			features[featureRow][column++] = "Single".equals(customer.getRelation()) ? 1
					: "Married".equals(customer.getRelation()) ? 2 : 3;
			features[featureRow][column++] = customer.getFamilySize();
			features[featureRow][column++] = getJobIndex(customer.getJobLevel());
			features[featureRow][column++] = getSalaryIndex(customer.getIncome());
			features[featureRow][column++] = customer.getOwnedVehicles();

			if (customer.getSale() != null) {
				int typeIndex = typeMap.get(customer.getSale().getModel());
				int colorIndex = colorMap.get(customer.getSale().getColor());
				sales[featureRow][0] = typeIndex;
				sales[featureRow][1] = colorIndex;
			} else {
				sales[featureRow][0] = 0;
				sales[featureRow][1] = 0;
			}

			featureRow++;
		}
	}

	private static double getSalaryIndex(String income) {
		// TODO Auto-generated method stub
		double value = 0;
		String[] input = income.split(" ");

		switch (input[input.length - 1]) {
		case "34,999":
			value = 2;
			break;
		case "99,999":
			value = 3;
			break;
		case "74,999":
			value = 5;
			break;
		case "25,000":
			value = 1;
			break;
		case "49,999":
			value = 4;
			break;
		case "100000":
			value = 6;
			break;
		default:
			value = 0;
		}
		return value;
	}

	private static double getJobIndex(String jobLevel) {
		double value = 0;
		switch (jobLevel) {
		case "Entry Level":
			value = 2;
			break;
		case "Manager":
			value = 3;
			break;
		case "Director":
			value = 5;
			break;
		case "Sr. Manager":
			value = 4;
			break;
		case "intern":
			value = 1;
			break;
		default:
			value = 0;
		}

		return value;
	}

	private static int extractSales(Workbook workbook, Map<Long, Customer> customerMap, Map<String, Integer> colorMap,
			Map<String, Integer> typeMap) {
		boolean firstRow = true;
		int salesCount = 0;
		Sheet sheet = workbook.getSheetAt(2);
		Iterator<Row> rowIterator = sheet.iterator();
		while (rowIterator.hasNext()) {
			Iterator<Cell> cellIterator = rowIterator.next().cellIterator();
			if (firstRow) {
				firstRow = false;
				continue;
			}
			Sale sale = new Sale();
			Customer customer = new Customer();
			customer.setSale(sale);
			customer.setId(Double.valueOf(getNextValue(cellIterator)).longValue());
			customerMap.put(customer.getId(), customer);
			sale.setSaleDate(getNextValue(cellIterator));
			sale.setModel(getNextValue(cellIterator));
			sale.setColor(getNextValue(cellIterator));
			sale.setPanaromicRoof(Double.valueOf(getNextValue(cellIterator)).intValue());
			sale.setBlackBody(Double.valueOf(getNextValue(cellIterator)).intValue());
			sale.setHyperblackAluminiumWheel(Double.valueOf(getNextValue(cellIterator)).intValue());
			sale.setCruiseControl(Double.valueOf(getNextValue(cellIterator)).intValue());
			sale.setMetallicCoat(Double.valueOf(getNextValue(cellIterator)).intValue());
			sale.setLeatherTrimmedHeat(Double.valueOf(getNextValue(cellIterator)).intValue());
			sale.setVentSportSeat(Double.valueOf(getNextValue(cellIterator)).intValue());

			int colorCount = 1;
			if (colorMap.containsKey(sale.getColor())) {
				colorCount = colorCount + colorMap.get(sale.getColor());
			}
			colorMap.put(sale.getColor(), colorCount);

			int typeCount = 1;
			if (typeMap.containsKey(sale.getModel())) {
				typeCount = typeCount + typeMap.get(sale.getModel());
			}
			typeMap.put(sale.getModel(), typeCount);

			salesCount++;

		}
		return salesCount;
	}

	private static void extractLeads(Workbook workbook, Map<Long, Customer> customerMap, int index) {
		boolean firstRow = true;
		Sheet sheet = workbook.getSheetAt(index);
		Iterator<Row> rowIterator = sheet.iterator();
		while (rowIterator.hasNext()) {
			Iterator<Cell> cellIterator = rowIterator.next().cellIterator();
			if (firstRow) {
				firstRow = false;
				continue;
			}
			long id = Double.valueOf(getNextValue(cellIterator)).longValue();
			Customer customer = customerMap.get(id);
			if(index ==3 ){
				customer = new Customer();
			}
			if (customer != null) {

				customer.setId(id);
				customer.setFirstName(getNextValue(cellIterator));
				customer.setLastName(getNextValue(cellIterator));
				customer.setCampaignResponse(getNextValue(cellIterator));
				customer.setTimeSpentOnCompanySite(getNextValue(cellIterator));
				customer.setVisitsToCompanySite(getNextValue(cellIterator));
				customer.setSportsScore(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setMoviesScore(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setTechnologyScore(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setFinanceScore(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setPoliticsScore(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setTravelScore(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setBusinessScore(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setInternationalScore(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setAge(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setGender(getNextValue(cellIterator));
				customer.setRelation(getNextValue(cellIterator));
				customer.setFamilySize(Double.valueOf(getNextValue(cellIterator)).intValue());
				customer.setJobLevel(getNextValue(cellIterator));
				customer.setIncome(getNextValue(cellIterator));
				customer.setOwnedVehicles(Double.valueOf(getNextValue(cellIterator)).intValue());

				customerMap.put(customer.getId(), customer);
			}
		}
	}

	private static String getNextValue(Iterator<Cell> cellIterator) {
		String value = "0";
		if (cellIterator.hasNext()) {
			Cell cell = cellIterator.next();
			switch (cell.getCellType()) {
			case Cell.CELL_TYPE_STRING:
				value = cell.getStringCellValue();
				break;
			case Cell.CELL_TYPE_NUMERIC:
				value = cell.getNumericCellValue() + "";
				break;
			case Cell.CELL_TYPE_FORMULA:
				value = cell.getCellFormula();
				break;
			case Cell.CELL_TYPE_BOOLEAN:
				value = cell.getBooleanCellValue() + "";
				break;
			default:
				value = "0";
			}

		}
		return value;
	}

}
