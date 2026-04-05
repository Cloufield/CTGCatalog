import sys
import os
import shutil
import pandas as pd
from load_data import load_biobanks

def fix_prefix_suffix(df_combined):
    if "ADD_PREFIX" in df_combined.columns and "ADD_SUFFIX" in df_combined.columns and "USE_FIRST_AUTHOR" in df_combined.columns: 
        df_combined[["ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR"]] = df_combined[["ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR"]].fillna("0")
        df_combined["NAME"] = df_combined[["NAME","ADD_PREFIX","ADD_SUFFIX","USE_FIRST_AUTHOR","TYPE","PMID","FIRST_AUTHOR"]].fillna("").apply(lambda x: add_prefix_suffix_to_name(x), axis=1 )
    return df_combined

def fix_name(df_combined):
    # fix name
    df_combined["NAME"] = df_combined["NAME"].str.strip().str.replace(r"\s+", " ", regex=True)
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
            # Sibling pages live at /Sumstats_* / etc.; ./Biobanks_*.md would wrongly resolve to /Sumstats_*/Biobanks_*.md
            topic = biobank_to_topic[lowered_strpped_key]["TOPIC"]
            label = biobank_to_topic[lowered_strpped_key]["NAME"]
            md_url_string.append(
                "[{}](../Biobanks_{}/#{}) ".format(label, topic, formatted_i)
            )
    return ",".join(md_url_string)


def format_related_biobanks(df_combined):
    is_not_na = ~df_combined["RELATED_BIOBANK"].isna()
    if not is_not_na.any():
        return df_combined

    biobanks = load_biobanks()
    if biobanks.empty:
        return df_combined

    biobanks = biobanks.copy()
    biobanks["NAME"] = biobanks["NAME"].str.strip()
    biobanks["_key"] = biobanks["NAME"].str.lower()
    biobanks = biobanks.set_index("_key")[["NAME", "TOPIC"]]

    biobank_to_topic = biobanks.to_dict(orient="index")

    df_combined.loc[is_not_na,"RELATED_BIOBANK"]  = df_combined.loc[is_not_na,"RELATED_BIOBANK"].apply(lambda x:add_related_biobanks(x, biobank_to_topic)) 
    return df_combined


def _catalog_bool_flag(v) -> bool:
    """True for JSON/DataFrame 1, 1.0, or string '1'; False for 0, NaN, blank."""
    if v is None:
        return False
    try:
        if pd.isna(v):
            return False
    except TypeError:
        pass
    try:
        return float(v) == 1.0
    except (TypeError, ValueError):
        return str(v).strip() in ("1", "1.0")


def add_prefix_suffix_to_name(series):
    name = series["NAME"]
    prefix_i = series["ADD_PREFIX"]
    suffix_i = series["ADD_SUFFIX"]
    first_author_i = series["USE_FIRST_AUTHOR"]
    prefix = series["TYPE"]
    suffix= series["PMID"]
    first_author = series["FIRST_AUTHOR"] 

    name_string = "{}".format(name)

    if _catalog_bool_flag(first_author_i):
        fa = str(first_author).strip()
        if fa:
            name_string = "{}, et al".format(fa)
    if _catalog_bool_flag(prefix_i):
        if len(prefix) > 0:
            name_string = "{}-{}".format(prefix, name_string)
    if _catalog_bool_flag(suffix_i):
        if len(suffix) > 0:
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
    if "CITATION" not in df_combined.columns:
        df_combined["CITATION"] = pd.NA
    # Only use explicit CITATION from JSON (PubMed sync or hand-authored). Do not
    # fabricate from other fields and do not promote MANUAL_CITATION here.
    cit = df_combined["CITATION"].astype("string")
    blank = cit.isna() | (cit.str.strip() == "")
    df_combined["CITATION"] = cit.mask(blank, pd.NA)
    has_cit = df_combined["CITATION"].notna()
    df_combined.loc[has_cit, "CITATION"] = df_combined.loc[
        has_cit, "CITATION"
    ].astype(str).str.replace("\n", "<br><br>", regex=False)
    return df_combined

def fix_name_link(df_combined):
    df_combined["NAME_FOR_LINK"] = (
        df_combined["NAME"]
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "-", regex=True)
        .str.replace(r"[^a-zA-Z0-9-]+", "", regex=True)
        .str.replace(r"[-]+", "-", regex=True)
    )
    df_combined["TABLE_NAME"] = "[" +df_combined["NAME"] +"]"+"(#"+ df_combined["NAME_FOR_LINK"] + ")" 
    return df_combined

def fix_name_header(df_combined):
    df_combined = df_combined.rename(columns={"NAME":"_NAME"})
    df_combined = df_combined.rename(columns={"TABLE_NAME":"NAME"})
    return df_combined

def format_main(df_combined, type="tools"):
    df_combined = df_combined.copy()

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