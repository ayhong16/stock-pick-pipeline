import os
from pipeline.parsers.parser import Parser
import html

class StockTwitsParser(Parser):

    def parse(self):
        directory = f"{self.src}/StockTwits_2020_2022_Raw/"
        for root, dirs, files in os.walk(directory):
            ticker = root.split("/")[-1].split("_")[0]
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    df = self.create_df(file_path)
                    df["ticker"] = file.split("_")[0]
                    df["source"] = "Twitter"
                    df["body"] = df["body"].apply(html.unescape)
                    self.append_df(df)
            if ticker == "":
                print("Starting...")
            else:
                print(f"Finished {ticker}...")
