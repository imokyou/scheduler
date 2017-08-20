# coding=utf-8
import json
from django.http import HttpResponse


def HttpJSONResponse(js):
    return HttpResponse(json.dumps(js),
                        content_type='application/json')


def NormalResp(d={}):
    return HttpResponse(json.dumps({'c': 0, 'm': '', 'd': d}),
                        content_type='application/json')

def ErrResp(errmsg):
    return HttpResponse(json.dumps({'c': errmsg[0], 'm': errmsg[1], 'd': {}}),
                        content_type='application/json')