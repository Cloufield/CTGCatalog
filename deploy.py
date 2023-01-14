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
  name: material
  features:
    - navigation.tabs
    - navigation.top
  font:
    code: Roboto Mono
    text: Roboto
  palette:
    primary: indigo
    accent: indigo

extra_css:
  - "stylesheets/extra.css"

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
  - mkdocs-jupyter
'''
shutil.copyfile("./README.md", "./docs/index.md")
part2="nav: \n    - Home : index.md\n"
for dirname in ["Tools","Sumstats","Reference_data","Visualization","Population_Genetics"]: #"Programming","NGS",
    for root, dirs, files in os.walk("./"+dirname):
        #print(root)
	
	## get current directory
        currentfolder = root.strip(".|/").split("/")[-1]
        files.sort()
	
	## for files in the current directory
        for name in files:
	    ## get full path for a file
            file = os.path.join(root,name)
	    
            ## reconstruct the name / in path to _
            filerename = ("_".join(file.strip(".|/").split("/")))
            
            ## if there are subdirectories
            if filerename[-2:]=="md" and len(dirs)>0:
                ## file sub categories
                part2+=" "*2*len(file.strip(".|/").split("/"))+"- " + root.strip(".|/").split("/")[-1] +":"
                part2+="\n"
                ## file md
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
