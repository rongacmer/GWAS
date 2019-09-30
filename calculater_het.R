imiss <- read.table("Alldata_maf.imiss",header=TRUE) #读取位点缺失文件
het <- read.table("Alldata_maf.het",header=TRUE) #读取包含纯合型个数的文件
het$meanHet <- (het$N.NM. - het$O.HOM.)/het$N.NM. #计算杂合率
upplimit <- mean(het$meanHet)+(3*sd(het$meanHet)) #计算杂合率筛选上限
lowlimit <- mean(het$meanHet)-(3*sd(het$meanHet)) #计算杂合率筛选下限
#将在上下限之外的样本的FID和IID记录到一个het.remove变量中
het.remove <- het[which(het$meanHet < lowlimit | het$meanHet > upplimit),c("FID","IID")]
imiss.remove <- imiss[which(imiss$F_MISS > 0.08),c("FID","IID")]
#将所要剔除的样本索引合并保存
write.table(rbind(het.remove,imiss.remove) ,"Alldata_maf.imiss-vs-het.remove", append = FALSE, quote = FALSE, sep = " ", row.names = FALSE, col.names = FALSE)
