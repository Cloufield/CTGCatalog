import pandas as pd
import re
df = pd.read_excel("~/biobanks.xlsx",dtype="string")
df["Name"]= "[" + df["BIOBANK&COHORT"] + "](" + '#' +  df["BIOBANK&COHORT"].str.lower().str.replace(" ","-").str.replace("[-]+","-").str.replace("[^a-zA-Z0-9\-_]","").str.strip() +")"  
df["Link"]= "[Here](" +  df["URL"] +")"  
with open("./README.md","w") as file:
    file.write("# Biobanks & Cohorts\n\n## Summary Table\n\n")
    
df.loc[:,["Name","CONTINENT","LOCATION","SAMPLE SIZE","Link"]].to_markdown("./README.md",index=None, mode="a")

with open("./README.md","a") as file:
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
