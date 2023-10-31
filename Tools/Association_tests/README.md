# Contents
- Single variant association tests
    - PLINK
    - PLINK2
    - EMMAX
    - GEMMA
    - fastGWA
    - fastGWA-GLMM
    - REGENIE
    - SAIGE
    - Bolt-lMM
    - POLMM
- Gene-based analysis (rare variant)
    - REGENIE
    - SAIGE-GENE
    - SAIGE-GENE+
    - SKAT
    - SKAT-O
    - STAAR
- GWAS using family history
    - GWAX
    - LT-FH
    - SiblingGWAS
    - snipar
- Case-case GWAS
    - CC-GWAS
- GWAS of longitudinal trajectories
    - TrajGWAS
- PGS-adjusted GWAS
    - PGS-adjusted GWAS

---
# Single variant association tests
## PLINK  
- FULLNAME: PLINK
- SHORTNAME: PLINK
- DESCRIPTION: A Tool Set for Whole-Genome Association and Population-Based Linkage Analyses. PLINK is a free, open-source whole genome association analysis toolset, designed to perform a range of basic, large-scale analyses in a computationally efficient manner. The focus of PLINK is purely on analysis of genotype/phenotype data, so there is no support for steps prior to this (e.g. study design and planning, generating genotype or CNV calls from raw data). Through integration with gPLINK and Haploview, there is some support for the subsequent visualization, annotation and storage of results.
- URL: https://www.cog-genomics.org/plink/
- CITATION: Purcell, Shaun, et al. "PLINK: a tool set for whole-genome association and population-based linkage analyses." The American journal of human genetics 81.3 (2007): 559-575.

## PLINK2
- FULLNAME:PLINK2
- SHORTNAME:PLINK2
- URL: https://www.cog-genomics.org/plink/2.0/
- CITATION: Chang, Christopher C., et al. "Second-generation PLINK: rising to the challenge of larger and richer datasets." Gigascience 4.1 (2015): s13742-015.

## EMMAX
- FULLNAME:efficient mixed-model association eXpedited
- SHORTNAME:EMMAX
- URL: https://genome.sph.umich.edu/wiki/EMMAX
- DESCRIPTION: EMMAX is a statistical test for large scale human or model organism association mapping accounting for the sample structure. In addition to the computational efficiency obtained by EMMA algorithm, EMMAX takes advantage of the fact that each loci explains only a small fraction of complex traits, which allows us to avoid repetitive variance component estimation procedure, resulting in a significant amount of increase in computational time of association mapping using mixed model.
- CITATION:

## GEMMA
- FULLNAME: genome-wide efficient mixed-model association 
- SHORTNAME: GEMMA
- DESCRIPTION: GEMMA is the software implementing the Genome-wide Efficient Mixed Model Association algorithm for a standard linear mixed model and some of its close relatives for genome-wide association studies (GWAS). It fits a standard linear mixed model (LMM) to account for population stratification and sample structure for single marker association tests. It fits a Bayesian sparse linear mixed model (BSLMM) using Markov chain Monte Carlo (MCMC) for estimating the proportion of variance in phenotypes explained (PVE) by typed genotypes (i.e. chip heritability), predicting phenotypes, and identifying associated markers by jointly modeling all markers while controlling for population structure. It is computationally efficient for large scale GWAS and uses freely available open-source numerical libraries.
- URL: http://stephenslab.uchicago.edu/software.html#gemma
- CITATION: Zhou, Xiang, and Matthew Stephens. "Genome-wide efficient mixed-model analysis for association studies." Nature genetics 44.7 (2012): 821-824.

## BOLT-lMM
- FULLNAME:BOLT-lMM
- SHORTNAME: BOLT-lMM
- DESCRIPTION: The BOLT-LMM software package currently consists of two main algorithms, the BOLT-LMM algorithm for mixed model association testing, and the BOLT-REML algorithm for variance components analysis (i.e., partitioning of SNP-heritability and estimation of genetic correlations).
- URL: https://alkesgroup.broadinstitute.org/BOLT-LMM/BOLT-LMM_manual.html
- CITATION: Loh, Po-Ru, et al. "Efficient Bayesian mixed-model analysis increases association power in large cohorts." Nature genetics 47.3 (2015): 284-290.
-KEY WORDS: non-infinitesimal model,  mixture of two Gaussian distributions 

## SAIGE
- FULLNAME:Scalable and Accurate Implementation of GEneralized mixed model
- SHORTNAME: SAIGE
- URL: https://github.com/weizhouUMICH/SAIGE
- DESCRIPTION: SAIGE is an R package with Scalable and Accurate Implementation of Generalized mixed model (Chen, H. et al. 2016). It accounts for sample relatedness and is feasible for genetic association tests in large cohorts and biobanks (N > 400,000). SAIGE performs single-variant association tests for binary traits and quantitative taits. For binary traits, SAIGE uses the saddlepoint approximation (SPA)(mhof, J. P. , 1961; Kuonen, D. 1999; Dey, R. et.al 2017) to account for case-control imbalance.
- CITATION: Zhou, Wei, et al. "Efficiently controlling for case-control imbalance and sample relatedness in large-scale genetic association studies." Nature genetics 50.9 (2018): 1335-1341.
-KEY WORDS:case-control imbalance, saddlepoint approximation (SPA)

## fastGWA
- FULLNAME: fastGWA
- SHORTNAME:fastGWA
- URL: https://yanglab.westlake.edu.cn/software/gcta/#fastGWA
- CITATION: Jiang, Longda, et al. "A resource-efficient tool for mixed model association analysis of large-scale data." Nature genetics 51.12 (2019): 1749-1755.
-KEY WORDS:  grid-search-based REML algorithm

## fastGWA-GLMM
- FULLNAME: fastGWA-GLMM
- SHORTNAME: fastGWA-GLMM
- URL: https://yanglab.westlake.edu.cn/software/gcta/#fastGWA
- CITATION: Jiang, Longda, et al. "A generalized linear mixed model association tool for biobank-scale data." Nature genetics 53.11 (2021): 1616-1621.

## REGENIE
- FULLNAME:REGENIE
- SHORTNAME:REGENIE
- URL: https://github.com/rgcgithub/regenie
- DESCRIPTION:regenie is a C++ program for whole genome regression modelling of large genome-wide association studies. It is developed and supported by a team of scientists at the Regeneron Genetics Center.
- CITATION: Mbatchou, Joelle, et al. "Computationally efficient whole-genome regression for quantitative and binary traits." Nature genetics 53.7 (2021): 1097-1103.
- KEY WORDS: whole genome regression

## POLMM
- FULLNAME:proportional odds logistic mixed model (POLMM)
- SHORTNAME:POLMM
- URL: https://github.com/WenjianBI/POLMM
- DESCRIPTION: Proportional Odds Logistic Mixed Model (POLMM) for ordinal categorical data analysis
- CITATION: Bi, W., Zhou, W., Dey, R., Mukherjee, B., Sampson, J. N., & Lee, S. (2021). Efficient mixed model approach for large-scale genome-wide association studies of ordinal categorical phenotypes. The American Journal of Human Genetics, 108(5), 825-839.
- KEY WORDS: ordinal categorical phenotypes

---

# Gene-based analysis (rare variant)
## REGENIE
- FULLNAME:REGENIE
- SHORTNAME:REGENIE
- URL: https://github.com/rgcgithub/regenie
- DESCRIPTION:regenie is a C++ program for whole genome regression modelling of large genome-wide association studies. It is developed and supported by a team of scientists at the Regeneron Genetics Center.
- CITATION: Mbatchou, Joelle, et al. "Computationally efficient whole-genome regression for quantitative and binary traits." Nature genetics 53.7 (2021): 1097-1103.
- KEY WORDS: whole genome regression

## SAIGE-GENE /  SAIGE-GENE+
- FULLNAME: SAIGE-GENE / SAIGE-GENE+
- SHORTNAME: SAIGE-GENE / SAIGE-GENE+
- URL: https://github.com/weizhouUMICH/SAIGE
- CITATION: Zhou, Wei, et al. "SAIGE-GENE+ improves the efficiency and accuracy of set-based rare variant association tests." Nature Genetics (2022): 1-4.
- CITATION: Zhou, Wei, et al. "Scalable generalized linear mixed model for region-based association tests in large biobanks and cohorts." Nature genetics 52.6 (2020): 634-639.

## STAAR
- FULLNAME: variant-set test for association using annotation information
- SHORTNAME: STAAR
- URL: https://github.com/xihaoli/STAAR
- DESCRIPTION: STAAR is an R package for performing variant-Set Test for Association using Annotation infoRmation (STAAR) procedure in whole-genome sequencing (WGS) studies. STAAR is a general framework that incorporates both qualitative functional categories and quantitative complementary functional annotations using an omnibus multi-dimensional weighting scheme. STAAR accounts for population structure and relatedness, and is scalable for analyzing large WGS studies of continuous and dichotomous traits.
- CITATION: Li, Xihao, et al. "Dynamic incorporation of multiple in silico functional annotations empowers rare variant association analysis of large whole-genome sequencing studies at scale." Nature genetics 52.9 (2020): 969-983.
- KEY WORDS: functional annotations


## SKAT
- FULLNAME: sequence kernel association test
- SHORTNAME: SKAT
- URL:  https://www.hsph.harvard.edu/skat/
- DESCRIPTION: SKAT is a SNP-set (e.g., a gene or a region) level test for association between a set of rare (or common) variants and dichotomous or quantitative phenotypes, SKAT aggregates individual score test statistics of SNPs in a SNP set  and efficiently computes SNP-set level p-values, e.g. a gene or a region level p-value, while adjusting for covariates, such as principal components to account for population stratification. SKAT also allows for power/sample size calculations for designing for sequence association studies.
- CITATION:Wu, Michael C., et al. "Rare-variant association testing for sequencing data with the sequence kernel association test." The American Journal of Human Genetics 89.1 (2011): 82-93.
- KEY WORDS: 


## SKAT-O
- FULLNAME: sequence kernel association test - optimal test
- SHORTNAME: SKAT-O
- URL:https://www.hsph.harvard.edu/skat/
- DESCRIPTION: estimating the correlation parameter in the kernel matrix to maximize the power, which corresponds to the estimated weight in the linear combination of the burden test and SKAT test statistics that maximizes power.
- CITATION: Lee, Seunggeun, Michael C. Wu, and Xihong Lin. "Optimal tests for rare variant effects in sequencing association studies." Biostatistics 13.4 (2012): 762-775.

# GWAS using family history
## GWAX
- FULLNAME: genome-wide association by proxy
- SHORTNAME: GWAX
- DESCRIPTION:  In randomly ascertained cohorts, replacing cases with their first-degree relatives enables studies of diseases that are absent (or nearly absent) in the cohort.
- CITATION: Liu, J. Z., Erlich, Y., & Pickrell, J. K. (2017). Case–control association mapping by proxy using family history of disease. Nature genetics, 49(3), 325-331.

## LT-FH
- FULLNAME: liability threshold model, conditional on case–control status and family history
- SHORTNAME: LT-FH
- URL:https://alkesgroup.broadinstitute.org/UKBB/LTFH/
- DESCRIPTION: an association method based on posterior mean genetic liabilities under a liability threshold model, conditional on case-control status and family history (LT-FH)
- CITATION:Liu, J. Z., Erlich, Y., & Pickrell, J. K. (2017). Case–control association mapping by proxy using family history of disease. Nature genetics, 49(3), 325-331.

## SiblingGWAS
- FULL NAME: Within-sibship genome-wide association analyses
- SHORT NAME: SiblingGWAS
- URL: https://github.com/LaurenceHowe/SiblingGWAS
- YEAR: 2022
- DESCRIPTION: Scripts for running GWAS using siblings to estimate Within-Family (WF) and Between-Family (BF) effects of genetic variants on continuous traits. Allows the inclusion of more than two siblings from one family.
- CITATION: Howe, L. J., Nivard, M. G., Morris, T. T., Hansen, A. F., Rasheed, H., Cho, Y., ... & Davies, N. M. (2022). Within-sibship genome-wide association analyses decrease bias in estimates of direct genetic effects. Nature genetics, 54(5), 581-592.

## snipar
- FULLNAME: single nucleotide imputation of parents
- SHORTNAME: snipar
- DESCRIPTION: snipar (single nucleotide imputation of parents) is a Python package for inferring identity-by-descent (IBD) segments shared between siblings, imputing missing parental genotypes, and for performing family based genome-wide association and polygenic score analyses using observed and/or imputed parental genotypes.
- YEAR: 2022
- URL: https://github.com/AlexTISYoung/snipar
- CITATION: Young, A. I., Nehzati, S. M., Benonisdottir, S., Okbay, A., Jayashankar, H., Lee, C., ... & Kong, A. (2022). Mendelian imputation of parental genotypes improves estimates of direct genetic effects. Nature genetics, 54(6), 897-905.
- CITATION: Guan, J., Nehzati, S. M., Benjamin, D. J., & Young, A. I. (2022). Novel estimators for family-based genome-wide association studies increase power and robustness. bioRxiv, 2022-10.
# Case-case GWAS

## CC-GWAS 
- FULLNAME: case–case genome-wide association study
- SHORTNAME: CC-GWAS 
- URL:https://github.com/wouterpeyrot/CCGWAS
- DESCRIPTION: The CCGWAS R package provides a tool for case-case association testing of two different disorders based on their respective case-control GWAS results
- CITATION: Peyrot, W. J., & Price, A. L. (2021). Identifying loci with different allele frequencies among cases of eight psychiatric disorders using CC-GWAS. Nature genetics, 53(4), 445-454.

# GWAS of longitudinal trajectories
## TrajGWAS
- FULLNAME: GWAS of longitudinal trajectories
- SHORTNAME: TrajGWAS
- DESCRIPTION: TrajGWAS.jl is a Julia package for performing genome-wide association studies (GWAS) for continuous longitudinal phenotypes using a modified linear mixed effects model. It builds upon the within-subject variance estimation by robust regression (WiSER) method and can be used to identify variants associated with changes in the mean and within-subject variability of the longitduinal trait.
- YEAR: 2022
- URL: https://github.com/OpenMendel/TrajGWAS.jl
- CITATION: Ko, S., German, C. A., Jensen, A., Shen, J., Wang, A., Mehrotra, D. V., ... & Zhou, J. J. (2022). GWAS of longitudinal trajectories at biobank scale. The American Journal of Human Genetics, 109(3), 433-445.
- Keywords: biomarker trajectories, mean, within-subject (WS) variability, linear mixed effect model, within-subject variance estimation by robust regression (WiSER) method

# PGS-adjusted GWAS

## PGS-adjusted GWAS
- FULLNAME: PGS-adjusted GWAS
- SHORTNAME: PGS-adjusted GWAS
- DESCRIPTION: adjustment of GWAS analyses for polygenic scores (PGSs) increases the statistical power for discovery across all ancestries
- YEAR: 2023
- CITATION: Campos, A. I., Namba, S., Lin, S. C., Nam, K., Sidorenko, J., Wang, H., ... & Yengo, L. (2023). Boosting the power of genome-wide association studies within and across ancestries by using polygenic scores. Nature Genetics, 1-8.
- Keywords: LOCO-PGSs, two-stage meta-analysis strategy

# Reviews
- CITAION:Povysil, Gundula, et al. "Rare-variant collapsing analyses for complex traits: guidelines and applications." Nature Reviews Genetics 20.12 (2019): 747-759.
