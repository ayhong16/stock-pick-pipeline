import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates


def plot_news_sentiment(src):
    df = pd.read_csv(src)
    df['news_sentiment'] = df['news_sentiment'].replace(0, np.nan)
    df = df[['date', 'news_sentiment']]
    df = df.iloc[:100].dropna()

    fig = plt.figure()
    plt.plot(df['date'], df['news_sentiment'])
    plt.tight_layout()


def plot_stock_data(ticker):
    src = f"./data/precombined/{ticker}/stock_data.csv"
    df = pd.read_csv(src)
    df = df[(df["date"] >= "2016-01-01") & (df["date"] <= "2022-01-01")]
    df["date"] = pd.to_datetime(df["date"])
    print(min(df["date"]), max(df["date"]))
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['close'])

    dates = ["2016-01-01", "2016-07-01", "2017-01-01", "2017-07-01",
             "2018-01-01", "2018-07-01", "2019-01-01", "2019-07-01", "2020-01-01",
             "2020-07-01", "2021-01-01", "2021-07-01", "2022-01-01"]
    plt.xticks(dates, rotation=45)

    plt.xlabel("Date")
    plt.ylabel("Close Price ($)")
    plt.title(f"{ticker} Close Price During COVID-19")
    plt.savefig(f"./data/plots/{ticker} Close Price During COVID-19")
    plt.show()


def plot_stock_sentiment(ticker):
    stocktwits_src = f"./data/StockTwits/{ticker}_pre_processed.csv"


if __name__ == '__main__':
    # plot_news_sentiment("./output/NVDA_combined_data.csv")
    # plot_news_sentiment("./output/NVDA_combined_imputed_data.csv")
    plot_stock_data("NVDA")
