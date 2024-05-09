# Contents
- Heritability
    - LDSC
    - GCTA - GREML
    - HDL
- Local Heritability/ Local genetic correlation
    - LAVA
    - HESS
    - GNOVA
    - SUPERGNOVA
    - HEELS
- Genetic correlation
    - cross-trait LDSC
    - popcorn
    - S-LDXR

## LDSC
- SHORT NAME:LDSC
- FULL NAME:LD Score Regression
- CATEGORY: Heritability
- YEAR:2015
- DESCRIPTION:ldsc is a command line tool for estimating heritability and genetic correlation from GWAS summary statistics. ldsc also computes LD Scores.
- URL:https://github.com/bulik/ldsc
- CITATION :Bulik-Sullivan, Brendan K., et al. "LD Score regression distinguishes confounding from polygenicity in genome-wide association studies." Nature genetics 47.3 (2015): 291-295.

## GCTA - GREML
- SHORT NAME: GREML
- FULL NAME:Genome-wide complex trait analysis (GCTA) Genome-based restricted maximum likelihood (GREML) 
- CATEGORY: Heritability
- YEAR:2010
- DESCRIPTION:GCTA-GREML analysis: estimating the variance explained by the SNPs / GCTA-GREML analysis for a case-control study
- URL: https://yanglab.westlake.edu.cn/software/gcta/#GREML
- CITATION :(quantitative)Yang, Jian, et al. "Common SNPs explain a large proportion of the heritability for human height." Nature genetics 42.7 (2010): 565-569.
- CITATION :(case-control )Lee, Sang Hong, et al. "Estimating missing heritability for disease from genome-wide association studies." The American Journal of Human Genetics 88.3 (2011): 294-305.
- CITATION :(partition the genetic variance into individual chromosomes and genomic segments) Yang, Jian, et al. "Genome partitioning of genetic variation for complex traits using common SNPs." Nature genetics 43.6 (2011): 519-525.
- CITATION :(Bivariate GREML) Lee, Sang Hong, et al. "Estimation of pleiotropy between complex diseases using single-nucleotide polymorphism-derived genomic relationships and restricted maximum likelihood." Bioinformatics 28.19 (2012): 2540-2542.
- CITATION :(GREML-LDMS) Yang, Jian, et al. "Genetic variance estimation with imputed variants finds negligible missing heritability for human height and body mass index." Nature genetics 47.10 (2015): 1114-1120.

## HDL
- SHORT NAME:HDL
- FULL NAME:High-Definition Likelihood
- CATEGORY: Heritability
- YEAR:2020
- DESCRIPTION:High-Definition Likelihood (HDL) is a likelihood-based method for estimating genetic correlation using GWAS summary statistics. Compared to LD Score regression (LDSC), It reduces the variance of a genetic correlation estimate by about 60%.
- URL:https://github.com/zhenin/HDL/
- CITATION :Ning, Z., Pawitan, Y., & Shen, X. (2020). High-definition likelihood inference of genetic correlations across human complex traits. Nature genetics, 52(8), 859-864.


## LAVA
- DESCRIPTION:LAVA is a tool to conduct genome-wide, local genetic correlation analysis on multiple traits, using GWAS summary statistics as input.
- URL: https://ctg.cncr.nl/software/lava
- CATEGORY: Local heritability/genetic correlation
- YEAR: 2022
- CITATION:Werme, J., van der Sluis, S., Posthuma, D. et al. An integrated framework for local genetic correlation analysis. Nat Genet 54, 274–282 (2022). https://doi.org/10.1038/s41588-022-01017-y

## HESS
- SHORT NAME: HESS
- FULL NAME: Heritability Estimation from Summary Statistics
- CATEGORY: Local heritability/genetic correlation
- DESCRIPTION:HESS (Heritability Estimation from Summary Statistics) is a software package for estimating and visualizing local SNP-heritability and genetic covariance (correlation) from GWAS summary association data.
- YEAR: 2016
- URL: https://huwenboshi.github.io/hess/
- CITATION: Shi, Huwenbo, Gleb Kichaev, and Bogdan Pasaniuc. "Contrasting the genetic architecture of 30 complex traits from summary association data." The American Journal of Human Genetics 99.1 (2016): 139-153.
- CITATION: Shi, Huwenbo, et al. "Local genetic correlation gives insights into the shared genetic architecture of complex traits." The American Journal of Human Genetics 101.5 (2017): 737-751.

## GNOVA
- SHORT NAME:GNOVA
- FULL NAME:GeNetic cOVariance Analyzer
- CATEGORY: Local heritability/genetic correlation
- YEAR:2017
- DESCRIPTION:A principled framework to estimate annotation-stratified genetic covariance using GWAS summary statistics.
- URL:https://github.com/xtonyjiang/GNOVA
- CITATION :Lu, Qiongshi, et al. "A powerful approach to estimating annotation-stratified genetic covariance via GWAS summary statistics." The American Journal of Human Genetics 101.6 (2017): 939-964.

## SUPERGNOVA
- SHORT NAME:SUPERGNOVA
- FULL NAME:SUPER GeNetic cOVariance Analyzer
- CATEGORY: Local heritability/genetic correlation
- YEAR:2021
- DESCRIPTION:SUPERGNOVA (SUPER GeNetic cOVariance Analyzer) is a statistical framework to perform local genetic covariance analysis. 
- URL:https://github.com/qlu-lab/SUPERGNOVA
- CITATION :Zhang, Yiliang, et al. "SUPERGNOVA: local genetic correlation analysis reveals heterogeneous etiologic sharing of complex traits." Genome biology 22.1 (2021): 1-30.

## HEELS
- SHORT NAME:HEELS
- FULL NAME: Heritability Estimation with high Efficiency using LD and association Summary Statistics
- CATEGORY: Local heritability/genetic correlation
- YEAR:2023
- DESCRIPTION:HEELS is a Python-based command line tool that produce accurate and precise local heritability estimates using summary-level statistics (marginal association test statistics along with the empirical (in-sample) LD statistics).
- URL: [https://github.com/huilisabrina/HEELS](https://github.com/huilisabrina/HEELS)
- CITATION :Li, H., Mazumder, R., & Lin, X. (2023). Accurate and efficient estimation of local heritability using summary statistics and the linkage disequilibrium matrix. Nature Communications, 14(1), 7954.

## cross-trait LDSC
- SHORT NAME: cross-trait LDSC
- FULL NAME:cross-trait LD Score Regression
- CATEGORY: Genetic correlation
- YEAR: 2015
- DESCRIPTION:ldsc is a command line tool for estimating heritability and genetic correlation from GWAS summary statistics. ldsc also computes LD Scores.
- URL: https://github.com/bulik/ldsc
- CITATION : Bulik-Sullivan, Brendan, et al. "An atlas of genetic correlations across human diseases and traits." Nature genetics 47.11 (2015): 1236-1241.
- KEYWORDS: cross-trait, LD score regression

## popcorn
- SHORT NAME:popcorn
- FULL NAME:popcorn
- CATEGORY: Genetic correlation
- YEAR:2016
- DESCRIPTION:Popcorn is a program for estimaing the correlation of causal variant effect. This is the python3 version of Popcorn and still under development sizes across populations in GWAS.
- URL:https://github.com/brielin/Popcorn
- CITATION :Brown, Brielin C., et al. "Transethnic genetic-correlation estimates from summary statistics." The American Journal of Human Genetics 99.1 (2016): 76-88.
- KEYWORDS: trans-ethnic

## S-LDXR
- SHORT NAME: S-LDXR
- FULL NAME: S-LDXR
- CATEGORY: Genetic correlation
- YEAR: 2021
- DESCRIPTION: S-LDXR is a software for estimating enrichment of stratified squared trans-ethnic genetic correlation across genomic annotations from GWAS summary statistics data.
- CITATION: Shi, H., Gazal, S., Kanai, M., Koch, E. M., Schoech, A. P., Siewert, K. M., ... & Price, A. L. (2021). Population-specific causal disease effect sizes in functionally important regions impacted by selection. Nature communications, 12(1), 1098.
- URL: https://huwenboshi.github.io/s-ldxr/
- KEYWORDS: trans-ethnic, stratified, functional categories