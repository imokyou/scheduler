# coding=utf8
from lib import utils


def test(request):
    return utils.NormalResp()


def get_list(request):
    return utils.NormalResp({'m': 'this is schedules'})


def add_schedule(request):
    return utils.NormalResp({'m': 'this is add schedule'})


def update_schedule(request, id):
    return utils.NormalResp({'m': 'this is update schedule'})


def delete_schedule(request, id):
    return utils.NormalResp({'m': 'this is delete schedule'})


def schedule_configs(request, schedule_id):
    return utils.NormalResp({'m': 'this is schedule configs'})


def add_schedule_config(request, schedule_id):
    return utils.NormalResp({'m': 'this is add schedule config'})


def update_schedule_config(request, schedule_id, id):
    return utils.NormalResp({'m': 'this is update schedule config'})


def delete_schedule_config(request, schedule_id, id):
    return utils.NormalResp({'m': 'this is delete schedule config'})


