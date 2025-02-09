import sys
import os
import shutil
import pandas as pd

def format_data(df_combined_in):

    df_combined = df_combined_in.copy()
    
    # fix name
    df_combined["NAME"] = df_combined["NAME"].str.strip().str.replace('\s+' , " ",regex=True)

    #try:
    if "ADD_PREFIX" in df_combined.columns and "ADD_SUFFIX" in df_combined.columns and "USE_FIRST_AUTHOR" in df_combined.columns: 
        df_combined[["ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR"]] = df_combined[["ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR"]].fillna("0")
        df_combined["NAME"] = df_combined[["NAME","ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR","TYPE","PMID","FIRST_AUTHOR"]].fillna("").apply(lambda x: add_prefix_suffix_to_name(x), axis=1 )
        #print("fixing names -----------------------------------------------")
    #except:
    #    pass

    # fix JOURNAL_INFO
    try:
        #df_combined.loc[df_combined["TYPE"]=="Review","NAME"] = "Review-" + df_combined.loc[df_combined["TYPE"]=="Review","FIRST_AUTHOR"]
        df_combined["JOURNAL_INFO"] =   df_combined[['JOURNAL', 'ISO', 'YEAR', 'VOLUME', 'ISSUE', 'PAGE']].apply(lambda x: format_string(x) ,axis=1)
        is_journal_info_empty = df_combined[['JOURNAL', 'ISO', 'YEAR', 'VOLUME', 'ISSUE', 'PAGE']].isna().all(axis=1)
        df_combined.loc[is_journal_info_empty, "JOURNAL_INFO"] = pd.NA
    except:
        pass

    # fix PUBMED_LINK
    is_pubmedid = ~df_combined["PMID"].isna()
    df_combined.loc[is_pubmedid, "PUBMED_LINK"] = "["+ df_combined.loc[is_pubmedid, "PMID"] + "](" + "https://pubmed.ncbi.nlm.nih.gov/" +  df_combined.loc[is_pubmedid, "PMID"] + ")"
    
    # fix URL
    # multiple urls
    is_url = ~df_combined["URL"].isna()
    df_combined.loc[is_url,"URL"]  = df_combined.loc[is_url,"URL"].apply(lambda x:fix_url(x))

    return df_combined

def format_data_sumstats(df_combined):
    is_not_na = ~df_combined["RELATED_BIOBANK"].isna()
    df_combined.loc[is_not_na, "RELATED_BIOBANK"] = "["+ df_combined.loc[is_not_na, "RELATED_BIOBANK"]  + "](" + "./Sumstats_Biobanks_Cohorts_README.md#" + df_combined.loc[is_not_na, "RELATED_BIOBANK"].str.replace('\s+',"-",regex=True).str.lower() + ")"
    return df_combined

def format_string(series):
    string = []
    for i in series:
        if i is not None:
            string.append(str(i))
    return " ; ".join(string)

def add_prefix_suffix_to_name(series):
    name = series["NAME"]
    prefix_i = series["ADD_PREFIX"]
    suffix_i = series["ADD_SUFFIX"]
    first_author_i = series["USE_FIRST_AUTHOR"]
    prefix = series["TYPE"]
    suffix= series["PMID"]
    first_author = series["FIRST_AUTHOR"] 

    name_string = "{}".format(name)

    if first_author_i == "1" :
            if len(first_author)>0:
                name_string = "{}".format(first_author)
    if prefix_i == "1" :
            if len(prefix) >0:
                name_string = "{}-{}".format(prefix, name_string)
    if suffix_i == "1":
            if len(suffix) >0:
                name_string = "{}-{}".format(name_string, suffix)
    return name_string

def fix_url(urls):
    url_list = urls.split()
    md_url_string=""
    for i in url_list:
         md_url_string+="[{}]({}) ".format(i,i)
    return md_url_string
     

def fix_citation(df_combined):
    if not df_combined["CITATION"].isna().all():
        df_combined.loc[df_combined["CITATION"].isna(),"CITATION"] = df_combined.loc[df_combined["CITATION"].isna(),"MANUAL_CITATION"].str.strip()
        df_combined["CITATION"] = df_combined["CITATION"].str.replace('\n','<br><br>')
    return df_combined

def fix_name_link(df_combined):
    df_combined["NAME_FOR_LINK"] = df_combined["NAME"].str.strip().str.lower().str.replace('\s+','-',regex=True).str.replace('[^a-zA-Z0-9-]+','',regex=True).str.replace('[-]+','-',regex=True)
    df_combined["TABLE_NAME"] = "[" +df_combined["NAME"] +"]"+"(#"+ df_combined["NAME_FOR_LINK"] + ")" 
    return df_combined

def fix_name_header(df_combined):
    df_combined = df_combined.rename(columns={"NAME":"_NAME"})
    df_combined = df_combined.rename(columns={"TABLE_NAME":"NAME"})
    return df_combined

def format_main(df_combined, type="tools"):
    #general
    df_combined = format_data(df_combined)
    
    #topic specific format
    if type=="sumstats":
        df_combined = format_data_sumstats(df_combined)

    #other 
    df_combined = fix_name_link(df_combined)
    df_combined = fix_name_header(df_combined)
    df_combined = fix_citation(df_combined)
    
    return df_combined