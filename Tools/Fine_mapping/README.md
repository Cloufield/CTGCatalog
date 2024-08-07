# Contents
- FINEMAP
- SUSIE 
- SUSIE-RSS
- SUSIEx
- mvSuSiE
- MESuSiE
- SparsePro
- CAVIAR
- CAVIARBF
- MsCAVIAR
- CAFEH 
- PAINTOR 
- MR-MEGA
- RFR/SuSiE-inf/FINEMAP-inf
- JAM
- mJAM

## FINEMAP
- SHORT NAME: FINEMAP
- FULL NAME: FINEMAP
- YEAR: 2016
- DESCRIPTION: FINEMAP is a program for 1.identifying causal SNPs, 2. estimating effect sizes of causal SNPs, 3 estimating the heritability contribution of causal SNPs 
- URL : http://www.christianbenner.com/
- CITATION: Benner, C., Spencer, C. C., Havulinna, A. S., Salomaa, V., Ripatti, S., & Pirinen, M. (2016). FINEMAP: efficient variable selection using summary data from genome-wide association studies. Bioinformatics, 32(10), 1493-1501.
- KEYWORDS: Shotgun Stochastic Search (SSS)

## SUSIE
- SHORT NAME: SUSIE
- FULL NAME: sum of single effects
- YEAR: 2020
- DESCRIPTION: The susieR package implements a simple new way to perform variable selection in multiple regression (y = Xb + e). The methods implemented here are particularly well-suited to settings where some of the X variables are highly correlated, and the true effects are highly sparse (e.g. <20 non-zero effects in the vector b). One example of this is genetic fine-mapping applications, and this application was a major motivation for developing these methods.
- URL : https://stephenslab.github.io/susieR/index.html
- CITATION : Wang, G., Sarkar, A., Carbonetto, P. & Stephens, M. (2020). A simple new approach to variable selection in regression, with application to genetic fine mapping. Journal of the Royal Statistical Society, Series B 82, 1273–1300. https://doi.org/10.1111/rssb.12388
- KEYWORDS: fine-mapping, sum of single-effects (SuSiE) regression, iterative Bayesian stepwise selection (IBSS)

## SUSIE-RSS
- SHORT NAME: SUSIE-RSS
- FULL NAME: sum of single effects regression with summary statistics
- YEAR: 2022
- DESCRIPTION: The susieR package implements a simple new way to perform variable selection in multiple regression (y = Xb + e). The methods implemented here are particularly well-suited to settings where some of the X variables are highly correlated, and the true effects are highly sparse (e.g. <20 non-zero effects in the vector b). One example of this is genetic fine-mapping applications, and this application was a major motivation for developing these methods.
- URL : https://stephenslab.github.io/susieR/index.html
- CITATION : Zou, Yuxin, et al. "Fine-mapping from summary data with the “Sum of Single Effects” model." PLoS Genetics 18.7 (2022): e1010299.
- KEYWORDS: fine-mapping, summary statistics

## SUSIEx 
- SHORT NAME:SUSIEx
- FULL NAME:SUSIEx
- YEAR:2023
- DESCRIPTION: SuSiEx is a Python based command line tool that performs cross-ethnic fine-mapping using GWAS summary statistics and LD reference panels. The method is built on the Sum of Single Effects (SuSiE) model.
- URL : https://github.com/getian107/SuSiEx
- CITATION : https://www.medrxiv.org/content/10.1101/2023.01.07.23284293v2
- KEYWORDS: cross-ancestry, fine-mapping

## MultiSuSiE  
- SHORT NAME:MultiSuSiE 
- FULL NAME: MultiSuSiE
- YEAR:2024
- DESCRIPTION: MultiSuSiE is a multi-ancestry extension of the Sum of Single Effects model (Wang et al. 2020 J. R. Statist. Soc. B, Zou et al. 2022 PLoS Genet.) implemented in Python.
- URL : https://github.com/jordanero/MultiSuSiE
- CITATION : Rossen, J. et al. MultiSuSiE improves multi-ancestry fine-mapping in All of Us whole-genome sequencing data. medRxiv 2024.05.13.24307291 (2024) doi:10.1101/2024.05.13.24307291
- KEYWORDS: cross-ancestry, fine-mapping

## mvSuSiE 
- SHORT NAME:mvSuSiE
- FULL NAME:mvSuSiE
- YEAR:2023
- DESCRIPTION: Implements a multivariate generalization of the "Sum of Single Effects" (SuSiE) model for variable selection in multivariate linear regression.
- URL : https://github.com/stephenslab/mvsusieR
- CITATION: Zou, Y., Carbonetto, P., Xie, D., Wang, G., & Stephens, M. (2023). Fast and flexible joint fine-mapping of multiple traits via the Sum of Single Effects model. bioRxiv, 2023-04.
- KEYWORDS: multi-trait, fine-mapping

## MESuSiE
- SHORT NAME: MESuSiE
- FULL NAME:  multi-ancestry sum of the single effects model
- YEAR:2024
- DESCRIPTION: MESuSiE relies on GWAS summary statistics from multiple ancestries, properly accounts for the LD structure of the local genomic region in multiple ancestries, and explicitly models both shared and ancestry-specific causal signals to accommodate causal effect size similarity as well as heterogeneity across ancestries. MESuSiE outputs posterior inclusion probability of variant being shared or ancestry-specific causal variants. 
- URL: https://github.com/borangao/MESuSiE
- CITATION: Gao, B., Zhou, X. MESuSiE enables scalable and powerful multi-ancestry fine-mapping of causal variants in genome-wide association studies. Nat Genet (2024). https://doi.org/10.1038/s41588-023-01604-7
- KEYWORDS: multi-trait, fine-mapping

## SparsePro
- SHORT NAME: SparsePro
- FULL NAME: SparsePro
- YEAR: 2021
- DESCRIPTION: SparsePro is a command line tool for efficiently conducting genome-wide fine-mapping. Our method has two key features: First, by creating a sparse low-dimensional projection of the high-dimensional genotype, we enable a linear search of causal variants instead of an exponential search of causal configurations in most existing methods; Second, we adopt a probabilistic framework with a highly efficient variational expectation-maximization algorithm to integrate statistical associations and functional priors.
- URL : https://github.com/zhwm/SparsePro
- CITATION: Zhang, W., Najafabadi, H. S., & Li, Y. (2021). SparsePro: an efficient genome-wide fine-mapping method integrating summary statistics and functional annotations. bioRxiv.
- CITATION: Zhang, W., Najafabadi, H., & Li, Y. (2023). SparsePro: An efficient fine-mapping method integrating summary statistics and functional annotations. PLoS genetics, 19(12), e1011104.

## CAVIAR
- SHORT NAME: CAVIAR
- FULL NAME: causal variants identification in associated regions
- YEAR: 2014
- DESCRIPTION: a statistical framework that quantifies the probability of each variant to be causal while allowing an arbitrary number of causal variants.
- URL : http://genetics.cs.ucla.edu/caviar/
- CITATION: Hormozdiari, F., Kostem, E., Kang, E. Y., Pasaniuc, B., & Eskin, E. (2014). Identifying causal variants at loci with multiple signals of association. Genetics, 198(2), 497-508.


## CAVIARBF
- SHORT NAME: CAVIARBF
- FULL NAME: CAVIAR Bayes factor
- YEAR: 2015
- DESCRIPTION: a fine-mapping method using marginal test statistics in the Bayesian framework
- URL : https://bitbucket.org/Wenan/caviarbf/src/master/
- CITATION: Chen, W., Larrabee, B. R., Ovsyannikova, I. G., Kennedy, R. B., Haralambieva, I. H., Poland, G. A., & Schaid, D. J. (2015). Fine mapping causal variants with an approximate Bayesian method using marginal test statistics. Genetics, 200(3), 719-736.
- KEYWORDS: Bayes factor


## MsCAVIAR
- SHORT NAME: MsCAVIAR
- FULL NAME: multiple study causal variants identification in associated regions
- YEAR: 2021
- DESCRIPTION: MsCAVIAR is a method for fine-mapping (identifying causal variants among GWAS associated variants) by leveraging information from multiple studies. One important application area is trans-ethnic fine mapping. 
- URL : https://github.com/nlapier2/MsCAVIAR
- CITATION: LaPierre, N., Taraszka, K., Huang, H., He, R., Hormozdiari, F., & Eskin, E. (2021). Identifying causal variants by fine mapping across multiple studies. PLoS genetics, 17(9), e1009733.
- KEYWORDS: multi-study finemapping

## CAFEH
- SHORT NAME: CAFEH
- FULL NAME: colocalization and fine-mapping in the presence of allelic heterogeneity
- YEAR: 2022
- DESCRIPTION: CAFEH is a method that performs finemapping and colocalization jointly over multiple phenotypes. CAFEH can be run with 10s of phenotypes and 1000s of variants in a few minutes.
- URL : https://github.com/karltayeb/cafeh
- CITATION: Arvanitis, M., Tayeb, K., Strober, B. J., & Battle, A. (2022). Redefining tissue specificity of genetic regulation of gene expression in the presence of allelic heterogeneity. The American Journal of Human Genetics, 109(2), 223-239.
- KEYWORDS: multi-trait, finemapping, colocalization


## PAINTOR
- SHORT NAME: PAINTOR 
- FULL NAME: Probabilistic Annotation INtegraTOR
- YEAR: 2014
- DESCRIPTION: Finding causal variants that underlie known risk loci is one of the main post-GWAS challenges. Here we present PAINTOR (Probabilistic Annotation INtegraTOR), a probabilistic framework that integrates association strength with genomic functional annotation data to improve accuracy in selecting plausible causal variants for functional validation. The main output of PAINTOR are probabilities for every variant to be causal that can be used for prioritization in functional assays to establish biological causality.
- URL : https://bogdan.dgsom.ucla.edu/pages/paintor/
- CITATION: Kichaev, G., Yang, W. Y., Lindstrom, S., Hormozdiari, F., Eskin, E., Price, A. L., ... & Pasaniuc, B. (2014). Integrating functional data to prioritize causal variants in statistical fine-mapping studies. PLoS genetics, 10(10), e1004722.
- KEYWORDS: Empirical Bayes prior

## MR-MEGA
- SHORT NAME: MR-MEGA
- FULL NAME: Meta-Regression of Multi-AncEstry Genetic Association
- YEAR: 2017
- DESCRIPTION: MR-MEGA (Meta-Regression of Multi-AncEstry Genetic Association) is a tool to detect and fine-map complex trait association signals via multi-ancestry meta-regression.  This approach uses genome-wide metrics of diversity between populations to derive axes of genetic variation via multi-dimensional scaling [Purcell 2007].  Allelic effects of a variant across GWAS, weighted by their corresponding standard errors, can then be modelled in a linear regression framework, including the axes of genetic variation as covariates.  The flexibility of this model enables partitioning of the heterogeneity into components due to ancestry and residual variation, which would be expected to improve fine-mapping resolution.
- URL : https://genomics.ut.ee/en/tools
- CITATION: Mägi, R., Horikoshi, M., Sofer, T., Mahajan, A., Kitajima, H., Franceschini, N., ... & Morris, A. P. (2017). Trans-ethnic meta-regression of genome-wide association studies accounting for ancestry increases power for discovery and improves fine-mapping resolution. Human molecular genetics, 26(18), 3639-3650.
- KEYWORDS: Multi-AncEstry

## RFR SuSiE-inf FINEMAP-inf
- SHORT NAME: RFR
- FULL NAME: Replication Failure Rate 
- YEAR: 2022
- DESCRIPTION: Replication Failure Rate (RFR), a metric to assess the consistency of fine-mapping results based on downsampling a large cohort. SuSiE-inf and FINEMAP-inf, that extend SuSiE and FINEMAP to incorporate a term for infinitesimal effects in addition to a small number of larger causal effects of interest. 
- URL : https://github.com/FinucaneLab/fine-mapping-inf
- CITATION:Cui, R., Elzur, R. A., Kanai, M., Ulirsch, J. C., Weissbrod, O., Daly, M., ... & Finucane, H. K. (2022). Improving fine-mapping by modeling infinitesimal effects. bioRxiv.
- CITATION: Cui, R., Elzur, R. A., Kanai, M., Ulirsch, J. C., Weissbrod, O., Daly, M. J., ... & Finucane, H. K. (2023). Improving fine-mapping by modeling infinitesimal effects. Nature Genetics, 1-8.

## JAM
- SHORT NAME: JAM
- FULL NAME:  joint analysis of marginal summary statistics
- YEAR: 2016
- DESCRIPTION: Bayesian variable selection under a range of likelihoods, including linear regression for continuous outcomes, logistic regression for binary outcomes, Weibull regression for survival outcomes binary and survial outcomes, and the "JAM" model for summary genetic association data.
- URL : https://github.com/pjnewcombe/R2BGLiMS
- CITATION: Newcombe, Paul J., David V. Conti, and Sylvia Richardson. "JAM: a scalable Bayesian framework for joint analysis of marginal SNP effects." Genetic epidemiology 40.3 (2016): 188-201.

## mJAM
- SHORT NAME: mJAM
- FULL NAME: multi-population JAM
- YEAR: 2022
- URL : https://github.com/USCbiostats/hJAM/R
- CITATION: Shen, J., Jiang, L., Wang, K., Wang, A., Chen, F., Newcombe, P. J., ... & Conti, D. V. (2022). Fine-mapping and credible set construction using a multi-population joint analysis of marginal summary statistics from genome-wide association studies. bioRxiv, 2022-12.
- KEYWORDS: multi-population
