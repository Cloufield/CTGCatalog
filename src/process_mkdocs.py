import sys
import os
import shutil
import pandas as pd

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

part2="nav: \n    - Home : index.md\n"

part2+='''    - Sumstats:
      - Sumstats: Sumstats_Sumstats_README.md
      - Biobanks_Cohorts: Sumstats_Biobanks_Cohorts_README.md
      - Metabolomics: Metabolomics_Metabolomics_README.md
      - Proteomics: Proteomics_Proteomics_README.md
      - Imaging: Imaging_Imaging_README.md\n'''

def write_mkdcos(part1=part1, part2=part2):

    ##################################################################################################################################################################################################################

    def format_path(series):
        path_list=[]
        for i in series:
            if i!="" and i is not None:
                path_list.append(i)
        return "_".join(path_list)

    def format_level(series):
        level = 1
        for i in series:
            if i!="":
                level+=1
        return level
    ##################################################################################################################################################################################################################

    for dirname in ["Tools","Visualization","Population_Genetics" ]: 
        raw_dir = pd.read_excel("../CTGCatalog.xlsx",sheet_name = dirname, dtype={"PMID":"string"})
        folder_cols =[]


        # "FOLDER1" "FOLDER2" "FOLDER3" ... 
        for col in raw_dir.columns:
            if "FOLDER" in col:
                folder_cols.append(col)
        
        raw_dir.loc[:, folder_cols ] = raw_dir.loc[:, folder_cols].fillna("")
        raw_dir["TYPE"] = raw_dir["TYPE"].fillna("MISC")
        
        # create PATH using all folder_cols
        raw_dir["PATH"] = raw_dir[folder_cols].apply(lambda x: format_path(x), axis=1)
        df_dir = raw_dir.loc[:, folder_cols].dropna(subset=folder_cols[0]).fillna("")
        
        # get path and calculate indent level
        path_df = df_dir.groupby(folder_cols).count().reset_index()
        path_df["PATH"] = path_df[folder_cols].apply(lambda x: format_path(x), axis=1)
        path_df["LEVEL"] = path_df[folder_cols].apply(lambda x: format_level(x), axis=1)
        
        # get the root folder for each level
        level_root_dic ={col:list() for col in folder_cols}
        for index in range(len(folder_cols)):
            if index< len(folder_cols)-1:
                level_count = path_df.groupby(folder_cols[index])["PATH"].count()
                level_root_dic[folder_cols[index]]+=list(level_count[level_count>1].index.values)      
        
        # write page for each category
        main_file = "../docs/"+dirname+"_README.md"
        shutil.copyfile("../"+dirname+"/README.md", main_file)
        with open(main_file,"a") as file:
            file.write("\n\n")
            file.write("## {} - {} \n".format("Contents",dirname))
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
    
    #tab############################################
    spaces = " " * 2 * (1+1)
    dirname = "Reference"
    value = "{}_README.md".format(dirname)
    single_line = "{}- {}: \n".format( spaces ,dirname)
    part2+= single_line
    ############################################

    for dirname in ["Phenotype","Genome","Gene","Variant","Protein","Annotation"]: 
        raw_dir = pd.read_excel("../CTGCatalog_reference.xlsx",sheet_name = dirname, dtype={"PMID":"string"})
        if len(raw_dir)>0:
            folder_cols =[]
        
            # "FOLDER1" "FOLDER2" "FOLDER3" ... 
            for col in raw_dir.columns:
                if "FOLDER" in col:
                    folder_cols.append(col)

            raw_dir.loc[:, folder_cols ] = raw_dir.loc[:, folder_cols ].fillna("")
            raw_dir["TYPE"] = raw_dir["TYPE"].fillna("MISC")
            
            # create PATH using all folder_cols
            raw_dir["PATH"] = raw_dir[folder_cols].apply(lambda x: format_path(x), axis=1)
            df_dir = raw_dir# .loc[:, folder_cols].dropna(subset=folder_cols[0]).fillna("")
            
            # get path and calculate indent level
            path_df = df_dir.groupby(folder_cols).count().reset_index()
            print(path_df)
            path_df["PATH"] = path_df[folder_cols].apply(lambda x: format_path(x), axis=1)
            path_df["LEVEL"] = path_df[folder_cols].apply(lambda x: format_level(x), axis=1)
            
            # get the root folder for each level
            level_root_dic ={col:list() for col in folder_cols}
            for index in range(len(folder_cols)):
                if index< len(folder_cols)-1:
                    level_count = path_df.groupby(folder_cols[index])["PATH"].count()
                    level_root_dic[folder_cols[index]]+=list(level_count[level_count>1].index.values)      
            
            for index, row in path_df.iterrows():

                spaces = " " * 2 * (1+ row["LEVEL"])
                col = "FOLDER_{}".format( row["LEVEL"]-1 )
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
    with open("../mkdocs.yml",mode="w") as file:
        file.write(part1+part2)