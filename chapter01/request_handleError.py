#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/1 9:18
software: PyCharm
description: requests的一些高级用法，如文件上传、cookie设置、代理设置等。
'''

'''part1URLError'''
from urllib import request,error

# try:
#     res = request.urlopen('http://cuiqingcai.com/index.htm')
# except error.URLError as e:
#     print(e.reason)

'''part2'''
import socket

try:
    res = request.urlopen('https://www.baidu.com',timeout=0.1)
except error.URLError as e:
    print(type(e.reason))
    if isinstance(e.reason,socket.timeout):
        print("time out")