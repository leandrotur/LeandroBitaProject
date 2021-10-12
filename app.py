from flask import Flask, Blueprint
from market_data.routes import market_data_bp

app = Flask(__name__)

home = Blueprint('home', __name__, static_folder='static', template_folder='templates')


@home.route('/')
def index():
    return "This is the index route."


app.register_blueprint(home)

app.register_blueprint(market_data_bp, url_prefix='/market_data')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
