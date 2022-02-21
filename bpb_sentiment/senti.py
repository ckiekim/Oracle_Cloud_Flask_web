from flask import Blueprint, render_template, request, session, g
from flask import current_app, redirect, url_for
from sklearn.datasets import load_digits
#from konlpy.tag import Okt
import os, re, joblib
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import my_util.general_util as gu
from my_util.weather import get_weather

senti_bp = Blueprint('senti_bp', __name__)
menu = {'ho':0, 'bb':0, 'us':0, 'li':0,
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0, 'st':1}

digits_max_index = 445
mnist_max_index = 10487
imdb_max_index = 6249
naver_max_index = 48994

class Okt():
    def morphs(self):
        pass

@senti_bp.route('/imdb', methods=['GET', 'POST'])
def imdb():
    if request.method == 'GET':
        return render_template('sentiment/imdb.html', menu=menu, weather=get_weather())
    else:
        test_data = []
        if request.form['option'] == 'index':
            index = gu.get_index(request.form['index'], imdb_max_index)
            #index = int(request.form['index'] or '0')
            df_test = pd.read_csv('static/data/IMDB_test.csv')
            test_data.append(df_test.iloc[index, 0])
            label = '긍정' if df_test.sentiment[index] else '부정'
        else:
            test_data.append(request.form['review'])
            label = '직접 확인'

        imdb_count_lr = joblib.load('static/model/imdb_count_lr.pkl')
        imdb_tfidf_lr = joblib.load('static/model/imdb_tfidf_lr.pkl')
        pred_cl = '긍정' if imdb_count_lr.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if imdb_tfidf_lr.predict(test_data)[0] else '부정'
        result_dict = {'label':label, 'pred_cl':pred_cl, 'pred_tl':pred_tl}
        return render_template('sentiment/imdb_res.html', menu=menu, review=test_data[0],
                                res=result_dict, weather=get_weather())

@senti_bp.route('/naver', methods=['GET', 'POST'])
def naver():
    if request.method == 'GET':
        return render_template('sentiment/naver.html', menu=menu, weather=get_weather())
    else:
        if request.form['option'] == 'index':
            index = gu.get_index(request.form['index'], naver_max_index)
            #index = int(request.form['index'] or '0')
            df_test = pd.read_csv('static/data/naver/movie_test.tsv', sep='\t')
            org_review = df_test.document[index]
            label = '긍정' if df_test.label[index] else '부정'
        else:
            org_review = request.form['review']
            label = '직접 확인'
 
        test_data = []
        review = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", org_review)
        okt = Okt()
        stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을']
        morphs = okt.morphs(review, stem=True) # 토큰화
        temp_X = ' '.join([word for word in morphs if not word in stopwords]) # 불용어 제거
        test_data.append(temp_X)

        naver_count_lr = joblib.load('static/model/naver_count_lr.pkl')
        naver_count_nb = joblib.load('static/model/naver_count_nb.pkl')
        naver_tfidf_lr = joblib.load('static/model/naver_tfidf_lr.pkl')
        naver_tfidf_nb = joblib.load('static/model/naver_tfidf_nb.pkl')
        pred_cl = '긍정' if naver_count_lr.predict(test_data)[0] else '부정'
        pred_cn = '긍정' if naver_count_nb.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if naver_tfidf_lr.predict(test_data)[0] else '부정'
        pred_tn = '긍정' if naver_tfidf_nb.predict(test_data)[0] else '부정'
        result_dict = {'label':label, 'pred_cl':pred_cl, 'pred_cn':pred_cn,
                                      'pred_tl':pred_tl, 'pred_tn':pred_tn}
        return render_template('sentiment/naver_res.html', menu=menu, review=org_review,
                                res=result_dict, weather=get_weather())

