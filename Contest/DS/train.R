data <- read.csv('train_data.csv')


data$Gender <- as.numeric(factor(data$Gender))
data$Married <- as.numeric(factor(data$Married))
data$Dependents =as.numeric(factor(data$Dependents))
data$Education =as.numeric(factor(data$Education))
data$Self_Employed=as.numeric(factor(data$Self_Employed))
data$Property_Area=as.numeric(factor(data$Property_Area))
data$LoanAmount = ifelse(is.na(data$LoanAmount),mean(data$LoanAmount,na.rm = T) ,data$LoanAmount)
data$Credit_History = ifelse(is.na(data$Credit_History),2 ,data$Credit_History)
data$Loan_Amount_Term = ifelse(is.na(data$Loan_Amount_Term),mean(data$Loan_Amount_Term,na.rm = T) ,data$Loan_Amount_Term)
data$ApplicantIncome <-matrix(scale(data$ApplicantIncome))
data$CoapplicantIncome <-matrix(scale(data$CoapplicantIncome))

data$Loan_Status <- ifelse(data$Loan_Status =='Y',1 ,0)
model <- glm(Loan_Status ~ Gender + Married + Dependents + Education + Self_Employed + ApplicantIncome + CoapplicantIncome+Credit_History+Property_Area , data = data,family = binomial(link="logit"))

train.results <- predict(model,newdata=data,type='response')
train.results <- ifelse(train.results > 0.5,1,0)
print(table(Predictions = train.results, TrueLabels =  data$Loan_Status))

data <- read.csv('test_data.csv')
data$Gender <- as.numeric(factor(data$Gender))
data$Married <- as.numeric(factor(data$Married))
data$Dependents =as.numeric(factor(data$Dependents))
data$Education =as.numeric(factor(data$Education))
data$Self_Employed=as.numeric(factor(data$Self_Employed))
data$Property_Area=as.numeric(factor(data$Property_Area))
data$LoanAmount = ifelse(is.na(data$LoanAmount),mean(data$LoanAmount,na.rm = T) ,data$LoanAmount)
data$Credit_History = ifelse(is.na(data$Credit_History),2 ,data$Credit_History)
data$Loan_Amount_Term = ifelse(is.na(data$Loan_Amount_Term),mean(data$Loan_Amount_Term,na.rm = T) ,data$Loan_Amount_Term)
data$ApplicantIncome <-matrix(scale(data$ApplicantIncome))
data$CoapplicantIncome <-matrix(scale(data$CoapplicantIncome))

fitted.results <- predict(model,newdata=data,type='response')
fitted.results <- ifelse(fitted.results > 0.5,1,0)

data$Loan_Status <- ifelse(fitted.results == 1,'Y','N')
data <- data[,c("Application_ID","Loan_Status")]

write.csv(data,"submission.csv",row.names = F)

