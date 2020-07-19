The program  has to be built with maven.It requires java 8
Go to the project root directory and run mvn clean package (or) mvn clean install
It generates the jar in target directory. 
The jar program takes a single excel file as input
The input file should be similar to test file provided
Program displays the propensity for the model and color

Sample Input: java -jar hackathon-0.0.1-SNAPSHOT.jar Customer_360_Hackathon_Input_Data_V1.xlsx

Algorithm
This applies a logistic regression model using normal equation. Another option would have been to use k distant neighbours 
The technical implementations uses JAMA library for matrix operations 