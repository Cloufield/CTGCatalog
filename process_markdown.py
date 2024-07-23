import sys
import os
import shutil
import pandas as pd

def format_string(series):
    string = []
    for i in series:
        if i is not None:
            string.append(str(i))
    return " ; ".join(string)
    
def format_data(df_combined):
    df_combined.loc[df_combined["CITATION"].isna(),"CITATION"] = df_combined.loc[df_combined["CITATION"].isna(),"MANUAL_CITATION"]
    
    df_combined.loc[df_combined["TYPE"]=="Review","NAME"] = "Review-" + df_combined.loc[df_combined["TYPE"]=="Review","FIRST_AUTHOR"]
    
    df_combined["JOURNAL_INFO"] =   df_combined[['JOURNAL', 'ISO', 'YEAR', 'VOLUME', 'ISSUE', 'PAGE']].apply(lambda x: format_string(x) ,axis=1)
    
    df_combined["NAME"] = df_combined["NAME"].str.replace(" ","-").str.replace(".","-")
    
    df_combined["PUBMED_LINK"] = "["+ df_combined["PMID"] + "](" + "https://pubmed.ncbi.nlm.nih.gov/" +  df_combined["PMID"] + ")"
    return df_combined

def overwrite_markdown(filename, df_combined):
    with open(filename,"w") as file:
        file.write("## Summary Table\n\n")
    
    df_combined = format_data(df_combined)
    #shortcuts to main text
    df_combined["TABLE_NAME"] = "[" +df_combined["NAME"] +"]"+"(#"+df_combined["NAME"].str.replace("\s+","-").str.lower() + ")"
    
    df_combined = df_combined.rename(columns={"NAME":"_NAME"})
    df_combined = df_combined.rename(columns={"TABLE_NAME":"NAME"})
    
    df_combined["CITATION"] = df_combined["CITATION"].str.replace('\n','<br><br>')
    
    

    table_columns = ["NAME","CITATION","YEAR"]
    sort_cols = ["NAME"]
    if "CATEGORY" in df_combined.columns:
        if not df_combined["CATEGORY"].isna().all():
            table_columns.insert(1,"CATEGORY")
            sort_cols.insert(0,"CATEGORY")
            df_combined["CATEGORY"] = df_combined["CATEGORY"].fillna("MISC")

    df_combined.sort_values(by=sort_cols).loc[:,table_columns].to_markdown(filename,index=None, mode="a")

    df_combined = df_combined.drop(columns=["NAME"])
    df_combined = df_combined.rename(columns={"_NAME":"NAME"})


    with open(filename,"a") as file:
        if "CATEGORY" in df_combined.columns:
            if not df_combined["CATEGORY"].isna().all():
                print_two_level(filename, df_combined)
            else:
                print_one_level(filename, df_combined)
        else:
            print_one_level(filename, df_combined)

        print("Overwriting {}...".format(filename))

def print_one_level(filename, df_combined):
    output_items = ['NAME', 'PUBMED_LINK', 
       'SHORT NAME', 'FULL NAME', 'DESCRIPTION', 'URL', 
       'KEYWORDS', 'USE', 'PREPRINT_DOI', 'SERVER',"JOURNAL_INFO", 'TITLE', 'CITATION',
       'MESH_MAJOR', 'MESH_MINOR', 'ABSTRACT', 'COPYRIGHT', 'DOI']
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

def print_two_level(filename, df_combined):
    output_items = ['NAME', 'PUBMED_LINK', 
       'SHORT NAME', 'FULL NAME', 'DESCRIPTION', 'URL', 
       'KEYWORDS', 'USE', 'PREPRINT_DOI', 'SERVER',"JOURNAL_INFO", 'TITLE', 'CITATION',
       'MESH_MAJOR', 'MESH_MINOR', 'ABSTRACT', 'COPYRIGHT', 'DOI']
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

files = [   "./docs/Tools_Annotation_README.md",
            "./docs/Tools_Association_tests_README.md",
            "./docs/Tools_Association_tests_RWAS_README.md",
            "./docs/Tools_Association_tests_TWAS_README.md",
            "./docs/Tools_Association_tests_eQTL_README.md",
            "./docs/Tools_Association_tests_sQTL_README.md",
            "./docs/Tools_Colocalization_README.md",
            "./docs/Tools_Data_processing_README.md",
            "./docs/Tools_Dimension_reduction_README.md",
            "./docs/Tools_Drug_discovery_README.md",
            "./docs/Tools_Fine_mapping_README.md",
            "./docs/Tools_Gene_prioritization_README.md",
            "./docs/Tools_Gene_set_pathway_analysis_README.md",
            "./docs/Tools_GxE_interactions_README.md",
            "./docs/Tools_HLA_README.md",
            "./docs/Tools_Heritability_and_genetic_correlation_README.md",
            "./docs/Tools_Imputation_README.md",
            "./docs/Tools_Mendelian_randomization_README.md",
            "./docs/Tools_Meta_and_Multi_triat_README.md",
            "./docs/Tools_Polygenic_risk_scores_README.md",
            "./docs/Tools_Polygenic_risk_scores_README.md.processed",
            "./docs/Tools_Power_analysis_README.md",
            "./docs/Tools_Proteomics_README.md",
            "./docs/Tools_Simulation_README.md",
            "./docs/Tools_Tissue_and_single_cell_README.md",
            "./docs/Tools_Winners_curse_README.md",
            "./docs/Tools_Dimension_reduction_README.md",
            "./docs/Tools_Fine_mapping_README.md",
            "./docs/Tools_Gene_set_pathway_analysis_README.md",
            "./docs/Tools_GxE_interactions_README.md",
            "./docs/Tools_Mendelian_randomization_README.md",
            "./docs/Tools_Meta_and_Multi_triat_README.md",
            "./docs/Tools_Power_analysis_README.md",
            "./docs/Tools_Proteomics_README.md",
            "./docs/Tools_Simulation_README.md",
            "./docs/Tools_Tissue_and_single_cell_README.md",
            "./docs/Tools_Winners_curse_README.md",
            "./docs/Population_Genetics_Admixture_README.md",
            "./docs/Population_Genetics_Selection_README.md",
            "./docs/Visualization_Chromosome_README.md",
            "./docs/Visualization_Forest_plot_README.md",
            "./docs/Visualization_GWAS_README.md",
            "./docs/Visualization_Heatmap_README.md",
            "./docs/Visualization_LD_README.md",
            "./docs/Visualization_Variants_on_protein_README.md"]


pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Population_Genetics",dtype={"PMID":"string"})
pop0["FIELD"] = "Population_Genetics"
pop = pop0

pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Tools",dtype={"PMID":"string"})
pop0["FIELD"] = "Tools"
pop = pd.concat([pop,pop0])

pop0 = pd.read_excel("CTGCatalog.xlsx",sheet_name="Visualization",dtype={"PMID":"string"})
pop0["FIELD"] = "Visualization"
pop = pd.concat([pop,pop0])

import sys 
sys.path.insert(0,"/home/yunye/work/github_projects/citationAPI/src")
import citebiomed as cb
query = cb.efetch_from_pubmed( list(pop["PMID"].dropna()) ,email="yunyehe.ctg@gmail.com")

pop_pmid = pd.merge(pop,query,on="PMID",how="left")
pop_pmid

for filename in files:
    if "README.md" in filename:
            file =  filename.replace("_README.md","").replace("./docs/Tools_","").replace("./docs/Population_","").replace("./docs/Visualization_","")
            df_combined = pop_pmid.loc[pop_pmid["FILE"]==file,:]
            overwrite_markdown(filename, df_combined)
