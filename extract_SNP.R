assoc_adj <- read.table("Mydata_final_adj.assoc.logistic",header=TRUE)
assoc_adj_final <- assoc_adj[which(!is.na(assoc_adj$P)),]
assoc_adj_final_sig<- assoc_adj_final[assoc_adj_final[,9]<0.001,]
assoc_adj_final_sig[c("logP")]<-(-log10(assoc_adj_final_sig[,9]))
write.table(assoc_adj_final_sig,file ="assoc_adj_final_sig.txt",sep =" ",quote =FALSE)
write.table(assoc_adj_final_sig[,2],file='SNP.txt',sep=" ",quote=FALSE,row.names = FALSE, col.names = FALSE)