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
            print u'waiting to send message.'
            self.keepfit_morning()
            self.keepfit_today_summary()
            sleep(60*5)

    def deliver(self, msg, to=WECHAT_RECEIVER):
        print to, msg.encode('utf8')
        # self.sender.send_to(msg.encode('utf8'), to)

    def keepfit_morning(self):
        '''
        早上7点发送 UTC 23点
        '''
        currutc = datetime.utcnow()
        if currutc.hour != 23:
            return None
        sdate = (currutc + timedelta(hours=8)).date()
        record = self.mgr.get_scheduler({'startdate': sdate, 'enddate': sdate, 'stype': 'keepfit'})
        if not record or record['notify_day']:
            return None
        msg = self.gen_msg(record)
        msg = u'今天训练\n%s' % msg
        self.deliver(msg)

        self.mgr.update_scheduler({'id': record['id'], 'notify_day': 1})

    def keepfit_today_summary(self):
        '''
        晚上21点发送， UTC 13点
        '''
        currutc = datetime.utcnow()
        if currutc.hour != 13:
            return None
        sdate = (currutc + timedelta(hours=8)).date()
        record = self.mgr.get_scheduler({'startdate': sdate, 'enddate': sdate, 'stype': 'keepfit'})
        if record and not record['notify_night']:
            msg = self.gen_msg(record)
            msg = u'今天训练总结\n%s' % msg
            self.deliver(msg)

            self.mgr.update_scheduler({'id': record['id'], 'notify_night': 1})

        # 再把明天的计划也发一发
        sdate = (currutc + timedelta(hours=32)).date()
        record = self.mgr.get_scheduler({'startdate': sdate, 'enddate': sdate, 'stype': 'keepfit'})
        msg = self.gen_msg(record)
        msg = u'明天训练\n%s' % msg
        self.deliver(msg)

    def gen_msg(self, record):
        title = record['title']
        sdate = record['startdate'].strftime('%Y-%m-%d')
        encourage = u'还有训练未完成,加油加油!!!'
        complete_percent = 0
        targets = u''

        todonum = 0
        donenum = 0
        for i in xrange(1, 10):
            index = u'item{}'.format(i)
            try:
                if record['todolist'][index].get('content', ''):
                    todonum = todonum + 1
                    tag = u''
                    if record['todolist'][index].get('done', 0) == 1:
                        donenum = donenum + 1
                        tag = u'✓'
                    targets += u'{}. {}{}\n'.format(i, record['todolist'][index].get('content', ''), tag)
            except KeyError:
                traceback.print_exc()
                pass
        try:
            complete_percent = donenum*100.0/todonum
        except:
            pass
        if complete_percent >= 100:
            encourage = u'完成所有训练. U R 666!!!'
        msg = u'日期:{}\n'.format(sdate)
        msg += u'主题:{}\n'.format(title)
        msg += u'完成度{}%,{}\n'.format(complete_percent, encourage)
        msg += u'目标:\n{}\n'.format(targets)
        return msg


if __name__ == '__main__':
    m = Messenger()
    m.run()
    '''
    msg = 'test {}'.format(datetime.utcnow())
    m.deliver(msg, WECHAT_RECEIVER.decode('utf8'))
    '''
