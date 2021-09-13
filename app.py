from flask import Flask, render_template, session, request, g
from my_util.weather import get_weather
from logging.config import dictConfig
import json, logging
from bp1_seoul.seoul import seoul_bp
from bp2_cartogram.carto import carto_bp
from bp3_crawling.crawl import crawl_bp
from bpx_bbs.bbs import bbs_bp
from bpz_user.user import user_bp

app = Flask(__name__)
app.secret_key = 'qwert12345'   # session, flash 사용하기 위해 설정
app.config['SESSION_COOKIE_PATH'] = '/'

app.register_blueprint(seoul_bp, url_prefix='/seoul')
app.register_blueprint(carto_bp, url_prefix='/cartogram')
app.register_blueprint(crawl_bp, url_prefix='/crawling')
app.register_blueprint(bbs_bp, url_prefix='/bbs')
app.register_blueprint(user_bp, url_prefix='/user')

with open('./log/logging.json', 'r') as file:
    config = json.load(file)
dictConfig(config)

@app.route('/')
def index():
    menu = {'ho':1, 'bb':0, 'li':0, 'rg':0,
            'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
            'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}
    client_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logging.debug(f'Connected to {client_addr}')
    try:
        logging.debug(f"uid:{session['uid']}, uname:{session['uname']}")
    except:
        session['uid'], session['uname'] = None, None
    ''' try:
        sess_uid, sess_uname = session['uid'], session['uname']
    except:
        sess_uid, sess_uname = None, None
    logging.debug(f"uid:{sess_uid}, uname:{sess_uname}") '''
    return render_template('index.html', menu=menu, weather=get_weather())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
