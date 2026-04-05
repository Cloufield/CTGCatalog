#!/bin/bash
#git pull

rm ./docs/*md
cd ./src && python ./main.py && cd ../
# Refresh PubMed GWAS trending page + interactive dashboard from ranking/ CSVs (main.py also runs this; repeat ensures latest data after build).
python3 ./scripts/render_trending_pubmed_gwas.py \
  || python3 ./scripts/render_trending_pubmed_gwas.py --stub
python ./scripts/minify_extra_css.py
zensical serve -a 127.0.0.1:8001

#mkdocs gh-deploy
