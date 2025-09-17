import sys
import os
import shutil
import pandas as pd

def print_one_level(filename, df_combined, output_items):
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
                            file.write("- **{}** : {} \n ".format(item.strip(), str(row[item]).strip()))

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

def write_markdown(filename, df_combined, output_items):
    with open(filename,"a") as file:
        if not df_combined["CATEGORY"].isna().all():
            print_two_level(filename, df_combined, output_items)
        else:
            print_one_level(filename, df_combined, output_items)