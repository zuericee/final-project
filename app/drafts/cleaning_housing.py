import os
import pandas as pd

def load_housing_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "raw_data")
    wohnungen_path = os.path.join(data_dir, "Wohnungsbestand.xlsx")
    xls = pd.ExcelFile(wohnungen_path)
    
    #Combine all years into one DataFrame
    all_dfs = []
    for sheet in xls.sheet_names:
        if not sheet.isdigit():
            continue
        temp_df = pd.read_excel(wohnungen_path, sheet_name=sheet, skiprows=9)
        # Keep only rows where the first column is "Kreis 1" to "Kreis 12"
        allowed_districts = [f"Kreis {i}" for i in range(1, 13)] + ["Ganze Stadt"]
        temp_df = temp_df[temp_df.iloc[:, 0].isin(allowed_districts)]
        
        temp_df["jahr"] = int(sheet)
        all_dfs.append(temp_df)

    df_wohnungen = pd.concat(all_dfs, ignore_index=True)

    #Rename columns and drop unwanted columns
    df_wohnungen.rename(
        columns={
            df_wohnungen.columns[0]: "district",
            df_wohnungen.columns [1]: "total housing units",
            df_wohnungen.columns [2]: "1 room",
            df_wohnungen.columns [3]: "2 rooms",
            df_wohnungen.columns [4]: "3 rooms",
            df_wohnungen.columns [5]: "4 rooms",
            df_wohnungen.columns [6]: "5 rooms",
            df_wohnungen.columns [7]: "6 rooms",
            df_wohnungen.columns [8]: "7 rooms",
            df_wohnungen.columns [9]: "8 rooms and more",
            }, inplace=True)
    
    df_wohnungen.rename(columns={"jahr": "year"}, inplace=True)
    df_wohnungen.drop(df_wohnungen.columns[10:13], axis=1, inplace=True)

    #Keep only columns we need for reshaping
    room_cols = ["2 rooms", "3 rooms", "4 rooms"]

    #Melt into long format: one row per district-year-room
    df_wohnungen = df_wohnungen.melt(
        id_vars=["district", "year", "total housing units"],
        value_vars=room_cols,
        var_name="rooms",
        value_name="count"
    )

    #Clean the "rooms" column (extract the number only)
    df_wohnungen["rooms"] = df_wohnungen["rooms"].str.extract(r"(\d)").astype(int)

    return df_wohnungen
