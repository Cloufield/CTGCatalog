# PRS methods, tools, reviews and benchmearks

- PLINK2
- PRSice-2
- PRSet
- LDpred
- LDpred2
- LDpred-funct
- LDpred2-auto
- PRS-CS
- PRS-CSx
- lassosum
- Multi-PGS
- PGSCatalog
- wMT-SBLUP
- pgsc_calc
- VIPRS
- MegaPRS
- BayesS
- BayesR
- SBayesR
- SBayesS
- SBayesRC
- TL-PRS
- ExPRSweb
- Cancer PRSweb
- PRS atlas
- metabolites PRS atlas
- PUMA-CUBS
- MiXeR
- SDPRX
- PRStuning
- BridgePRS
- PROSPER


## PLINK2
- SHORT NAME: PLINK2 
- FULL NAME: PLINK2
- DESCRIPTION: The second-generation versions of PLINK will offer dramatic improvements in performance and compatibility.
- URL :  https://www.cog-genomics.org/plink/2.0/
- CITATION: Chang, C.C., Chow, C.C., Tellier, L.C. et al. Second-generation PLINK: rising to the challenge of larger and richer datasets. GigaSci 4, 7 (2015). https://doi.org/10.1186/s13742-015-0047-8
- USE: calculate PRS using genotype data.

## PRSice-2
- SHORT NAME: PRSice-2
- FULL NAME: PRSice-2
- DESCRIPTION: PRSice (pronounced 'precise') is a Polygenic Risk Score software for calculating, applying, evaluating and plotting the results of polygenic risk scores (PRS) analyses.
- URL : https://www.prsice.info/
- CITATION: Shing Wan Choi, Paul F O'Reilly, PRSice-2: Polygenic Risk Score software for biobank-scale data, GigaScience, Volume 8, Issue 7, July 2019, giz082, https://doi.org/10.1093/gigascience/giz082

## PRSet
- SHORT NAME: PRSet
- FULL NAME: PRSet
- DESCRIPTION: A new feature of PRSice is the ability to perform set base/pathway based analysis. This new feature is called PRSet.
- URL : https://www.prsice.info/quick_start_prset/
- CITATION: Choi SW, Garcia-Gonzalez J, Ruan Y, et al. The power of pathway-based polygenic risk scores. Research Square; 2021. DOI: 10.21203/rs.3.rs-643696/v1.
- KEYWORDS: pathway-based

## LDpred
- SHORT NAME: LDpred
- FULL NAME: LDpred
- DESCRIPTION: LDpred is a Python based software package that adjusts GWAS summary statistics for the effects of linkage disequilibrium (LD).
- URL : https://github.com/bvilhjal/ldpred
- CITATION: Vilhjálmsson, B. J., Yang, J., Finucane, H. K., Gusev, A., Lindström, S., Ripke, S., ... & Marsal, S. (2015). Modeling linkage disequilibrium increases accuracy of polygenic risk scores. The american journal of human genetics, 97(4), 576-592.
- KEYWORDS: Bayesian, Gaussian infinitesimal prior, python

## LDpred2
- SHORT NAME: LDpred2
- FULL NAME: LDpred2
- DESCRIPTION: LDpred-2 is one of the dedicated PRS programs which is an R package that uses a Bayesian approach to polygenic risk scoring.
- URL : https://privefl.github.io/bigsnpr/articles/LDpred2.html
- CITATION: Privé, F., Arbel, J., & Vilhjálmsson, B. J. (2020). LDpred2: better, faster, stronger. Bioinformatics, 36(22-23), 5424-5431.
- KEYWORDS: Bayesian, R, LDpred2-grid (LDpred2), LDpred2-auto, LDpred2-sparse

## LDpred2-auto
- SHORT NAME: LDpred2-auto
- FULL NAME: LDpred2-auto
- DESCRIPTION: LDpred2 is a widely used Bayesian method for building polygenic scores (PGS). LDpred2-auto can infer the two parameters from the LDpred model, h^2 and p, so that it does not require an additional validation dataset to choose best-performing parameters. Here, we present a new version of LDpred2-auto, which adds a third parameter alpha to its model for modeling negative selection. Additional changes are also made to provide better sampling of these parameters. 
- URL : https://privefl.github.io/bigsnpr/articles/LDpred2.html
- CITATION: Inferring disease architecture and predictive ability with LDpred2-auto Florian Privé, Clara Albiñana, Bogdan Pasaniuc, Bjarni J. Vilhjálmsson bioRxiv 2022.10.10.511629; doi: https://doi.org/10.1101/2022.10.10.511629
- KEYWORDS: Bayesian, new LDpred2-auto, α (relationship between MAF and beta)

## LDpred-funct
- SHORT NAME: LDpred-funct
- FULL NAME: LDpred-funct
- DESCRIPTION: LDpred-funct is a method for polygenic prediction that leverages trait-specific functional priors to increase prediction accuracy.
- URL : https://github.com/carlaml/LDpred-funct
- CITATION: Márquez-Luna, C., Gazal, S., Loh, P. R., Kim, S. S., Furlotte, N., Auton, A., & Price, A. L. (2021). Incorporating functional priors improves polygenic prediction accuracy in UK Biobank and 23andMe data sets. Nature Communications, 12(1), 1-11.
- KEYWORDS: Bayesian, functional priors

## PRS-CS
- SHORT NAME: PRS-CS
- FULL NAME: PRS-CS
- YEAR: 2019
- DESCRIPTION: PRS-CS is a Python based command line tool that infers posterior SNP effect sizes under continuous shrinkage (CS) priors using GWAS summary statistics and an external LD reference panel.
- URL : https://github.com/getian107/PRScs
- CITATION: Ge, T., Chen, CY., Ni, Y. et al. Polygenic prediction via Bayesian regression and continuous shrinkage priors. Nat Commun 10, 1776 (2019). https://doi.org/10.1038/s41467-019-09718-5
- KEYWORDS: continuous shrinkage (CS) prior

## PRS-CSx
- SHORT NAME: PRS-CSx
- FULL NAME: PRS-CSx
- YEAR: 2022
- DESCRIPTION: PRS-CSx is a Python based command line tool that integrates GWAS summary statistics and external LD reference panels from multiple populations to improve cross-population polygenic prediction. Posterior SNP effect sizes are inferred under coupled continuous shrinkage (CS) priors across populations. 
- URL : https://github.com/getian107/PRScsx
- CITATION: Ruan, Y., Lin, YF., Feng, YC.A. et al. Improving polygenic prediction in ancestrally diverse populations. Nat Genet 54, 573–580 (2022). https://doi.org/10.1038/s41588-022-01054-7
- KEYWORDS: continuous shrinkage (CS) prior,  cross-population

## lassosum
- SHORT NAME: lassosum
- FULL NAME: lassosum
- YEAR: 2017
- DESCRIPTION: lassosum is a method for computing LASSO/Elastic Net estimates of a linear regression problem given summary statistics from GWAS and Genome-wide meta-analyses, accounting for Linkage Disequilibrium (LD), via a reference panel.
- URL : https://github.com/tshmak/lassosum
- CITATION: Mak, T. S. H., Porsch, R. M., Choi, S. W., Zhou, X., & Sham, P. C. (2017). Polygenic scores via penalized regression on summary statistics. Genetic epidemiology, 41(6), 469-480.
- KEYWORDS: penalized regression

## BayesR
- SHORT NAME: BayesR
- FULL NAME: BayesR
- YEAR: 2015
- DESCRIPTION: Bayesian mixture model to dissect genetic variation for disease in human populations and to construct more powerful risk predictors
- URL:https://cnsgenomics.com/software/gctb/#Overview
- CITATION:Moser, G., Lee, S. H., Hayes, B. J., Goddard, M. E., Wray, N. R., & Visscher, P. M. (2015). Simultaneous discovery, estimation and prediction analysis of complex traits using a Bayesian mixture model. PLoS genetics, 11(4), e1004969.

## BayesS
- SHORT NAME: BayesS
- FULL NAME: BayesS
- YEAR: 2018
- URL:https://cnsgenomics.com/software/gctb/#Overview
- CITATION:Zeng, J., De Vlaming, R., Wu, Y., Robinson, M. R., Lloyd-Jones, L. R., Yengo, L., ... & Yang, J. (2018). Signatures of negative selection in the genetic architecture of human complex traits. Nature genetics, 50(5), 746-753.

## SBayesR
- SHORT NAME: SBayesR
- FULL NAME: SBayesR
- YEAR: 2019
- DESCRIPTION: extend a powerful individual-level data Bayesian multiple regression model (BayesR) to one that utilises summary statistics from genome-wide association studies, SBayesR.
- URL:https://cnsgenomics.com/software/gctb/#Overview
- CITATION:Lloyd-Jones, L. R., Zeng, J., Sidorenko, J., Yengo, L., Moser, G., Kemper, K. E., ... & Visscher, P. M. (2019). Improved polygenic prediction by Bayesian multiple regression on summary statistics. Nature communications, 10(1), 1-11.

## SBayesS
- SHORT NAME: SBayesS
- FULL NAME: SBayesS
- YEAR: 2021
- DESCRIPTION: estimate multiple genetic architecture parameters including selection signature using only GWAS summary statistics
- URL:https://cnsgenomics.com/software/gctb/#Overview
- CITATION:Zeng, J., Xue, A., Jiang, L., Lloyd-Jones, L. R., Wu, Y., Wang, H., ... & Yang, J. (2021). Widespread signatures of natural selection across human complex traits and functional genomic categories. Nature communications, 12(1), 1-12.

## SBayesRC
- SHORT NAME: SBayesRC
- FULL NAME: SBayesRC
- YEAR: 2022
- URL:https://cnsgenomics.com/software/gctb/#Overview
- DESCRIPTION: SBayesRC integrates GWAS summary statistics with functional genomic annotations to improve polygenic prediction of complex traits.
- CITATION: Zheng, Z., Liu, S., Sidorenko, J., Yengo, L., Turley, P., Ani, A., ... & Zeng, J. (2022). Leveraging functional genomic annotations and genome coverage to improve polygenic prediction of complex traits within and between ancestries. bioRxiv, 2022-10.
- CITATION: Zheng, Z., Liu, S., Sidorenko, J. et al. Leveraging functional genomic annotations and genome coverage to improve polygenic prediction of complex traits within and between ancestries. Nat Genet (2024). https://doi.org/10.1038/s41588-024-01704-y
- KEYWORDS: functional genomic annotation, whole-genome variants,  cross-ancestry

## TL-PRS
- SHORT NAME: TL-PRS
- FULL NAME: transfer learning PRS
- YEAR: 2022
- URL: https://github.com/ZhangchenZhao/TLPRS
- DESCRIPTION: This R package helps users to construct multi-ethnic polygenic risk score (PRS) using transfer learning. It can help predict PRS of minor ancestry using summary statistics from exsiting resources, such as UK Biobank.
- CITATION: Zhao, Z., Fritsche, L. G., Smith, J. A., Mukherjee, B., & Lee, S. (2022). The Construction of Multi-ethnic Polygenic Risk Score using Transfer Learning. medRxiv.

## Multi-PGS
- SHORT NAME: Multi-PGS
- YEAR: 2022
- FULL NAME: Multi-PGS
- DESCRIPTION: a framework to generate enriched PGS from a wealth of publicly available genome-wide association studies, combining thousands of studies focused on many different phenotypes, into a multi-PGS
- URL : https://github.com/ClaraAlbi/paper_multiPGS
- CITATION: Albiñana, C., Zhu, Z., Schork, A. J., Ingason, A., Aschard, H., Brikell, I., ... & Vilhjálmsson, B. J. (2023). Multi-PGS enhances polygenic prediction by combining 937 polygenic scores. Nature Communications, 14(1), 4702.

## wMT-SBLUP
- SHORT NAME: wMT-SBLUP
- YEAR: 2018
- FULL NAME: weighted approximate multi-trait summary statistic BLUP
- URL : https://github.com/uqrmaie1/smtpred
- CITATION: Maier, R.M., Zhu, Z., Lee, S.H. et al. Improving genetic prediction by leveraging genetic correlations among human diseases and traits. Nat Commun 9, 989 (2018). https://doi.org/10.1038/s41467-017-02769-6

## PGSCatalog
- SHORT NAME: PGS Catalog
- FULL NAME: PGS Catalog
- DESCRIPTION: The PGS Catalog is an open database of published polygenic scores (PGS). Each PGS in the Catalog is consistently annotated with relevant metadata; including scoring files (variants, effect alleles/weights), annotations of how the PGS was developed and applied, and evaluations of their predictive performance.
- URL : https://www.pgscatalog.org/
- CITATION: Lambert, S. A., Gil, L., Jupp, S., Ritchie, S. C., Xu, Y., Buniello, A., ... & Inouye, M. (2021). The Polygenic Score Catalog as an open database for reproducibility and systematic evaluation. Nature Genetics, 53(4), 420-425.
- KEYWORDS: PGS database

## pgsc_calc
- SHORT NAME: pgsc_calc
- FULL NAME: The Polygenic Score Catalog Calculator
- YEAR: 2022
- DESCRIPTION: pgsc_calc is a bioinformatics best-practice analysis pipeline for calculating polygenic [risk] scores on samples with imputed genotypes using existing scoring files from the Polygenic Score (PGS) Catalog and/or user-defined PGS/PRS.
- URL : https://github.com/PGScatalog/pgsc_calc
- CITATION: https://github.com/PGScatalog/pgsc_calc
- KEYWORDS: PRS calculation pipeline

## VIPRS
- SHORT NAME: VIPRS
- FULL NAME: Variational inference of polygenic risk scores
- YEAR: 2022
- DESCRIPTION: viprs is a python package that implements scripts and utilities for running variational inference algorithms on genome-wide association study (GWAS) data for the purposes polygenic risk estimation.
- URL : https://github.com/shz9/viprs
- CITATION: Zabad, S., Gravel, S., & Li, Y. (2022). Fast and Accurate Bayesian Polygenic Risk Modeling with Variational Inference. bioRxiv.
- KEYWORDS:  Variational Inference (VI)

## ExPRSweb
- SHORT NAME: ExPRSweb
- FULL NAME: exposure polygenic risk scores (ExPRSs)
- YEAR: 2022
- DESCRIPTION: Integrating published and freely available genome-wide association studies (GWAS) summary statistics from multiple sources (published GWAS, the NHGRI-EBI GWAS Catalog, FinnGen- or UKB-based GWAS), we created an online repository for exposure polygenic risk scores (ExPRS) for health-related exposure traits. Our framework condenses these summary statistics into ExPRS using linkage disequilibrium pruning and p-value thresholding (P&T) or penalized, genome-wide effect size weighting. We evaluate them in the cohort of the Michigan Genomics Initiative (MGI), a longitudinal biorepository effort at Michigan Medicine, and in the population-based UK Biobank Study (UKB). For each ExPRS construct, measures on performance, accuracy, and discrimination are provided. Beyond the ExPRS evaluation in MGI and UKB, the ExPRSweb platform features construct downloads, evaluation in the top percentiles, and phenome-wide ExPRS association studies (ExPRS-PheWAS) for a subset of ExPRS that are predictive for the corresponding exposure.
- URL : https://exprsweb.sph.umich.edu:8443/
- CITATION: Ma, Y., Patil, S., Zhou, X., Mukherjee, B., & Fritsche, L. G. (2022). ExPRSweb-An Online Repository with Polygenic Risk Scores for Common Health-related Exposures. medRxiv.
- KEYWORDS: exposure PRS

## Cancer PRSweb
- SHORT NAME: Cancer PRSweb
- FULL NAME: Cancer PRSweb
- YEAR: 2020
- DESCRIPTION: Our framework condenses these summary statistics into PRS using linkage disequilibrium pruning and p-value thresholding (fixed or data-adaptively optimized thresholds) or penalized, genome-wide effect size weighting. We evaluate them in the cancer-enriched cohort of the Michigan Genomics Initiative (MGI), a longitudinal biorepository effort at Michigan Medicine, and in the population-based UK Biobank Study (UKB). For each PRS construct, measures on performance, calibration, and discrimination are provided. Beyond the cancer PRS evaluation in MGI and UKB, the PRSweb platform features construct downloads, risk evaluation in the top percentiles, and phenome-wide PRS association studies (PRS-PheWAS) for a subset of PRS that are predictive for the primary cancer.
- URL : https://prsweb.sph.umich.edu:8443/
- CITATION: Fritsche, L. G., Patil, S., Beesley, L. J., VandeHaar, P., Salvatore, M., Ma, Y., ... & Mukherjee, B. (2020). Cancer PRSweb: an online repository with polygenic risk scores for major cancer traits and their evaluation in two independent biobanks. The American Journal of Human Genetics, 107(5), 815-836.
- KEYWORDS: Cancer PRS

## PRS atlas  
- SHORT NAME: PRS atlas
- FULL NAME: PRS atlas
- DESCRIPTION: This web application can be used to query findings from an analysis of 162 polygenic risk scores and 551 complex traits using data from the UK Biobank study1. Traits were selected based on the heritability analysis conducted by the Neale Lab2 (P<0.05). We encourage users of this resource to conduct follow-up analyses of associations to robustly identify causal relationships between complex traits.
- URL : http://mrcieu.mrsoftware.org/PRS_atlas/
- CITATION: Richardson, T. G., Harrison, S., Hemani, G., & Smith, G. D. (2019). An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. Elife, 8, e43657.

## metabolites PRS atlas
- SHORT NAME: metabolites PRS atlas
- FULL NAME: metabolites PRS atlas
- DESCRIPTION: This web application can be used to query findings from a systematic analysis of 129 polygenic risk scores and 249 circulating metabolits using high-throughput nuclear magnetic resonance data from the UK Biobank study1,2. We encourage users of this resource to conduct follow-up analyses of associations to investigate potential causal and non-causal metabolic biomarkers. Age-stratified results can be used to investigate how potential sources of collider bias (e.g. statin therapy) may influence findings in the full sample
- URL : http://mrcieu.mrsoftware.org/metabolites_PRS_atlas/
- CITATION:Fang, S., Holmes, M. V., Gaunt, T. R., Smith, G. D., & Richardson, T. G. (2022). Constructing an atlas of associations between polygenic scores from across the human phenome and circulating metabolic biomarkers. eLife.

## PUMA-CUBS
- SHORT NAME:PUMA-CUBS
- FULL NAME:PUMA-CUBS
- DESCRIPTION:an ensemble learning strategy named PUMACUBS to combine multiple PRS models into an ensemble score without requiring external data for model fitting.
- URL :https://github.com/qlu-lab/PUMAS
- CITATION:Zhao, Zijie, et al. "Optimizing and benchmarking polygenic risk scores with GWAS summary statistics." bioRxiv (2022).

## MiXeR
- SHORT NAME: MiXeR
- FULL NAME: MiXeR
- DESCRIPTION: Causal Mixture Model for GWAS summary statistics
- URL :https://github.com/precimed/mixer
- CITATION: （univariate） Holland, Dominic, et al. "Beyond SNP heritability: Polygenicity and discoverability of phenotypes estimated with a univariate Gaussian mixture model." PLoS Genetics 16.5 (2020): e1008612.
- CITATION:（cross-trait analysis）Frei, Oleksandr, et al. "Bivariate causal mixture model quantifies polygenic overlap between complex traits beyond genetic correlation." Nature communications 10.1 (2019): 1-11.

## SDPRX
- SHORT NAME: SDPRX
- FULL NAME: SDPRX
- DESCRIPTION: SDPRX is a statistical method for cross-population prediction of complex traits. It integrates GWAS summary statistics and LD matrices from two populations (EUR and non-EUR) to compuate polygenic risk scores.
- URL : https://github.com/eldronzhou/SDPRX
- CITATION:Zhou, Geyu, Tianqi Chen, and Hongyu Zhao. "SDPRX: A statistical method for cross-population prediction of complex traits." The American Journal of Human Genetics (2022).

## PRStuning 
- SHORT NAME: PRStuning
- FULL NAME: PRStuning
- DESCRIPTION: Estimate Testing AUC for Binary Phenotype Using GWAS Summary Statistics from the Training Data 
- CITATION: Jiang, W., Chen, L., Girgenti, M. J., & Zhao, H. (2023). Tuning Parameters for Polygenic Risk Score Methods Using GWAS Summary Statistics from Training Data. Research Square.

## BridgePRS
- SHORT NAME: BridgePRS
- FULL NAME: BridgePRS
- DESCRIPTION: BridgePRS is a Bayesian-ridge (Bridge) approach, which "bridges" the PRS between two populations of different ancestry, developed to tackle the "PRS Portability Problem". The PRS Portability Problem causes lower accuracy PRS in underrepresented populations due to the biased sampling in GWAS data collection.
- YEAR: 2023
- URL: https://www.bridgeprs.net/
- CITATION: Hoggart, C. J., Choi, S. W., García-González, J., Souaiaia, T., Preuss, M., & O’Reilly, P. F. (2023). BridgePRS leverages shared genetic effects across ancestries to increase polygenic risk score portability. Nature Genetics, 1-7.

## PROSPER
- SHORT NAME: PROSPER
- FULL NAME: Polygenic Risk scOres based on enSemble of PEnalized Regression models
- DESCRIPTION: PROSPER is a new multi-ancestry PRS method with penalized regression followed by ensemble learning. This software is a command line tool based on R programming language. Large-scale benchmarking study shows that PROSPER could be the leading method to reduce the disparity of PRS performance across ancestry groups
- YEAR:2023
- URL: https://github.com/Jingning-Zhang/PROSPER
- CITATION: Zhang, J., Zhan, J., Jin, J., Ma, C., Zhao, R., O’Connell, J., ... & 23andMe Research Team. (2023). An ensemble penalized regression method for multi-ancestry polygenic risk prediction. BioRxiv.

## shaPRS
- SHORT NAME: shaPRS
- FULL NAME: shaPRS
- YEAR: 2024
- URL : https://github.com/mkelcb/shaprs
- DESCRIPTION: Leveraging shared genetic effects across traits and ancestries improves accuracy of polygenic scores
- CITATION : Kelemen, M., Vigorito, E., Fachal, L., Anderson, C. A., & Wallace, C. (2021). ShaPRS: leveraging shared genetic effects across traits or ancestries improves accuracy of polygenic scores. The American Journal of Human Genetics.
- KEYWORDS: cross-ancestry, genetic correlation

## Tutorial-Choi
- SHORT NAME: PRS Tutorial
- FULL NAME: PRS Tutorial
- DESCRIPTION: This tutorial provides a step-by-step guide to performing basic polygenic risk score (PRS) analyses and accompanies our PRS Guide paper. The aim of this tutorial is to provide a simple introduction of PRS analyses to those new to PRS, while equipping existing users with a better understanding of the processes and implementation "underneath the hood" of popular PRS software.
- URL : https://choishingwan.github.io/PRS-Tutorial/
- CITATION: Choi, S. W., Mak, T. S. H., & O’Reilly, P. F. (2020). Tutorial: a guide to performing polygenic risk score analyses. Nature protocols, 15(9), 2759-2772.

## Review-Peter
- CITATION: Peter M. Visscher,Loic Yengo,Nancy J. Cox,Naomi R. Wray,Discovery and implications of polygenicity of common diseases, Science, 373, 6562, (1468-1473), (2021). /doi/10.1126/science.abi8206

## Review-Kachuri
- CITATION: Kachuri, L., Chatterjee, N., Hirbo, J. et al. Principles and methods for transferring polygenic risk scores across global populations. Nat Rev Genet (2023).

## Review-Wang
- CITATION: Wang, Y., Tsuo, K., Kanai, M., Neale, B. M., & Martin, A. R. (2022). Challenges and Opportunities for Developing More Generalizable Polygenic Risk Scores. Annual Review of Biomedical Data Science, 5.

## Benchmark-Wang
- CITATION: Wang, C., Zhang, J., Zhou, X., & Zhang, L. (2022). A comprehensive investigation of statistical and machine learning approaches for predicting complex human diseases on genomic variants. bioRxiv.
