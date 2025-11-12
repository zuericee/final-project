import os
import pandas as pd

#Prepare Paths for Data Reading

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "raw_data")

#Read in Bevökerung nach Stadtquartier

bevölkerung_path = os.path.join(data_dir, "Bevoelkerung_nach_Stadtquartier.csv")
df_bevoelkerung = pd.read_csv(bevölkerung_path, sep=";")
print("\nBevölkerung nach Stadtquartier:")
print(df_bevoelkerung.head())