# Data Preprocessing Template

# Importing the dataset
dataset = read.csv('Position_Salaries.csv')
dataset=dataset[,2:3]

predData=dataset[1,]
predData[1,1]=6.5

regressor=lm(formula = Salary ~ .,data = dataset)
predData$Salary=predict(object = regressor,newdata = predData)

library(ggplot2)
ggplot()+
  geom_point(aes(dataset$Level,dataset$Salary),color='red')+
  geom_line(aes(dataset$Level,predict(object = regressor,newdata = dataset)),color='blue')+
  ggtitle('Salary Linear Predictor')+
  xlab('Level')+
  ylab('Salary')

dataset$Level1=dataset$Level^2
predData$Level1=predData$Level^2
dataset$Level2=dataset$Level^3
predData$Level2=predData$Level^3
dataset$Level3=dataset$Level^4
predData$Level3=predData$Level^4
regressor=lm(formula = Salary ~ .,data = dataset)
predData$Salary=predict(object = regressor,newdata = predData)

library(ggplot2)
ggplot()+
  geom_point(aes(dataset$Level,dataset$Salary),color='red')+
  geom_line(aes(dataset$Level,predict(object = regressor,newdata = dataset)),color='blue')+
  ggtitle('Salary Polynomial Predictor')+
  xlab('Level')+
  ylab('Salary')
