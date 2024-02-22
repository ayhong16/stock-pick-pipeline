import pandas as pd
import os
from datetime import datetime
import pytz


class Parser:

    def __init__(self, columns=None, ticker=None, src="./data", dest="./output/data.csv", start_date=None, end_date=None):
        self.src = src
        self.dest = dest
        self.columns = columns
        self.ticker = ticker
        if start_date is not None:
            self.start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
        if end_date is not None:
            self.end_date = pd.to_datetime(end_date, format="%Y-%m-%d")

    def create_df(self, csv):
        df_src = pd.read_csv(csv)
        return df_src

    def append_df(self, df_src):
        df_selected_columns = df_src[self.columns]
        df_selected_columns.to_csv(self.dest, index=False, mode='a', header=not os.path.exists(self.dest))

    def parse(self):
        pass
