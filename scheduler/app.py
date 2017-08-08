# coding=utf8
import traceback
import json
from datetime import datetime, timedelta
from flask import Flask,request, render_template, redirect, jsonify
from models import DbMgr
from settings import *

app = Flask(__name__)
mgr = DbMgr()


def normal_resp(data=[]):
    ret = {'code': 0, 'data': data}
    return jsonify(ret)


def error_resp(msg):
    ret = {'code': -1, 'msg': msg}
    return jsonify(ret)


@app.route('/')
def index():
    return normal_resp()


@app.route('/api/schedules/<stype>')
def list(stype):
    params = {
        'stype': stype
    }
    records = mgr.get_schedulers(params)
    return normal_resp(records)


@app.route('/api/schedule/<int:sid>')
def detail(sid):
    params = {
        'id': sid
    }
    record = mgr.get_scheduler(params)
    return normal_resp(record)


@app.route('/api/schedule/add')
def add():
    try:
        if request.method == 'POST':
            title = request.form['title']
            stype = request.form['stype']
            startdate = request.form['startdate']
            remaindays = request.form['remaindays']
            todolist = request.form['todolist']

            if not startdate:
                startdate = datetime.utcnow() + timedelta(hours=8)
                startdate = startdate.strftime('%Y%m%d')
            else:
                startdate = datetime.strptime(startdate, '%Y%m%d')

            remaindays = int(record['remaindays'])
            for i in xrange(remaindays):
                record = {
                    'user_id': 1,
                    'title': title,
                    'stype': stype,
                    'complete_percent': 0,
                    'startdate': (startdate + timedelta(days=i)).strftime('%Y%m%d'),
                    'remaindays': 1,
                    'items': json.dumps(todolist)
                }
                mgr.add_scheduler(record)
            return normal_resp()
    except:
        traceback.print_exc()
        return error_resp('something error')
    return normal_resp()


@app.route('/api/schedule/update/<int:sid>')
def update(sid):
    try:
        if request.method == 'POST':
            sid = sid
            title = request.form['title']
            stype = request.form['stype']
            startdate = request.form['startdate']
            todolist = request.form['todolist']

            donenum = 0
            todonum = 0
            for k, v in enumerate(json.loads(todolist).values()):
                if v['content']:
                    todonum = todonum + 1
                    if v['done'] == 1:
                        donenum = donenum + 1
            if not donenum or not todonum:
                complete_percent = 0
            else:
                complete_percent = (donenum*100.0)/todonum

            record = {
                'id': sid,
                'title': title,
                'stype': stype,
                'startdate': startdate,
                'complete_percent': complete_percent,
                'items': todolist
            }
            self.mgr.update_scheduler(record)

            return normal_resp()
    except:
        traceback.print_exc()
        return error_resp('something error')
    return normal_resp()


if __name__ == '__main__':
    app.run(debug=True)
