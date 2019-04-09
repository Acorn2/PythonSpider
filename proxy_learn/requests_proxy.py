#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/5 16:34
software: PyCharm
description: 
'''
import requests

proxy = '127.0.0.1:9743'
proxies = {
    'http':'http://' + proxy,
    'https' : 'https://' + proxy
}

try:
    response = requests.get('http://httpbin.org/get',proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print(e)