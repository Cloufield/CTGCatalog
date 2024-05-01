#!/bin/bash
git pull
python ./deploy.py
python process_markdown.py
#mkdocs serve
mkdocs gh-deploy
