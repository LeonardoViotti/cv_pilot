
#------------------------------------------------------------------------------------
# Settings

import pandas as pd
from zipfile import ZipFile
import os
import glob

#------------------------------------------------------------------------------------
# Globals

DATA = 'C:/Users/wb519128/Dropbox/Work/WB/CV/Ethiopia/data/pilot-results'
DATA_raw = os.path.join(DATA, "raw")
 
#------------------------------------------------------------------------------------
# Load data

# Get all files 
zip_files = glob.glob(DATA_raw + "/*.zip")

# with ZipFile(zip_files[0]) as myzip:

# List all files inside .zip
all_files_in_zip = ZipFile(zip_files[0]).namelist()


foo = list(filter(lambda x:'PET Conflict Data - All Movements.csv' in x, all_files_in_zip))

bar = ZipFile(zip_files[0]).open(foo[0])


pd.read_csv(bar)