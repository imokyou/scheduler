# coding=utf8
from __future__ import unicode_literals
from wxpy import *
from wechat_sender import *


class WechatServer(object):

    def __init__(self):
        self.bot = None

    def listen(self):
        self.bot = Bot(cache_path=True, console_qr=True)
        listen(self.bot)

    def run(self):
        self.listen()


if __name__ == '__main__':
    wx = WechatServer()
    wx.run()
