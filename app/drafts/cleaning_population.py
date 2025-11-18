import os
import pandas as pd

def load_population_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "raw_data")
    population_path = os.path.join(data_dir, "Bevoelkerung_nach_Stadtquartier.csv")
    df = pd.read_csv(population_path, sep=',', quotechar='"')
    df.rename(columns={
    'StichtagDatJahr': 'year',
    'QuarSort': 'district number',
    'QuarLang': 'district',
    'AnzBestWir': 'population'
    }, inplace=True)
    df.drop(columns=['district number'], inplace=True)
    return df

df = load_population_data()