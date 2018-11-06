dataset = read.csv(file='Data.csv')
dataset$Age = ifelse(is.na(dataset$Age),mean(dataset$Age,na.rm = T) ,dataset$Age)
dataset$Salary = ifelse(is.na(dataset$Salary),mean(dataset$Salary,na.rm = T) ,dataset$Salary)

dataset$Purchased=factor(dataset$Purchased,levels = c('Yes','No'),labels = c(1,0))
dataset$Country=factor(dataset$Country,levels = c('France','Spain','Germany'),labels = c(1,2,3))
dataset[,2:3]=scale(dataset[,2:3])

library(caTools)
set.seed(25)
split=sample.split(dataset$Purchased,SplitRatio = 0.8)
training_set=subset(dataset,split == T )
test_set=subset(dataset,split == F )