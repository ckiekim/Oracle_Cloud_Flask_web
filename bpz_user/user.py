from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for, flash
from datetime import datetime, timedelta
import os, hashlib, base64
import db.db_module as dm
from my_util.weather import get_weather

user_bp = Blueprint('user_bp', __name__)
menu = {'ho':0, 'li':0, 'rg':1, 
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html', menu=menu, weather=get_weather())
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']
        uname = request.form['uname']
        email = request.form['email']
        if dm.get_user_info(uid):           # 중복 uid
            flash('중복된 uid 입니다.')
            return redirect(url_for('user_bp.register'))
        elif pwd != pwd2:                   # 패스워드 불일치
            flash('입력한 패스워드가 일치하지 않습니다.')
            return redirect(url_for('user_bp.register'))
        else:
            pwd_sha256 = hashlib.sha256(pwd.encode())
            hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
            dm.insert_user((uid, hashed_pwd, uname, email))
            return redirect('/')


