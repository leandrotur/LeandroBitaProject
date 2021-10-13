from flask import Blueprint, jsonify
from flask import request
from market_data.services import run_statistics
from loguru import logger
from market_data.validations import validate_request

"""
Get stats
"""


class Error(Exception):
    """Base class for other exceptions"""
    pass


market_data_bp = Blueprint('market_data', __name__)


@market_data_bp.route("/statistics", methods=["GET"])
def runstats():
    # exaxmple: http://127.0.0.1:5000/market_data/statistics?ticker=IBM&start_date=2021-10-10
    message = {
        'status': 200,
        'message': 'OK',
        "error": False,
        'data': ''
    }
    try:
        # querystring set
        ticker = request.args.get('ticker')
        start_date = request.args.get('start_date')
        # querystring validations
        validate_request(ticker, start_date)
        # calculate stats
        dict_obj = run_statistics(ticker, start_date)
        message['data'] = dict_obj
    except KeyError as e:
        logger.error(f"Error: {e}; {message['message']}")
        message['message'] = "Key Error. Please, make sure to send all the necessary parameters"
        message['error'] = True
        message['status'] = 400

    except AssertionError as e:
        logger.error(f"Error: {e}; {message['message']}")
        message['message'] = "Type Error. Please, make sure to send the right data type for each parameter"
        message['error'] = True
        message['status'] = 400

    except (TypeError, AttributeError, ValueError) as e:
        logger.error(f"Error: {e}; {message['message']}")
        message['message'] = str(e.args[0])
        message['error'] = True
        message['status'] = 400

    except Exception as e:
        logger.error(f"Error: {e}; {message['message']}")
        message['message'] = str(e.args[0])
        message['error'] = True
        message['status'] = 401

    resp = jsonify(message)
    resp.status_code = message['status']
    logger.info(
        f"Data received {resp}"
    )
    print(resp)
    return resp
