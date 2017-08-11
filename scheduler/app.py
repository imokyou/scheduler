# coding=utf8
import traceback
import json
from datetime import datetime, timedelta
from flask import Flask,request, render_template, redirect, jsonify
from flask_cors import CORS, cross_origin
from models import DbMgr
from settings import *

app = Flask(__name__)
mgr = DbMgr()


def summary_targets(todolist):
    complete_percent, encourage, targets = 0, '', []
    if todolist:
        donenum, todonum = 0, 0
        for i in xrange(1, 10):
            iname = 'item{}'.format(i)
            if iname not in todolist:
                continue
            v = todolist[iname]
            if v['content']:
                todonum = todonum + 1
                if v['done'] == 1:
                    donenum = donenum + 1
                targets.append({
                    'content': v['content'], 'done': v['done']
                })

        if not donenum or not todonum:
            complete_percent = 0
        else:
            complete_percent = (donenum*100.0)/todonum
        if complete_percent >= 100:
            encourage = '完成度100%, 离梦想又近一步!'
        else:
            encourage = '完成度{}%, 白日梦和梦想的距离是整个大西洋!'.format(complete_percent)
    return complete_percent, encourage, targets


def normal_resp(data=[]):
    ret = {'code': 0, 'data': data}
    return jsonify(ret)


def error_resp(msg):
    ret = {'code': -1, 'msg': msg}
    return jsonify(ret)


@app.route('/')
def index():
    return normal_resp()


@app.route('/api/schedules/<stype>/')
@cross_origin()
def list(stype):
    params = {
        'stype': stype
    }
    records = mgr.get_schedulers(params)

    ret = []
    currutc8 = datetime.utcnow() + timedelta(hours=8)
    for r in records:
        info = {
            'id': r['id'],
            'is_today': 0,
            'stype': r['stype'],
            'title': r['title'],
            'date': r['startdate'].strftime('%Y-%m-%d'),
            'complete_percent': r['complete_percent'],
            'summary': '',
            'targets': []
        }
        complete_percent, encourage, targets = summary_targets(r['todolist'])
        info['summary'] = encourage
        info['targets'] = targets
        if info['date'] == currutc8.strftime('%Y-%m-%d'):
            info['is_today'] = 1

        ret.append(info)
    return normal_resp(ret)


@app.route('/api/schedule/<int:sid>')
def detail(sid):
    params = {
        'id': sid
    }
    record = mgr.get_scheduler(params)
    return normal_resp(record)


@app.route('/api/schedule/<int:id>/del/')
@cross_origin()
def delete(id):
    try:
        mgr.delete_schedule_by_id(id)
    except:
        traceback.print_exc()
        return error_resp('something error')
    return normal_resp()


@app.route('/api/schedule/add/', methods=['GET', 'POST'])
@cross_origin()
def add():
    try:
        if request.method == 'POST':
            title = request.form['title']
            stype = request.form['stype']
            startdate = request.form['startdate']
            try:
                items = {}
                for k, v in enumerate(json.loads(request.form['targets'])):
                    if not v:
                        v = ''
                    items['item{}'.format(k+1)] = {'content': v, 'done': 0}
            except:
                traceback.print_exc()
                items = []
            print items

            if not startdate:
                startdate = datetime.utcnow() + timedelta(hours=8)
            else:
                try:
                    startdate = datetime.strptime(startdate, '%Y%m%d')
                except:
                    startdate = datetime.strptime(startdate, '%Y-%m-%d')

            remaindays = 1
            for i in xrange(remaindays):
                record = {
                    'user_id': 1,
                    'title': title,
                    'stype': stype,
                    'complete_percent': 0,
                    'startdate': '',
                    'remaindays': 1,
                    'items': json.dumps(items)
                }
                try:
                    record['startdate'] = (startdate + timedelta(days=i)).strftime('%Y%m%d')
                except:
                    record['startdate'] = (startdate + timedelta(days=i)).strftime('%Y-%m-%d')
                mgr.add_scheduler(record)
            return normal_resp()
    except:
        traceback.print_exc()
        return error_resp('something error')
    return normal_resp()


@app.route('/api/schedule/<int:id>/update/', methods=['GET', 'POST'])
@cross_origin()
def update(id):
    try:
        if request.method == 'POST':
            id = request.form.get('id', '')
            title = request.form.get('title', '')
            sdate = request.form.get('date', '')
            targets = request.form.get('targets', '')

            items = {}
            donenum = 0
            todonum = 0
            for k, v in enumerate(json.loads(targets)):
                items['item{}'.format(k+1)] = v
                if v['content']:
                    todonum = todonum + 1
                    if v['done'] == 1:
                        donenum = donenum + 1
            if not donenum or not todonum:
                complete_percent = 0
            else:
                complete_percent = (donenum*100.0)/todonum

            record = {'id': id, 'complete_percent': complete_percent}
            if title:
                record['title'] = title
            if sdate:
                record['startdate'] = sdate
            if items:
                record['items'] = json.dumps(items)

            # print record
            mgr.update_scheduler(record)

            return normal_resp()
    except:
        traceback.print_exc()
        return error_resp('something error')
    return normal_resp()


if __name__ == '__main__':
    app.run(debug=True)
