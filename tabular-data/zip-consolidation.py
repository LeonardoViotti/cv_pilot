
#------------------------------------------------------------------------------------
# Settings

EXPORT = False

import pandas as pd
from zipfile import ZipFile
import os
import glob

#------------------------------------------------------------------------------------
# Globals

DATA = 'C:/Users/wb519128/Dropbox/Work/WB/CV/Ethiopia/data'
DATA_sample = os.path.join(DATA, "sample")
DATA_pilot_results = os.path.join(DATA, "pilot-results")
DATA_raw = os.path.join(DATA_pilot_results, "raw")
 
#------------------------------------------------------------------------------------
# Files and data configuratioons

# Set csv schemas
schema_pet = ['pet', 'date', 'time', 'arrived_first', 'u1_id',
          'u1_mov', 'u1_type', 'u1_conf_speed', 'u1_med_speed', 
          'u2_id', 'u2_mov', 'u2_type', 'u2_conf_speed', 
          'u2_med_speed', 'url']
schema_users = ['date', 'u_id', 'entry_time', 'exit_time',  'user_type', 'med_speed', 'mov']
schema_speed = ['hour', 'movement', 'avg_speed']

# Get all zipped file names 
zip_files = glob.glob(DATA_raw + "/*.zip")

# To do:
#   - Add ID

# Speed Data Aggregated by Time - Hourly - All Movements.csv
# Road Users Data - All Movements.csv


#------------------------------------------------------------------------------------
# Load data and create dataset

# Create empty df instance for each main dataframe
pet_df = pd.DataFrame(columns = schema_pet)
pet_df['pilot_id'] = None

speed_df = pd.DataFrame(columns = schema_speed)
speed_df['pilot_id'] = None

users_df = pd.DataFrame(columns = schema_users)
users_df['pilot_id'] = None

# Loop over all zip files
for file in zip_files:
    # List all files inside .zip
    all_files_in_zip_i = ZipFile(file).namelist()
    
    # Find PET dataset file
    pet_df_name_i = list(filter(lambda x:'PET Conflict Data - All Movements.csv' in x, all_files_in_zip_i))[0]
    speed_df_name_i = list(filter(lambda x:'Speed Data Aggregated by Time - Hourly - All Movements.csv' in x, all_files_in_zip_i))[0]
    users_df_name_i = list(filter(lambda x:'Road Users Data - All Movements.csv' in x, all_files_in_zip_i))[0]
    
    # Read csv into pandas
    pet_df_i = pd.read_csv(ZipFile(file).open(pet_df_name_i), names = schema_pet, header=0)
    speed_df_i = pd.read_csv(ZipFile(file).open(speed_df_name_i), names = schema_speed, header=0)
    users_df_i = pd.read_csv(ZipFile(file).open(users_df_name_i), names = schema_users, header=0)
    
    # Get pliot id
    pilot_id_i = file[-7:-4] # Grab last 3 characters before ".zip"
    
    # Add ID!
    pet_df_i['pilot_id'] = pilot_id_i
    speed_df_i['pilot_id'] = pilot_id_i
    users_df_i['pilot_id'] = pilot_id_i
    
    # Append to consolidated df
    pet_df = pet_df.append(pet_df_i)
    users_df = users_df.append(users_df_i)
    speed_df = speed_df.append(speed_df_i)
    
    print('Opening: ' + file)
    print('Pilot number: ' + pilot_id_i)

#------------------------------------------------------------------------------------
# Add original intersection id

# Load sample data
pilot_sample = pd.read_csv(os.path.join(DATA_sample , 'pilot-intersections.csv'))

# Keep only ids
pilot_sample_ids = pilot_sample[['id', 'intersection_num']]\
    .rename(columns = {'id': 'pilot_id',
                       'intersection_num': 'id'})
pilot_sample_ids['pilot_id'] = pilot_sample_ids['pilot_id'].astype(int)


# Add id to tables
pet_df['pilot_id'] = pet_df['pilot_id'].astype(int)
speed_df['pilot_id'] = speed_df['pilot_id'].astype(int)
users_df['pilot_id'] = users_df['pilot_id'].astype(int)

pet_df = pet_df.merge(pilot_sample_ids, on = 'pilot_id')
speed_df = speed_df.merge(pilot_sample_ids, on = 'pilot_id')
users_df = users_df.merge(pilot_sample_ids, on = 'pilot_id')

#------------------------------------------------------------------------------------
# Export
if EXPORT:
    pet_df.to_csv(os.path.join(DATA_pilot_results, 'pet-conflict-all-juntions.csv'))
    users_df.to_csv(os.path.join(DATA_pilot_results, 'users-all-juntions.csv'))
    speed_df.to_csv(os.path.join(DATA_pilot_results, 'movements-speed-all-juntions.csv'))

#------------------------------------------------------------------------------------
# Create empty dictionary

# Load original column
def grab_cols(file):
    return pd.read_csv(file, nrows=0).columns.to_list()

pet_df_cols = grab_cols(ZipFile(file).open(pet_df_name_i))
speed_df_cols = grab_cols(ZipFile(file).open(speed_df_name_i))
users_df_cols = grab_cols(ZipFile(file).open(users_df_name_i))

def create_dict(columns_list, label_list):
    dict_df = pd.DataFrame(list(zip(columns_list, label_list)), 
               columns =['column', 'label'])
    dict_df['description'] = None
    dict_df['comments'] = None
    return dict_df

pet_dict_df = create_dict(schema_pet, pet_df_cols)
users_dict_df = create_dict(schema_users, users_df_cols)
speed_dict_df = create_dict(schema_speed, speed_df_cols)

# Export
if EXPORT:
    pet_dict_df.to_csv(os.path.join(DATA_pilot_results, 'pet-conflict-all-juntions-dictionary-TEMPLATE.csv'))
    users_dict_df.to_csv(os.path.join(DATA_pilot_results, 'users-all-juntions-dictionary-TEMPLATE.csv'))
    speed_dict_df.to_csv(os.path.join(DATA_pilot_results, 'movements-speed-all-juntions-dictionary-TEMPLATE.csv'))

# Initial descriptions, some may be filled later

