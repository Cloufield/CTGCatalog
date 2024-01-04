#!/bin/bash
git pull
python ./deploy.py
mkdocs gh-deploy
