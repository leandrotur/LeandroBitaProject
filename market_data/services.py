from market_data.queries import query_daily_data_for_instrument


def run_statistics(
        ticker: str, date: str
):
    """ Stores the oficial daily market data of an instrument.
    """
    data = query_daily_data_for_instrument(ticker, date)
    return data
