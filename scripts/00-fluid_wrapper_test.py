import fluid_wrapper
import pandas as pd
import utils
import os

src = "/Users/artzoydstudio/Documents/GitHub/batch-sample-analysis/database/dataframes/all_files_metadata/bloc_0.csv"




def get_audio_path(df_row):
    metadata = utils.read_json(os.path.join(df_row["database_path"], "metadata.json"))
    return metadata["file_path"]

df = pd.read_csv(src)

for index, row in df.iterrows():
    if index == 8 or index == 0:
        mfcc = fluid_wrapper.mfcc(get_audio_path(row))
        stats = fluid_wrapper.stats(mfcc)
        print(row["channels"])
        print(get_audio_path(row))
        res = fluid_wrapper._wave_to_np(stats)
        print(res.shape)

        utils.write_json({"analysis" : res.tolist()}, os.path.join(os.getcwd(), str(index) + ".json"))

        flat = res.flatten()
        print(flat.shape)


fluid_wrapper._remove_temp()





# mfcc = fluid_wrapper.mfcc(src)
# stats = fluid_wrapper.stats(mfcc)

# print(fluid_wrapper._wave_to_np(stats))

# fluid_wrapper._remove_temp()