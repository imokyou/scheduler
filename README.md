# 日程表

## 模块设计
* 微信网页站的登陆器：wechat_server
* 通知发送器notify，利用微信文件助手发送日程消息通知
* notifier改成用微信发送到微信好的的方式，也就是用小号通知大号


## 程序设计
* wxpy以及wechat_sender模块搭建微信消息通知服务
* flask做后台管理
* wechat_server一直运行，利用wxpy的缓存模块维持微信网页版登陆状态
* notifier轮询数据库，如条件符合则发消息到当前登陆的微信


## TodoList
* flask后台用户及登陆系统
* flask后台兼容移动端
* 美化消息通知格式
* 系统兼容多用户使用，也就是不同用户自动生成不同的sender


## 相关问题的解决方法
* InsecurePlatformWarning: A true SSLContext object is not available. 其实因是为requests请求一个https，但是没有设置verify=False而且也不建议这么设置，要嘛升级python3.x，要嘛装库pip install pyopenssl ndg-httpsclient pyasn1. 

* 如果生成的二维码乱码，可能是系统设置的字符集不对，试试在~/.bashrc上加一句： export LC_ALL="en_US.UTF-8"