from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for, flash
from datetime import date, timedelta
import os, logging, math
import db.db_module as dm
from my_util.weather import get_weather

bbs_bp = Blueprint('bbs_bp', __name__)
menu = {'ho':0, 'bb':1, 'li':0, 'rg':0, 
        'se':0, 'cg':0, 'cr':0, 'wc':0, 'rs':0,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}

@bbs_bp.route('/list/<int:page>', methods=['GET'])
def list(page):
    if not session['uid']:
        flash('게시판을 이용하려면 로그인을 하세요.')
        return redirect('/')

    session['current_page'] = page
    offset = (page - 1) * 10
    count = dm.get_bbs_counts()
    total_page = math.ceil(count / 10)
    start_page = math.floor((page - 1) / 10) * 10 + 1
    end_page = math.ceil(page / 10) * 10
    end_page = total_page if end_page>total_page else end_page
    rows = dm.get_bbs_list(offset)
    today = date.today().strftime("%Y-%m-%d")
    return render_template('bbs/list.html', menu=menu, bbs_list=rows,
                            today=today, weather=get_weather(),
                            page_no=page, start_page=start_page, 
                            end_page=end_page, total_page=total_page)

@bbs_bp.route('/view/<int:bid>', methods=['GET'])
def view(bid):
    row = dm.get_bbs_data(bid)
    inc = 0 if row[1] == session['uid'] else 1  # 본인 글은 조회수를 증가시키지 않음
    rows = dm.get_replies(bid)
    if inc==1:
        dm.increase_view_count(bid)
    return render_template('bbs/view.html', menu=menu, weather=get_weather(),
                            inc=inc, row=row, replies=rows,
                            page=session['current_page'])

@bbs_bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        pass
    else:
        pass
