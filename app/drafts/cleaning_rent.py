import os
import pandas as pd

def load_rent_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "raw_data")
    rent_path = os.path.join(data_dir, "Mietpreise.csv")
    df = pd.read_csv(rent_path, sep=',', quotechar='"')
    #Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    #Shorter, easier-to-use names
    df = df.rename(columns={
    'stichtagdatjahr': 'year',
    'raumeinheitlang': 'area_type',
    'gliederunglang': 'district',
    'zimmersort': 'rooms',
    'gemeinnuetziglang': 'nonprofit',
    'einheitlang': 'unit_kind',
    'preisartlang': 'price_type'
    })
    #Reshape summary stats to tidy format ---
    #This will create a long format with percentile and confidence interval
    stat_cols = ['mean','qu10','qu25','qu50','qu75','qu90']
    ci_cols = ['meanl','meanu','qu10l','qu10u','qu25l','qu25u','qu50l','qu50u','qu75l','qu75u','qu90l','qu90u']
    #Reset the index
    df = df.reset_index(drop=True)
    # Delete multiple columns
    df.drop(columns=["zimmerlang", "stichtagdatmonat", "gemeinnuetzigsort", "einheitsort", "preisartsort", "raumeinheitsort", "gliederungsort"], inplace=True)
    return df

df = load_rent_data()