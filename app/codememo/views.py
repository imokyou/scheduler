# coding=utf8
from lib import utils


def test(request):
    return utils.NormalResp()


def get_list(request):
    return utils.NormalResp({'m': 'this is codememo codes'})


def add_codememo(request):
    return utils.NormalResp({'m': 'this is add codememo'})


def update_codememo(request, id):
    return utils.NormalResp({'m': 'this is update codememo'})


def delete_codememo(request, id):
    return utils.NormalResp({'m': 'this is delete codememo'})



