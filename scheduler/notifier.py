# coding=utf8
from __future__ import unicode_literals
import traceback
from datetime import datetime, timedelta
from time import sleep
from wechat_sender import Sender
from models import DbMgr


class Notifier(object):

    def __init__(self):
        self.mgr = DbMgr()
        self.sender = Sender()

    def run(self):
        startdate = (datetime.utcnow() + timedelta(hours=8)).date()
        enddate = (datetime.utcnow() + timedelta(hours=32)).date()
        records = self.mgr.get_schedulers({'startdate': startdate, 'enddate': enddate}, desc=False)
        for r in records:
            if r['startdate'].strftime('%Y%m%d') == startdate.strftime('%Y%m%d'):
                complete_percent, msg = self.gen_msg(r)
                msg = '今日({}) '.format(r['startdate'].strftime('%Y%m%d')) + msg
                print msg
                self.sender.send(msg)
                sleep(10)

            elif r['startdate'].strftime('%Y%m%d') == enddate.strftime('%Y%m%d'):
                complete_percent, msg = self.gen_msg(r)

                print '明日({}) '.format(r['startdate'].strftime('%Y%m%d')) + msg
                self.sender.send('明日({}) '.format(r['startdate'].strftime('%Y%m%d')) + msg)
                sleep(10)

                msg = '今日({}) '.format(r['startdate'].strftime('%Y%m%d')) + msg
                tomorro_morning = datetime.utcnow() + timedelta(hours=10)
                sender.delay_send(content=msg, time=tomorro_morning, title=r['title'], remind=timedelta(minutes=1))
                sleep(10)
        print 'Done!!!'

    def gen_msg(self, record):
        complete_percent = 0
        encourage = '加油加油!!!'
        msg = '{},完成度{},{}\n'

        todonum = 0
        donenum = 0
        for i in xrange(1, 10):
            index = 'item{}'.format(i)
            try:
                if record['todolist'][index].get('content', ''):
                    todonum = todonum + 1
                    tag = ''
                    if record['todolist'][index].get('done', 0) == 1:
                        donenum = donenum + 1
                        tag = '✓'
                    msg += '{}. {}{}\n'.format(i, record['todolist'][index].get('content', ''), tag)
            except KeyError:
                traceback.print_exc()
                pass
        try:
            complete_percent = donenum*100.0/todonum
        except:
            complete_percent = 0
        if complete_percent >= 90:
            encourage = 'U R 666!!!'
        msg = msg.format(record['title'], complete_percent, encourage)

        return complete_percent, msg


if __name__ == '__main__':
    ner = Notifier()
    currtime = datetime.utcnow() + timedelta(hours=8)
    stype = ['keepfit', 'work', 'stady', 'life']
    # ner.send('这是测试信息 >>>>>> {}'.format(currtime.strftime('%Y-%m-%d %H:%M:%S')))
    ner.run()
    '''
    sender = Sender()
    msg = '2017-08-07训练完成度25%, 加油加油!!\n'
    msg += '1. 胸部训练-KEEP徒手胸肌训练 ✓\n'
    msg += '2. 胸部训练-下斜俯卧撑12x4、哑铃平地卧推15x4、哑铃平地飞鸟12x4\n'
    msg += '3. HIIT刷脂\n'
    msg += '4. 跑步4KM以上\n'
    sender.send(msg)
    '''
