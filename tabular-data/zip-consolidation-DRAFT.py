
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

# Set csv schemas
schema_pet = ['pet', 'date', 'time', 'arrived_first', 'u1_id',
          'u1_mov', 'u1_type', 'u1_conf_speed', 'u1_med_speed', 
          'u2_id', 'u2_mov', 'u2_type', 'u2_conf_speed', 
          'u2_med_speed', 'url']

schema_user = ['date', 'u_id', 'entry_time', 'exit_time',  'user_type', 'med_speed', 'mov']


schema_mov_speed = ['hour', 'movement', 'avg_speed']



# Get all files 
zip_files = glob.glob(DATA_raw + "/*.zip")

# with ZipFile(zip_files[0]) as myzip:

# List all files inside .zip
all_files_in_zip = ZipFile(zip_files[0]).namelist()

# Find PET dataset file
pet_df_name = list(filter(lambda x:'PET Conflict Data - All Movements.csv' in x, all_files_in_zip))[0]

# Load PET dataset into a dataframe
pet_df = pd.read_csv(ZipFile(zip_files[0]).open(pet_df_name))

# To do:
#   - Add ID
#   - Add Schema
#   - Loop trough all the files

# Speed Data Aggregated by Time - Hourly - All Movements.csv
# Road Users Data - All Movements.csv



# Create empty df instance for each main dataframe
pet_df = pd.DataFrame(columns = schema_pet)


for file in zip_files:
    # print(file)
    # List all files inside .zip
    all_files_in_zip_i = ZipFile(file).namelist()
    
    # Find PET dataset file
    pet_df_name_i = list(filter(lambda x:'PET Conflict Data - All Movements.csv' in x, all_files_in_zip_i))[0]
    
    # Read csv into pandas
    pet_df_i = pd.read_csv(ZipFile(file).open(pet_df_name_i), names = schema_pet, header=0)
    
    # Add ID!
    
    # Append to consolidated df
    pet_df = pet_df.append(pet_df_i)
    
    print(pet_df_name_i)
