import pandas as pd

from parsers.stock_twits_parser import StockTwitsParser
from pipeline.parsers.combine_data_parser import CombineDataParser
from pipeline.parsers.news_headlines_parser import NewsHeadlinesParser
from scrapers.alphavantage_scraper import AlphaVantageScraper
import os
from dotenv import load_dotenv
from scrapers.benzinga_scraper import BenzingaScraper


if __name__ == '__main__':
    load_dotenv()
    ## StockTwitsParser
    # columns = ["created_at", "body_prepared", "ticker", "source", "sentiment"]
    # parser = StockTwitsParser(columns, ticker="TSLA", src="./data/StockTwits/TSLA_pre_processed.csv", dest="./output/TSLA/tsla_stocktwits_final.csv")
    # parser.parse()

    # scraper = AlphaVantageScraper()
    # scraper.scrape_stocks("NVDA", "2013-04-11", "2022-02-28")

    # scraper = BenzingaScraper()
    # scraper.scrape_news("AMZN", "2019-07-23", "2022-03-05")

    # analyst_parser = NewsHeadlinesParser(["date", "title", "stock", "source"], src="./data/News_Headlines/analyst_ratings_processed.csv", dest="./output/TSLA/tsla_news_headlines.csv", ticker="TSLA")
    # analyst_parser.parse()

    combine_parser = CombineDataParser(ticker="TSLA", src="./data/precombined", dest=f"./output")
    combine_parser.parse()




