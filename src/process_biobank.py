import sys
import os
import shutil
import pandas as pd

def write_biobank():
    biobank_md_path = "../docs/Sumstats_Biobanks_Cohorts_README.md"

    df = pd.read_excel("../CTGCatalog.xlsx",sheet_name="Biobanks",dtype="string")
    df["NAME_FOR_TABLE"] = df["BIOBANK&COHORT"].str.strip().str.lower().str.replace('\s+','-',regex=True).str.replace('[^a-zA-Z0-9-]+','',regex=True).str.replace('[-]+','-',regex=True)
    df["Name"]= "[" + df["BIOBANK&COHORT"] + "](" + '#' + df["NAME_FOR_TABLE"]  +")"
    df["Link"]= "[Here](" +  df["URL"] +")"

    with open(biobank_md_path,"w") as file:
        file.write("# Biobanks & Cohorts\n\n")

    with open(biobank_md_path,"a") as file:
        file.write("This is an effort to collect the information on major biobanks or cohorts with genomic data around the world.\n\n")

    with open(biobank_md_path,"a") as file:
        file.write("## Summary Table\n\n")

    df.loc[:,["Name","CONTINENT","SAMPLE SIZE","Link"]].to_markdown(biobank_md_path,index=None, mode="a")

    with open(biobank_md_path,"a") as file:
        for continent in df["CONTINENT"].sort_values().unique():
            file.write("\n")
            file.write("\n")
            file.write("## {}".format(continent))
            for index, row in df.loc[df["CONTINENT"]==continent,:].sort_values(by=["BIOBANK&COHORT"]).iterrows():
                file.write("\n")
                file.write("\n")
                file.write("### {}\n\n".format(row["BIOBANK&COHORT"]))
                for item in df.columns:
                    if not pd.isna(row[item]):
                        if item == "CITATION":
                            for cite in row[item].strip().split("\n"):
                                file.write("- {} : {} \n ".format(item.strip(), cite.strip()))
                        else:
                            file.write("- {} : {} \n ".format(item.strip(), row[item].strip()))