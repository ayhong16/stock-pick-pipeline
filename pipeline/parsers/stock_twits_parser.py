import os

import pandas as pd

from pipeline.parsers.parser import Parser
import html

class StockTwitsParser(Parser):

    def parse(self):
        directory = f"{self.src}/StockTwits_2020_2022_Raw/"
        for root, dirs, files in os.walk(directory):
            ticker = root.split("/")[-1].split("_")[0]
            if ticker == "NVDA":
                earliest = None
                latest = None
                for file in files:
                    if file.endswith(".csv"):
                        file_path = os.path.join(root, file)
                        df = self.create_df(file_path)
                        df["ticker"] = file.split("_")[0]
                        df["source"] = "Twitter"
                        df["created_at"] = pd.to_datetime(df["created_at"])
                        early = df["created_at"].min()
                        late = df["created_at"].max()
                        if earliest is None or early < earliest:
                            earliest = early
                        if latest is None or late > latest:
                            latest = late
                        self.append_df(df)
                print(f"earliest date: {earliest}")
                print(f"latest date: {latest}")
                if ticker == "":
                    print("Starting...")
                else:
                    print(f"Finished {ticker}...")
