import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

from pipeline.parsers.parser import Parser


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


def knn_imputer(df):
    df_imputation = df.copy()
    cols = df_imputation.columns.tolist()
    cols.remove('date')

    df_imputation["date"] = df_imputation["date"].apply(lambda x: x.timestamp())
    df_imputation["date"] = df_imputation["volume"].astype('float64')

    # Normalize features in the copy for imputation
    scaler = StandardScaler()
    df_imputation_scaled = scaler.fit_transform(df_imputation)

    # Apply KNN imputation to the scaled data
    knn = KNNImputer(n_neighbors=5)
    df_imputation_scaled = knn.fit_transform(df_imputation_scaled)

    # Convert back to DataFrame
    df_imputation_unscaled = scaler.inverse_transform(df_imputation_scaled)
    df_imputation_unscaled = pd.DataFrame(df_imputation_unscaled, columns=df_imputation.columns)

    # Update the original dataframe with the imputed values
    df['news_sentiment'] = df_imputation_unscaled['news_sentiment']
    df['raw_social_media_sentiment'] = df_imputation_unscaled['raw_social_media_sentiment']
    df['thresholded_social_media_sentiment'] = df_imputation_unscaled['thresholded_social_media_sentiment']
    return df


class CombineDataParser(Parser):

    def parse(self):
        print(f"Starting CombineDataParser for {self.ticker}...")
        stocktwits_file = f'{self.src}/{self.ticker}/stocktwits_sentiment.csv'
        news_file = f'{self.src}/{self.ticker}/news_sentiment.csv'
        stock_file = f'{self.src}/{self.ticker}/stock_data.csv'
        indicators_file = f'{self.src}/{self.ticker}/indicators.csv'

        # Read CSV files into pandas DataFrames
        stocktwits_df = pd.read_csv(stocktwits_file, lineterminator='\n')
        news_df = pd.read_csv(news_file)
        stock_df = pd.read_csv(stock_file)
        indicators_df = pd.read_csv(indicators_file)
        stock_df.drop('timestamp', axis=1, inplace=True)

        # Standardize column names
        stocktwits_df.rename(columns={'created_at': 'date'}, inplace=True)
        stock_df.rename(columns={'timestamp': 'date'}, inplace=True)

        stocktwits_df = self._organize_df(stocktwits_df)
        news_df = self._organize_df(news_df)
        stock_df = self._organize_df(stock_df)
        indicators_df = self._organize_df(indicators_df)

        # Group by date and calculate sentiment scores
        social_media_sentiment_group = stocktwits_df.groupby('date')
        news_sentiment_group = news_df.groupby('date')
        raw_social_media_sentiment = social_media_sentiment_group.apply(
            lambda df: calculate_sentiment_score(df, bi=True, col_name="raw label"))
        raw_social_media_sentiment = raw_social_media_sentiment.reset_index(name="raw_social_media_sentiment")
        thresh_social_media_sentiment = social_media_sentiment_group.apply(
            lambda df: calculate_sentiment_score(df, bi=False, col_name="thresholded label"))
        thresh_social_media_sentiment = thresh_social_media_sentiment.reset_index(
            name='thresholded_social_media_sentiment')
        news_sentiment = news_sentiment_group.apply(lambda df: calculate_sentiment_score(df, bi=False, col_name="label")
                                                    ).reset_index(name='news_sentiment')
        # Merge dataframes on date
        result_df = pd.merge(raw_social_media_sentiment, news_sentiment, on='date', how='outer')
        result_df = pd.merge(result_df, thresh_social_media_sentiment, on='date', how='outer')
        result_df = pd.merge(result_df, stock_df, on='date', how='inner')
        result_df = pd.merge(result_df, indicators_df, on='date', how='inner')
        result_df = knn_imputer(result_df)
        result_df.to_csv(f"{self.dest}/{self.ticker}/{self.ticker}_combined_imputed_data.csv", index=False)
        print(f"Finished CombineDataParser for {self.ticker}!")

    def _organize_df(self, df):
        # Convert 'date' column to datetime format
        df['date'] = pd.to_datetime(df['date'], utc=True)
        df['date'] = pd.to_datetime(df['date'].dt.strftime('%Y-%m-%d'))

        # Filter data based on start and end dates
        df = df[(df['date'] >= self.start_date) & (df['date'] <= self.end_date)]
        return df
