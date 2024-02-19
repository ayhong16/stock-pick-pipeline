import pandas as pd
import os


class Parser:

    def __init__(self, columns, src="./data", dest="./output/sentiment.csv"):
        self.src = src
        self.dest = dest
        self.columns = columns

    def create_df(self, csv):
        df_src = pd.read_csv(csv)
        return df_src

    def append_df(self, df_src):
        df_selected_columns = df_src[self.columns]
        df_selected_columns.to_csv(self.dest, index=False, mode='a', header=not os.path.exists(self.dest))

    def parse(self):
        pass
