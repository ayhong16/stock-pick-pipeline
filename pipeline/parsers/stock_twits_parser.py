import os
from pipeline.parsers.parser import Parser
import html

class StockTwitsParser(Parser):

    def parse(self):
        print(f"Starting StockTwitsParser for {self.ticker}...")
        file_path = f"{self.src}"
        df = self.create_df(file_path)
        df["ticker"] = self.ticker
        df["source"] = "Twitter"
        self.append_df(df)
        print(f"Finished StockTwitsParser for {self.ticker}!")
