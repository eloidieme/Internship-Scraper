import pandas as pd
from datetime import datetime

class Processor:
    def __init__(self, data, locations, categories, contracts, min_date = datetime(2024, 6, 30)) -> None:
        self.data = data
        self.locations = locations
        self.categories = categories
        self.contracts = contracts
        self.min_date = min_date

    def filter_location(self, data):
        filtered = list(filter(lambda d: d['lieu'] in self.locations, data))
        return filtered

    def filter_category(self, data):
        filtered = list(filter(lambda d: d['categorie'] in self.categories, data))
        return filtered

    def filter_contract(self, data):
        filtered = list(filter(lambda d: d['contrat'] in self.contracts, data))
        return filtered
        
    def get_filtered_data(self):
        data = self.data
        data = self.filter_location(data)
        data = self.filter_category(data)
        data = self.filter_contract(data)
        return data

def pandas_converter(data):
    df = pd.json_normalize(data)
    df = df.replace("immediat", datetime.now().strftime("%d/%m/%Y"))
    df = df.replace("Non spécifié", datetime.now().strftime("%d/%m/%Y"))
    df["debut"] = pd.to_datetime(df["debut"], dayfirst=True)
    df = df[df["debut"] > datetime(2024, 6, 30)]
    df["debut"] = df["debut"].dt.strftime('%d/%m/%Y')
    df = df.astype({"debut": str, "date": str})
    df = df.reset_index().drop("index", axis=1)
    return df