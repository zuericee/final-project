import os
import pandas as pd

#Paths vorbereiten

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "app", "data")

#Excel-Datei Wohnungsbestand einlesen

wohnungen_path = os.path.join(data_dir, "BAU507T5073_Wohnungs-und-Zimmerbestand_nach-Zimmerzahl-Stadtquartier.xlsx")
df_wohnungen = pd.read_excel(wohnungen_path)
print("Wohnungsbestand:")
print(df_wohnungen.head())

#Bevölkerung nach Stadtquartier einlesen

bevoelkerung_path = os.path.join(data_dir, "Bevoelkerung_nach_Stadtquartier.csv")
df_bevoelkerung = pd.read_csv(bevoelkerung_path, sep=";")
print("\nBevölkerung nach Quartier:")
print(df_bevoelkerung.head())

#Mietpreisbandbreiten einlesen

mietpreise_path = os.path.join(data_dir, "mietpreisbandbreiten.csv")
df_mietpreise = pd.read_csv(mietpreise_path, sep=";")
print("\nMietpreisbandbreiten:")
print(df_mietpreise.head())