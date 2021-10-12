"""
validations
"""
from dateutil.parser import parse
import datetime
from loguru import logger


# define Python user-defined exceptions
class CustomError(Exception):
    """Base class for other exceptions"""
    pass


class UnAcceptedValueError(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)


def validate_date_format(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:

        raise TypeError("Incorrect data format, should be YYYY-MM-DD")


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)

    except ValueError:
        raise ValueError("Request contains a not valid start_date")


def validate_request(ticker: str, start_date: str):
    """Validates the content and the types of the market_data endpoint 
    request body.
    """
    # Validating types.
    is_date(start_date)
    validate_date_format(start_date)
