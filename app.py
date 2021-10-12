from flask import Flask, Blueprint
from market_data.routes import market_data_bp

app = Flask(__name__)

app.register_blueprint(market_data_bp, url_prefix='/market_data')
app.config['JSON_SORT_KEYS'] = False


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
