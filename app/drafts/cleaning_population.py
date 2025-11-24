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
    'QuarLang': 'neighbourhood',
    'AnzBestWir': 'population'
    }, inplace=True)

    df.drop(columns=['district number'], inplace=True)
    
    # Mapping Quartier → Kreis
    quarter_to_district = {
    "Affoltern": "Kreis 11",
    "Albisrieden": "Kreis 9",
    "Alt-Wiedikon": "Kreis 3",
    "Altstetten": "Kreis 9",
    "City": "Kreis 1",
    "Enge": "Kreis 2",
    "Escher Wyss": "Kreis 5",
    "Fluntern": "Kreis 7",
    "Friesenberg": "Kreis 3",
    "Gewerbeschule": "Kreis 5",
    "Hard": "Kreis 4",
    "Hirslanden": "Kreis 7",
    "Hirzenbach": "Kreis 12",
    "Hochschulen": "Kreis 5",
    "Höngg": "Kreis 10",
    "Hottingen": "Kreis 7",
    "Langstrasse": "Kreis 4",
    "Leimbach": "Kreis 2",
    "Lindenhof": "Kreis 1",
    "Mühlebach": "Kreis 8",
    "Oberstrass": "Kreis 6",
    "Oerlikon": "Kreis 11",
    "Rathaus": "Kreis 1",
    "Saatlen": "Kreis 12",
    "Schwamendingen-Mitte": "Kreis 12",
    "Seebach": "Kreis 11",
    "Seefeld": "Kreis 8",
    "Sihlfeld": "Kreis 3",
    "Unterstrass": "Kreis 6",
    "Weinegg": "Kreis 8",
    "Werd": "Kreis 4",
    "Wipkingen": "Kreis 10",
    "Witikon": "Kreis 7",
    "Wollishofen": "Kreis 2",
    "Kreis 3 südlicher Teil (Alt-Wiedikon und Friesenberg)": "Kreis 3",
    "Schwamendingen (ganzer Kreis 12)": "Kreis 12"
    }
    df["district"] = df["neighbourhood"].map(quarter_to_district)

    total_rows = (
        df.groupby("year", as_index=False)["population"]
        .sum()
        .assign(quarter="Ganze Stadt", district="Ganze Stadt")
    )

    df = pd.concat([df, total_rows], ignore_index=True)
    return df

df = load_population_data()