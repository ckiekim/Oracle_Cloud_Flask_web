from flask import Flask, render_template, session, request, g
from my_util.weather import get_weather
from logging.config import dictConfig
import json, logging

app = Flask(__name__)

with open('./logging.json', 'r') as file:
    config = json.load(file)
dictConfig(config)

@app.route('/')
def index():
    menu = {'ho':1, 'da':0, 'ml':0, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    client_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logging.debug(f'Connected to {client_addr}')
    return render_template('index.html', menu=menu, weather=get_weather())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
