# coding=utf8
from __future__ import unicode_literals
from wxpy import *
from wechat_sender import *
from settings import *


class WechatServer(object):

    def run(self):
        bot = Bot(cache_path=True, console_qr=True)
        listen(bot, token=WECHAT_TOKEN)


if __name__ == '__main__':
    wx = WechatServer()
    wx.run()
