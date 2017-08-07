# coding=utf8
import json
from datetime import datetime, timedelta
from flask import Flask,request, render_template, redirect
from models import DbMgr
from settings import *

app = Flask(__name__)
mgr = DbMgr()


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/login')
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html')


@app.route('/logout')
def logout():
    return "Logout"


@app.route('/schedule/list/<stype>')
def list(stype=''):
    records = mgr.get_schedulers({'stype': stype})
    return render_template('list.html', records=records, stype=stype)


@app.route('/schedule/detail/<int:sid>')
def detail(sid=''):
    record = mgr.get_scheduler({'sid': sid})
    return render_template('detail.html', record=record)


@app.route('/schedule/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        sid = request.form['sid']
        user_id = request.form['uid']
        title = request.form['title']
        stype = request.form['stype']
        startdate = request.form['startdate']
        remaindays = request.form['remaindays']
        todolist = {
            'item1': {'content': request.form['item1'], 'done': 1 if request.form.get('item1_done', '') else 0},
            'item2': {'content': request.form['item2'], 'done': 1 if request.form.get('item2_done', '') else 0},
            'item3': {'content': request.form['item3'], 'done': 1 if request.form.get('item3_done', '') else 0},
            'item4': {'content': request.form['item4'], 'done': 1 if request.form.get('item4_done', '') else 0},
            'item5': {'content': request.form['item5'], 'done': 1 if request.form.get('item5_done', '') else 0},
            'item6': {'content': request.form['item6'], 'done': 1 if request.form.get('item6_done', '') else 0},
            'item7': {'content': request.form['item7'], 'done': 1 if request.form.get('item7_done', '') else 0},
            'item8': {'content': request.form['item8'], 'done': 1 if request.form.get('item8_done', '') else 0},
            'item9': {'content': request.form['item9'], 'done': 1 if request.form.get('item9_done', '') else 0},
            'item10': {'content': request.form['item10'], 'done': 1 if request.form.get('item10_done', '') else 0}
        }

        donenum = 0
        todonum = 0
        for k, v in enumerate(todolist.values()):
            if v['content']:
                todonum = todonum + 1
                if v['done'] == 1:
                    donenum = donenum + 1
        if not donenum or not todonum:
            complete_percent = 0
        else:
            complete_percent = (donenum*100.0)/todonum

        if not startdate:
            startdate = datetime.utcnow() + timedelta(hours=8)
            startdate = startdate.strftime('%Y%m%d')
        else:
            startdate = datetime.strptime(startdate, '%Y%m%d')
        record = {
            'id': sid,
            'user_id': user_id,
            'title': title,
            'stype': stype,
            'user_id': 1,
            'complete_percent': complete_percent,
            'startdate': startdate,
            'remaindays': remaindays,
            'items': json.dumps(todolist)
        }
        if not sid:
            remaindays = int(record['remaindays'])
            for i in xrange(remaindays):
                record['remaindays'] = 1
                record['startdate'] = (startdate + timedelta(days=i)).strftime('%Y%m%d')
                mgr.add_scheduler(record)
        else:
            record['remaindays'] = 1
            mgr.update_scheduler(record)
        return redirect('/schedule/list/{}'.format(stype))
    return render_template('add.html')


@app.route('/schedule/achieve')
def achieve():
    return "Schedule achieve"


@app.route('/schedule/delete')
def delete():
    return "Schedule delete"


if __name__ == '__main__':
    app.run(debug=True)
