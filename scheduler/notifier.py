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
        while True:
            print 'waiting to send message.'
            self.scheduler_morning()
            self.scheduler_today_summary()
            sleep(60*5)

    def scheduler_morning(self):
        '''
        早上7点发送 UTC 23点
        '''
        currutc = datetime.utcnow()
        if currutc.hour != 23:
            return None
        sdate = (currutc + timedelta(hours=8)).date()
        record = self.mgr.get_scheduler({'startdate': sdate, 'enddate': sdate})
        if record['notify_day']:
            return None
        complete_percent, msg = self.gen_msg(record)
        msg = '今天(%s) %s' % (record['startdate'].strftime('%Y%m%d'), msg)
        self.send(msg)

        self.mgr.update_scheduler({'id': record['id'], 'notify_day': 1})

    def scheduler_today_summary(self):
        '''
        晚上21点发送， UTC 13点
        '''
        currutc = datetime.utcnow()
        if currutc.hour != 13:
            return None
        sdate = (currutc + timedelta(hours=8)).date()
        record = self.mgr.get_scheduler({'startdate': sdate, 'enddate': sdate})
        if record['notify_night']:
            return None
        complete_percent, msg = self.gen_msg(record)
        msg = '今天(%s)总结 %s' % (record['startdate'].strftime('%Y%m%d'), msg)
        self.send(msg)

        self.mgr.update_scheduler({'id': record['id'], 'notify_night': 1})

        # 再把明天的计划也发一发
        sdate = (currutc + timedelta(hours=32)).date()
        record = self.mgr.get_scheduler({'startdate': sdate, 'enddate': sdate})
        complete_percent, msg = self.gen_msg(record)
        msg = '明天(%s) %s' % (record['startdate'].strftime('%Y%m%d'), msg)
        self.send(msg)

    def gen_msg(self, record):
        complete_percent = 0
        encourage = '还有训练未完成,加油加油!!!'
        msg = '{},完成度{}%.{}\n'

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
            encourage = '完成所有训练. U R 666!!!'
        msg = msg.format(record['title'], complete_percent, encourage)

        return complete_percent, msg

    def send(self, msg):
        print msg
        self.sender.send(msg)

    def send_delay(self, title, msg, delaytime):
        print msg
        self.sender.delay_send(content=msg, time=delaytime, title=title, remind=timedelta(minutes=1))


if __name__ == '__main__':
    ner = Notifier()
    currtime = datetime.utcnow() + timedelta(hours=8)
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
