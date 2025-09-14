#!/bin/bash
#git pull

rm ./docs/*md
cd ./src && python ./main.py && cd ../
mkdocs serve -a 127.0.0.1:8001

#mkdocs gh-deploy
