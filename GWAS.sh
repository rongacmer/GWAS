#!/bin/bash
########################################################################
curpath=$1
for p in `ls "$1"`;
do
    echo $p
    cd "${curpath}/$p"
    pwd
    #2.根据subjectID.txt从原始基因数据中筛选要保留的被试基因数据
    plink --bfile /media/rong/My\ Passport/GWAS/Origin/Alldata_maf_qc1 --noweb --keep train.txt --make-bed --out Mydata
    ##修改性状
    # python3 /media/rong/My\ Passport/GWAS/Script/toolbox.py -f1 Mydata.fam -f2 /media/rong/My\ Passport/GWAS/subject_list/MCIc.xlsx -f3 /media/rong/My\ Passport/GWAS/subject_list/MCInc.xlsx
    ###########################筛选位点######################################
    #计算数据缺失
    plink --bfile Mydata --het --out Mydata
    plink --bfile Mydata --missing --out Mydata
    echo SNP_missing:`awk '$5 > 0.05' Mydata.lmiss|wc -l` >>log.txt
    awk 'NR < 2 { next } $5 > 0.05' Mydata.lmiss > Mydata.lmiss.exclude
    plink --bfile Mydata --make-bed --exclude Mydata.lmiss.exclude --out Mydata_qc2

    #用--test-missing计算病例组和对照组的位点缺失率。生成一个.missing结果文件
    plink --bfile Mydata_qc2 --test-missing --out Mydata_qc2
    #用--hardy命令计算Hardy–Weinberg平衡，结果保存在.hwe文件中
    plink --bfile Mydata_qc2 --hardy --out Mydata_qc2
    #查找对照组中P值小于0.000001的位点的位点号
    awk '$3=="UNAFF" && $9 < 0.000001 {print $2}' Mydata_qc2.hwe > Mydata_qc2.hwe.exclude
    #删除这些位点，处理后的数据保存到gwas_example_qc4文件组
    plink --bfile Mydata_qc2 --exclude Mydata_qc2.hwe.exclude --make-bed --out Mydata_qc3

    ##*******************根据连锁不平衡性筛选位点
    #以200为窗口，计算R方，根据阈值0.2（阈值越小越严格），找出独立性强的SNP到prune.in
    plink --bfile Mydata_qc3 --indep-pairwise 200 5 0.6 --out Mydata_qc3
    #保留prune.in里的位点，保留的数据保存到gwas_example_qc4_indep文件组
    plink --bfile Mydata_qc3 --extract Mydata_qc3.prune.in --make-bed --out Mydata_qc3_indep

    ##*******************根据个体独立性筛选被试根据个体独立性删样本
    #使用genome命令计算亲缘系数，生成一个.genome文件。
    plink --bfile Mydata_qc3_indep --genome --out Mydata_qc3_indep
    head Mydata_maf_qc3_indep.genome
    #genome文件里的PI_HAT代表亲缘系数，亲缘系数越大，亲缘关系越亲。去掉这种样本。
    awk 'NR < 2 { next } $10 > 0.1875 {print $1"\t"$2}' Mydata_qc3_indep.genome > Mydata_qc3_indep.genome.remove
    plink --bfile Mydata_qc3_indep --remove Mydata_qc3_indep.genome.remove --make-bed --out Mydata_final

    #对比质量控制前后的数据，观察变化
    echo before SNP `wc -l Mydata.bim` >> log.txt  #质控前SNP数 
    echo before samble `wc -l Mydata.fam` >> log.txt  #质控前样本数
    echo after SNP `wc -l Mydata_final.bim` >> log.txt #质控后SNP数
    echo after samble `wc -l Mydata_final.fam` >> log.txt #质控后样本数

    ##*******************分析人群分层现象
    #先重新算一遍SNP独立性（同步骤6.5），因为后面又删除了样本，样本数对计算SNP独立性有影响，出于严谨，可以再算一遍。
    plink --bfile Mydata_final --indep-pairwise 200 5 0.6 --out Mydata_final
    plink --bfile Mydata_final --extract Mydata_final.prune.in --make-bed --out Mydata_final_indep 

    ##*******************主成分分析，用pca命令计算出前20个主成分（默认值为20，可用count参数设置）
    #生成两个文件.eigenva（特征值文件）l和.eigenvec（特征向量文件）
    plink --bfile Mydata_final_indep --pca --out Mydata_final_pca
    # head Mydata_final_pca.eigenvec

    ##*******************用--assoc或--linear做关联分析（分析模型为卡方等位基因测验）
    #“--linear”指的是用的连续型线性回归，如果表型数据为数值型，则用--linear
    #如果表型为二项式（即0、1）类型，则用“--logistic”或--assoc
    #plink --bfile gwas_example_final --assoc --out gwas_example_final
    #head gwas_example_final.assoc

    ##关联分析————不使用PCA进行人群分层校正
    #plink --bfile Mydata_final --linear --out Mydata_final
    #head Mydata_final.assoc.linear
    ##关联分析————使用PCA的结果校正人群分层现象
    plink --bfile Mydata_final --logistic hide-covar --covar Mydata_final_pca.eigenvec --covar-number 1-20 --out Mydata_final_adj
    # head Mydata_final_adj.assoc.linear
    Rscript /media/rong/My\ Passport/GWAS/Script/extract_SNP.R
    plink --bfile Mydata --extract SNP.txt --recodeA --out final_train
    plink --bfile /media/rong/My\ Passport/GWAS/Origin/Alldata_maf_qc1 --keep test.txt --extract SNP.txt --recodeA --out final_test
    plink --bfile /media/rong/My\ Passport/GWAS/Origin/Alldata_maf_qc1 --keep /media/rong/My\ Passport/GWAS/Origin/valid/test.txt --extract SNP.txt --recodeA --out final_valid 
    sed 's/NA/-1/g' final_train.raw>final_train.out
    sed 's/NA/-1/g' final_test.raw>final_test.out
    sed 's/NA/-1/g' final_valid.raw>final_valid.out
    cd "$curpath"
done
