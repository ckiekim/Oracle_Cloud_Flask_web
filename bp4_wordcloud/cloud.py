from flask import Blueprint, render_template, request, session, g
from flask import current_app
from werkzeug.utils import secure_filename
import os, logging
from my_util.weather import get_weather
from my_util.wordCloud import engCloud, hanCloud

cloud_bp = Blueprint('cloud_bp', __name__)
menu = {'ho':0, 'bb':0, 'li':0, 'rg':0,
        'se':0, 'cg':0, 'cr':0, 'wc':1, 'rs':0,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}

@cloud_bp.route('/han/gift')
def gift():
    textfile = os.path.join(current_app.root_path, 'static/data/gift.txt')
    maskfile = os.path.join(current_app.root_path, 'static/img/heart.jpg')
    logging.debug(f'{textfile}, {maskfile}')
    stop_words = []
    img_file = os.path.join(current_app.root_path, 'static/img/text.png')
    with open(textfile) as fp:
        text = fp.read()
    hanCloud(text, stop_words, maskfile, img_file)
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('wordcloud/text_res.html', menu=menu, weather=get_weather(),
                            filename='gift.txt', mtime=mtime)

@cloud_bp.route('/eng/<option>')
def eng(option):
    if option == 'Alice':
        filename = 'Alice.txt'
        maskfile = os.path.join(current_app.root_path, 'static/img/Alice_mask.png')
        stop_words = ['said']
    else:
        filename = 'A_new_hope.txt'
        maskfile = os.path.join(current_app.root_path, 'static/img/Stormtrooper_mask.png')
        stop_words = ['int', 'ext']
    
    textfile = os.path.join(current_app.root_path, 'static/data/') + filename
    logging.debug(f'{textfile}, {maskfile}')
    img_file = os.path.join(current_app.root_path, 'static/img/text.png')
    with open(textfile) as fp:
        text = fp.read()
    if option == 'Starwars':
        text = text.replace('HAN', 'Han')
        text = text.replace("LUKE'S", 'Luke')
    engCloud(text, stop_words, maskfile, img_file)
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('wordcloud/text_res.html', menu=menu, weather=get_weather(),
                            filename=filename, mtime=mtime)        

@cloud_bp.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'GET':
        return render_template('wordcloud/text.html', menu=menu, weather=get_weather())
    else:
        lang = request.form['lang']
        f_text = request.files['text']
        file_text = os.path.join(current_app.root_path, 'static/upload/') + f_text.filename
        f_text.save(file_text)
        if request.files['mask']:
            f_mask = request.files['mask']
            file_mask = os.path.join(current_app.root_path, 'static/upload/') + f_mask.filename
            f_mask.save(file_mask)
        else:
            file_mask = None
        stop_words = request.form['stop_words']
        current_app.logger.debug(f"{lang}, {f_text}, {request.files['mask']}, {stop_words}")

        text = open(file_text, encoding='utf-8').read()
        stop_words = stop_words.split(' ') if stop_words else []
        img_file = os.path.join(current_app.root_path, 'static/img/text.png')
        if lang == 'en':
            engCloud(text, stop_words, file_mask, img_file)
        else:
            hanCloud(text, stop_words, file_mask, img_file)

        mtime = int(os.stat(img_file).st_mtime)
        return render_template('wordcloud/text_res.html', menu=menu, weather=get_weather(),
                                filename=f_text.filename, mtime=mtime)
