library(tidyr)
library(dplyr)
library(data.table)
data <- fread("train_data.csv")

colnames(data) <- c('Click.Time','Ad.Slot.Id','Advertiser.Id','Audiences','Call.Identifier','Click.IP','User.Id','Geography.Id','Impression.Id','Impression.IP'
                    ,'Ad.id','Reference.Url','Site.Id','User.Agent','is_fraud')
data$Click.Time <- as.numeric(factor(data$Click.Time))
data$Click.IP <- as.numeric(factor(data$Click.IP))
data$Impression.IP <- as.numeric(factor(data$Impression.IP))
data$User.Agent <- as.numeric(factor(data$User.Agent))
data$Audiences <- as.numeric(factor(data$Audiences))
data <- data[!(is.na(data$is_fraud))]
model <- glm(is_fraud ~ Click.IP+Click.Time+Advertiser.Id+User.Id+User.Agent+Impression.Id+Impression.IP
               +Ad.id+Reference.Url+Site.Id
               , data = data,family = binomial(link="logit"))
  
results <- predict(model,newdata=data,type='response')
results <- ifelse(results > 0.5,1,0)
print(table(Predictions = results, TrueLabels =  data$is_fraud))


data <- fread("test_data.csv")
test <- data
colnames(data) <- c('Click.Time','Ad.Slot.Id','Advertiser.Id','Audiences','Call.Identifier','Click.IP','User.Id','Geography.Id','Impression.Id','Impression.IP'
                    ,'Ad.id','Reference.Url','Site.Id','User.Agent')
data$Click.Time <- as.numeric(factor(data$Click.Time))
data$Click.IP <- as.numeric(factor(data$Click.IP))
data$Impression.IP <- as.numeric(factor(data$Impression.IP))
data$User.Agent <- as.numeric(factor(data$User.Agent))
data$Audiences <- as.numeric(factor(data$Audiences))

results <- predict(model,newdata=data,type='response')


colnames(test) <- c('click_time','ad_slot_id','advertiser_id','audiences','call_identifier','click_ip','user_id','geography_id','impression_id','impression_ip','ad_id','reference_url','site_id','user_agent')
test$fraud_click_probability <- round(results,digits = 2)
test$is_fraud <-  ifelse(results>0.5,1,0)
write.csv(test,"submission.csv",row.names = F)






