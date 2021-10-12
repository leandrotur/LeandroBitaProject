from flask import Blueprint, jsonify
from flask import request
from market_data.services import run_statistics

market_data_bp = Blueprint('market_data', __name__)


@market_data_bp.route("/statistics", methods=["GET"])
def runstats():
    #exaxmple: http://127.0.0.1:5000/market_data/statistics?ticker=IBM&fromdate=2021-10-10
    ticker = request.args.get('ticker')
    fromdate = request.args.get('fromdate')
    dict_obj = run_statistics(ticker, fromdate)
    message = {
        'status': 200,
        'message': 'OK',
        'Statistics': dict_obj
    }
    resp = jsonify(message)
    resp.status_code = 200
    print(resp)
    return resp

