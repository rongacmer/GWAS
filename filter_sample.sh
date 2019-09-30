####样本水平


#质量控制
#1.根据最小等位基因频率（MFAF筛选样本）
plink --bfile ADNI_cluster_01_forward_757LONI --freq --out Mydata ADNI_cluster_01_forward_757LONI
echo MAF length:`awk '$5 <0.05' ADNI_cluster_01_forward_757LONI.frq | wc -l`>log.txt

plink --bfile ADNI_cluster_01_forward_757LONI --maf 0.05 --make-bed --out Alldata_maf


# 根据杂合率筛选被试
#计算纯合子个数
plink --bfile Alldata_maf --het --out Alldata_maf
#计算数据缺失
plink --bfile Alldata_maf --missing --out Alldata_maf
echo missing:`awk '$6 > 0.08' Alldata_maf.imiss| wc -l`>>log.txt
Rscript /media/rong/My\ Passport/GWAS/Script/calculater_het.R
#根据remove名单删除样本
plink --bfile Alldata_maf --remove Alldata_maf.imiss-vs-het.remove  --make-bed --out Alldata_maf_qc1

echo sum of sample:`less Alldata_maf_qc1.fam|wc -l` >>log.txt