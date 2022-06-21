import numpy as np
import pandas as pd
# kaggle data source
# https://www.kaggle.com/datasets/camnugent/sandp500
def process_kaggle_data(src='all_stocks_5yr.csv'):
    df = pd.read_csv(src)
    df = df[['close', 'Name']]
    tickers = df['Name'].unique()
    tmp = df[df['Name'] == 'AAPL']['close']
    N = len(tmp.values) - 1 # len of returns are 1 less than len of prices
    daily_returns = []
    for tick in tickers:
        tmp = df[df['Name'] == tick]['close']
        priceList = tmp.iloc[:].values
        tmp_daily_returns = (priceList[1:] - priceList[:-1])/priceList[:-1]
        if len(tmp_daily_returns) == N: # filter out the ones with wrong number of daily returns
            daily_returns.append(tmp_daily_returns)
    X = np.array(daily_returns)
    np.savetxt('test_daily_returns.txt', X)
    return X

if __name__ == "__main__":
    process_kaggle_data()
