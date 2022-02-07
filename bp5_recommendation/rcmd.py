from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for, flash
import pandas as pd
import my_util.rcmd_util as mr
import my_util.general_util as gu
from my_util.weather import get_weather

rcmd_bp = Blueprint('rcmd_bp', __name__)
menu = {'ho':0, 'bb':0, 'us':0, 'li':0, 
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':1,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}

movie_max_index = 9999
book_max_index = 2380

@rcmd_bp.route('/movie', methods=['GET', 'POST'])
def movie():
    if request.method == 'GET':
        return render_template('rcmd/spinner.html', menu=menu, weather=get_weather())
    else:
        mr.get_cosine_sim()
        df = pd.read_csv('static/data/movies_meta_summary.csv')
        
        movie_dict = dict(zip(df.title, df.index))
        return render_template('rcmd/movie.html', menu=menu, weather=get_weather(),
                                movie_dict=movie_dict)

@rcmd_bp.route('/movie_res', methods=['POST'])
def movie_res():
    kind = request.form['kind']
    if kind == 'list':
        index = int(request.form['list'])
    elif kind == 'index':
        index = gu.get_index(request.form['index'], movie_max_index)
        #index = int(request.form['index'] or '0')
    else:
        title = request.form['title']
        index = mr.get_movie_index(title)
        if index < 0:
            flash('입력한 영화제목 데이터가 없습니다.')
            return redirect(url_for('rcmd_bp.movie'))

    movie_list, title = mr.get_recommendations(index)
    return render_template('rcmd/movie_res.html', menu=menu, weather=get_weather(),
                            movie_list=movie_list, title=title)

@rcmd_bp.route('/book', methods=['GET', 'POST'])
def book():
    df = pd.read_csv('static/data/books2.csv')
    if request.method == 'GET':
        book_dict = dict(zip(df.title, df.index))
        return render_template('rcmd/book.html', menu=menu, weather=get_weather(),
                                book_dict=book_dict)
    else:
        kind = request.form['kind']
        if kind == 'list':
            index = int(request.form['list'])
        elif kind == 'index':
            index = gu.get_index(request.form['index'], book_max_index)
            #index = int(request.form['index'] or '0')
        else:
            title = request.form['title']
            index = mr.get_book_index(title)
            if index < 0:
                flash('입력한 도서제목 데이터가 없습니다.')
                return redirect(url_for('rcmd_bp.book'))
    
    book_indices = mr.get_recommended_books(index)
    book_list = []
    for i in book_indices:
        book_list.append([df.image_link[i], df.title[i], df.author[i], df.genre[i]])
    return render_template('rcmd/book_res.html', menu=menu, weather=get_weather(),
                            book_list=book_list)