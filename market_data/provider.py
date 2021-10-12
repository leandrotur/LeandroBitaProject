"""
AlphaVantage provider
"""
from datetime import datetime

from loguru import logger
import requests


# from utils.postgres_handler import PostgresHandler


def query_daily_data_for_instrument(ticker: str, startdate: str):
    """Queries the quote-level id of an instrument based on the instrument-level
    id (PermID) and the exchange MIC.
    """

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey=demo'
    r = requests.get(url)
    data = r.json()
    logger.debug(f"Executing query: {url}")
    # result = db.execute(query)
    #  quote_id = result["id"].values[0]
    logger.info(
        f"Data received {data}"
    )
    print(data)

    return data


