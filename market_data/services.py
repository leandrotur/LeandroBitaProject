from market_data.provider import query_daily_data_for_instrument
from settings import rf
import pandas as pd
import numpy as np

"""
Calc stats service
"""


def etl_market_data(data):
    data = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index').sort_index(axis=1)
    data = data.rename(columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close',
                                '5. adjusted close': 'AdjClose', '6. volume': 'Volume'})
    data = data[['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']]
    data['AdjClose'] = pd.to_numeric(data['AdjClose'], errors='coerce')
    return data


def run_statistics(
        ticker: str, date: str
):
    """ Calculates statistics for an instrument
    """
    # get data from provider
    data_json = query_daily_data_for_instrument(ticker, date)
    # to dataframe
    data = etl_market_data(data_json)
    # filter by date
    data = data[:f'{date}']
    # get statistics
    annual_return = cagr(data, True)
    annual_vol = volatility(data, True)
    ret = cagr(data, False)
    vol = volatility(data, False)
    # sharpe = sharpe_ratio(data, 0.03)
    sharpe = sharpe_ratio_v2(annual_return, annual_vol, rf)
    last_price = data['AdjClose'][-1]
    # set message -- > to refactor
    message = {'stock': {
        'ticker': ticker,
        'last adjclose': last_price},
        'Stats': {
            'return': ret,
            'annual return': annual_return,
            'volatility': vol,
            'annual volatility': annual_vol,
            'sharpe ratio': sharpe}
    }

    return message


def cagr(data, annual: bool):
    df = data.copy()
    df['daily_returns'] = df['AdjClose'].pct_change()
    df['cumulative_returns'] = (1 + df['daily_returns']).cumprod()
    trading_days = 252
    n = len(df) / trading_days
    if annual:
        cagr = (df['cumulative_returns'][-1]) ** (1 / n) - 1
    else:
        cagr = (df['cumulative_returns'][-1]) - 1
    return cagr


def volatility(data, annual: bool):
    df = data.copy()
    df['daily_returns'] = df['AdjClose'].pct_change()
    trading_days = 252
    if annual:
        vol = df['daily_returns'].std() * np.sqrt(trading_days)
    else:
        vol = df['daily_returns'].std()
    return vol


def sharpe_ratio(data, rf):
    df = data.copy()
    sharpe = (cagr(df, 1) - rf) / volatility(df, 1)
    return sharpe


def sharpe_ratio_v2(cagr, volatility, rf):
    sharpe = (cagr - rf) / volatility
    return sharpe
