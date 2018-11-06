# Data Preprocessing Template

# Importing the dataset
dataset = read.csv('50_Startups.csv')
dataset$State=factor(x=dataset$State,labels=c(1,2,3),levels = c('New York','Florida','California'))

# Splitting the dataset into the Training set and Test set
# install.packages('caTools')
library(caTools)
set.seed(123)
split = sample.split(dataset$Profit, SplitRatio = 0.8)
training_set = subset(dataset, split == TRUE)
test_set = subset(dataset, split == FALSE)

regressor=lm(formula = Profit ~ R.D.Spend+Marketing.Spend,data = training_set)
summary(regressor)
test_set$pred=predict(regressor,test_set)
