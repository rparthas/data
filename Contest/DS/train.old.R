data <- read.csv('train_data.csv')
test <- read.csv('test_data.csv')

data$Gender <- as.numeric(factor(data$Gender))
data$Married <- as.numeric(factor(data$Married))
data$Dependents =as.numeric(factor(data$Dependents))
data$Education =as.numeric(factor(data$Education))
data$Self_Employed=as.numeric(factor(data$Self_Employed))
data$Property_Area=as.numeric(factor(data$Property_Area))
data$LoanAmount = ifelse(is.na(data$LoanAmount),mean(data$LoanAmount,na.rm = T) ,data$LoanAmount)
data$Credit_History = ifelse(is.na(data$Credit_History),0 ,data$Credit_History)
data$Loan_Amount_Term = ifelse(is.na(data$Loan_Amount_Term),mean(data$Loan_Amount_Term,na.rm = T) ,data$Loan_Amount_Term)


data$Loan_Status <- ifelse(data$Loan_Status =='Y',1 ,0)
model <- glm(Loan_Status ~ Gender + Married + Dependents + Education + Self_Employed + ApplicantIncome + CoapplicantIncome+LoanAmount+Loan_Amount_Term+Credit_History+Property_Area , data = data,family = binomial(link="logit"))

train.results <- predict(model,newdata=data,type='response')
train.results <- ifelse(train.results > 0.5,1,0)
print(table(Predictions = train.results, TrueLabels =  data$Loan_Status))


test$Gender <- as.numeric(factor(test$Gender))
test$Married <- as.numeric(factor(test$Married))
test$Dependents =as.numeric(factor(test$Dependents))
test$Education =as.numeric(factor(test$Education))
test$Self_Employed=as.numeric(factor(test$Self_Employed))
test$Property_Area=as.numeric(factor(test$Property_Area))
test$LoanAmount = ifelse(is.na(test$LoanAmount),mean(test$LoanAmount,na.rm = T) ,test$LoanAmount)
test$Credit_History = ifelse(is.na(test$Credit_History),0 ,test$Credit_History)
test$Loan_Amount_Term = ifelse(is.na(test$Loan_Amount_Term),mean(test$Loan_Amount_Term,na.rm = T) ,test$Loan_Amount_Term)


fitted.results <- predict(model,newdata=test,type='response')
fitted.results <- ifelse(fitted.results > 0.5,1,0)

test$Loan_Status <- ifelse(fitted.results == 1,'Y','N')
test <- test[,c("Application_ID","Loan_Status")]

write.csv(test,"submission.csv",row.names = F)

