import sys
import os
import shutil
import pandas as pd
from load_data import load_table_and_ref
from process_md import write_md
from process_homepage import  write_homepage
from process_mkdocs import  write_mkdcos

# Load Data and Ref
table_and_ref = load_table_and_ref()

# Tools
write_md(table_and_ref)
# Homepage
write_homepage()

write_mkdcos()