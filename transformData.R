setwd("~/Documents/Networks/ProjectData")
library(plyr)
library(stringr)
data <- read.csv("loanslenders_2017.csv")
data$LENDERS <- as.character(data$LENDERS)
data <- data[,-1]
s <- strsplit(data$LENDERS, split = ", ")
newdata <- data.frame(LOAN_ID = rep(data$LOAN_ID, sapply(s, length)), LENDERS = unlist(s))
newdata$LENDERS <- as.character(newdata$LENDERS)
newdata <- unique(newdata)
write.csv(newdata, "bipartite_graph_data_2017.csv")
#create unique IDs
nodeID <- seq(1,189719,1)
username <- unique(newdata$LENDERS)
uniqueidusers <- data.frame(nodeID,username)
uniqueidusers$username <- as.character(uniqueidusers$username)
write.csv(uniqueidusers, "Username_NodeID_Mapping.csv")
#uniqueidusers <- read.csv("Username_NodeID_Mapping.csv")
#uniqueidusers <- uniqueidusers[,-1]
bipartite_edgelist <- merge(newdata, uniqueidusers, by.x=c("LENDERS"), by.y=c("username"))
bipartite_edgelist <- bipartite_edgelist[,-1]
colnames(bipartite_edgelist)[2] <- "USER_ID"
bipartite_edgelist <- bipartite_edgelist[ , c("LOAN_ID","USER_ID")]
write.csv(bipartite_edgelist, "bipartite_edgelist_2017.csv", row.names = FALSE)


#category data
data <- read.csv("loans_lenders_category_2017.csv")
cleaneddata <- read.csv("bipartite_edgelist_2017.csv")
data <- data[,-c(1,4)]
bipartite_edgelist <- merge(data, cleaneddata, by=c("LOAN_ID"))
category_split <- split(bipartite_edgelist[,c(1,3)], bipartite_edgelist$SECTOR_NAME)

N <- names(category_split)
for (i in seq_along(N)) write.csv(category_split[[i]], file=paste0(N[i], ".csv"), row.names = FALSE)

#team data
data <- read.csv("teamdata_processed.csv", header = FALSE)
mapping <- read.csv("Username_NodeID_Mapping_2017.csv")
mapping <- mapping[,-1]
mapping$username <- str_trim(mapping$username, side = "both")
data$V1 <- data$V1 + 505000
data$V2 <- as.character(data$V2)

merged <- merge(data, mapping, by.x=c("V2"), by.y=c("username"))
merged <- merged[,-1]

