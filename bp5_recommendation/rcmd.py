from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for, flash
from datetime import date, timedelta
import os, logging, time
import pandas as pd
import my_util.rcmd_util as mr
from my_util.weather import get_weather

rcmd_bp = Blueprint('rcmd_bp', __name__)
menu = {'ho':0, 'bb':0, 'li':0, 'rg':0, 
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':1,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}

@rcmd_bp.route('/movie', methods=['GET', 'POST'])
def movie():
    if request.method == 'GET':
        return render_template('rcmd/spinner.html', menu=menu, weather=get_weather())
    else:
        mr.get_cosine_sim()
        df = pd.read_csv('static/data/movies_meta_summary.csv')
        df = df.head(10034).dropna().drop_duplicates()
        df.reset_index(inplace=True)
        df.drop(['index'], axis=1, inplace=True)
        
        movie_dict = dict(zip(df.title, df.index))
        return render_template('rcmd/movie.html', menu=menu, weather=get_weather(),
                                movie_dict=movie_dict)