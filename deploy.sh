#!/bin/zsh
git pull
python ./deploy.py
mkdocs gh-deploy
