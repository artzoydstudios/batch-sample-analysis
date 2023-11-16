"""
03 CREATE PANDAS DATAFRAMES

Create pandas dataframes for blocs of max_entries entries in the database.
The dataframes will be exported as csv to database_path/dataframes/all_files_metadata
"""

import utils
import os
import pandas as pd
import csv

database_path = "/Users/artzoydstudio/Documents/GitHub/batch-sample-analysis/database"
max_entries = 1000

def process(db_path, num_entries):
    count = 0
    current_data_frame = None
    df_index = -1
    for root, dirs, files in os.walk(db_path):
        for file in files:
            if file == "metadata.json":
                metadata_path = os.path.join(root, file)
                metadata = utils.read_json(metadata_path)
                if metadata["audio_data"] != None:
                    data_frame_idx = count % num_entries
                    if data_frame_idx == 0:
                        if df_index != -1:
                            save_data_frame(current_data_frame, os.path.join(db_path, "dataframes", "all_files_metadata"), df_index)
                        current_data_frame = create_empty_dataframe()
                        df_index = df_index + 1
                    print(count, data_frame_idx)
                    print(f"Adding {metadata_path}...")
                    append_to_dataframe(os.path.dirname(metadata_path), current_data_frame, metadata)
                    
                    count = count + 1
                else:
                    print(f"\t{metadata_path} had no audio data.")
    save_data_frame(current_data_frame, os.path.join(db_path, "dataframes", "all_files_metadata"), df_index)

def create_empty_dataframe():
    df = pd.DataFrame()
    df['database_path'] = None
    df['duration'] = None
    df['samples'] = None
    df['sample_rate'] = None
    df['channels'] = None
    df['bit_depth'] = None
    return df

def append_to_dataframe(db_path, df, data):
    to_append = {
        "database_path" : db_path,
        "duration" : data["audio_data"]["duration"],
        "samples" : data["audio_data"]["samples"],
        "sample_rate" : data["audio_data"]["sample_rate"],
        "channels" : data["audio_data"]["channels"],
        "bit_depth" : data["audio_data"]["bit_depth"]
    }
    df.loc[len(df)] = to_append

def save_data_frame(df, root_path, idx):
    if os.path.isdir(root_path) == False:
        os.makedirs(root_path)
    df.to_csv(os.path.join(root_path, f"bloc_{str(idx)}.csv"), index = False, quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)

process(database_path, max_entries)