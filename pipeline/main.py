from parsers.stock_twits_parser import StockTwitsParser

if __name__ == '__main__':
    columns = ["created_at", "body", "ticker", "source"]
    parser = StockTwitsParser(columns)
    parser.parse()

