import sys
import os
import shutil
import pandas as pd
from format_citation import cite

def format_path_full(series):
    path_list=[]
    for i in series:
        if i!="":
            path_list.append(i)
    return "../docs/"+"_".join(path_list)+"_README.md"

def load_table_and_ref():
    source = "csv"
    tempfile= "../formatted_main_table.xlsx"
    dtype = {"PMID":"string","ADD_PREFIX":"string","ADD_SUFFIX":"string","USE_FIRST_AUTHOR":"string"}
    path = "../CTGCatalog.xlsx"
    if not os.path.isfile(tempfile):
        print("Loading data from main excel tables...")
        pop=pd.DataFrame()
        for sheet in ["Population_Genetics","Tools","Visualization","Sumstats","Proteomics","Metabolomics","Imaging"]:
            pop0 = pd.read_excel(path ,sheet_name=sheet,dtype=dtype)
            pop0["FIELD"] = sheet
            pop = pd.concat([pop,pop0],ignore_index=True)

        if source == "pubmed":
            import sys 
            sys.path.insert(0,"/home/yunye/work/github_projects/citationAPI/src")
            import citebiomed as cb
            print("Matching PMID from PUBMED....")
            query = cb.efetch_from_pubmed( list(pop["PMID"].dropna()) ,email="yunyehe.ctg@gmail.com")
            pop_pmid = pd.merge(pop,query,on="PMID",how="left")
            pop_pmid.to_excel(tempfile,index=None)
        
        else:
            ref = pd.read_csv("../References.csv",sep=",",dtype="string")
            ref = ref.dropna(subset="PMID").drop_duplicates(subset="PMID")
            ref = ref.rename(columns={
                "Title":"TITLE",
                "Journal":"ISO",
                "Full journal":"JOURNAL",
                "Publication year":"YEAR",
                "Volume":"VOLUME",
                "Pages":"PAGE",
                "Issue":"ISSUE",
                "Copyright":"COPYRIGHT",
                "Abstract":"ABSTRACT",
            })

            ref["FIRST_AUTHOR"] = ref["Authors"].str.split(",").str[0]
            ref["CITATION"] = ref.fillna("").apply(lambda x: cite(x),axis=1)

            pop_pmid = pd.merge(pop,ref,on="PMID",how="left")
            pop_pmid.loc[~pop_pmid["PMID"].isin(ref["PMID"]),"PMID"].dropna().drop_duplicates().to_csv("../not_in_lib.pmidlist",index=None,header=None) 
    else:
        pop_pmid = pd.read_excel(tempfile,dtype="string")

    folder_cols =["FIELD"]
    for col in pop_pmid.columns:
        if "FOLDER" in col:
            folder_cols.append(col)
    pop_pmid["PATH"] = pop_pmid[folder_cols].fillna("").apply(lambda x: format_path_full(x), axis=1)
    
    print(pop_pmid["PATH"].unique())
    return pop_pmid

def load_ref():
    source = "csv"
    tempfile= "../formatted_reference_table.xlsx"
    dtype = {"PMID":"string","ADD_PREFIX":"string","ADD_SUFFIX":"string","USE_FIRST_AUTHOR":"string"}
    path = "../CTGCatalog_reference.xlsx"
    if not os.path.isfile(tempfile):
        xl = pd.ExcelFile(path)
        print("Loading data from main excel tables...")
        for index, sheet_name in enumerate(xl.sheet_names):
            pop0 = pd.read_excel(path ,sheet_name=sheet_name,dtype=dtype)
            pop0["FIELD"] = sheet_name
            if index==0:
                pop = pop0
            else:
                pop = pd.concat([pop,pop0])

        if source == "pubmed":
            import sys 
            sys.path.insert(0,"/home/yunye/work/github_projects/citationAPI/src")
            import citebiomed as cb
            print("Matching PMID from PUBMED....")
            query = cb.efetch_from_pubmed( list(pop["PMID"].dropna()) ,email="yunyehe.ctg@gmail.com")
            pop_pmid = pd.merge(pop,query,on="PMID",how="left")
            pop_pmid.to_excel(tempfile,index=None)
        
        else:
            ref = pd.read_csv("../References.csv",sep=",",dtype="string")
            ref = ref.dropna(subset="PMID").drop_duplicates(subset="PMID")
            ref = ref.rename(columns={
                "Title":"TITLE",
                "Journal":"ISO",
                "Full journal":"JOURNAL",
                "Publication year":"YEAR",
                "Volume":"VOLUME",
                "Pages":"PAGE",
                "Issue":"ISSUE",
                "Copyright":"COPYRIGHT",
                "Abstract":"ABSTRACT",
            })

            ref["FIRST_AUTHOR"] = ref["Authors"].str.split(",").str[0]
            ref["CITATION"] = ref.fillna("").apply(lambda x: cite(x),axis=1)

            pop_pmid = pd.merge(pop,ref,on="PMID",how="left")
            pop_pmid.loc[~pop_pmid["PMID"].isin(ref["PMID"]),"PMID"].dropna().drop_duplicates().to_csv("../not_in_lib.pmidlist",index=None,header=None) 
    else:
        pop_pmid = pd.read_excel(tempfile,dtype="string")

    folder_cols =["FIELD"]
    for col in pop_pmid.columns:
        if "FOLDER" in col:
            folder_cols.append(col)
    pop_pmid["PATH"] = pop_pmid[folder_cols].fillna("").apply(lambda x: format_path_full(x), axis=1)
    
    print(pop_pmid["PATH"].unique())
    return pop_pmid