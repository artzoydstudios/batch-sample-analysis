# import pandas as pd

# src = ""

# df = pd.read_csv(src)

# print(df)

import numpy as np
test = "/Users/artzoydstudio/Documents/GitHub/batch-sample-analysis/database/HD 10/Exp #6/algadafe kbd2/c-accumbb-ext3/basic_mfcc_analysis.npy"

opened = np.load(test)

print(opened)
print(opened.shape)
print(type(opened))