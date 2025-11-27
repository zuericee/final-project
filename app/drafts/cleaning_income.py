import os
import pandas as pd

def load_income_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "raw_data")
    income_path = os.path.join(data_dir, "income.csv")
    df = pd.read_csv(income_path, sep=',', quotechar='"')

    df.rename(columns={
    'KreisLang': 'district',
    'StichtagDatJahr': 'year',
    'SteuerEinkommen_p50': 'median income',
    'SteuerTarifLang': 'tax tariff',
    'SteuerEinkommen_p25': '25th percentile income',
    'SteuerEinkommen_p75': '75th percentile income',
    }, inplace=True)

    df.drop(columns=['KreisSort', 'KreisCd', 'SteuerTarifSort', 'SteuerTarifCd'], inplace=True)

    return df