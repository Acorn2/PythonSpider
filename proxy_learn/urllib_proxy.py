#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/5 16:03
software: PyCharm
description: 
'''
from urllib.error import URLError
from urllib.request import ProxyHandler,build_opener

proxy = '127.0.0.1:9743'
proxy_handler = ProxyHandler({
    'http':'http://' + proxy,
    'https' : 'https://' + proxy
})

opener = build_opener(proxy_handler)
try:
    response = opener.open('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)