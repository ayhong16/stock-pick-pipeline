import os
from datetime import datetime

import requests


def convert_date_format(input_date):
    try:
        # Parse the input date string
        date_object = datetime.strptime(input_date, "%Y-%m-%d")

        # Convert the date to the desired format
        output_date = date_object.strftime("%Y%m%dT0000")

        return output_date
    except ValueError:
        print("Invalid date format. Please provide a date in the format YYYY-MM-DD.")

class BenzingaScraper:
    def __init__(self, dest="./output/"):
        self.dest = dest
        self.url = "https://api.benzinga.com/api/v2/news"

    def scrape_news(self, ticker, start_date, end_date):
        querystring = {
            "tickers": ticker,
            "dateFrom": start_date,
            "dateTo": end_date,
            "token": os.environ['BENZINGA_API_KEY']
        }
        headers = {"accept": "application/json"}
        response = requests.request("GET", self.url, headers=headers, params=querystring)
        print(response.text)
