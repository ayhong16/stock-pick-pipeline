import requests
import os
import pandas as pd
import io
from datetime import datetime


def convert_date_format(input_date):
    try:
        # Parse the input date string
        date_object = datetime.strptime(input_date, "%Y-%m-%d")

        # Convert the date to the desired format
        output_date = date_object.strftime("%Y%m%dT0000")

        return output_date
    except ValueError:
        print("Invalid date format. Please provide a date in the format YYYY-MM-DD.")

class AlphaVantageScraper:
    def __init__(self, dest="./output/"):
        self.dest = dest
        self.url = "https://www.alphavantage.co/query?"

    def scrape_stocks(self, ticker, start_date, end_date):
        print(f"Starting to fetch {ticker} stock data...")
        url = f"{self.url}function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&datatype=csv&apikey={os.environ['ALPHAVANTAGE_API_KEY']}"
        r = requests.get(url)
        if r.status_code == 200:
            data = pd.read_csv(io.StringIO(r.text))
            data['date'] = pd.to_datetime(data['timestamp'])
            filtered_data = data[(data['timestamp'] >= start_date) & (data['timestamp'] <= end_date)]
            filtered_data.to_csv(f"{self.dest}{ticker}_stock_data.csv", index=False)
            print(f"Download {ticker} stock data!")
        else:
            print(f"Failed to download {ticker} stock data...")

    def scrape_news(self, ticker, start_date, end_date):
        start_date = convert_date_format(start_date)
        end_date = convert_date_format(end_date)
        print(start_date)
        url = f"{self.url}function=NEWS_SENTIMENT&tickers={ticker}&limit=50&time_from={start_date}&sort=EARLIEST&apikey={os.environ['ALPHAVANTAGE_API_KEY']}"
        print(url)
