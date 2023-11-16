import os
import json

def collect_files(path, accepted = []):
    final_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1][1:].lower()
            if ext in accepted or len(accepted) == 0:
                final_list.append(os.path.join(root, file))
    return final_list

def write_json(content, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False)

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)