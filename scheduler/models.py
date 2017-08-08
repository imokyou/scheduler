# coding=utf8
import traceback
import json
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, create_engine, Numeric, Text, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import *

dburl = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DBUSER, DBPASSWD, DBHOST, DBPORT, DBNAME)
engine = create_engine(dburl, echo=False)
DBSession = sessionmaker(bind=engine)

# 创建对象的基类:
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }


class User(BaseModel):
    __tablename__ = 'user'
    id = Column("id", Integer, primary_key=True)
    username = Column(String(256))
    email = Column(String(256))
    password = Column(String(256))
    is_superuser = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    def conv_result(self):
        info = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_superuser': self.is_superuser,
            'created_at': self.created_at
        }
        return info


class Scheduler(BaseModel):
    __tablename__ = 'scheduler'
    id = Column("id", Integer, primary_key=True)
    title = Column(String(512))
    user_id = Column('uid', Integer)
    stype = Column(String(256))
    startdate = Column(DateTime)
    remaindays = Column(Integer)
    complete_percent = Column(Numeric, default='0')
    items = Column(Text)
    notify_day = Column(Integer, default='0')
    notify_night = Column(Integer, default='0')
    created_at = Column(DateTime, default=datetime.utcnow)

    def conv_result(self):
        info = {
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'stype': self.stype,
            'startdate': self.startdate,
            'remaindays': self.remaindays,
            'complete_percent': float(self.complete_percent),
            'todolist': json.loads(self.items),
            'notify_day': self.notify_day,
            'notify_night': self.notify_night,
            'created_at': self.created_at
        }
        return info


class NotifyLog(BaseModel):
    __tablename__ = 'notify_log'
    id = Column("id", Integer, primary_key=True)
    uid = Column(Integer)
    sid = Column(Integer)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class DbMgr(object):
    def __init__(self):
        self.session = DBSession()

    def add_scheduler(self, record={}):
        try:
            if not record:
                return None
            self.session.add(Scheduler(**record))
            self.session.commit()
        except:
            traceback.print_exc()
            self.session.rollback()
        finally:
            self.session.close()

    def update_scheduler(self, record):
        try:
            if 'id' not in record:
                return None
            sid = record['id']
            del record['id']
            self.session.query(Scheduler).filter(Scheduler.id == sid).update(record)
            self.session.commit()
            return True
        except:
            traceback.print_exc()
            self.session.rollback()
        finally:
            self.session.close()
        return None

    def get_scheduler(self, params={}):
        ret = self.get_schedulers(params)
        if ret:
            return ret[0]
        return None

    def get_schedulers(self, params={}, desc=True):
        try:
            ret = []
            q = self.session.query(Scheduler, User).filter(Scheduler.user_id == User.id)
            if params.get('id', 0):
                q = q.filter(Scheduler.id == params['id'])
            if params.get('uid', 0):
                q = q.filter(Scheduler.uid == params['uid'])
            if params.get('stype', ''):
                q = q.filter(Scheduler.stype == params['stype'])
            if params.get('startdate', ''):
                q = q.filter(Scheduler.startdate >= params['startdate'])
            if params.get('enddate', ''):
                q = q.filter(Scheduler.startdate <= params['enddate'])
            ret = []
            if desc:
                q = q.order_by(Scheduler.startdate.desc())
            else:
                q = q.order_by(Scheduler.startdate)
            for r in q.all():
                sinfo = r.Scheduler.conv_result()
                sinfo['user'] = r.User.conv_result()
                ret.append(sinfo)
        except:
            traceback.print_exc()
            self.session.rollback()
        finally:
            self.session.close()
        return ret


if __name__ == '__main__':
    mgr = DbMgr()
    '''
    items = {
        'item1': {'content': 'xxxxxxxx', 'done': 1},
        'item2': {'content': 'sssssssss', 'done': 1}
    }
    sch = {
        'title': '测试计划',
        'startdate': '20170808',
        'remaindays': 3,
        'uid': 1,
        'stype': 'keepfit',
        'items': json.dumps(items)
    }
    mgr.add_scheduler(sch)
    '''
    records = mgr.get_schedulers()
    for r in records:
        print r

