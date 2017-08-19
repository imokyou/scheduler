# coding=utf8
import traceback
import json
from datetime import datetime
from config import errors
from lib import utils
from dbmodel.models import Schedule, ScheduleConfig


def test(request):
    return utils.NormalResp()


def get_schedules(request):
    try:
        p = int(request.GET.get('p', 1))
        n = int(request.GET.get('n', 7))

        q = Schedule.objects
        results = q.all()[n*(p-1): n*p]
        data = []
        for r in results:
            info = {
                'id': r.id,
                'stype': r.stype,
                'subject': r.subject,
                'sdate': r.sdate.strftime('%Y-%m-%d'),
                'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': '',
                'targets': []
            }
            try:
                info['updated_at'] = r.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
            try:
                info['targets'] = json.loads(r.targets)
            except:
                pass
            data.append(info)
        return utils.NormalResp(data)
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


def get_schedule(request, id):
    try:
        try:
            s = Schedule.objects.get(id=id)
        except:
            return utils.ErrResp(errors.DataNotExists)
        data = {
            'id': s.id,
            'stype': s.stype,
            'subject': s.subject,
            'sdate': s.sdate.strftime('%Y-%m-%d'),
            'created_at': s.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': '',
            'targets': []
        }
        try:
            data['updated_at'] = s.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
        try:
            data['targets'] = json.loads(s.targets)
        except:
            pass
        return utils.NormalResp(data)
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


def add_schedule(request):
    try:
        stype = request.POST.get('stype', '')
        subject = request.POST.get('subject', '')
        sdate = request.POST.get('sdate', '')
        targets = request.POST.get('targets', '')
        if not stype or not subject or not sdate or not targets:
            return utils.ErrResp(errors.ArgMis)
        
        try:
            sdate = datetime.strptime(sdate, '%Y-%m-%d')
        except:
            return utils.ErrResp(errors.ArgFormatInvalid)
        
        try:
            targets = json.loads(targets)
        except:
            return utils.ErrResp(errors.ArgFormatInvalid)

        s = Schedule(
            stype=stype,
            subject=subject,
            sdate=sdate,
            targets=json.dumps(targets)
        )
        s.save()
        return utils.NormalResp({'id': s.id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


def update_schedule(request, id):
    try:
        try:
            schedule = Schedule.objects.get(id=id)
        except:
            return utils.ErrResp(errors.DataNotExists)
        
        schedule.stype = request.POST.get('stype', schedule.stype)
        schedule.subject = request.POST.get('subject', schedule.subject)
        schedule.targets = request.POST.get('targets', schedule.targets)

        sdate = request.POST.get('sdate', '')
        if sdate:
            sdate = datetime.strptime(sdate, '%Y-%m-%d')
            schedule.sdate = sdate

        schedule.save()
        return utils.NormalResp({'id': schedule.id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


def delete_schedule(request, id):
    try:
        try:
            schedule = Schedule.objects.get(id=id)
        except:
            return utils.ErrResp(errors.DataNotExists)
        schedule.delete()
        return utils.NormalResp({'id': schedule.id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


def schedule_configs(request, schedule_id):
    try:
        q = ScheduleConfig.objects.filter(schedule_id=int(schedule_id))
        results = q.all()
        data = []
        for r in results:
            info = {
                'id': r.id,
                'schedule_id': schedule_id,
                'value': r.value,
                'key': r.key
            }
            data.append(info)
        return utils.NormalResp(data)
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


def add_schedule_config(request, schedule_id):
    try:
        key = request.POST.get('key', '')
        value = request.POST.get('value', '')
        if not key or not value:
            return utils.ErrResp(errors.ArgMis)
    
        s = ScheduleConfig(
            schedule_id=schedule_id,
            key=key,
            value=value
        )
        s.save()
        return utils.NormalResp({'id': s.id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


def update_schedule_config(request, schedule_id, id):
    try:
        try:
            sconfig = ScheduleConfig.objects.get(schedule_id=int(schedule_id), id=int(id))
        except:
            return utils.ErrResp(errors.DataNotExists)
        
        sconfig.key = request.POST.get('key', sconfig.key)
        sconfig.value = request.POST.get('value', sconfig.value)
        sconfig.save()
        return utils.NormalResp({'id': id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


def delete_schedule_config(request, schedule_id, id):
    try:
        try:
            sconfig = ScheduleConfig.objects.get(schedule_id=int(schedule_id), id=int(id))
        except:
            return utils.ErrResp(errors.DataNotExists)
        sconfig.delete()
        return utils.NormalResp({'id': id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


