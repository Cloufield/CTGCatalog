import sys
import os
import shutil

part1='''site_name: CTGCatalog
site_author: HE Yunye
repo_name: 'GitHub'
repo_url: https://github.com/Cloufield/CTGCatalog/
edit_uri: ""
copyright: "CTGCatalog is licensed under the MIT license"
theme:
  name: null
  custom_dir: 'cinder'
  color_theme:  github"
'''
shutil.copyfile("./README.md", "./docs/index.md")
part2="nav: \n    - Home : index.md\n"
for dirname in ["Tools","Sumstats","Reference_data","Programming","NGS"]:
    for root, dirs, files in os.walk("./"+dirname):
        #print(root)
        currentfolder=root.strip(".|/").split("/")[-1]
        for name in files:
            file = os.path.join(root,name)
            filerename = ("".join(file.strip(".|/").split("/")))
            if len(dirs)>0:
                part2+=" "*2*len(file.strip(".|/").split("/"))+"- " + root.strip(".|/").split("/")[-1] +":"
                part2+="\n"
                part2+=" "*2*(1+len(file.strip(".|/").split("/")))+"- " + root.strip(".|/").split("/")[-1] +": "+filerename
                part2+="\n"
                shutil.copyfile(file, "./docs/"+filerename)
            #print(filerename)
            if filerename[-2:]=="md" and len(dirs)==0:
                part2+=" "*2*len(file.strip(".|/").split("/"))+"- " + root.strip(".|/").split("/")[-1] +": "+filerename
                part2+="\n"
                shutil.copyfile(file, "./docs/"+filerename)
with open("./mkdocs.yml",mode="w") as file:
    file.write(part1+part2)