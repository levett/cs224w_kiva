setwd("~/Documents/Networks/ProjectData")
data <- read.csv("loanslenders_2017.csv")
data <- data[,-1]
s <- strsplit(data$LENDERS, split = ",")
newdata <- data.frame(LOAN_ID = rep(data$LOAN_ID, sapply(s, length)), LENDERS = unlist(s))
newdata <- unique(newdata)
write.csv(newdata, "bipartite_graph_data_2017.csv")
#create unique IDs
nodeID <- seq(1,504376,1)
username <- unique(newdata$LENDERS)
uniqueidusers <- data.frame(nodeID,username)
write.csv(uniqueidusers, "Username_NodeID_Mapping.csv")

bipartite_edgelist <- merge(newdata, uniqueidusers, by.x=c("LENDERS"), by.y=c("username"))
bipartite_edgelist <- bipartite_edgelist[,-1]
colnames(bipartite_edgelist)[2] <- "USER_ID"
bipartite_edgelist <- bipartite_edgelist[ , c("USER_ID","LOAN_ID")]
write.csv(bipartite_edgelist, "bipartite_edgelist_2017.csv", row.names = FALSE)
