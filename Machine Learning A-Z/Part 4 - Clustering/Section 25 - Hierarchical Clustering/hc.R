dataset = read.csv('Mall_Customers.csv')
x <- dataset[4:5]

dendogram=hclust(d=dist(x,method = "euclidean"),method = 'ward.D')
plot(dendogram,main=paste('Dendogram'),xlab='hclust',ylab='Distance')

hc=hclust(d=dist(x,method = "euclidean"),method = 'ward.D')
y_hc=cutree(hc,5)


library(cluster)
clusplot(x,y_hc,lines=0,shade=TRUE,color=TRUE,plotchar =FALSE,span = TRUE,main=paste('client clusters'),xlab='Annual Income',ylab='Spending Score',labels = 2)
