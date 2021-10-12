from flask import Blueprint

from market_data.services import run_statistics

market_data_bp = Blueprint('market_data', __name__)


@market_data_bp.route("/statistics", methods=["GET"])
def display_returned_api():
    return run_statistics('IBM', ''), 200
