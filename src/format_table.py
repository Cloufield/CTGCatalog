import sys
import os
import shutil
import pandas as pd
from load_data import load_biobanks

def fix_journal_info(df_combined):
    # fix JOURNAL_INFO
    try:
        #df_combined.loc[df_combined["TYPE"]=="Review","NAME"] = "Review-" + df_combined.loc[df_combined["TYPE"]=="Review","FIRST_AUTHOR"]
        df_combined["JOURNAL_INFO"] =   df_combined[['JOURNAL', 'ISO', 'YEAR', 'VOLUME', 'ISSUE', 'PAGE']].apply(lambda x: format_string(x) ,axis=1)
        is_journal_info_empty = df_combined[['JOURNAL', 'ISO', 'YEAR', 'VOLUME', 'ISSUE', 'PAGE']].isna().all(axis=1)
        df_combined.loc[is_journal_info_empty, "JOURNAL_INFO"] = pd.NA
    except:
        pass
    return df_combined

def fix_prefix_suffix(df_combined):
    if "ADD_PREFIX" in df_combined.columns and "ADD_SUFFIX" in df_combined.columns and "USE_FIRST_AUTHOR" in df_combined.columns: 
        df_combined[["ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR"]] = df_combined[["ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR"]].fillna("0")
        df_combined["NAME"] = df_combined[["NAME","ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR","TYPE","PMID","FIRST_AUTHOR"]].fillna("").apply(lambda x: add_prefix_suffix_to_name(x), axis=1 )
    return df_combined

def fix_name(df_combined):
    # fix name
    df_combined["NAME"] = df_combined["NAME"].str.strip().str.replace('\s+' , " ",regex=True)
    return df_combined

def fix_pubmed_id(df_combined):
    # fix PUBMED_LINK
    is_pubmedid = ~df_combined["PMID"].isna()
    df_combined.loc[is_pubmedid, "PUBMED_LINK"] = "["+ df_combined.loc[is_pubmedid, "PMID"] + "](" + "https://pubmed.ncbi.nlm.nih.gov/" +  df_combined.loc[is_pubmedid, "PMID"] + ")"
    return df_combined



def add_related_biobanks(biobanks, biobank_to_topic):
    biobanks_list = biobanks.split(",")
    md_url_string=[]
    for i in biobanks_list:
         lowered_strpped_key = i.strip().lower()
         if lowered_strpped_key in biobank_to_topic.keys():
            formatted_i = "-".join(lowered_strpped_key.split()) 
            md_url_string.append("[{}](./Biobanks_{}.md#{}) ".format(i,  biobank_to_topic[lowered_strpped_key]["TOPIC"],formatted_i ))                
    return ",".join(md_url_string)    

def format_related_biobanks(df_combined):
    is_not_na = ~df_combined["RELATED_BIOBANK"].isna()
    
    biobanks = load_biobanks()
    biobanks["NAME"] = biobanks["NAME"].str.strip().str.lower()

    biobanks = biobanks.rename(columns={"NAME":"RELATED_BIOBANK"})[["RELATED_BIOBANK","TOPIC"]].set_index("RELATED_BIOBANK")
    
    biobank_to_topic = biobanks.to_dict(orient="index")

    df_combined.loc[is_not_na,"RELATED_BIOBANK"]  = df_combined.loc[is_not_na,"RELATED_BIOBANK"].apply(lambda x:add_related_biobanks(x, biobank_to_topic)) 
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

def fix_url_single(urls):
    url_list = urls.split()
    md_url_string=[]
    for i in url_list:
         md_url_string.append("[{}]({}) ".format(i,i))
    return ",".join(md_url_string)   

def fix_url(df_combined):
    # fix URL
    # multiple urls
    is_url = ~df_combined["URL"].isna()
    df_combined.loc[is_url,"URL"]  = df_combined.loc[is_url,"URL"].apply(lambda x:fix_url_single(x)) 
    return df_combined    

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
    df_combined = df_combined.copy()

    df_combined = fix_journal_info(df_combined)
    df_combined = fix_prefix_suffix(df_combined)
    df_combined = fix_name(df_combined)
    df_combined = fix_pubmed_id(df_combined)
    df_combined = fix_url(df_combined)
    #topic specific format
    if type=="sumstats":
        df_combined = format_related_biobanks(df_combined)

    #other 
    df_combined = fix_name_link(df_combined)
    df_combined = fix_name_header(df_combined)
    df_combined = fix_citation(df_combined)
    
    return df_combined