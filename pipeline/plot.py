import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


if __name__ == '__main__':
    src = f"./output/NVDA_combined_data.csv"
    df = pd.read_csv(src)
    df['news_sentiment'] = df['news_sentiment'].replace(0, np.nan)
    df = df[['date', 'news_sentiment']]
    df = df.iloc[:100].dropna()

    fig = plt.figure()
    plt.plot(df['date'], df['news_sentiment'])
    plt.tight_layout()

    src = f"./output/NVDA_combined_imputed_data.csv"
    df = pd.read_csv(src)
    df['news_sentiment'] = df['news_sentiment'].replace(0, np.nan)
    df = df[['date', 'news_sentiment']]
    df = df.iloc[:100].dropna()

    fig1 = plt.figure()
    plt.plot(df['date'], df['news_sentiment'])
    plt.tight_layout()
    plt.show()
