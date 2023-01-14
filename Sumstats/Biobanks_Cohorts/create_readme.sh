#!/bin/bash

wget -O biobanks.xlsx https://www.dropbox.com/s/61gatpd0lro9k5c/biobanks.xlsx?dl=1
python ./biobanks_to_md.py
