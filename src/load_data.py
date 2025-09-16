import sys
import os
import shutil
import pandas as pd
from format_citation import cite

def load_table_and_ref():
    source = "csv"
    tempfile= "../formatted_main_table.xlsx"
    dtype = {"PMID":"string","ADD_PREFIX":"string","ADD_SUFFIX":"string","USE_FIRST_AUTHOR":"string"}
    
    
    paths = ["../CTGCatalog.xlsx","../CTGCatalog_reference.xlsx"] 
    sheets=[
        ["Biobanks","Tools","Sumstats","Proteomics","Metabolomics","Imaging","Single_Cell"],
        ["Genome","Gene","Variant","Phenotype","Annotation","Epigenetics","Transcriptome","LD","Cell","Protein"]
    ]


    if not os.path.isfile(tempfile):
        print("Loading data from main excel tables...")
        pop=pd.DataFrame()
        for i, path in enumerate(paths):
            for sheet in sheets[i]:
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
    
    for i in ["SECTION","TOPIC","SUBTOPIC"]:
        pop_pmid[i] = pop_pmid[i].str.replace("\\s+","_",regex=True)
        pop_pmid[i] = pop_pmid[i].str.replace("-","_",regex=True)

    return pop_pmid

def load_biobanks():
    df = pd.read_excel("../CTGCatalog.xlsx",sheet_name="Biobanks")
    return df