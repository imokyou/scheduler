# coding=utf8
from __future__ import unicode_literals
import traceback
from datetime import datetime, timedelta
from time import sleep
from wechat_sender import Sender
from models import DbMgr
from settings import *


class Messenger(object):

    def __init__(self):
        self.sender = Sender(token=WECHAT_TOKEN)
        self.mgr = DbMgr()

    def run(self):
        while True:
            print 'waiting to send message.'
            self.scheduler_morning()
            self.scheduler_today_summary()
            sleep(60*5)

    def deliver(self, msg, to=WECHAT_RECEIVER):
        print to, msg
        self.sender.send_to(msg, to)

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
        msg = self.gen_msg(record)
        msg = '今天(%s) %s' % (record['startdate'].strftime('%Y%m%d'), msg)
        self.deliver(msg)

        self.mgr.update_scheduler({'id': record['id'], 'notify_day': 1})

    def scheduler_today_summary(self):
        '''
        晚上21点发送， UTC 13点
        '''
        currutc = datetime.utcnow()
        if currutc.hour != 7:
            return None
        sdate = (currutc + timedelta(hours=8)).date()
        record = self.mgr.get_scheduler({'startdate': sdate, 'enddate': sdate})
        if record['notify_night']:
            return None
        msg = self.gen_msg(record)
        msg = '今天(%s)总结 %s' % (record['startdate'].strftime('%Y%m%d'), msg)
        self.deliver(msg)

        self.mgr.update_scheduler({'id': record['id'], 'notify_night': 1})

        # 再把明天的计划也发一发
        sdate = (currutc + timedelta(hours=32)).date()
        record = self.mgr.get_scheduler({'startdate': sdate, 'enddate': sdate})
        msg = self.gen_msg(record)
        msg = '明天(%s) %s' % (record['startdate'].strftime('%Y%m%d'), msg)
        self.deliver(msg)

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

        return msg


if __name__ == '__main__':
    m = Messenger()
    m.run()
    '''
    msg = 'test {}'.format(datetime.utcnow())
    m.deliver(msg, WECHAT_RECEIVER.decode('utf8'))
    '''
