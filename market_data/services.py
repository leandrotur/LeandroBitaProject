from market_data.provider import query_daily_data_for_instrument
import pandas as pd
import numpy as np


def run_statistics(
        ticker: str, date: str
):
    """ Calculates statistics for an instrument
    """
    # getdate
    datajson = query_daily_data_for_instrument(ticker, date)
    # ETL --> to refactor
    data = pd.DataFrame.from_dict(datajson['Time Series (Daily)'], orient='index').sort_index(axis=1)
    data = data.rename(columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close',
                                '5. adjusted close': 'AdjClose', '6. volume': 'Volume'})
    data = data[['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']]
    data['AdjClose'] = pd.to_numeric(data['AdjClose'], errors='coerce')
    data = data[:f'{date}']
    # ETL end

    # get statistics
    annual_return = cagr(data, True)
    annual_vol = volatility(data, True)
    ret = cagr(data, False)
    vol = volatility(data, False)
    sharpe = sharpe_ratio(data, 0.03)

    last_price = data['AdjClose'][-1]

    # set message -- > to refactor
    message = {
        'ticker': ticker,
        'last adjclose': last_price,
        'return': ret,
        'annual return': annual_return,
        'annual volatility': annual_vol,
        'volatility': vol,
        'sharpe': sharpe
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
