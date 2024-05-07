import sys
import os
import shutil
import pandas as pd

def combine_row(df_combined, row_dict):
    if row_dict != {}:
        df_row = pd.DataFrame(data=row_dict,index=[0])
        df_combined = pd.concat([df_combined, df_row],ignore_index=True)    
    return df_combined

def overwrite_markdown(filename, df_combined):
    with open(filename,"w") as file:
        file.write("## Summary Table\n\n")
    
    df_combined["TABLE_NAME"] = "[" +df_combined["NAME"] +"]"+"(#"+df_combined["NAME"].str.replace("\s+","-").str.lower() + ")"
    df_combined = df_combined.rename(columns={"NAME":"_NAME"})
    df_combined = df_combined.rename(columns={"TABLE_NAME":"NAME"})
    df_combined["CITATION"] = df_combined["CITATION"].str.replace('\n','<br><br>')
    
    table_columns = ["NAME","CITATION"]
    sort_cols = ["NAME"]
    if "CATEGORY" in df_combined.columns:
        table_columns.insert(1,"CATEGORY")
        sort_cols.insert(0,"CATEGORY")

    df_combined.sort_values(by=sort_cols).loc[:,table_columns].to_markdown(filename,index=None, mode="a")
    
    df_combined["CITATION"] = df_combined["CITATION"].str.replace('<br><br>','\n')
    df_combined = df_combined.drop(columns=["NAME"])
    df_combined = df_combined.rename(columns={"_NAME":"NAME"})
    

    with open(filename,"a") as file:
        if "CATEGORY" in df_combined.columns:
            print_two_level(filename, df_combined)
        else:
            print_one_level(filename, df_combined)

        print("Overwriting {}...".format(filename))

def print_one_level(filename, df_combined):
    with open(filename,"a") as file:
        for index, row in df_combined.sort_values(by=["NAME"]).iterrows():
            file.write("\n")
            file.write("\n")
            file.write("## {}\n".format(row["NAME"]))
            file.write("\n")
            for item in df_combined.columns:
                if not pd.isna(row[item]):
                    if "\n" in item:
                        for record in row[item].strip().split("\n"):
                            file.write("- {} : {} \n ".format(item.strip(), record.strip()))
                    else:
                        file.write("- {} : {} \n ".format(item.strip(), row[item].strip()))    

def print_two_level(filename, df_combined):
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
                    if not pd.isna(row[item]):
                        if "\n" in item:
                            for record in row[item].strip().split("\n"):
                                file.write("- {} : {} \n ".format(item.strip(), record.strip()))
                        else:
                            file.write("- {} : {} \n ".format(item.strip(), row[item].strip()))   


files = ["./docs/Tools_Polygenic_risk_scores_README.md", 
         "./docs/Tools_Fine_mapping_README.md",
         "./docs/Tools_Association_tests_README.md",
         "./docs/Tools_Colocalization_README.md",
         "./docs/Tools_Data_processing_README.md",
         "./docs/Tools_Annotation_README.md",
         "./docs/Tools_Gene_prioritization_README.md",
         "./docs/Tools_HLA_README.md",
         "./docs/Tools_Imputation_README.md"]

for filename in files:
    if "README.md" in filename: 
        df_combined = pd.DataFrame()
        try:
            with open(filename,"r") as file:
                lines = file.readlines()
                row_dict = {}
                for index, line in enumerate(lines):
                    if len(line.strip())>2:
                        if line.strip()[:2]=="##":
                            df_combined = combine_row(df_combined, row_dict)    
                            row_dict={"NAME":line.replace("##","").strip()}

                        if line.strip()[0]=="-" and ":" in line:
                            header = line.split(":", 1)[0].strip().strip("-").strip()
                            if header in row_dict.keys():
                                row_dict[header] += "\n"+line.split(":", 1)[1].strip()
                            else:
                                row_dict[header] = line.split(":", 1)[1].strip()
                    if index == len(lines)-1:
                        df_combined = combine_row(df_combined, row_dict)
                
            overwrite_markdown(filename, df_combined)
        except:
            print("ERROR:", filename)
            pass
    else:
        continue