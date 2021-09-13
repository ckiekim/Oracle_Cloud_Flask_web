from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for, flash
from datetime import datetime, timedelta
import os, hashlib, base64
import db.db_module as dm
from my_util.weather import get_weather

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    menu = {'ho':0, 'li':0, 'rg':1, 
            'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
            'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}
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

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    menu = {'ho':0, 'li':1, 'rg':0, 
            'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
            'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}
    if request.method == 'GET':
        return render_template('user/login.html', menu=menu, weather=get_weather())
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        if not dm.get_user_info(uid):
            flash('잘못된 uid 입니다.')
            return redirect(url_for('user_bp.login'))
        else:
            db_pwd, uname, _, _ = dm.get_user_info(uid)
            pwd_sha256 = hashlib.sha256(pwd.encode())
            hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
            if db_pwd != hashed_pwd:
                flash('잘못된 패스워드입니다.')
                return redirect(url_for('user_bp.login'))
            else:
                flash(f'{uname}님 환영합니다.')
                session['uid'] = uid
                session['uname'] = uname
                return redirect('/')    # 게시판으로 이동

@user_bp.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.pop('uid', None)
        session.pop('uname', None)
        return redirect('/')