"""
02 GET METADATA

Update the metadata of entries in the database (found at path database_path) 
with basic data like duration, sampling rate, channels etc.
"""

import audiofile
import utils
import os

database_path = "/Users/artzoydstudio/Documents/GitHub/batch-sample-analysis/database"

def process(db_path):
    bad_formats = []
    count = 1
    for root, dirs, files in os.walk(db_path):
        for file in files:
            if file == "metadata.json":
                print(count)
                metadata_path = os.path.join(root, file)
                sample_metadata = utils.read_json(metadata_path)
                audio_path = sample_metadata["file_path"]
                if "audio_data" in sample_metadata:
                    if sample_metadata["audio_data"] == None:
                        print(f"Treating {audio_path}...")
                        try:
                            sample_metadata["audio_data"] = get_data(audio_path)
                        except:
                            sample_metadata["audio_data"] = None
                            bad_formats.append(audio_path)
                    else:
                        print(f"{audio_path} already had audio data.")
                else:
                    print(f"Treating {audio_path}...")
                    try:
                        sample_metadata["audio_data"] = get_data(audio_path)
                    except:
                        sample_metadata["audio_data"] = None
                        bad_formats.append(audio_path)
                utils.write_json(sample_metadata, metadata_path)
                count = count + 1
    sample_metadata = utils.read_json(os.path.join(db_path, "db_metadata.json"))
    sample_metadata["bad_formats"] = bad_formats
    utils.write_json(sample_metadata, os.path.join(db_path, "db_metadata.json"))

def get_data(path):
    signal, sampling_rate = audiofile.read(path)
    return {
        "duration" : audiofile.duration(path),
        "samples" : audiofile.samples(path),
        "sample_rate" : sampling_rate,
        "channels" : audiofile.channels(path),
        "bit_depth" : audiofile.bit_depth(path)
    }

process(database_path)