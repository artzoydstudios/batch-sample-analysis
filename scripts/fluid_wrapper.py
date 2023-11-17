import subprocess
import os
import uuid
import scipy
import shutil
import torch
import torchaudio

def mfcc(src, chans):
    if chans > 1:
        src = _convert_to_mono(src)
    out_dest = os.path.join(_create_temp(), f"{str(uuid.uuid4())}_output.wav")

    call_list = ["fluid-mfcc", "-source", src, "-features", out_dest]

    subprocess.run(call_list)

    return out_dest

def stats(src):
    out_dest = os.path.join(_create_temp(), f"{str(uuid.uuid4())}_output.wav")

    call_list = ["fluid-stats", "-source", src, "-stats", out_dest]

    subprocess.run(call_list)

    return out_dest

def _wave_to_np(path):
    try:
        rate, data = scipy.io.wavfile.read(path)
        return data
    except:
        print(f"Unable to read {path}")

def _create_temp():
    path = os.path.join(os.getcwd(), "temp")
    if os.path.isdir(path) == False:
        os.makedirs(path)
    return path

def _remove_temp():
    path = os.path.join(os.getcwd(), "temp")
    if os.path.isdir(path):
        shutil.rmtree(path)

def _convert_to_mono(path):
    print(f"\tConverting {path} to mono...")
    temp_path = _create_temp()
    new_path = os.path.join(temp_path, f"{str(uuid.uuid4())}_input.wav")
    waveform, sr = torchaudio.load(path)
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim = 0, keepdim = True)
    torchaudio.save(new_path, waveform, sr)
    return new_path