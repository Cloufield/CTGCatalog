import sys
import os
import shutil
import pandas as pd

#######################################################################################################################################################################################################
shutil.copyfile("./README.md", "./docs/index.md")


biobank_md_path = "./docs/Sumstats_Biobanks_Cohorts_README.md"

df = pd.read_excel("CTGCatalog.xlsx",sheet_name="Biobanks",dtype="string")
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


biobank_header = '''

### Sumstats and Biobanks/Cohorts

'''

df = pd.read_excel("CTGCatalog.xlsx",sheet_name="Biobanks",dtype="string")

with open("./docs/index.md","a") as homepage:
    homepage.write(biobank_header)
    single_line = "- {} : {}\n".format("[Biobanks/Cohorts](Sumstats_Biobanks_Cohorts_README.md)", len(df))
    homepage.write(single_line)
    
    for sheet in ["Sumstats","Proteomics"]:
        df = pd.read_excel("CTGCatalog.xlsx",sheet_name=sheet,dtype={"PMID":"string"})
        type_dir = df.groupby("TYPE")["NAME"].count()
        string_list=[]
        for key,value in type_dir.items():
            type_string = "{} - {}".format(key,value)
            string_list.append(type_string)
        type_line = " , ".join(string_list)
        key = "[{}]({}_README.md)".format(sheet, sheet)
        single_line = "- {} : {}\n".format(key, type_line)
        homepage.write(single_line)

#######################################################################################################################################################################################################


##################################################################################################################################################################################################################
part1='''site_name: CTGCatalog
site_author: HE Yunye
repo_name: 'GitHub'
repo_url: https://github.com/Cloufield/CTGCatalog/
edit_uri: ""
copyright: "CTGCatalog is licensed under the MIT license"

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.top
    - search.highlight
    - search.suggest
    - search.share
  font:
    code: Roboto Mono
    text: Roboto
  palette:
    primary: blue
    accent: blue
  logo:
    assets/logo.png
  favicon:
    assets/logo.png

extra_css:
  - stylesheets/extra.css

markdown_extensions:
  - toc:
      toc_depth: 3
  - admonition
  - tables
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.arithmatex:
      generic: true

extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
  - https://unpkg.com/tablesort@5.3.0/dist/tablesort.min.js
  - javascripts/tablesort.js

plugins:
  - search
  - mkdocs-jupyter
'''

##################################################################################################################################################################################################################
def format_path(series):
    path_list=[]
    for i in series:
        if i!="":
            path_list.append(i)
    return "_".join(path_list)

def format_level(series):
    level = 1
    for i in series:
        if i!="":
            level+=1
    return level

part2="nav: \n    - Home : index.md\n"
part2+='''    - Sumstats:
      - Sumstats: Sumstats_README.md
      - Biobanks_Cohorts: Sumstats_Biobanks_Cohorts_README.md
      - Metabolomics: Metabolomics_Metabolomics_README.md
      - Proteomics: Proteomics_Proteomics_README.md\n'''

for dirname in ["Tools","Visualization","Population_Genetics" ]: 
    main_file = "./docs/"+dirname+"_README.md"
    shutil.copyfile("./"+dirname+"/README.md", main_file)
    raw_dir = pd.read_excel("CTGCatalog.xlsx",sheet_name = dirname, dtype={"PMID":"string"})
    folder_cols =[]
    
    for col in raw_dir.columns:
        if "FOLDER" in col:
             folder_cols.append(col)
    
    raw_dir.loc[:, folder_cols ] = raw_dir.loc[:, folder_cols ].fillna("")
    raw_dir["TYPE"] = raw_dir["TYPE"].fillna("MISC")
    raw_dir["PATH"] = raw_dir[folder_cols].apply(lambda x: format_path(x), axis=1)

    df_dir = raw_dir.loc[:, folder_cols].dropna(subset=folder_cols[0]).fillna("")
    print(folder_cols)
    path_df = df_dir.groupby(folder_cols).count().reset_index()
    path_df["PATH"] = path_df[folder_cols].apply(lambda x: format_path(x), axis=1)
    path_df["LEVEL"] = path_df[folder_cols].apply(lambda x: format_level(x), axis=1)
    
    level_root_dic ={col:list() for col in folder_cols}
    for index in range(len(folder_cols)):
        if index< len(folder_cols)-1:
            level_count = path_df.groupby(folder_cols[index])["PATH"].count()
            level_root_dic[folder_cols[index]]+=list(level_count[level_count>1].index.values)
    

    # ###################################################
    with open("./docs/index.md","a") as homepage:

        with open(main_file,"a") as file:
            file.write("\n\n")
            file.write("## {} - {} \n".format("Contents",dirname))
            homepage.write("### {} - {} \n".format("Contents",dirname))
            file.write("\n")

            for index, row in path_df.iterrows():

                type_dir = raw_dir.loc[raw_dir["PATH"]==row["PATH"],:].groupby("TYPE")["NAME"].count()
                string_list=[]
                for key,value in type_dir.items():
                    type_string = "{} - {}".format(key,value)
                    string_list.append(type_string)
                type_line = " , ".join(string_list)

                spaces = " " * 2 * (row["LEVEL"]-1)
                col = "FOLDER_{}".format(row["LEVEL"]-1)
                string = row[col]
                link_string = "{}_{}_README.md".format(dirname, row["PATH"])
                
                key = "[{}]({})".format(string, link_string)
                single_line = "{}- {} : {}\n".format( spaces ,key, type_line)
                file.write(single_line)
                homepage.write(single_line)
        
    
    #tab############################################
    spaces = " " * 2 * (1+ 1)
    key = dirname
    value = "{}_README.md".format(dirname)
    single_line = "{}- {}: \n".format( spaces ,key)
    part2+= single_line
    
    #tab_apge############################################
    spaces = " " * 2 * (1+ 2)
    single_line = "{}- {}: {} \n".format( spaces ,key, value)
    part2+= single_line
    
    for index, row in path_df.iterrows():

        spaces = " " * 2 * (1+ row["LEVEL"])
        col = "FOLDER_{}".format(row["LEVEL"]-1)
        key = row[col]
        value = "{}_{}_README.md".format(dirname, row["PATH"])
        if row["PATH"] in level_root_dic[col]:
            single_line = "{}- {}:\n".format(spaces ,key)
            part2+= single_line
            spaces = " " * 2 * (1+ row["LEVEL"]+1)
            single_line = "{}- {}: {}\n".format(spaces ,key, value)
            part2+= single_line
        else:
            single_line = "{}- {}: {}\n".format( spaces ,key, value)
            part2+= single_line
##################################################################################################################################################################################################################
with open("./mkdocs.yml",mode="w") as file:
    file.write(part1+part2)

##################################################################################################################################################################################################################
about_text = '''

## About

For more Complex Trait Genomics contents, please check [https://gwaslab.com/](https://gwaslab.com/)

Contact : gwaslab@gmail.com

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fcloufield.github.io%2FCTGCatalog%2F&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Daily%2FTotal+views&edge_flat=false)](https://hits.seeyoufarm.com)'''

with open("./docs/index.md","a") as homepage:
    homepage.write(about_text)
###############################################################################################################################################################################################################

def format_string(series):
    string = []
    for i in series:
        if i is not None:
            string.append(str(i))
    return " ; ".join(string)
    
def format_data(df_combined_in):

    df_combined = df_combined_in.copy()
    df_combined["NAME"] = df_combined["NAME"].str.strip().str.replace('\s+' , " ",regex=True)

    df_combined.loc[df_combined["CITATION"].isna(),"CITATION"] = df_combined.loc[df_combined["CITATION"].isna(),"MANUAL_CITATION"]
    
    df_combined.loc[df_combined["TYPE"]=="Review","NAME"] = "Review-" + df_combined.loc[df_combined["TYPE"]=="Review","FIRST_AUTHOR"]
    
    df_combined["JOURNAL_INFO"] =   df_combined[['JOURNAL', 'ISO', 'YEAR', 'VOLUME', 'ISSUE', 'PAGE']].apply(lambda x: format_string(x) ,axis=1)
    is_journal_info_empty = df_combined[['JOURNAL', 'ISO', 'YEAR', 'VOLUME', 'ISSUE', 'PAGE']].isna().all(axis=1)
    df_combined.loc[is_journal_info_empty, "JOURNAL_INFO"] = pd.NA
    
    is_pubmedid = ~df_combined["PMID"].isna()
    df_combined.loc[is_pubmedid, "PUBMED_LINK"] = "["+ df_combined.loc[is_pubmedid, "PMID"] + "](" + "https://pubmed.ncbi.nlm.nih.gov/" +  df_combined.loc[is_pubmedid, "PMID"] + ")"

    is_url = ~df_combined["URL"].isna()
    df_combined.loc[is_url,"URL"] = "["+ df_combined.loc[is_url, "URL"] + "](" + df_combined.loc[is_url, "URL"] + ")"

    return df_combined

def format_data_sumstats(df_combined):
    is_not_na = ~df_combined["RELATED_BIOBANK"].isna()
    df_combined.loc[is_not_na, "RELATED_BIOBANK"] = "["+ df_combined.loc[is_not_na, "RELATED_BIOBANK"]  + "](" + "./Sumstats_Biobanks_Cohorts_README.md#" + df_combined.loc[is_not_na, "RELATED_BIOBANK"].str.replace('\s+',"-",regex=True).str.lower() + ")"
    return df_combined

def overwrite_markdown(filename, df_combined, output_items):
    with open(filename,"w") as file:
        file.write("## Summary Table\n\n")
    
    #general format
    df_combined = format_data(df_combined)
    #topic specific format
    if filename=="./docs/Sumstats_README.md" or filename=="./docs/Proteomics_Proteomics_README.md":
        df_combined = format_data_sumstats(df_combined)
    
    #shortcuts to main text
    df_combined["NAME_FOR_LINK"] = df_combined["NAME"].str.replace('[^A-Za-z0-9\s]+',"-",regex=True).str.replace('\s+','-',regex=True).str.replace('[-]+','-',regex=True).str.lower()
    df_combined["TABLE_NAME"] = "[" +df_combined["NAME"] +"]"+"(#"+ df_combined["NAME_FOR_LINK"] + ")"
    
    df_combined = df_combined.rename(columns={"NAME":"_NAME"})
    df_combined = df_combined.rename(columns={"TABLE_NAME":"NAME"})
    
    df_combined["CITATION"] = df_combined["CITATION"].str.replace('\n','<br><br>')
    
    ## topic-specifc table
    if filename=="./docs/Sumstats_README.md":
        table_columns = ["NAME","MAIN_ANCESTRY"]
    elif filename=="./docs/Proteomics_Proteomics_README.md":
        table_columns = ["NAME","PLATFORM","YEAR","TITLE"]
    else:
        table_columns = ["NAME","CITATION","YEAR"]
    sort_cols = ["NAME"]

    if "CATEGORY" in df_combined.columns:
        if not df_combined["CATEGORY"].isna().all():
            table_columns.insert(1,"CATEGORY")
            sort_cols.insert(0,"CATEGORY")
            df_combined["CATEGORY"] = df_combined["CATEGORY"].fillna("MISC")

    to_output = df_combined.sort_values(by=sort_cols).loc[:,table_columns].fillna("NA")
    to_output.to_markdown(filename, index=None, mode="a")

    df_combined = df_combined.drop(columns=["NAME"])
    df_combined = df_combined.rename(columns={"_NAME":"NAME"})


    with open(filename,"a") as file:
        if "CATEGORY" in df_combined.columns:
            if not df_combined["CATEGORY"].isna().all():
                print_two_level(filename, df_combined, output_items)
            else:
                print_one_level(filename, df_combined, output_items)
        else:
            print_one_level(filename, df_combined)

        print("Overwriting {}...".format(filename))

def print_one_level(filename, df_combined, output_items):
    output_items = ['NAME', 'PUBMED_LINK', 
       'SHORT NAME', 'FULL NAME', 'DESCRIPTION', 'URL', 
       'KEYWORDS', 'USE', 'PREPRINT_DOI', 'SERVER',"JOURNAL_INFO", 'TITLE', 'CITATION',
       'MESH_MAJOR', 'MESH_MINOR', 'ABSTRACT', 'COPYRIGHT', 'DOI',"RELATED_BIOBANK","MAIN_ANCESTRY"]
    with open(filename,"a") as file:
        for index, row in df_combined.sort_values(by=["NAME"]).iterrows():
            file.write("\n")
            file.write("\n")
            file.write("## {}\n".format(row["NAME"]))
            file.write("\n")
            for item in df_combined.columns:
                if item in output_items:
                    if not pd.isna(row[item]):
                        if "\n" in item:
                            for record in row[item].strip().split("\n"):
                                file.write("- **{}** : {} \n ".format(item.strip(), record.strip()))
                        else:
                            file.write("- **{}** : {} \n ".format(item.strip(), row[item].strip()))

def print_two_level(filename, df_combined, output_items):

    
    with open(filename,"a") as file:
        for category in df_combined["CATEGORY"].sort_values().unique():
            file.write("\n")
            file.write("\n")
            file.write("## {}\n".format(category))
            file.write("\n")

            for index, row in df_combined.loc[df_combined["CATEGORY"]==category,:].sort_values(by=["CATEGORY","NAME"]).iterrows():
                file.write("\n")
                file.write("\n")
                file.write("### {}\n".format(row["NAME"]))
                file.write("\n")
                for item in df_combined.columns:
                    if item in output_items:
                        if not pd.isna(row[item]):
                            if "\n" in item:
                                for record in row[item].strip().split("\n"):
                                    file.write("- **{}** : {} \n ".format(item.strip(), record.strip()))
                            else:
                                file.write("- **{}** : {} \n ".format(item.strip(), row[item].strip()))

output_items = ['NAME', 'PUBMED_LINK', 
       'SHORT NAME', 'FULL NAME', 'DESCRIPTION', 'URL', 
       'KEYWORDS', 'USE', 'PREPRINT_DOI', 'SERVER',"JOURNAL_INFO", 'TITLE', 'CITATION',
       'MESH_MAJOR', 'MESH_MINOR', 'ABSTRACT', 'COPYRIGHT', 'DOI',"RELATED_BIOBANK","MAIN_ANCESTRY"]

tempfile= "formatted_main_table.xlsx"
if not os.path.isfile(tempfile):
    pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Population_Genetics",dtype={"PMID":"string"})
    pop0["FIELD"] = "Population_Genetics"
    pop = pop0

    pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Tools",dtype={"PMID":"string"})
    pop0["FIELD"] = "Tools"
    pop = pd.concat([pop,pop0])

    pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Visualization",dtype={"PMID":"string"})
    pop0["FIELD"] = "Visualization"
    pop = pd.concat([pop,pop0])

    pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Sumstats",dtype={"PMID":"string"})
    pop0["FIELD"] = ""
    pop = pd.concat([pop,pop0])

    pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Proteomics",dtype={"PMID":"string"})
    pop0["FIELD"] = "Proteomics"
    pop = pd.concat([pop,pop0])

    pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Metabolomics",dtype={"PMID":"string"})
    pop0["FIELD"] = "Metabolomics"
    pop = pd.concat([pop,pop0])

    import sys 
    sys.path.insert(0,"/home/yunye/work/github_projects/citationAPI/src")
    import citebiomed as cb
    print("Matching PMID from PUBMED....")
    query = cb.efetch_from_pubmed( list(pop["PMID"].dropna()) ,email="yunyehe.ctg@gmail.com")

    pop_pmid = pd.merge(pop,query,on="PMID",how="left")
    pop_pmid.to_excel(tempfile,index=None)
else:
    pop_pmid = pd.read_excel(tempfile,dtype="string")

def format_path_full(series):
    path_list=[]
    for i in series:
        if i!="":
            path_list.append(i)
    return "./docs/"+"_".join(path_list)+"_README.md"

folder_cols =["FIELD"]
for col in pop_pmid.columns:
    if "FOLDER" in col:
        folder_cols.append(col)
pop_pmid["PATH"] = pop_pmid[folder_cols].fillna("").apply(lambda x: format_path_full(x), axis=1)

print(pop_pmid["PATH"].unique())

for path in pop_pmid["PATH"].unique():
    df_combined = pop_pmid.loc[pop_pmid["PATH"]==path,:]
    overwrite_markdown(path, df_combined, output_items)




            