import os

import pandas as pd

from pipeline.parsers.parser import Parser
import html


def replace_html_entities(text):
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", "\"")
    text = text.replace("&apos;", "'")
    text = text.replace("&39;", "'")
    text = text.replace("quot;", "\"")
    text = text.replace("â€˜", "'")
    text = text.replace("â€™", "'")
    return text


class StockTwitsParser(Parser):

    def parse(self):
        print(f"Starting StockTwitsParser for {self.ticker}...")
        file_path = f"{self.src}"
        df = self.create_df(file_path)
        df["ticker"] = self.ticker
        df["source"] = "Twitter"
        df["sentiment"] = df["sentiment"].apply(lambda x: "neutral" if pd.isna(x) or x == "" else ("negative" if x.lower() == "bearish" else "positive"))
        df["body_prepared"] = df["body_prepared"].apply(lambda x: replace_html_entities(x))
        self.append_df(df)
        print(f"Finished StockTwitsParser for {self.ticker}!")
