activity <- fread('Code-Gladiators-Activity.csv')
aum <- fread('Code-Gladiators-AUM.csv')
inv <- read.csv('Code-Gladiators-InvestmentExperience.csv')
txn <- fread('Code-Gladiators-Transaction.csv')

txn <- txn[!(txn$Transaction_Type == 'P' & txn$Amount < 0),]
txn <- txn[!(txn$Transaction_Type == 'R' & txn$Amount > 0),]
txn <- txn[,c(1,2,3,4,10)]
txn <- aggregate(Amount ~ Unique_Advisor_Id+Unique_Investment_Id+Month+Transaction_Type,data=txn,sum)
txn$Amount <- ifelse(txn$Amount<0,0-txn$Amount,txn$Amount)
txn$Amount <- matrix(scale(txn$Amount))

aum$Shares <- matrix(scale(aum$Shares))
aum$AUM <- matrix(scale(aum$AUM))
 
activity <- activity[,c(1,2,4)]
activity$Activity_Count <- matrix(scale(activity$Activity_Count))
 
inv <- inv[,c(1,3,5,22)]
inv$Net.Flows <- matrix(scale(inv$Net.Flows))

aumAct <- merge(aum,activity,by=c("Unique_Advisor_Id","Month"))
data <- merge(txn,aumAct,by=c("Unique_Advisor_Id","Unique_Investment_Id","Month"))
data <- merge(data,inv,by=c("Unique_Investment_Id","Month"))
 
rm(activity,aum,aumAct,inv,txn)
data <- unique(data)
data$Transaction_Type <- ifelse(data$Transaction_Type=='R',1,0)
 
model <- glm(Transaction_Type ~ Unique_Investment_Id + Unique_Advisor_Id + Activity_Count + Amount + Shares+AUM+Net.Flows , data = data,family = binomial(link="logit"))
 
results <- data.frame(Propensity_Score = round(predict(model, type = "response"),2),
                      Redeem_Status= ifelse(model$model$Transaction_Type==1,'YES','NO'))
print(table(Predictions = results$Redeem_Status, TrueLabels =  data$Transaction_Type))
results$Unique_Investment_Id <- data$Unique_Investment_Id
results$Unique_Advisor_Id <- data$Unique_Advisor_Id
results <- results %>%
  select(-Propensity_Score,-Redeem_Status,everything())
write.csv(results,'submission.csv',row.names = F)



