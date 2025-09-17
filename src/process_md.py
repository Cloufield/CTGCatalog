import sys
import os
import shutil
import pandas as pd
from format_table import format_main
from print_level import write_markdown

def configure_type(filename):
    type = "tools"
    if "Sumstats" in filename:
        type="sumstats"
    return type

def configure_table_columns(df_combined, filename):
    ## topic-specifc table
    if "Sumstats." in filename:
        table_columns = ["NAME","MAIN_ANCESTRY"]
    elif "Proteomics" in filename:
        table_columns = ["NAME","PLATFORM","YEAR","TITLE"]
    elif "Biobanks_" in filename:
        table_columns = ["NAME","CONTINENT","SAMPLE SIZE","URL"]
    else:
        table_columns = ["NAME","CITATION","YEAR"]
    
    sort_cols = ["NAME"]

    if "CATEGORY" in df_combined.columns:
        if not df_combined["CATEGORY"].isna().all():
            table_columns.insert(1,"CATEGORY")
            sort_cols.insert(0,"CATEGORY")
            df_combined["CATEGORY"] = df_combined["CATEGORY"].fillna("MISC")
    
    return table_columns, sort_cols

def overwrite_markdown(filename, df_combined, output_items):
    with open(filename,"w") as file:
        file.write("## Summary Table\n\n")
    
    #general format
    df_combined = format_main(df_combined, configure_type(filename))

    table_columns, sort_cols = configure_table_columns(df_combined, filename)
    
    to_output = df_combined.sort_values(by=sort_cols).loc[:,table_columns].fillna("NA")

 
    to_output.to_markdown(filename, index=None, mode="a")

    df_combined = df_combined.drop(columns=["NAME"])
    df_combined = df_combined.rename(columns={"_NAME":"NAME"})

    write_markdown(filename, df_combined, output_items)


###########################################################################################################################################################################################################################

def write_md(pop_pmid):
    output_items = ['NAME', 'PUBMED_LINK', 
       'SHORT NAME', 'FULL NAME', 'DESCRIPTION', 'URL', 
       'KEYWORDS', 'USE', 'PREPRINT_DOI', 'SERVER',"JOURNAL_INFO", 'TITLE', 'CITATION',
       'MESH_MAJOR', 'MESH_MINOR', 'ABSTRACT', 'COPYRIGHT', 'DOI',"RELATED_BIOBANK",
       "MAIN_ANCESTRY","SAMPLE SIZE","ANCESTRY",
       "ARRAY","WGS/WES","TRANSCRIPTOME","METABOLOME","PROTEOME","METHYLOME","METAGENOME","IMAGAING","DATA ACCESS",
       "ARROW_SUMMARY","AI_GENERATED"
       
       ]
    pop_pmid = add_path(pop_pmid)

    for path in pop_pmid["PATH"].unique():
        df_combined = pop_pmid.loc[pop_pmid["PATH"]==path,:]
        
        overwrite_markdown(path, df_combined, output_items)


def format_path_full(series):
    path_list=[]
    for i in series:
        if i!="":
            path_list.append(i)
    return "../docs/"+"_".join(path_list)+".md"

def add_path(df_combined):
    folder_cols =["SECTION","TOPIC","SUBTOPIC"]
    
    if "TOPIC" not in df_combined.columns:
        df_combined["TOPIC"]=""
    if "SUBTOPIC" not in df_combined.columns:
        df_combined["SUBTOPIC"]=""   
    
    # create a path 
    # SECTION [_TOPIC] [_SUBTOPIC]
    df_combined["PATH"] = df_combined[folder_cols].fillna("").apply(lambda x: format_path_full(x), axis=1)
    
    return df_combined