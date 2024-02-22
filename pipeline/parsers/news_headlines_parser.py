from pipeline.parsers.parser import Parser
import os


class NewsHeadlinesParser(Parser):

    def parse(self):
        if self.ticker is None:
            print("Ticker is required for NewsHeadlinesParser")
            return
        print(f"Starting NewsHeadlinesParser for {self.ticker}...")
        file_path = f"{self.src}"
        df = self.create_df(file_path)
        df = df[df["stock"] == self.ticker]
        df["source"] = "Benzinga"
        self.append_df(df)
        print(f"Finished NewsHeadlinesParser for {self.ticker}!")
