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
        return redirect('/user/login')

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

@bbs_bp.route('/reply', methods=['POST'])
def reply():
    bid = request.form['bid']
    uid = request.form['uid']
    content = request.form['content']
    isMine = 1 if session['uid'] == uid else 0
    dm.insert_reply((bid, session['uid'], content, isMine))
    dm.increase_reply_count(bid)
    return redirect(url_for('bbs_bp.list', page=session['current_page']))

@bbs_bp.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('bbs/write.html', menu=menu, weather=get_weather(),
                                page=session['current_page'])
    else:
        title = request.form['title']
        content = request.form['content']
        if len(title) > 100 or len(content) > 1000:
            flash('제목을 100자 이하로 줄여주세요.\n' * (len(title) > 100) + 
                  '본문을 1000자 이하로 줄여주세요' * (len(content) > 1000))
            return redirect(url_for('bbs_bp.write'))
        dm.insert_bbs((session['uid'], title, content))
        return redirect(url_for('bbs_bp.list', page=1))

@bbs_bp.route('/update/<uid>/bid/<int:bid>', methods=['GET', 'POST'])
def update(uid, bid):
    if request.method == 'GET':
        if session['uid'] == uid:
            row = dm.get_bbs_data(bid)
            return render_template('bbs/update.html', menu=menu, weather=get_weather(),
                                    row=row, page=session['current_page'])
        else:
            flash('수정 권한이 없습니다.')
            return redirect(url_for('bbs_bp.view', bid=bid))
    else:
        title = request.form['title']
        content = request.form['content']
        if len(title) > 100 or len(content) > 1000:
            flash('제목을 100자 이하로 줄여주세요.\n' * (len(title) > 100) + 
                  '본문을 1000자 이하로 줄여주세요' * (len(content) > 1000))
            return redirect(f'/bbs/update/{uid}/bid/{bid}')
        dm.update_bbs((title, content, bid))
        return redirect(url_for('bbs_bp.view', bid=bid))

@bbs_bp.route('/delete/<uid>/bid/<int:bid>', methods=['GET'])
def delete(uid, bid):
    if session['uid'] == uid:
        return render_template('bbs/delete.html', menu=menu, weather=get_weather(),
                                bid=bid, page=session['current_page'])
    else:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('bbs_bp.view', bid=bid))

@bbs_bp.route('/deleteConfirm/<int:bid>', methods=['GET'])
def deleteConfirm(bid):
    dm.delete_bbs(bid)
    return redirect(url_for('bbs_bp.list', page=session['current_page']))
