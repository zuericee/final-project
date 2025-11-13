import os
import pandas as pd

def load_housing_data(debug=False):
    # Prepare Paths for Data Reading
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "raw_data")
    wohnungen_path = os.path.join(data_dir, "Wohnungsbestand.xlsx")

    # Optionally print all sheets
    xls = pd.ExcelFile(wohnungen_path)
    if debug:
        print("Available sheets:")
        print(xls.sheet_names)

    # Combine all years into one DataFrame
    all_dfs = []
    for sheet in xls.sheet_names:
        if not sheet.isdigit():
            continue
        temp_df = pd.read_excel(wohnungen_path, sheet_name=sheet, skiprows=9)
        temp_df["jahr"] = int(sheet)
        all_dfs.append(temp_df)
        if debug:
            print(f"Loaded sheet: {sheet}")
            print(temp_df.head())

    df_wohnungen = pd.concat(all_dfs, ignore_index=True)

    #Rename first column and drop unwanted columns
    df_wohnungen.rename(columns={df_wohnungen.columns[0]: "City district"}, inplace=True)
    df_wohnungen.drop(df_wohnungen.columns[10:13], axis=1, inplace=True)

    if debug:
        print("Combined DataFrame:")
        print(df_wohnungen.head())

    return df_wohnungen