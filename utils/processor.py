import pandas as pd
from datetime import datetime

def json_to_pandas(path):
    df = pd.read_json(path)
    df = df.replace("immediat", datetime.now().strftime("%d/%m/%Y"))
    df["debut"] = pd.to_datetime(df["debut"], dayfirst=True)
    df = df[df["debut"] > datetime(2024, 6, 30)]
    df = df.astype({"debut": str})
    df = df.reset_index().drop("index", axis=1)
    return df