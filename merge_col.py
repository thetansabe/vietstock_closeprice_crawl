import pandas as pd
from os import walk

# target folder
folder = "sep_stock"
# get all files in folder
files = []
for (dirpath, dirnames, filenames) in walk(folder):
    files.extend(filenames)
    break


# read all files
df = pd.DataFrame()
out = pd.DataFrame()

target_path = folder + "/"

for file in files:
    target_col = file.split(".")[0].upper()

    df = pd.read_excel(target_path + file)
    out[target_col] = df[target_col]

# write to excel
out.to_excel("merged.xlsx", index=False)


