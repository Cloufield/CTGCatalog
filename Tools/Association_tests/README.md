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
## PLINK2
## EMAX
## GEMMA
## fastGWA
## REGENIE
## SAIGE
## Bolt-lMM
---

# Gene-based analysis (rare variant)
## regenie
## SAIGE-gene 
## SAIGE-GENE+
## SKAT-O

---

# eQTL
## MatrixEQTL 
- SHORT NAME : Matrix eQTL
- FULL NAME : Matrix eQTL
- URL: http://www.bios.unc.edu/research/genomic_software/Matrix_eQTL/
- DESCRIPTION : Matrix eQTL is designed for fast eQTL analysis on large datasets. Matrix eQTL can test for association between genotype and gene expression using linear regression with either additive or ANOVA genotype effects. The models can include covariates to account for factors as population stratification, gender, and clinical variables. It also supports models with heteroscedastic and/or correlated errors, false discovery rate estimation and separate treatment of local (cis) and distant (trans) eQTLs.
- CITATION: Shabalin, Andrey A. "Matrix eQTL: ultra fast eQTL analysis via large matrix operations." Bioinformatics 28.10 (2012): 1353-1358.

## FastQTL 
- SHORT NAME : FastQTL
- FULL NAME : FastQTL
- URL: https://github.com/francois-a/fastqtl
- DESCRIPTION : In order to discover quantitative trait loci (QTLs), multi-dimensional genomic datasets combining DNA-seq and ChiP-/RNA-seq require methods that rapidly correlate tens of thousands of molecular phenotypes with millions of genetic variants while appropriately controlling for multiple testing. FastQTL implements a popular cis-QTL mapping strategy in a user- and cluster-friendly tool. FastQTL also proposes an efficient permutation procedure to control for multiple testing.
- CITATION: Ongen, Halit, et al. "Fast and efficient QTL mapper for thousands of molecular phenotypes." Bioinformatics 32.10 (2016): 1479-1485.

## TReCASE 
- SHORT NAME : TReCASE (asSeq)
- FULL NAME : Total Read Count and Allele-Specific Expression
- URL: http://www.bios.unc.edu/~wsun/software.htm
- DESCRIPTION : A Statistical Framework for eQTL Mapping Using RNA-seq Data.
- CITATION: Sun, Wei. "A statistical framework for eQTL mapping using RNA‐seq data." Biometrics 68.1 (2012): 1-11.

## RASQUAL
Fine-mapping cellular QTLs with RASQUAL and ATAC-seq
- SHORT NAME : RASQUAL
- FULL NAME :Robust Allele Specific QUAntitation and quality controL
- URL: https://github.com/natsuhiko/rasqual
- DESCRIPTION : RASQUAL (Robust Allele Specific QUAntification and quality controL) maps QTLs for sequenced based cellular traits by combining population and allele-specific signals.
- CITATION: Kumasaka, Natsuhiko, Andrew J. Knights, and Daniel J. Gaffney. "Fine-mapping cellular QTLs with RASQUAL and ATAC-seq." Nature genetics 48.2 (2016): 206-213.

---
# sQTL
## THISTLE 
- SHORT NAME: THISTLE
- FULL NAME:testing for heterogeneity between isoform-eQTL effects
- DESCRIPTION:THISTLE (testing for heterogeneity between isoform-eQTL effects) is a transcript-based splicing QTL (sQTL) mapping method that uses either individual-level genotype and RNA-seq data or summary-level isoform-eQTL data.
- URL : https://yanglab.westlake.edu.cn/software/osca/#THISTLE
- CITATION:Qi, T., Wu, Y., Fang, H. et al. Genetic control of RNA splicing and its distinct role in complex trait variation. Nat Genet 54, 1355–1363 (2022). https://doi.org/10.1038/s41588-022-01154-4

## sQTLseekeR
- SHORT NAME: sQTLseekeR
- FULL NAME: sQTLseekeR
- DESCRIPTION:sQTLseekeR is a R package to detect splicing QTLs (sQTLs), which are variants associated with change in the splicing pattern of a gene. Here, splicing patterns are modeled by the relative expression of the transcripts of a gene.
- URL :https://github.com/jmonlong/sQTLseekeR
- CITATION: Monlong, J., Calvo, M., Ferreira, P. et al. Identification of genetic variants associated with alternative splicing using sQTLseekeR. Nat Commun 5, 4698 (2014). https://doi.org/10.1038/ncomms5698

## LeafCutter
- SHORT NAME: LeafCutter
- FULL NAME:LeafCutter
- DESCRIPTION: Leafcutter quantifies RNA splicing variation using short-read RNA-seq data. The core idea is to leverage spliced reads (reads that span an intron) to quantify (differential) intron usage across samples.
- URL : https://davidaknowles.github.io/leafcutter/
- CITATION:Li, Y.I., Knowles, D.A., Humphrey, J. et al. Annotation-free quantification of RNA splicing using LeafCutter. Nat Genet 50, 151–158 (2018). https://doi.org/10.1038/s41588-017-0004-9
