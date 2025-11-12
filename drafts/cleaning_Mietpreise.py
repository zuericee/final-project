import os
import pandas as pd

#Prepare Paths for Data Reading

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "raw_data")

#Read in Mietpreisbandbreiten

mietpreise_path = os.path.join(data_dir, "Mietpreise.csv")
df_mietpreise = pd.read_csv(mietpreise_path, sep=";")
print("\nMietpreisbandbreiten:")
print(df_mietpreise.head())