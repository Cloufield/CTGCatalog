# Contents
- Single variant association tests
  - PLINK
  - PLINK2
  - EMAX
  - GEMMA
  - fastGWA
  - REGENIE
  - SAIGE
  - Bolt-lMM
- Gene-based analysis (rare variant)
  - regenie
  - SAIGE-GENE
  - SAIGE-GENE+
  - SKAT-O

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
- CITATION:  Korte, Arthur, et al. "A mixed-model approach for genome-wide association studies of correlated traits in structured populations." Nature genetics 44.9 (2012): 1066-1071.

## GEMMA
- FULLNAME:
- SHORTNAME:
- URL: 
- CITATION: 

## SAIGE
- FULLNAME:
- SHORTNAME:
- URL: 
- CITATION: 

## Bolt-lMM
- FULLNAME:
- SHORTNAME:
- URL: 
- CITATION: 

## fastGWA-lmm
- FULLNAME:
- SHORTNAME:
- URL: 
- CITATION: 

## fastGWA-glmm
- FULLNAME:
- SHORTNAME:
- URL: 
- CITATION: 

## REGENIE
- FULLNAME:REGENIE
- SHORTNAME:REGENIE
- URL: https://github.com/rgcgithub/regenie
- DESCRIPTION:regenie is a C++ program for whole genome regression modelling of large genome-wide association studies. It is developed and supported by a team of scientists at the Regeneron Genetics Center.
- CITATION: Mbatchou, Joelle, et al. "Computationally efficient whole-genome regression for quantitative and binary traits." Nature genetics 53.7 (2021): 1097-1103.
- KEY WORDS: whole genome regression

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
