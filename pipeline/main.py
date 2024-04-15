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
    # parser = StockTwitsParser(columns, ticker="AAPL", src="./data/StockTwits/AAPL_pre_processed.csv", dest="./output/AAPL/aapl_stocktwits_final.csv")
    # parser.parse()

    # scraper = AlphaVantageScraper()
    # scraper.scrape_stocks("NVDA", "2019-12-31", "2022-02-27")

    # scraper = BenzingaScraper()
    # scraper.scrape_news("AAPL", "2019-12-31", "2022-02-27")

    # analyst_parser = NewsHeadlinesParser(["date", "title", "stock", "source"], src="./data/News_Headlines/analyst_ratings_processed.csv", dest="./output/aapl_news_headlines.csv", ticker="AAPL")
    # analyst_parser.parse()

    combine_parser = CombineDataParser(ticker="AAPL", src="./data/precombined", dest="./output",
                                       start_date="2019-12-31", end_date="2022-02-27")
    combine_parser.parse()


