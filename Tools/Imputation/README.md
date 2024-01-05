# Contents
- Phasing & Imputation Tool
    - BEAGLE
    - Eagle
    - SHAPEIT
    - IMPUTE
    - Mach/minimac
    - fastPHASE
    - GLIMPSE
- Imputation of structural variants
    - 1KG SV imputation panel (long-read sequencing)
- Imputation of HLA
    - SNP2HLA
    - DEEP*HLA
    - CookHLA
    - HIBAG
- Imputation Panel
    - 1KG
    - TOPMED
    - HRC
    - RESHAPE
    - SEAD
- Imputation Server
    - Michigan
    - TOPMed
    - Sanger
    - Nyuwa
    - Westlake
    - CNGB Imputation Service

## Phasing & Imputation
### BEAGLE
- URL: [https://faculty.washington.edu/browning/beagle/beagle.html](https://faculty.washington.edu/browning/beagle/beagle.html)
- CITATION: (beagle) Browning, Sharon R., and Brian L. Browning. "Rapid and accurate haplotype phasing and missing-data inference for whole-genome association studies by use of localized haplotype clustering." The American Journal of Human Genetics 81.5 (2007): 1084-1097.
- CITATION: (beagle 4.1)Browning, Brian L., and Sharon R. Browning. "Genotype imputation with millions of reference samples." The American Journal of Human Genetics 98.1 (2016): 116-126.
- CITATION: (beagle 5.4 phasing) Browning, Brian L., et al. "Fast two-stage phasing of large-scale sequence data." The American Journal of Human Genetics 108.10 (2021): 1880-1890.
- CITATION: (beagle 5.4 imputation) Browning, Brian L., Ying Zhou, and Sharon R. Browning. "A one-penny imputed genome from next-generation reference panels." The American Journal of Human Genetics 103.3 (2018): 338-348.

### Eagle 
- URL:[https://alkesgroup.broadinstitute.org/Eagle/](https://alkesgroup.broadinstitute.org/Eagle/)
- CITATION:(EAGLE1) Loh, Po-Ru, Pier Francesco Palamara, and Alkes L. Price. "Fast and accurate long-range phasing in a UK Biobank cohort." Nature genetics 48.7 (2016): 811-816.
- CITATION:(EAGLE2) Loh, Po-Ru, et al. "Reference-based phasing using the Haplotype Reference Consortium panel." Nature genetics 48.11 (2016): 1443-1448.

### SHAPEIT
- URL:[https://odelaneau.github.io/shapeit4/](https://odelaneau.github.io/shapeit4/)
- URL:[https://jmarchini.org/shapeit3/](https://jmarchini.org/shapeit3/)
- URL:[https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html](https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html)
- CITATION:(SHAPEIT5) Hofmeister, R. J., Ribeiro, D. M., Rubinacci, S., & Delaneau, O. (2023). Accurate rare variant phasing of whole-genome and whole-exome sequencing data in the UK Biobank. Nature Genetics, 55(7), 1243-1249.
- CITATION:(SHAPEIT5) Hofmeister, R. J., Ribeiro, D. M., Rubinacci, S., & Delaneau, O. (2022). Accurate rare variant phasing of whole-genome and whole-exome sequencing data in the UK Biobank. bioRxiv, 2022-10.
- CITATION:(SHAPEIT4) Delaneau, Olivier, et al. "Accurate, scalable and integrative haplotype estimation." Nature communications 10.1 (2019): 1-10.
- CITATION:(SHAPEIT3) O'Connell, Jared, et al. "Haplotype estimation for biobank-scale data sets." Nature genetics 48.7 (2016): 817-820.
- CITATION:(SHAPEIT2) Delaneau, Olivier, Jean-Francois Zagury, and Jonathan Marchini. "Improved whole-chromosome phasing for disease and population genetic studies." Nature methods 10.1 (2013): 5-6.
- CITATION:(SHAPEIT1) Delaneau, Olivier, Jonathan Marchini, and Jean-François Zagury. "A linear complexity phasing method for thousands of genomes." Nature methods 9.2 (2012): 179-181.

### IMPUTE
- URL: [https://jmarchini.org/software/](https://jmarchini.org/software/)
- CITATION: (IMPUTE) Marchini, Jonathan, et al. "A new multipoint method for genome-wide association studies by imputation of genotypes." Nature genetics 39.7 (2007): 906-913.
- CITATION: (IMPUTE2) Howie, Bryan N., Peter Donnelly, and Jonathan Marchini. "A flexible and accurate genotype imputation method for the next generation of genome-wide association studies." PLoS genetics 5.6 (2009): e1000529.
- CITATION: (IMPUTE4) Bycroft, Clare, et al. "The UK Biobank resource with deep phenotyping and genomic data." Nature 562.7726 (2018): 203-209.
- CITATION: (IMPUTE5) Rubinacci, Simone, Olivier Delaneau, and Jonathan Marchini. "Genotype imputation using the positional burrows wheeler transform." PLoS genetics 16.11 (2020): e1009049.

### MACH / minimach
- URL: [http://csg.sph.umich.edu/abecasis/MaCH/index.html](http://csg.sph.umich.edu/abecasis/MaCH/index.html)
- URL: [https://genome.sph.umich.edu/wiki/Minimac](https://genome.sph.umich.edu/wiki/Minimac)
- URL: [https://genome.sph.umich.edu/wiki/Minimac2](https://genome.sph.umich.edu/wiki/Minimac2)
- URL: [https://genome.sph.umich.edu/wiki/Minimac3](https://genome.sph.umich.edu/wiki/Minimac3)
- URL: [https://genome.sph.umich.edu/wiki/Minimac4](https://genome.sph.umich.edu/wiki/Minimac4)
- CITATION: (MACH) Li, Yun, et al. "MaCH: using sequence and genotype data to estimate haplotypes and unobserved genotypes." Genetic epidemiology 34.8 (2010): 816-834.
- CITATION: (pre-phasing, minimac) Howie, Bryan, et al. "Fast and accurate genotype imputation in genome-wide association studies through pre-phasing." Nature genetics 44.8 (2012): 955-959.
- CITATION: (minimac2) Fuchsberger, Christian, Gonçalo R. Abecasis, and David A. Hinds. "minimac2: faster genotype imputation." Bioinformatics 31.5 (2015): 782-784.
- CITATION: (minimac3) Das, Sayantan, et al. "Next-generation genotype imputation service and methods." Nature genetics 48.10 (2016): 1284-1287.

### fastPHASE
- URL: [http://scheet.org/software.html](http://scheet.org/software.html)
- CITATION:Scheet, Paul, and Matthew Stephens. "A fast and flexible statistical model for large-scale population genotype data: applications to inferring missing genotypes and haplotypic phase." The American Journal of Human Genetics 78.4 (2006): 629-644.

### GLIMPSE
- FULL NAME: Genotype Likelihoods IMputation and PhaSing mEthod
- SHORT NAME:  GLIMPSE
- URL:[https://odelaneau.github.io/GLIMPSE/](https://odelaneau.github.io/GLIMPSE/)
- DESCRIPTION: GLIMPSE is a phasing and imputation method for large-scale low-coverage sequencing studies.
- CITATION: Rubinacci, S., Ribeiro, D. M., Hofmeister, R. J., & Delaneau, O. (2021). Efficient phasing and imputation of low-coverage sequencing data using large reference panels. Nature Genetics, 53(1), 120-126.
- CITATION: (using GLIMPSE for ancient DNA) Sousa da Mota, B., Rubinacci, S., Cruz Dávalos, D. I., G. Amorim, C. E., Sikora, M., Johannsen, N. N., ... & Delaneau, O. (2023). Imputation of ancient human genomes. Nature Communications, 14(1), 3660.

## Imputation of structural variants
### 1KG SV imputation panel (long-read sequencing)
- CITATION: Noyvert, B., Erzurumluoglu, A. M., Drichel, D., Omland, S., Andlauer, T. F., Mueller, S., ... & Ding, Z. (2023). Imputation of structural variants using a multi-ancestry long-read sequencing panel enables identification of disease associations. medRxiv, 2023-12.

## Imputation of HLA

### SNP2HLA

- URL: http://software.broadinstitute.org/mpg/snp2hla/
- CITATION:Jia, X., Han, B., Onengut-Gumuscu, S., Chen, W. M., Concannon, P. J., Rich, S. S., ... & de Bakker, P. I. (2013). Imputing amino acid polymorphisms in human leukocyte antigens. PloS one, 8(6), e64683.

### DEEP*HLA

- URL: https://github.com/tatsuhikonaito/DEEP-HLA
- CITATION: Naito, T., Suzuki, K., Hirata, J., Kamatani, Y., Matsuda, K., Toda, T., & Okada, Y. (2021). A deep learning method for HLA imputation and trans-ethnic MHC fine-mapping of type 1 diabetes. Nature communications, 12(1), 1639.

### CookHLA

- URL: https://github.com/WansonChoi/CookHLA
- CITATION: Cook, S., Choi, W., Lim, H., Luo, Y., Kim, K., Jia, X., ... & Han, B. (2021). Accurate imputation of human leukocyte antigens with CookHLA. Nature Communications, 12(1), 1264.

### HIBAG

- URL: https://github.com/zhengxwen/HIBAG
- CITATION: Zheng, X., Shen, J., Cox, C., Wakefield, J. C., Ehm, M. G., Nelson, M. R., & Weir, B. S. (2014). HIBAG—HLA genotype imputation with attribute bagging. The pharmacogenomics journal, 14(2), 192-200.

### review
- CITATION: 

## Imputation panel

### 1000 Genomes
- CITATION: 1000 Genomes Project Consortium. "A global reference for human genetic variation." Nature 526.7571 (2015): 68.
### HRC
- CITATION: the Haplotype Reference Consortium. "A reference panel of 64,976 haplotypes for genotype imputation". Nature genetics, 2016, 48(10): 1279-1283.
### TOPMED
- CITATION: Taliun, Daniel, et al. "Sequencing of 53,831 diverse genomes from the NHLBI TOPMed Program." Nature 590.7845 (2021): 290-299.

### HGDP+1kGP
- SHORT NAME: HGDP+1kGP
- FULL NAME:Human Genome Diversity Project + 1000 Genomes project
- URL: https://gnomad.broadinstitute.org/news/2020-10-gnomad-v3-1-new-content-methods-annotations-and-data-availability/#the-gnomad-hgdp-and-1000-genomes-callset
- CITATION: Koenig, Z., Yohannes, M. T., Nkambule, L. L., Goodrich, J. K., Kim, H. A., Zhao, X., ... & Martin, A. R. (2023). A harmonized public resource of deeply sequenced diverse human genomes. bioRxiv, 2023-01.

### RESHAPE
- SHORT NAME : RESHAPE
- FULL NAME : REcombine and Share HAPlotypEs
- URL : [https://github.com/TheoCavinato/RESHAPE](https://github.com/TheoCavinato/RESHAPE)
- DESCRIPTION: RESHAPE removes sample-level genetic information from a reference panel to create a synthetic reference panel. By providing it with a genetic map and the VCF/BCF of a reference panel, RESHAPE outputs a VCF/BCF of the same size where each haplotypes corresponds to a mosaic of the original haplotypes of the reference panel.
- CITATION: Cavinato, T., Rubinacci, S., Malaspinas, A. S., & Delaneau, O. (2023). A resampling-based approach to share reference panels. bioRxiv, 2023-04.

### South and East Asian Reference Database (SEAD) reference panel
- URL: [https://imputationserver.westlake.edu.cn/](https://imputationserver.westlake.edu.cn/)
- CITATION: Yang, M. Y., Zhong, J. D., Li, X., Bai, W. Y., Yuan, C. D., Qiu, M. C., ... & Zheng, H. F. (2023). SEAD: an augmented reference panel with 22,134 haplotypes boosts the rare variants imputation and GWAS analysis in Asian population. medRxiv, 2023-12.

## Imputation Server
### TOPMED
- URL: [https://imputation.biodatacatalyst.nhlbi.nih.gov/#!](https://imputation.biodatacatalyst.nhlbi.nih.gov/#!)
- CITATION:Taliun, D., Harris, D. N., Kessler, M. D., Carlson, J., Szpiech, Z. A., Torres, R., ... & Stilp, A. M. (2021). Sequencing of 53,831 diverse genomes from the NHLBI TOPMed Program. Nature, 590(7845), 290-299.

### Michigan
- URL :[https://imputationserver.sph.umich.edu/index.html#!](https://imputationserver.sph.umich.edu/index.html#!)
- URL: [https://imputationserver.readthedocs.io/en/latest/](https://imputationserver.readthedocs.io/en/latest/)
- CITATION: Das, Sayantan, et al. "Next-generation genotype imputation service and methods." Nature genetics 48.10 (2016): 1284-1287.

### NyuWa 
- URL: [http://bigdata.ibp.ac.cn/refpanel/getstarted.php](http://bigdata.ibp.ac.cn/refpanel/getstarted.php)
- CITATION: Zhang, P., Luo, H., Li, Y., Wang, Y., Wang, J., Zheng, Y., ... & Han100K Initiative. (2021). NyuWa Genome resource: a deep whole-genome sequencing-based variation profile and reference panel for the Chinese population. Cell Reports, 37(7), 110017.

### Westlake
- URL: [https://imputationserver.westlake.edu.cn/](https://imputationserver.westlake.edu.cn/)
- CITATION: Cong, P. K., Bai, W. Y., Li, J. C., Yang, M. Y., Khederzadeh, S., Gai, S. R., ... & Zheng, H. F. (2022). Genomic analyses of 10,376 individuals in the Westlake BioBank for Chinese (WBBC) pilot project. Nature Communications, 13(1), 1-15.
  
### CNGB Imputation Service
- URL: [https://db.cngb.org/imputation/](https://db.cngb.org/imputation/)
- CITATION: Yu, C., Lan, X., Tao, Y., Guo, Y., Sun, D., Qian, P., ... & Li, L. (2022). A High-resolution Haplotype-resolved Reference Panel Constructed from the China Kadoorie Biobank Study. medRxiv, 2022-12.

### Sanger
- URL: [https://imputation.sanger.ac.uk/](https://imputation.sanger.ac.uk/)
- CITATION: "A reference panel of 64,976 haplotypes for genotype imputation." Nature genetics 48, no. 10 (2016): 1279-1283.

## Reviews
- CITATION: Marchini, Jonathan, and Bryan Howie. "Genotype imputation for genome-wide association studies." Nature Reviews Genetics 11.7 (2010): 499-511.
- CITATION: Li, Yun, et al. "Genotype imputation." Annual review of genomics and human genetics 10 (2009): 387.
- CITATION: Das, Sayantan, Gonçalo R. Abecasis, and Brian L. Browning. "Genotype imputation from large reference panels." Annu Rev Genomics Hum Genet 19.1 (2018): 73-96.
