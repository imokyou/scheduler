## 相关问题的解决方法
* InsecurePlatformWarning: A true SSLContext object is not available. 其实因是为requests请求一个https，但是没有设置verify=False而且也不建议这么设置，要嘛升级python3.x，要嘛装库pip install pyopenssl ndg-httpsclient pyasn1. 

* 如果生成的二维码乱码，可能是系统设置的字符集不对，试试在~/.bashrc上加一句： export LC_ALL="en_US.UTF-8"