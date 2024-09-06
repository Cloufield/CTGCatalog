import sys
import os
import shutil
import pandas as pd
from load_data import load_ref
from process_md import write_md

def write_reference():
    # Load Data and Ref
    ref = load_ref()

    # Tools
    write_md(ref)