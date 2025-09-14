import sys
import os
import shutil
import pandas as pd

##########################################################################################################################################################################################################################

def write_homepage():
    
    ############################################################################################################################################################################################################################
    about_text = "**[Complex Trait Genetics Catalog](https://cloufield.github.io/CTGCatalog/)** : A collection of commonly used resources for analysis in complex trait genetics, including reference data, publicly sumstats and commonly used tools. All entries in this repo are manually curated."
    with open("../docs/index.md","w") as homepage:
        homepage.write(about_text)

    ###########################################################################################################################################################################################################################        
    combined_df = pd.DataFrame()
    for dirname in ["Biobanks"]: 
        combined_df = pd.read_excel("../CTGCatalog.xlsx",sheet_name = dirname, dtype={"PMID":"string"})

    counts = combined_df[["NAME","CONTINENT"]].groupby(["CONTINENT"]).count().reset_index()
    counts = counts.rename(columns={"CONTINENT":"Location","NAME":"Count"})

    with open("../docs/index.md","a") as file:
        file.write("\n\n## Biobanks and cohorts \n\n")

    with open("../docs/index.md","a") as file:
        file.write("\n\n")
    
    counts.to_markdown("../docs/index.md",index=None, mode="a")
    
    with open("../docs/index.md","a") as file:
        file.write("\n\n")
#
    ############################################################################################################################################################################################################################        
    combined_df = pd.DataFrame()
    for dirname in ["Sumstats","Proteomics","Imaging"]: 
        raw_dir = pd.read_excel("../CTGCatalog.xlsx",sheet_name = dirname, dtype={"PMID":"string"})
        combined_df = pd.concat([combined_df, raw_dir],ignore_index=True)
    
    combined_df["CATEGORY"] = combined_df["CATEGORY"].fillna("MISC")
    counts = combined_df[["TOPIC","NAME","CATEGORY"]].groupby(["TOPIC","CATEGORY"]).count().reset_index()
    counts = counts.rename(columns={"TOPIC":"Field","NAME":"Count","CATEGORY":"Category"})

    with open("../docs/index.md","a") as file:
        file.write("## Sumstats \n\n")

    with open("../docs/index.md","a") as file:
        file.write("\n\n")
    
    counts.to_markdown("../docs/index.md",index=None, mode="a")
    
    with open("../docs/index.md","a") as file:
        file.write("\n\n")
    ###########################################################################################################################################################################################################################
    combined_df = pd.DataFrame()
    for dirname in ["Tools"]: 
        raw_dir = pd.read_excel("../CTGCatalog.xlsx",sheet_name = dirname, dtype={"PMID":"string"})
        combined_df = pd.concat([combined_df, raw_dir],ignore_index=True)
        # top page
        #main_file = "../docs/"+dirname+"_README.md"
        #shutil.copyfile("../"+dirname+"/README.md", main_file)
    
    combined_df["CATEGORY"] = combined_df["CATEGORY"].fillna("MISC")
    counts = combined_df[["TOPIC","NAME","CATEGORY"]].groupby(["TOPIC","CATEGORY"]).count().reset_index()
    counts = counts.rename(columns={"TOPIC":"Field","NAME":"Count","CATEGORY":"Category"})

    with open("../docs/index.md","a") as file:
        file.write("## Tools \n\n")

    with open("../docs/index.md","a") as file:
        file.write("\n\n")
    
    counts.to_markdown("../docs/index.md",index=None, mode="a")
    
    with open("../docs/index.md","a") as file:
        file.write("\n\n")
#
    ###########################################################################################################################################################################################################################

    ###########################################################################################################################################################################################################################
    with open("../docs/index.md","a") as file:
        file.write("\n## About\n")
        file.write("\nFor more Complex Trait Genomics contents, please check [https://gwaslab.com/](https://gwaslab.com/)\n")
        file.write("\nContact : gwaslab@gmail.com\n")
