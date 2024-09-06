import sys
import os
import shutil
import pandas as pd

###########################################################################################################################################################################################################################
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

biobank_header = '''

### Sumstats and Biobanks/Cohorts

'''
def write_homepage(biobank_header=biobank_header):
    df = pd.read_excel("../CTGCatalog.xlsx",sheet_name="Biobanks",dtype="string")



    ###########################################################################################################################################################################################################################
    with open("../docs/index.md","a") as homepage:
        homepage.write(biobank_header)
        single_line = "- {} : {}\n".format("[Biobanks/Cohorts](Sumstats_Biobanks_Cohorts_README.md)", len(df))
        homepage.write(single_line)
        
        for sheet in ["Sumstats","Proteomics","Imaging"]:
            df = pd.read_excel("../CTGCatalog.xlsx",sheet_name=sheet,dtype={"PMID":"string"})
            type_dir = df.groupby("TYPE")["NAME"].count()
            string_list=[]
            for key,value in type_dir.items():
                type_string = "{} - {}".format(key,value)
                string_list.append(type_string)
            type_line = " , ".join(string_list)
            key = "[{}]({}_{}_README.md)".format(sheet, sheet,sheet)
            single_line = "- {} : {}\n".format(key, type_line)
            homepage.write(single_line)

    ###########################################################################################################################################################################################################################
    for dirname in ["Tools","Visualization","Population_Genetics" ]: 
        main_file = "../docs/"+dirname+"_README.md"
        shutil.copyfile("../"+dirname+"/README.md", main_file)
        raw_dir = pd.read_excel("../CTGCatalog.xlsx",sheet_name = dirname, dtype={"PMID":"string"})
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
        with open("../docs/index.md","a") as homepage:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ",main_file)
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
                    print(single_line)
                    homepage.write(single_line)

    ###########################################################################################################################################################################################################################
    about_text = '''

    ## About

    For more Complex Trait Genomics contents, please check [https://gwaslab.com/](https://gwaslab.com/)

    Contact : gwaslab@gmail.com

    [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fcloufield.github.io%2FCTGCatalog%2F&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Daily%2FTotal+views&edge_flat=false)](https://hits.seeyoufarm.com)'''

    with open("../docs/index.md","a") as homepage:
        homepage.write(about_text)