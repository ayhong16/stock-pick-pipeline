from pipeline.parsers.parser import Parser
import pandas as pd
import numpy as np


def calculate_sentiment_score(df, bi=False, col_name='labels'):
    positive_count = df[df[col_name] == 'positive'].shape[0]
    negative_count = df[df[col_name] == 'negative'].shape[0]
    neutral_count = df[df[col_name] == 'neutral'].shape[0]

    if positive_count + negative_count + neutral_count == 0:
        return 0

    if bi:
        sentiment_score = np.log((1 + positive_count) / (1 + negative_count))
    else:
        sentiment_score = (positive_count - negative_count) / (positive_count + negative_count + neutral_count)
    return sentiment_score


class CombineDataParser(Parser):

    def parse(self):
        print(f"Starting CombineDataParser for {self.ticker}...")
        stocktwits_file = f'{self.src}/{self.ticker}/stocktwits_sentiment.csv'
        news_file = f'{self.src}/{self.ticker}/news_sentiment.csv'
        stock_file = f'{self.src}/{self.ticker}/stock_data.csv'

        # Read CSV files into pandas DataFrames
        stocktwits_df = pd.read_csv(stocktwits_file, lineterminator='\n')
        news_df = pd.read_csv(news_file)
        stock_df = pd.read_csv(stock_file)
        stock_df.drop('timestamp', axis=1, inplace=True)

        # Standardize column names
        stocktwits_df.rename(columns={'created_at': 'date'}, inplace=True)
        stock_df.rename(columns={'timestamp': 'date'}, inplace=True)

        # Convert 'date' column to datetime format
        stocktwits_df['date'] = pd.to_datetime(stocktwits_df['date'], utc=True)
        stocktwits_df['date'] = pd.to_datetime(stocktwits_df['date'].dt.strftime('%Y-%m-%d'))
        news_df['date'] = pd.to_datetime(news_df['date'], utc=True)
        news_df['date'] = pd.to_datetime(news_df['date'].dt.strftime('%Y-%m-%d'))
        stock_df['date'] = pd.to_datetime(stock_df['date'], utc=True)
        stock_df['date'] = pd.to_datetime(stock_df['date'].dt.strftime('%Y-%m-%d'))

        # Filter data based on start and end dates
        stocktwits_df = stocktwits_df[
            (stocktwits_df['date'] >= self.start_date) & (stocktwits_df['date'] <= self.end_date)]
        news_df = news_df[(news_df['date'] >= self.start_date) & (news_df['date'] <= self.end_date)]
        stock_df = stock_df[(stock_df['date'] >= self.start_date) & (stock_df['date'] <= self.end_date)]

        # Group by date and calculate sentiment scores
        social_media_sentiment_group = stocktwits_df.groupby('date')
        news_sentiment_group = news_df.groupby('date')
        raw_social_media_sentiment = social_media_sentiment_group.apply(
            lambda df: calculate_sentiment_score(df, bi=True, col_name="raw label"))
        raw_social_media_sentiment = raw_social_media_sentiment.reset_index(name="raw_social_media_sentiment")
        thresh_social_media_sentiment = social_media_sentiment_group.apply(
            lambda df: calculate_sentiment_score(df, bi=False, col_name="thresholded label"))
        thresh_social_media_sentiment = thresh_social_media_sentiment.reset_index(name='thresholded_social_media_sentiment')
        news_sentiment = news_sentiment_group.apply(lambda df: calculate_sentiment_score(df, bi=False, col_name="label")
                                                    ).reset_index(name='news_sentiment')
        # Merge dataframes on date
        result_df = pd.merge(raw_social_media_sentiment, news_sentiment, on='date', how='outer').fillna(0)
        result_df = pd.merge(result_df, thresh_social_media_sentiment, on='date', how='outer').fillna(0)
        result_df = pd.merge(result_df, stock_df, on='date', how='inner').fillna(0)
        result_df.to_csv(f"{self.dest}/{self.ticker}_combined_data.csv", index=False)
        print(f"Finished CombineDataParser for {self.ticker}!")
