import sys
import os
import shutil
import pandas as pd
from format_citation import cite
from format_table import format_data
from format_table import format_data_sumstats
from format_table import format_string
from format_table import add_prefix_suffix_to_name
from format_table import format_main
from print_level import write_markdown

def configure_type(filename):
    type = "tools"
    if filename=="../docs/Sumstats_README.md" or filename=="../docs/Proteomics_Proteomics_README.md":
        type="sumstats"
    return type

def configure_table_columns(df_combined, filename):
    ## topic-specifc table
    if filename=="../docs/Sumstats_README.md":
        table_columns = ["NAME","MAIN_ANCESTRY"]
    elif filename=="../docs/Proteomics_Proteomics_README.md":
        table_columns = ["NAME","PLATFORM","YEAR","TITLE"]
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
        'MESH_MAJOR', 'MESH_MINOR', 'ABSTRACT', 'COPYRIGHT', 'DOI',"RELATED_BIOBANK","MAIN_ANCESTRY"]

    for path in pop_pmid["PATH"].unique():
        df_combined = pop_pmid.loc[pop_pmid["PATH"]==path,:]
        print(path, len(df_combined))
        overwrite_markdown(path, df_combined, output_items)