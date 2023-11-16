"""
04 FIND DOUBLES

Update the metadata of entries in the database (found at path database_path) 
with basic data like duration, sampling rate, channels etc.
"""

import audiofile
import utils
import os

database_path = "/Users/artzoydstudio/Documents/GitHub/batch-sample-analysis/database"

def process(db_path):
    count = 1
    for root, dirs, files in os.walk(db_path):
        for file in files:
            if file == "metadata.json":
                print(count)
                metadata_path = os.path.join(root, file)
                count = count + 1

process(database_path)