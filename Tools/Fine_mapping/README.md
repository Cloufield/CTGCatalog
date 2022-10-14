# Contents
- FINEMAP
- SUSIE
- SparsePro
- CAVIAR
- CAVIARBF
- MsCAVIAR 
- PAINTOR 
- MR-MEGA

## FINEMAP
- SHORT NAME: FINEMAP
- FULL NAME: FINEMAP
- YEAR: 2016
- DESCRIPTION: FINEMAP is a program for 1.identifying causal SNPs, 2. estimating effect sizes of causal SNPs, 3 estimating the heritability contribution of causal SNPs 
- URL : [http://www.christianbenner.com/](http://www.christianbenner.com/)
- CITATION: Benner, C., Spencer, C. C., Havulinna, A. S., Salomaa, V., Ripatti, S., & Pirinen, M. (2016). FINEMAP: efficient variable selection using summary data from genome-wide association studies. Bioinformatics, 32(10), 1493-1501.
- KEY WORDS: Shotgun Stochastic Search (SSS)

## SUSIE
- SHORT NAME: SUSIE
- FULL NAME: sum of single effects
- YEAR: 2020
- DESCRIPTION: The susieR package implements a simple new way to perform variable selection in multiple regression (y = Xb + e). The methods implemented here are particularly well-suited to settings where some of the X variables are highly correlated, and the true effects are highly sparse (e.g. <20 non-zero effects in the vector b). One example of this is genetic fine-mapping applications, and this application was a major motivation for developing these methods.
- URL : [https://stephenslab.github.io/susieR/index.html](https://stephenslab.github.io/susieR/index.html)
- CITATION: Wang, G., Sarkar, A., Carbonetto, P. & Stephens, M. (2020). A simple new approach to variable selection in regression, with application to genetic fine mapping. Journal of the Royal Statistical Society, Series B 82, 1273–1300. https://doi.org/10.1111/rssb.12388

## SparsePro
- SHORT NAME: SparsePro
- FULL NAME: SparsePro
- YEAR: 2021
- DESCRIPTION: SparsePro is a command line tool for efficiently conducting genome-wide fine-mapping. Our method has two key features: First, by creating a sparse low-dimensional projection of the high-dimensional genotype, we enable a linear search of causal variants instead of an exponential search of causal configurations in most existing methods; Second, we adopt a probabilistic framework with a highly efficient variational expectation-maximization algorithm to integrate statistical associations and functional priors.
- URL : [https://github.com/zhwm/SparsePro](https://github.com/zhwm/SparsePro)
- CITATION: Zhang, W., Najafabadi, H. S., & Li, Y. (2021). SparsePro: an efficient genome-wide fine-mapping method integrating summary statistics and functional annotations. bioRxiv.

## CAVIAR
- SHORT NAME: CAVIAR
- FULL NAME: causal variants identification in associated regions
- YEAR: 2014
- DESCRIPTION: a statistical framework that quantifies the probability of each variant to be causal while allowing an arbitrary number of causal variants.
- URL : [http://genetics.cs.ucla.edu/caviar/](http://genetics.cs.ucla.edu/caviar/)
- CITATION: Hormozdiari, F., Kostem, E., Kang, E. Y., Pasaniuc, B., & Eskin, E. (2014). Identifying causal variants at loci with multiple signals of association. Genetics, 198(2), 497-508.


## CAVIARBF
- SHORT NAME: CAVIARBF
- FULL NAME: CAVIAR Bayes factor
- YEAR: 2015
- DESCRIPTION: a fine-mapping method using marginal test statistics in the Bayesian framework
- URL : [https://bitbucket.org/Wenan/caviarbf/src/master/](https://bitbucket.org/Wenan/caviarbf/src/master/)
- CITATION: Chen, W., Larrabee, B. R., Ovsyannikova, I. G., Kennedy, R. B., Haralambieva, I. H., Poland, G. A., & Schaid, D. J. (2015). Fine mapping causal variants with an approximate Bayesian method using marginal test statistics. Genetics, 200(3), 719-736.
- KEY WORDS: Bayes factor


## MsCAVIAR
- SHORT NAME: MsCAVIAR
- FULL NAME: multiple study causal variants identification in associated regions
- YEAR: 2021
- DESCRIPTION: MsCAVIAR is a method for fine-mapping (identifying causal variants among GWAS associated variants) by leveraging information from multiple studies. One important application area is trans-ethnic fine mapping. 
- URL : [https://github.com/nlapier2/MsCAVIAR](https://github.com/nlapier2/MsCAVIAR)
- CITATION: LaPierre, N., Taraszka, K., Huang, H., He, R., Hormozdiari, F., & Eskin, E. (2021). Identifying causal variants by fine mapping across multiple studies. PLoS genetics, 17(9), e1009733.
- KEY WORDS: multi-study finemapping


## PAINTOR
- SHORT NAME: PAINTOR 
- FULL NAME: Probabilistic Annotation INtegraTOR
- YEAR: 2014
- DESCRIPTION: Finding causal variants that underlie known risk loci is one of the main post-GWAS challenges. Here we present PAINTOR (Probabilistic Annotation INtegraTOR), a probabilistic framework that integrates association strength with genomic functional annotation data to improve accuracy in selecting plausible causal variants for functional validation. The main output of PAINTOR are probabilities for every variant to be causal that can be used for prioritization in functional assays to establish biological causality.
- URL : [https://bogdan.dgsom.ucla.edu/pages/paintor/](https://bogdan.dgsom.ucla.edu/pages/paintor/)
- CITATION: Kichaev, G., Yang, W. Y., Lindstrom, S., Hormozdiari, F., Eskin, E., Price, A. L., ... & Pasaniuc, B. (2014). Integrating functional data to prioritize causal variants in statistical fine-mapping studies. PLoS genetics, 10(10), e1004722.
- KEY WORDS: Empirical Bayes prior

## MR-MEGA
- SHORT NAME: MR-MEGA
- FULL NAME: Meta-Regression of Multi-AncEstry Genetic Association
- YEAR: 2017
- DESCRIPTION: MR-MEGA (Meta-Regression of Multi-AncEstry Genetic Association) is a tool to detect and fine-map complex trait association signals via multi-ancestry meta-regression.  This approach uses genome-wide metrics of diversity between populations to derive axes of genetic variation via multi-dimensional scaling [Purcell 2007].  Allelic effects of a variant across GWAS, weighted by their corresponding standard errors, can then be modelled in a linear regression framework, including the axes of genetic variation as covariates.  The flexibility of this model enables partitioning of the heterogeneity into components due to ancestry and residual variation, which would be expected to improve fine-mapping resolution.
- URL : [https://genomics.ut.ee/en/tools](https://genomics.ut.ee/en/tools)
- CITATION: Mägi, R., Horikoshi, M., Sofer, T., Mahajan, A., Kitajima, H., Franceschini, N., ... & Morris, A. P. (2017). Trans-ethnic meta-regression of genome-wide association studies accounting for ancestry increases power for discovery and improves fine-mapping resolution. Human molecular genetics, 26(18), 3639-3650.
- KEY WORDS: Multi-AncEstry
