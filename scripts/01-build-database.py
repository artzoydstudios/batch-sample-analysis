"""
01 BUILD DATABASE

Add all of the audio files within root_dir (recursive) as an entry in the database that is foudn at database_path.
Set a list of accepted audio files with accepted_files.
"""

import os
import utils

root_dir = "/Volumes/Public/Archives/Disques durs SCSI Akai"
accepted_files = ["wav", "aif", "aiff", "mp3", "wma", "aac", "flac", "m4a", "wave", "ogg"]
database_path = os.path.join(os.getcwd(), "database")

def process(path, db_path, accepted = []):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1][1:].lower()
            if ext in accepted or len(accepted) == 0:
                create_entry(os.path.join(root, file), path, db_path)
                count = count + 1
    
    global_metadate_path = os.path.join(db_path, "db_metadata.json")
    if os.path.isfile(global_metadate_path) == False:
        utils.write_json({
            "root" : path,
            "num_files" : count
        },
        global_metadate_path)
    else:
        original_metadata = utils.read_json(global_metadate_path)
        original_metadata["root"] = path
        original_metadata["num_files"] = count
        utils.write_json(original_metadata, global_metadate_path)
    

def create_entry(path, original_root, dest_dir):
    creation_path = path.split(original_root)[-1][1:]
    creation_path = os.path.splitext(creation_path)[0]
    creation_path = os.path.join(dest_dir, creation_path)
    if os.path.isdir(creation_path) == False:
        os.makedirs(creation_path)
    
    metadata_path = os.path.join(creation_path, "metadata.json")
    if os.path.isfile(metadata_path) == False:
        utils.write_json({
            "file_path" : path
        },
        metadata_path)
    else:
        original_metadata = utils.read_json(metadata_path)
        original_metadata["file_path"] = path
        utils.write_json(original_metadata, metadata_path)
    
    print(f'\tCreated entry for {path}')

process(root_dir, database_path, accepted_files)