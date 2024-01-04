#!/bin/bash

wget -O biobanks.xlsx "https://www.dropbox.com/scl/fi/3pjx4mlnhp15g6x3hk0hb/biobanks.xlsx?rlkey=3wq2do0anvbkf55xdasp3xvs0&dl=1"
python ./biobanks_to_md.py
