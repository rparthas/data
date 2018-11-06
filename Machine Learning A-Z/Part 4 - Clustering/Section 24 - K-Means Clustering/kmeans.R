dataset = read.csv('Mall_Customers.csv')
x <- dataset[4:5]

set.seed(6)
wcss <- vector()

for(i in 1:10)
  wcss[i]<-sum(kmeans(x=x,centers = i)$withinss)

plot(1:10,wcss,type='b',main=paste('client clusters'),xlab='Number of clusters',ylab='WCSS')

set.seed(29)
model <- kmeans(x=x,centers = 5)
#values <- fitted(model,method=c("centers","classes"))

library(cluster)
clusplot(x,model$cluster,lines=0,shade=TRUE,color=TRUE,plotchar =FALSE,span = TRUE,main=paste('client clusters'),xlab='Annual Income',ylab='Spending Score')
