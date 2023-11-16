# import pandas as pd

# src = ""

# df = pd.read_csv(src)

# print(df)

import numpy as np
test = "/Users/artzoydstudio/Documents/GitHub/batch-sample-analysis/database/HD 10/Exp #6/algadafe kbd2/00 asp 5 - asp 5.VS.VS/basic_mfcc_analysis.npy"

opened = np.load(test)

print(opened)
print(type(opened))