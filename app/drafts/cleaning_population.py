import os
import pandas as pd

def load_population_data():
    # Prepare Paths for Data Reading
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "raw_data")
    population_path = os.path.join(data_dir, "Bevoelkerung_nach_Stadtquartier.csv")

    # Adjust path and separator if needed
    df = pd.read_csv(population_path, sep=',', quotechar='"')
    print("Columns before processing:", df.columns)
    
    # If CSV was read as one column, split it
    if len(df.columns) == 1:
        df = df[df.columns[0]].str.split(',', expand=True)
        df.columns = ['StichtagDatJahr','QuarSort','QuarLang','AnzBestWir']
    
    print("Columns after processing:", df.columns)
    return df

df = load_population_data()
