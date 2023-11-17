"""
05 MFCC ANALYSIS

Iterate over all of the dataframes saved at dataframes, get the corresponding audio file,
then perform an MFCC analysis, saving the result in as a numpy array in the entries database folder.
"""

import fluid_wrapper
import pandas as pd
import utils
import os
import numpy as np

dataframes = "/Users/artzoydstudio/Documents/GitHub/batch-sample-analysis/database/dataframes/all_files_metadata"
analysis_filename = "basic_mfcc_analysis"
clean_every = 100

def process(df_src):
    count = 0
    df_list = utils.collect_files(df_src, ["csv"])
    for df_file in df_list:
        df = pd.read_csv(df_file)
        for index, row in df.iterrows():
            print(count)
            metadata = utils.read_json(os.path.join(row["database_path"], "metadata.json"))
            audio_path = metadata["file_path"]
            data_save_path = os.path.join(row["database_path"], f"{analysis_filename}.npy")
            if os.path.isfile(data_save_path) == False:
                print(f"Performing MFCC analysis for {audio_path}...")
                mfcc = fluid_wrapper.mfcc(metadata["file_path"], metadata["audio_data"]["channels"])
                stats = fluid_wrapper.stats(mfcc)
                res = fluid_wrapper._wave_to_np(stats)
                np.save(data_save_path, res)
                if count % clean_every == 0:
                    fluid_wrapper._remove_temp()
            else:
                print(f"There was already an MFCC analysis for {audio_path}.")
            count = count + 1
    fluid_wrapper._remove_temp()

process(dataframes)