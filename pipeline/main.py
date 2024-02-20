from parsers.stock_twits_parser import StockTwitsParser
import pandas as pd

if __name__ == '__main__':
    # clear csv
    with open('./output/sentiment.csv', 'r') as f:
        column_names = f.readline().strip().split(',')
    empty_df = pd.DataFrame(columns=column_names)
    empty_df.to_csv('./output/sentiment.csv', index=False)

    # preprocess data into csv
    columns = ["created_at", "body", "ticker", "source"]
    parser = StockTwitsParser(columns)
    parser.parse()

