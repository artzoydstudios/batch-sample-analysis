"""
05 PERFORM SEARCH

Give the path to an audio file with audio_file, and perform a nearest neighbour
search on the entire database at dataframes (give path to dataframes).
You can also filter out entrues with the filter_metadata dict.

TODO : Make the block analysis function "recursive" or something for arbitrary number of samples...
TODO : Optimize metadata reading.
"""
import numpy as np
import fluid_wrapper
import audiofile
import utils
import pandas as pd
import os
from sklearn.neighbors import NearestNeighbors
import time

audio_file = "/Users/jacob/Documents/Repos/batch-sample-analysis/test-corpus/Green-Box639 copie.wav"
dataframes = "/Users/jacob/Documents/Repos/batch-sample-analysis/database/dataframes"
analysis_file_name = "basic_mfcc_analysis"

num_neighbours_by_block = 2
final_num_neighbours = 5
output_file = True

filter_metadata = {
    "filter" : False,
    "max_duration" : {
        "filter" : True,
        "max_duration" : 3
    }
}

def process(src, df_folder, analysis_name, filters, num_n, final_num_n, save_file):
    t0 = time.time()

    input_analysis = perform_audio_file_analysis(src)
    input_analysis = parse_entry(input_analysis)

    df_file_list = utils.collect_files(df_folder, "csv")

    full_data = None
    full_labels = None
    done_first = False
    for df_file in df_file_list:
        as_np, labels = bloc_to_np(df_file, analysis_name, filters)
        nearest = get_nearest_neighbours(as_np, input_analysis, num_n)

        filtered = np.take(as_np, nearest[1][0], 0)
        filtered_labels = np.take(labels, nearest[1][0], 0)
        
        if done_first == False:
            full_data = filtered
            full_labels = filtered_labels
            done_first = True
        else:
            full_data = np.append(full_data, filtered, axis=0)
            full_labels = np.append(full_labels, filtered_labels, axis=0)
    
    final_nearest = get_nearest_neighbours(full_data, input_analysis, final_num_n)

    t1 = time.time()
    print_results(src, final_nearest, full_labels, t1 - t0)
    if save_file:
        save_results(final_nearest, full_labels)

def save_results(final_nn_result, labels):
    ret = {"neighbours" : []}
    for i, idx in enumerate(final_nn_result[1][0]):
        ret["neighbours"].append({
            "position" : i,
            "file" : labels[idx][0],
            "distance" : final_nn_result[0][0][i]
        })
    utils.write_json(ret, os.path.join(os.getcwd(), "OUTPUT.json"), 4)

def print_results(input_path, final_nn_result, labels, process_time):
    print(f"\n\n\n----------------\n\nNearest neighbour results for : \"{input_path}\":\n")

    for i, idx in enumerate(final_nn_result[1][0]):
        print(f"# {str(i + 1)} : \"{labels[idx][0]}\"")
        print(f"\tDistance : {final_nn_result[0][0][i]}")
    
    print(f"\nProcessing time : {process_time}.")
    print(f"\n----------------\n")

def get_nearest_neighbours(data, query, num_neighbours):
    if num_neighbours > data.shape[0]:
        num_neighbours = data.shape[0]
    neigh = NearestNeighbors(n_neighbors = num_neighbours)
    neigh.fit(data)
    result =  neigh.kneighbors([query])
    return result

def metadata_check(df_row, filter_data):
    ret = True
    entry_metadata = utils.read_json(os.path.join(df_row["database_path"], "metadata.json"))
    if filter_data["max_duration"]["filter"]:
        if entry_metadata["audio_data"]["duration"] > filter_data["max_duration"]["max_duration"]:
            ret = False
    return ret

def bloc_to_np(path, analysis_name, filters, write = False):
    df = pd.read_csv(path)
    df_np_array = None
    label_list = None
    added_first = False
    for index, row in df.iterrows():
        can_add = True
        if filters["filter"]:
            can_add = metadata_check(row, filters)
        if can_add:
            row_analysis_data = get_analysis_content(row, analysis_name)
            row_analysis_data = parse_entry(row_analysis_data)
            if added_first == False:
                df_np_array = row_analysis_data
                label_list = np.array([utils.read_json(os.path.join(row["database_path"], "metadata.json"))["file_path"]])
                added_first = True
            else:
                df_np_array = np.vstack([df_np_array, row_analysis_data])
                label_list = np.vstack([label_list, [utils.read_json(os.path.join(row["database_path"], "metadata.json"))["file_path"]]])
    if write:
        save_name = os.path.splitext(os.path.basename(path))[0]
        if os.path.isdir(os.path.join(os.getcwd(), "np_out")) == False:
            os.makedirs(os.path.join(os.getcwd(), "np_out"))
        np.savetxt(os.path.join(os.getcwd(), "np_out", f"{save_name}.npy"), df_np_array, delimiter=",")
        np.savetxt(os.path.join(os.getcwd(), "np_out", f"{save_name}_labels.npy"), label_list, delimiter=",", fmt="%s")
    return df_np_array, label_list

def perform_audio_file_analysis(src):
    mfcc = fluid_wrapper.mfcc(src, audiofile.channels(src))
    stat = fluid_wrapper.stats(mfcc)
    res = fluid_wrapper._wave_to_np(stat)
    fluid_wrapper._remove_temp()
    return res

def get_analysis_content(df_row, file_name):
    return np.load(os.path.join(df_row["database_path"], f"{file_name}.npy"))

def parse_entry(np_a):
    np_a = np_a.flatten() 
    return np_a

process(audio_file, dataframes, analysis_file_name, filter_metadata, num_neighbours_by_block, final_num_neighbours, output_file)