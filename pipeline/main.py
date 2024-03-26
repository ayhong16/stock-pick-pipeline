from parsers.stock_twits_parser import StockTwitsParser
from pipeline.parsers.combine_data_parser import CombineDataParser
from pipeline.parsers.news_headlines_parser import NewsHeadlinesParser
from scrapers.alphavantage_scraper import AlphaVantageScraper
import os
from dotenv import load_dotenv
from scrapers.benzinga_scraper import BenzingaScraper


if __name__ == '__main__':
    load_dotenv()
    ### StockTwitsParser
    # columns = ["created_at", "body_prepared", "ticker", "source", "sentiment"]
    # parser = StockTwitsParser(columns, ticker="NVDA", src="./data/StockTwits/NVDA_pre_processed.csv", dest="./output/nvda_stocktwits_final.csv")
    # parser.parse()

    # scraper = AlphaVantageScraper()
    # scraper.scrape_stocks("NVDA", "2010-01-01", "2020-01-01")

    # scraper = BenzingaScraper()
    # scraper.scrape_news("AAPL", "2021-01-01", "2021-01-10")

    # analyst_parser = NewsHeadlinesParser(["date", "title", "stock", "source"], src="./data/News_Headlines/analyst_ratings_processed.csv", dest="./output/nvda_news_headlines.csv", ticker="NVDA")
    # analyst_parser.parse()

    combine_parser = CombineDataParser(ticker="NVDA", src="./data/precombined", dest="./output",
                                       start_date="2014-01-01", end_date="2020-01-01")
    combine_parser.parse()
